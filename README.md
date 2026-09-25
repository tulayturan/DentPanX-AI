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

Lightweight reproducibility materials are available under `reproducibility/`, including:

- frozen split metadata and dataset configuration,
- recorded reproduction-environment metadata,
- seed-level independent-test summaries,
- class-level performance summaries,
- validation-only confidence-threshold metadata,
- fixed-threshold image-level bootstrap summaries,
- a minimal automated inference smoke test with archived expected outputs.

See:

- [REPRODUCIBILITY.md](REPRODUCIBILITY.md)
- [ARCHIVE_CONTENTS.md](ARCHIVE_CONTENTS.md)
- [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md)
- [draft v1.0.0 release notes](RELEASE_NOTES_v1.0.0.md)
- [installation and exact release environment](INSTALLATION.md)

The full MOPG-7 source dataset is not redistributed in this repository.

## Model and binary archive

Large binary and complete archived materials, including the deployment checkpoint and full reproducibility package, are intended for the versioned v1.0.0 archive/DOI record rather than normal Git tracking.

Recorded deployment-checkpoint SHA-256:

`6e32bba3e966a0cf3017eed68940395371f9ec9bf4813b0b13456a41c58d4861`

## Licensing and reuse

The source-code repository is released under the GNU Affero General Public License v3.0. See [LICENSE](LICENSE).

Additional reuse information is provided in:

- [MODEL_NOTICE.md](MODEL_NOTICE.md)
- [DATASET_NOTICE.md](DATASET_NOTICE.md)

These notices distinguish source-code licensing from terms that may apply to model weights, pretrained components, and the source dataset.

## Release status

The versioned `v1.0.0` reproducibility release associated with the manuscript revision has been published: https://github.com/tulayturan/DentPanX-AI/releases/tag/v1.0.0

The application source code and launch scripts are now version-controlled under `application/`. The deployment checkpoint and other large binary materials remain reserved for the versioned release/DOI archive.

## Citation

Citation metadata are available in [CITATION.cff](CITATION.cff). The archived DOI will be added after the v1.0.0 release is deposited.

## Research-use statement

DentPanX-AI is a research prototype. It is not intended to provide patient-level diagnosis, treatment recommendations, or clinical decision support without further external, prospective, usability, and regulatory evaluation.
