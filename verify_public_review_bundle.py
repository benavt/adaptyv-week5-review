"""Verify a hash-bound public site archive and optionally extract its allowlisted files."""
from pathlib import Path,PurePosixPath
import argparse,csv,hashlib,io,json,math,tarfile

def require(value,message):
    if not value:raise ValueError(message)
def digest(body):return hashlib.sha256(body).hexdigest()
def check_path(name):
    path=PurePosixPath(name)
    require(not path.is_absolute() and '\\' not in name and '..' not in path.parts and path.parts and path.parts[0]=='site','Unsafe archive path')
    require(all(not p.startswith('.') or p=='.nojekyll' for p in path.parts),'Hidden publication data is not allowed')
    return path

def review_counts(c):
    pool=c['candidatePool'];require(len(pool)==497 and len({s['id'] for s in pool})==497,'Wrong review population')
    counts=dict(candidates=497,shortlist=len(c['selectionDraft']['selectedIds']),nativeFast=0,originalDesigns=0,models=0,LigandForge=0,ExactPeptidePresent=0,ExactPeptideAbsent=0)
    require(counts['shortlist']==317,'Wrong highlighted population')
    wt_ids=set(c.get('affinityPilot',{}).get('candidates',[]))
    if wt_ids:counts['ExactWT']=0
    for subject in pool:
        counts['LigandForge']+=subject['designOrigin']['method']=='LigandForge'
        exact=[]
        for model in subject['modelCoverage']['models']:
            counts['models']+=1
            engine=model['foldingEngine']
            if engine=='boltz2-fast':counts['nativeFast']+=1
            elif engine=='original-diffused':counts['originalDesigns']+=1
            elif engine=='boltz2-exact':
                require(model['target'] in ['KRAS-G12D-pMHC','HLA-A11-beta2M-peptide-free']+(['KRAS-WT-pMHC'] if subject['id'] in wt_ids else []),'Unknown Exact condition')
                exact.append(model['target'])
                counts['ExactWT' if model['target']=='KRAS-WT-pMHC' else 'ExactPeptidePresent' if model['target']=='KRAS-G12D-pMHC' else 'ExactPeptideAbsent']+=1
            else:raise ValueError('Unapproved review engine')
        require(not exact or sorted(exact)==sorted(['KRAS-G12D-pMHC','HLA-A11-beta2M-peptide-free']+(['KRAS-WT-pMHC'] if subject['id'] in wt_ids else [])),'Unpaired Exact alternatives')
    require((counts['nativeFast'],counts['originalDesigns'],counts['LigandForge'])==(497,297,200),'Baseline model population changed')
    require((counts['ExactPeptidePresent'],counts['ExactPeptideAbsent']) in [(0,0),(497,497)],'Only a complete paired Exact publication is allowed')
    return counts

def verify_exact_analysis(c,read_asset):
    analysis=c.get('exactMetricsAnalysis')
    if analysis is None:return None
    require(analysis['status']=='computed_validated' and analysis['independent_interfaces']==2485,'Exact analysis is not validated')
    pool={s['id']:s for s in c['candidatePool']};assets={}
    for ref in analysis['assets']:
        path=ref['path'].removeprefix('site/');check_path('site/'+path);body=read_asset(path)
        require(digest(body)==ref['sha256'],'Exact analysis source hash differs');assets[path.rsplit('/',1)[-1]]=body
    require(set(assets)=={'exact-condition-scores.csv','exact-paired-scores.csv','exact-pose-comparisons.csv','summary.json'},'Unexpected analysis assets')
    tables={name:list(csv.DictReader(io.StringIO(body.decode()))) for name,body in assets.items() if name.endswith('.csv')}
    conditions=tables['exact-condition-scores.csv'];pairs=tables['exact-paired-scores.csv'];poses=tables['exact-pose-comparisons.csv']
    require((len(conditions),len(pairs),len(poses))==(994,497,2879),'Wrong comparison denominator')
    require({r['candidate_id'] for r in pairs}==set(pool) and len({(r['candidate_id'],r['condition']) for r in conditions})==994,'Unpaired or duplicate score identities')
    for row in conditions:
        subject=pool[row['candidate_id']];m=next(m for m in subject['modelCoverage']['models'] if m['id']==row['model_id'])
        require(m['modelSha256']==row['model_sha256'] and m['foldingEngine']=='boltz2-exact','Exact condition model binding differs')
        absent=row['condition']=='peptide_absent';require(absent==('peptide-free' in m['target']),'Peptide condition differs')
        require(not absent or row['peptide_ipSAE']=='','Absent peptide was assigned a score')
        for part in ['hla','beta2m','peptide']:
            if absent and part=='peptide':continue
            observations=[o for o in m['observations'] if o['metric']==part+'_ipSAE'];require(len(observations)==1 and observations[0]['value']==float(row[part+'_ipSAE']),'Native interface score differs')
    for row in poses:
        models={m['id']:m for m in pool[row['candidate_id']]['modelCoverage']['models']}
        require(all(models[row[key]]['modelSha256']==row[hashkey] for key,hashkey in [('model_id','model_sha256'),('reference_model_id','reference_model_sha256')]),'Pose model pair differs')
        require(row['scope'] in ['HLA181','HLA181_peptide10'] and not ('peptide_absent' in row['comparison'] and row['scope']!='HLA181'),'Incompatible condition pose scope')
        if row['target_sequence_matches']=='False':require(row['DockQ_heavy']=='','Mismatched target received heavy-atom DockQ')
        if pool[row['candidate_id']]['designOrigin']['method']=='LigandForge':require('original' not in row['comparison'],'Invented LigandForge reference pose')
    summary=json.loads(assets['summary.json']);require(summary['candidates']==497 and summary['independent_interfaces']==2485,'Summary denominator differs')
    return dict(conditions=994,pairs=497,poseComparisons=2879,independentInterfaces=2485)


