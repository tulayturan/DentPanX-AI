# DentPanX-AI v1.0.0 — Reproducibility Release

This release accompanies the manuscript **“DentPanX-AI: A Software System for Multi-Class Dental Finding Detection in Panoramic Radiographs.”**

## Scope

DentPanX-AI is research software integrating an RT-DETR-L detector for seven MOPG-7 dataset-defined categories in panoramic radiographs.

The release is intended to support transparent inspection and reproducibility of the software-centered workflow. It is not a clinically validated diagnostic medical device.

## Reproducibility materials

The v1.0.0 release is designed to include:

- deployment RT-DETR-L checkpoint;
- frozen split assignments and metadata;
- archived training configurations for seeds 42, 123, and 2026;
- seed-specific independent-test evaluation outputs;
- validation-only confidence-threshold materials;
- fixed-threshold image-level bootstrap outputs;
- precision-recall curves and confusion matrices;
- current reproduction-environment record;
- SHA-256 integrity manifest;
- minimal automated inference smoke test and expected outputs.

## Verified minimal smoke test

A minimal validation-partition test case was verified using:

- input size: 640;
- confidence threshold: 0.55;
- maximum detections: 300.

Expected and reproduced class composition:

- Wisdom Teeth: 4
- Dental Crown: 1
- Root Canal: 1

All six archived detections were reproduced during the revision verification run, with class composition preserved and localization IoU = 1.0000 for each matched detection.

## Statistical scope

Standard deviations across independently trained checkpoints describe training-related variability and are not sampling confidence intervals.

Sampling uncertainty at the deployment operating point was evaluated separately using a 5,000-replicate nonparametric image-level bootstrap for micro and class-specific precision, recall, and F1.

No bootstrap confidence intervals are claimed for mAP50, mAP50-95, or class-specific AP values in this release.

## Data

The full MOPG-7 source dataset is not redistributed. Users must obtain the dataset from its official source and comply with the license terms applicable to the dataset version they use.

## License and notices

Source-code licensing, model-weight notices, and dataset-use notices are provided separately in the repository and release archive.

## Integrity

Deployment checkpoint SHA-256:

`6e32bba3e966a0cf3017eed68940395371f9ec9bf4813b0b13456a41c58d4861`

The final DOI archive will include a complete `SHA256SUMS.csv` manifest generated after the release contents are frozen.
