# Adaptyv Week 5 candidate review

[Open the current public review](https://benavt.github.io/adaptyv-week5-review/?campaign=kras-g12d-pmhc-review&view=explorer&release=20261106-current-003).

The validated snapshot contains **781 candidates**: 200 LigandForge, 200 RFD3,
97 RFD4 and **284 APNovo redesigns**. All **317 existing highlights** are retained.
APNovo's final population filtering remains pending; 64 of the 284 currently
meet the provisional binder-TM ≥0.70 / heavy-atom-DockQ ≥0.23 structural gates.
They are not automatically shortlisted, and parent RFD4 scores are not inherited.

The **4,634 native model alternatives** comprise:

- 497 original Boltz2 Fast refolds and 297 original diffusion structures.
- 1,568 Boltz2 Exact structures: paired G12D/peptide-free models for every
  displayed candidate, plus six independently refolded WT pilot controls.
- All 994 AF3 and 994 OpenDDE Exact follow-ups for the original 497-candidate panel.
- 284 original APNovo designs, each matched to its independent Exact refolds.

The default Comparison panel shows all four generators using the same Exact
binder–HLA and binder–peptide ipSAE scopes. Paired confidence panels also include
all 781 candidates. Choose a point or Inspect candidate, then select the target
and folding engine to inspect its exact native model. AF3/OpenDDE are viewable
alternatives; Exact scores are not transferred to those structures. APNovo has
no Fast models, so it is absent from the Fast comparisons. Proposed hotspot
colors are pink, HLA teal, beta2M gray, peptide gold and the designed binder blue.

## Exploratory affinity evidence

**1,087 grouped-PCANN estimates** are included from the completed existing-model
scoring stage: G12D for 540 candidates, peptide-free for all 541 candidates in
that frozen scoring cohort, and six WT pilot controls. LF_1546's G12D pose has
no 5 Å binder–receptor interface and is explicitly unscorable, never assigned
zero Kd. The 240 APNovo candidates added after that scoring selection have no
PCANN estimates yet. The queued 535 additional WT controls and their scores
remain pending; they are not shown as complete.

The scored interaction is **designed binder A against HLA B, beta2M C and
presented peptide D**, or A against B/C when peptide-free. D is never treated
as the scored ligand. All 25 checkpoint outputs, model identities and source
hashes are retained in downloadable result records. Three shared-log-axis
comparison panels expose G12D, WT and peptide-free estimates. PCANN calibration
for pMHC is **unvalidated and exploratory**. These are not measured affinities
or demonstrated selectivity. DeltaForge has not run; external scoring credits
spent remain zero.

## Snapshot and source verification

The APNovo collection was frozen at **2026-11-06 10:44 EST**, retaining 568 paired
Exact refolds with finished native/resource validation; generation/refolding of
the remaining 740-design APNovo campaign continues. The publication timestamp
and exact model/method inventory are in `publication-manifest.json` and the page's
comparison scope. This is a dated snapshot, not a live compute dashboard.

Coordinate files use gzip transport to remain under the GitHub Pages site-size
limit. Decompression preserves the exact original native bytes. The viewer
checks both compressed transport identity and native scientific SHA256 before
parsing; native model IDs, atom coordinates, colors, display alignments and
model-bound measurements retain their identities. The archive verifier checks
all native hashes again. Current application source includes
[Campaign Manager PR28](https://github.com/benavt/Design_Campaign_Manager/pull/28).
Revisioned application imports prevent older cached modules from handling new
model transport metadata.

This repository contains publication controls; the scientific project repository
remains private. Native models and selected evidence come from the exact release
pinned in `publication.json`. An explicit Pages workflow dispatch verifies the
archive, file allowlist, native models, original 994-condition analysis, APNovo
source/reference identities and all published PCANN values and partner groups
before deployment. It rejects unsupported engines, inherited scores, missing
exploratory labels, unexpected candidates and links/special files.

Reviews and notes stay in each visitor's browser and can be exported. Private
machine paths, credentials, browser review notes, job requests and execution
queues are excluded. No scientific jobs or paid calls can run from this site.

The public review uses a single-campaign full-width layout, without campaign navigation or its mobile drawer. Scientific data retain the November 6 11:13 EST snapshot.

Publication uses the same Pages API/OIDC identity as the official deployment action, with a bounded thirty-minute status poll. A deployment POST is made once; uncertain responses and timeouts require reconciliation from the saved deployment receipt. No new deployment is created automatically. The existing write permissions, environment and concurrency protection are retained; Actions read permission verifies the uploaded artifact belongs to this exact run and commit.
