# Adaptyv Week 5 candidate review

Public hosting for the reviewed KRAS G12D pMHC design campaign snapshot.
The scientific project repository remains private. This repository contains
publication controls; model files are supplied through a hash-verified release.

The review contains **497 candidates**, **317 highlighted review candidates**
(41 RFD3, 76 RFD4 and 200 LigandForge), and **1,794 molecular structures**:
497 native Boltz2 Fast refolds, 297 original diffusion designs 994 validated
paired Boltz2 Exact alternatives and six WT Exact pilot models. Every candidate has one Exact refold with the KRAS
peptide and one with peptide-free HLA/beta2M.
The live `publication-manifest.json` records the deployed model inventory.

[Open the review](https://benavt.github.io/adaptyv-week5-review/?campaign=kras-g12d-pmhc-review&view=explorer).
Click a plotted point or use **Inspect candidate**, then select the native refold
or available original model. The default comparison shows exploratory G12D-versus-WT PCANN estimates for six
pilot candidates. The **Comparison** menu adds G12D versus peptide-free and WT
versus peptide-free, with shared logarithmic nM axes and equality guides. The
other 491 candidates have no PCANN estimates and are excluded from these plots,
not assigned zero. The seven existing confidence/pose panels remain available: paired HLA
confidence, peptide confidence versus HLA change, original-design DockQ,
Fast-pose DockQ, across-condition binder TM versus DockQ, Fast versus Exact
peptide confidence, and the retained Fast review. Each point opens its native
model; model-viewer controls remain available independently. LigandForge uses its top 10% peptide-ipSAE group;
reference-pose TM/DockQ remain unavailable.
Select **Boltz2 Exact** in the viewer, then choose the peptide-present or
peptide-free target. All 994 Exact models are scored with native ipSAE; 2,485 interface scores were
independently reproduced from retained PAE matrices. Downloadable condition,
paired and pose-comparison tables include model/reference hashes, scope and
missingness flags. Original Fast measurements and all highlights are unchanged.

Median paired HLA ipSAE change (present minus free) is +0.261 for RFD4, −0.098
for RFD3 and −0.423 for LigandForge in this selected cohort. These prediction
comparisons do not establish experimental binding or peptide selectivity.
There is one sample per condition. WT predictions cover only the six pilot candidates.
DockQ comparisons share HLA1–181 in both conditions; present-model design-pose
comparisons also include peptide1–10. Binder TM aligns the binder independently.
Original-design heavy-atom DockQ is available for 277 diffusion candidates;
20 target-mismatched originals remain unscored. Interfaces with no reference
contacts also remain missing, never zero.

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

Scored Exact updates additionally verify all 994 condition bindings, 497 pairs,
2,879 pose comparisons, source hashes and missing peptide/original-pose rules.

The November6 selectivity repair exposes the recorded HLA, beta2M and peptide interface confidence for all497 candidates in Target comparison. Native structures, scientific values and317 highlights are unchanged. The original repair did not include affinity predictions. The new exploratory pilot
adds 18 grouped-PCANN Kd estimates on their exact native models: two RFD3, two
RFD4 and two LigandForge candidates, each with G12D, WT and peptide-free controls.
The scored interaction is designed binder A against HLA B, beta2M C and (when
present) peptide D. PCANN pMHC calibration is unvalidated; these are not measured
affinities or demonstrated selectivity. No WT ipSAE/TM/DockQ is imputed.
Choose a pilot candidate and the WT target in the Boltz2 Exact viewer to inspect
its independent WT structure. The palette and all 317 highlights are preserved.
Download the plot comparison table or the native model for source-bound evidence.
DeltaForge has not been run and external scoring credits spent remain zero.
