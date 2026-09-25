# DentPanX-AI

DentPanX-AI is a research software system for multi-class dental finding detection in panoramic radiographs using an RT-DETR-L detector.

The repository accompanies a manuscript submitted to *BMC Oral Health* and is intended to support transparent, versioned, and verifiable research reuse.

## Scope

The software detects seven MOPG-7 dataset-defined categories:

- Missing
- Dental Crown
- Root Canal
- Caries
- Broken Down
- Wisdom Teeth
- Healthy

DentPanX-AI is intended for research and educational use. The reported results represent internal evaluation on the MOPG-7 dataset-defined categories and should not be interpreted as external clinical validation or as performance of a clinically validated diagnostic medical device.

## Reproducibility

The reproducibility materials include:

- frozen train/validation/test split assignments and metadata,
- archived training configurations,
- seed-specific evaluation results,
- validation-only confidence-threshold selection materials,
- image-level bootstrap outputs,
- precision-recall curves and selected evaluation figures,
- SHA-256 integrity manifests,
- a minimal automated smoke test with expected outputs.

The full source dataset is not redistributed in this repository.

## Release status

This repository is being prepared for the versioned v1.0.0 reproducibility release associated with the manuscript revision.

## Citation

Citation metadata and an archived DOI will be added with the versioned release.
