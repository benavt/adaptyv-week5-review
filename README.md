# Adaptyv Week 5 candidate review

[Open the twenty-candidate shortlist](https://benavt.github.io/adaptyv-week5-review/?campaign=kras-g12d-pmhc-review&view=explorer&release=20261109-viewer-001).

The November 9 update highlights **20 candidates** selected in the Week 5
academic report. Their order matches the submission CSV, with **14 RFD4,
2 RFD3 and 4 APNovo** sequences. An outer ring marks each selected candidate
in the comparison plots. The ranked shortlist appears below the inspector.
The upload CSV is available in campaign evidence.

## Campaign coverage

The complete pool contains **1,237 candidates** and **6,002 native models**.
It includes 200 RFD3, 97 RFD4, 200 LigandForge and 740 APNovo designs.
There are paired Boltz2 Exact G12D and peptide-free structures for all candidates,
six WT pilot controls, 497 Fast structures, 297 original diffusion structures,
994 AF3 structures, 994 OpenDDE structures and 740 original APNovo structures.

Scientific models and scores retain the **November 6, 2026** public snapshot.
The **1,087 PCANN estimates** in this snapshot use an exploratory pMHC calibration.
Later WT and PCANN analysis used in the academic report is outside this UI and
shortlist update. Predicted confidence and affinity require experimental testing.
The four selected APNovo candidates are explicit report selections. Their
recorded population-filtering status remains visible.

## Application and publication

The November 9 viewer repair uses [Campaign Manager PR31](https://github.com/benavt/Design_Campaign_Manager/pull/31). The Models table derives its rows and columns from this campaign’s native target, folding-engine and construct metadata. G12D, peptide-free and WT conditions replace the unrelated BETII rows. All 6,002 native structures are discoverable, with 141 alternatives across the twenty shortlisted candidates. The campaign contains the untagged construct.

The molecular viewer draws to its visible canvas directly. Target-condition
wording and the pMHC palette use HLA teal, beta2M gray, peptide gold and binder
blue. The published workspace preserves the existing shortlist revision and
browser review scope. Full upstream CI and all 348 JavaScript tests passed.
The pinned 3Dmol parser, native display transforms and cartoon mesh generation
passed for all 141 shortlisted-candidate structures. Visual browser verification
was unavailable on the publishing host.

The release pinned in `publication.json` contains the approved static files.
The Pages workflow verifies the full archive inventory, native model identities,
scientific metric bindings and every selected sequence against the upload CSV.
A pre-deployment check rejects removal of live models or regression of published
candidate and affinity-evidence counts.

Notes and reviews are browser-local and exportable. The public review has a
single-campaign full-width layout. It provides scientific evidence for review
and has no scientific job-submission backend.

Deployment uses the existing Pages OIDC identity, one deployment submission and
a bounded status poll. Receipts support reconciliation after uncertain outcomes.
