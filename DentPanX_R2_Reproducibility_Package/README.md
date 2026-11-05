# DentPanX-AI: Revision 2 supplementary materials

## Purpose
This folder contains supplementary analyses and reproducibility materials prepared during the second manuscript revision of DentPanX-AI. It supports image-level bootstrap estimation of AP/mAP confidence intervals and regeneration of selected false-positive and false-negative illustrations (Supplementary Figure S1).

For the software overview, installation and general use, refer to the main repository README. This folder supplements the main software documentation.

## Package contents
- `DentPanX_R2_Clean`: Colab notebook, preserved unchanged from the author-run version.
- `evidence/bootstrap/`: archived image-level inputs, AP/mAP confidence interval results and method record.
- `evidence/figures/`: normalized boxes, selected-example records, matching and coordinate records, and Supplementary Figure S1 in PNG/PDF formats.
- `evidence/SHA256.json`: checksums for the nine original evidence files.
- `SHA256.json`: checksums for all package files except this manifest itself.

Raw source radiographs, model weights and `split_assignments.csv` are not included. Their respective source licenses apply; this package does not introduce a new license.

## Running the notebook
1. Extract this package and open DentPanX_R2_Clean.ipynb in Colab; select T4 GPU.
2. Supply the frozen MOPG-7 source ZIP, best.pt and split_assignments.csv at the notebook paths, or edit those paths. The full notebook reconstructs source images and loads the model even when archived arrays are reused.
3. Copy the evidence folder to Drive. In notebook section 4, set ARCHIVE_ROOT to that evidence folder, ARCHIVE_CAPTURE = ARCHIVE_ROOT / "bootstrap", and ARCHIVE_FIG = ARCHIVE_ROOT / "figures". Leave SELECTION_PATH pointing to ARCHIVE_FIG / "final_selected_examples.csv".
4. In section 10 only, replace the two source expressions ARCHIVE_CAPTURE / "bootstrap_5000/AP_mAP_bootstrap_95CI.csv" and ARCHIVE_CAPTURE / "bootstrap_5000/bootstrap_method.json" with ARCHIVE_CAPTURE / "AP_mAP_bootstrap_95CI.csv" and ARCHIVE_CAPTURE / "bootstrap_method.json", respectively. The distributed evidence has these files directly under bootstrap.
5. Run cells in order with RECAPTURE=False to recalculate bootstrap results and regenerate the figure from archived arrays. New outputs are written to a separate revision2_reproduction directory. No model training occurs.


The archive is prepared for review; no public deposition or DOI is asserted. Figure regeneration requires the original radiographs. Stored numerical inputs and results can be inspected without them.

## Analysis methods
AP: Ultralytics 8.4.115, 315 images, 1,519 reference boxes, seven classes; confidence 0.001 for AP inference, 640 px, batch 2, FP32, max_det=300. Bootstrap: 5,000 complete-image resamples with replacement; seed 20261103; class AP absent when no corresponding target is sampled; seven-class mAP only when every class is present; percentile bounds 2.5 and 97.5. Original code's resampling order and AP computation are retained.


## Recorded environment
Python 3.13.16; torch 2.11.0+cu130; torchvision 0.26.0+cu130; CUDA 13.0; T4; numpy 2.4.6; pandas 2.2.3; Pillow 11.3.0; ultralytics 8.4.115. Only Ultralytics is installed/pinned by the notebook; Colab base packages may change. Runtime versions are written to environment.json.

## Verification scope
The author reported a successful Colab run on 4 November 2026 with archived inputs (`RECAPTURE=False`; run identifier `20261104_202550_d03916`). All 5,000 bootstrap replicates completed, AP/mAP estimates and percentile bounds matched the earlier results, and the six-panel figure was regenerated. 

