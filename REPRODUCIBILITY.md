# Reproducibility

This repository is accompanied by a versioned DentPanX-AI reproducibility package prepared for the manuscript revision.

## Included materials

The reproducibility package contains:

- the deployment RT-DETR-L checkpoint;
- frozen train/validation/test split assignments and split metadata;
- archived Ultralytics training configurations for seeds 42, 123, and 2026;
- seed-specific independent-test metrics and class-level results;
- validation-only confidence-threshold selection materials;
- image-level bootstrap distributions and summary tables;
- precision-recall curves and confusion matrices;
- SHA-256 checksums and package inventory;
- dataset and model notices;
- a minimal functional smoke test with archived expected outputs.

## Experimental separation

Three distinct concepts are kept separate:

1. **Training variability** — summarized across independently trained checkpoints.
2. **Sampling uncertainty** — evaluated using image-level bootstrap analyses at the deployment operating point.
3. **Software verification** — evaluated using the minimal smoke test and expected output files.

The smoke test is not an additional model-performance experiment and should not be interpreted as evidence of external clinical validity.

## Minimal smoke test

The archived functional test case uses the validation-partition image identified as:

- filename: `0000568.jpg`
- confidence threshold: `0.55`
- input size: `640`
- maximum detections: `300`

Expected class composition:

- Wisdom Teeth: 4
- Dental Crown: 1
- Root Canal: 1

During package verification, the test reproduced all six detections with matching class composition and localization consistency.

## Source dataset

The full MOPG-7 dataset is not redistributed in this repository. Users should obtain the dataset from its official source and comply with the terms applicable to the dataset version they use.

## Integrity

The archived reproducibility package includes a `SHA256SUMS.csv` manifest for file-integrity verification.

## Versioning

The first archived manuscript-revision release is designated `v1.0.0`.