def verify_affinity_pilot(c,read_asset):
    pilot=c.get('affinityPilot')
    if pilot is None:
        require(not any(o['metric']=='Kd_nM' for s in c['candidatePool'] for m in s['modelCoverage']['models'] for o in m.get('observations',[])),'Undeclared affinity observations')
        return None
    expected={'RFD3_7110040','RFD3_7116080','RFD4_8105063','RFD4_8105052','LF_1965','LF_1341'}
    require(set(pilot['candidates'])==expected and len(pilot['WTmodels'])==6,'Wrong exploratory pilot selection')
    require(pilot['status']=='completed_exploratory' and pilot['calibrationForPmhc']=='unvalidated_exploratory' and pilot['creditsSpent']==0 and pilot['providerCalls']==0,'Exploratory pilot boundary differs')
    pool={s['id']:s for s in c['candidatePool']}
    def load(ref):
        p=ref['path'].removeprefix('site/');check_path('site/'+p);body=read_asset(p);require(digest(body)==ref['sha256'],'Affinity source hash differs');return body
    assets={r['label']:load(r) for r in pilot['assets']};summary=json.loads(assets['pilot-summary.json'])
    require(summary['cases']==18 and summary['candidates']==6 and len(summary['predictions'])==18,'Wrong pilot denominator')
    predictions={(r['candidate_id'],r['condition']):r for r in summary['predictions']}
    require(set(predictions)=={(sid,cond) for sid in expected for cond in ['G12D','WT','peptide_free']},'Incomplete pilot panel')
    conditions={'G12D':'KRAS-G12D-pMHC','WT':'KRAS-WT-pMHC','peptide_free':'HLA-A11-beta2M-peptide-free'}
    calibrations=set();count=0
    for s in pool.values():
        for m in s['modelCoverage']['models']:
            for o in m.get('observations',[]):
                if o['metric']!='Kd_nM':continue
                count+=1;cond=next((k for k,v in conditions.items() if v==m['target']),None)
                require(s['id'] in expected and (s['id'],cond) in predictions,'Unapproved affinity scope')
                r=predictions[s['id'],cond];raw=json.loads(load(o['source']))
                require(raw==r,'PCANN source result differs from summary')
                require(o['value']==r['kd_nM'] and o['value']>0 and o['unit']=='nM','Kd differs or units invalid')
                require(o['modelId']==m['id']==r['model_id'] and o['modelSha256']==m['modelSha256']==r['model_sha256'],'Affinity model binding differs')
                require(o['scientificAcceptance']=='needs_review' and 'exploratory' in o['method'] and 'exploratory' in o['label'],'Missing exploratory qualification')
                rec=['B','C'] if cond=='peptide_free' else ['B','C','D']
                require(o['scope']['binder']==r['binder']=='A' and o['scope']['receptorChains']==r['receptor_chains']==rec,'Wrong biological partner grouping')
                require(r['chains']['A']==s['sequence'] and len(r['chains']['B'])==281 and len(r['chains']['C'])==99,'Native chain sequences differ')
                require(('D' not in r['chains']) if cond=='peptide_free' else r['chains']['D']==('VVVGAGGVGK' if cond=='WT' else 'VVVGADGVGK'),'Wrong presented peptide condition')
                require(m['molecularModel']['roles']==dict(binder='A',receptor='B') and m['molecularModel']['contextChains']==rec[1:],'Display chain grouping differs')
                energies=[round(v*.001987204258*298,2) for v in r['raw_ensemble_logKd']]
                require(len(energies)==25 and energies==r['ensemble_deltaG_kcal_mol'] and round(sum(energies)/25,2)==r['deltaG_kcal_mol'],'PCANN ensemble reduction differs')
                require(math.isclose(math.exp(r['deltaG_kcal_mol']/(.001987204258*298))*1e9,o['value'],rel_tol=1e-12),'Kd conversion differs')
                calibrations.add(o['calibrationId'])
    require(count==18 and len(calibrations)==1,'Wrong observation count or mixed calibration')
    require(len(pilot['observations'])==18 and len({r['observationId'] for r in pilot['observations']})==18,'Pilot observation audit differs')
    for row in pilot['WTmodels']:
        m=next(m for m in pool[row['candidateId']]['modelCoverage']['models'] if m['id']==row['modelId'])
        require(m['target']=='KRAS-WT-pMHC' and m['modelSha256']==row['modelSha256'],'WT identity differs')
        require(all(o['metric']=='Kd_nM' for o in m['observations']),'Uncalculated WT confidence was invented')
    presets=[p for p in c['explorerPlotPresets'] if p['id'].startswith('pcann-')]
    require(len(presets)==3 and all(p.get('sharedAxes') and p.get('identityLine') and 'Exploratory' in p['label'] for p in presets),'Missing exploratory comparison plots')
    return dict(candidates=6,WTmodels=6,PCANNestimates=18,calibration='unvalidated_exploratory',plots=3)

