# Adaptyv Week 5 candidate review

Public hosting for the reviewed KRAS G12D pMHC design campaign snapshot.
The scientific project repository remains private. This repository contains
publication controls; model files are supplied through a hash-verified release.

The snapshot contains **497 candidates**, **317 highlighted review candidates**
(41 RFD3, 76 RFD4 and 200 LigandForge), and **794 molecular structures**
(497 native Boltz2 Fast refolds plus 297 original diffusion designs).

[Open the review](https://benavt.github.io/adaptyv-week5-review/?campaign=kras-g12d-pmhc-review&view=explorer).
Click a plotted point or use **Inspect candidate**, then select the native refold
or available original model. The default axes compare peptide and HLA ipSAE so
all three methods are visible. LigandForge uses its top 10% peptide-ipSAE group;
reference-pose TM/DockQ remain unavailable.

Colors: HLA teal, peptide gold, proposed hotspots pink, beta2M gray and designed
binder deep blue. Models and scientific values retain their native identities.
These are computational candidates awaiting scientific/human review.

Reviews and notes stay in each visitor's browser. Export review changes to share
them. The site has no scientific execution backend or provider credentials.

Publication is manual. The workflow downloads only the release pinned in
`publication.json`, checks archive and manifest hashes, rejects unlisted files or
links, verifies all native model hashes, and deploys the verified static files.
The release excludes private machine paths, private review notes, execution
queues and candidates outside this approved review pool.
