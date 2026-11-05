"""Verify a hash-bound public site archive and optionally extract its allowlisted files."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,tarfile

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
    for subject in pool:
        counts['LigandForge']+=subject['designOrigin']['method']=='LigandForge'
        exact=[]
        for model in subject['modelCoverage']['models']:
            counts['models']+=1
            engine=model['foldingEngine']
            if engine=='boltz2-fast':counts['nativeFast']+=1
            elif engine=='original-diffused':counts['originalDesigns']+=1
            elif engine=='boltz2-exact':
                require(model['target'] in ['KRAS-G12D-pMHC','HLA-A11-beta2M-peptide-free'],'Unknown Exact condition')
                exact.append(model['target'])
                counts['ExactPeptidePresent' if model['target']=='KRAS-G12D-pMHC' else 'ExactPeptideAbsent']+=1
            else:raise ValueError('Unapproved review engine')
        require(not exact or sorted(exact)==sorted(['KRAS-G12D-pMHC','HLA-A11-beta2M-peptide-free']),'Unpaired Exact alternatives')
    require((counts['nativeFast'],counts['originalDesigns'],counts['LigandForge'])==(497,297,200),'Baseline model population changed')
    require((counts['ExactPeptidePresent'],counts['ExactPeptideAbsent']) in [(0,0),(497,497)],'Only a complete paired Exact publication is allowed')
    return counts

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
        result=dict(id=manifest['id'],files=len(expected),models=counts['models'],candidates=497,shortlist=317,archive_verified=True,output=str(output) if output else None)
        print(json.dumps(result));return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True);p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path);a=p.parse_args();verify(a.archive,json.loads(a.config.read_text()),a.output)