def verify(archive,config,output=None):
    archive=Path(archive);require(digest(archive.read_bytes())==config['archive_sha256'],'Archive hash differs from approved publication')
    with tarfile.open(archive,'r:gz') as tar:
        members=tar.getmembers();require(len(members)<=10000,'Too many publication entries')
        names=set()
        for member in members:
            check_path(member.name);require(member.isfile() or member.isdir(),'Links and special files are not allowed')
            require(member.name not in names,'Duplicate archive member');names.add(member.name)
        require(sum(m.size for m in members)<=1024**3,'Published site exceeds the 1 GiB envelope')
        manifest_member=tar.getmember('site/publication-manifest.json');manifest_bytes=tar.extractfile(manifest_member).read();require(digest(manifest_bytes)==config['manifest_sha256'],'Publication manifest hash differs')
        manifest=json.loads(manifest_bytes);require(manifest['id']==config['publication_id'],'Wrong publication identity')
        expected={'site/'+name for name in manifest['files']}|{'site/publication-manifest.json'}
        require({m.name for m in members if m.isfile()}==expected,'Archive contains unapproved or missing files')
        for name in expected:check_path(name)
        if output:
            output=Path(output);output.mkdir(parents=True,exist_ok=False)
        for member in members:
            if not member.isfile():continue
            body=tar.extractfile(member).read();relative=str(PurePosixPath(member.name).relative_to('site'))
            if relative!='publication-manifest.json':
                record=manifest['files'][relative];require(len(body)==record['bytes'] and digest(body)==record['sha256'],'Published file hash differs: '+relative)
            if output:
                path=output/relative;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(body)
        workspace=json.loads(tar.extractfile('site/data/published-workspace.json').read());require(len(workspace['campaigns'])==1,'Only the approved campaign may be published')
        c=workspace['campaigns'][0];pool={s['id']:s for s in c['candidatePool']};counts=review_counts(c)
        require(workspace.get('decisions')==[] and not workspace.get('jobRequests'),'Private review/job state was included')
        published_models={}
        for subject in pool.values():
            require(digest(subject['sequence'].encode())==subject['sequenceSha256'],'Sequence identity differs')
            for model in subject['modelCoverage']['models']:
                asset=model['molecularModel'];path=asset['url'].removeprefix('./');require(model['modelSha256']==asset['sha256'],'Model binding differs');require(manifest['files'][path]['sha256']==asset['sha256'],'Model file hash differs');published_models[path]=asset['sha256']
        require(len(published_models)==counts['models'] and published_models==manifest['modelFiles'],'Wrong native model inventory')
        require(all(manifest['counts'].get(k,0)==v for k,v in counts.items()),'Publication counts differ from models')
        exact_analysis=verify_exact_analysis(c,lambda path:tar.extractfile('site/'+path).read())
        affinity=verify_affinity_pilot(c,lambda path:tar.extractfile('site/'+path).read())
        result=dict(affinityPilot=affinity,exactAnalysis=exact_analysis,id=manifest['id'],files=len(expected),models=counts['models'],candidates=497,shortlist=317,archive_verified=True,output=str(output) if output else None)
        print(json.dumps(result));return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True);p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path);a=p.parse_args();verify(a.archive,json.loads(a.config.read_text()),a.output)
