# Adaptyv Week 5 candidate review

Public hosting for the reviewed KRAS G12D pMHC design campaign snapshot.
The scientific project repository remains private. This repository contains
publication controls; model files are supplied through a hash-verified release.

The review contains **497 candidates**, **317 highlighted review candidates**
(41 RFD3, 76 RFD4 and 200 LigandForge), and **1,788 molecular structures**:
497 native Boltz2 Fast refolds, 297 original diffusion designs and 994 validated
Boltz2 Exact alternatives. Every candidate has one Exact refold with the KRAS
peptide and one with peptide-free HLA/beta2M.
The live `publication-manifest.json` records the deployed model inventory.

[Open the review](https://benavt.github.io/adaptyv-week5-review/?campaign=kras-g12d-pmhc-review&view=explorer).
Click a plotted point or use **Inspect candidate**, then select the native refold
or available original model. The default axes compare peptide and HLA ipSAE so
all three methods are visible. LigandForge uses its top 10% peptide-ipSAE group;
reference-pose TM/DockQ remain unavailable.
Select **Boltz2 Exact** in the viewer, then choose the peptide-present or
peptide-free target. Existing scatter measurements retain their Fast model scope;
Exact-specific metric analyses are a separate next step.

Colors: HLA teal, peptide gold, proposed hotspots pink, beta2M gray and designed
binder deep blue. Models and scientific values retain their native identities.
These are computational candidates awaiting scientific/human review.

Reviews and notes stay in each visitor's browser. Export review changes to share
them. The site has no scientific execution backend or provider credentials.

Publication requires an explicit workflow dispatch. It downloads the release pinned in
`publication.json` or the scoped paired Exact configuration recorded in the dispatch,
checks archive and manifest hashes, rejects unlisted files or
links, verifies all native model hashes, and deploys the verified static files.
The release excludes private machine paths, private review notes, execution
queues and candidates outside this approved review pool.
Exact updates require all 497 paired conditions and retain every baseline model.
