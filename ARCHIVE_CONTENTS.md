# Archive Contents for v1.0.0

The versioned DentPanX-AI reproducibility archive is intended to contain the complete materials needed to audit the reported software-centered workflow.

## GitHub repository

The GitHub repository contains lightweight, version-controlled materials suitable for direct inspection:

- source-code license and citation metadata;
- dataset and model reuse notices;
- reproducibility documentation;
- frozen split metadata and dataset configuration;
- current reproduction-environment record;
- seed-level and class-level evaluation summaries;
- validation-selected threshold metadata;
- fixed-threshold bootstrap summaries;
- minimal smoke-test code and archived expected outputs.

## Versioned archive / DOI record

The archived v1.0.0 package should additionally contain materials that are too large, binary, or unsuitable for normal Git tracking:

- packaged application source and launch materials;
- deployment checkpoint `DentPanX_AI_RTDETR_L_best.pt`;
- full `split_assignments.csv`;
- complete archived training `args.yaml` files;
- complete validation prediction and ground-truth manifests;
- bootstrap metric distributions (`.npz`);
- precision-recall curves and confusion matrices;
- package inventory and SHA-256 manifest;
- exact dependency snapshot (`pip freeze`);
- minimal functional test materials, subject to source-dataset redistribution terms.

## Integrity

The final DOI archive should include `SHA256SUMS.csv` generated after all release files are frozen.

The deployment checkpoint SHA-256 recorded during revision is:

`6e32bba3e966a0cf3017eed68940395371f9ec9bf4813b0b13456a41c58d4861`

The minimal test image used during local verification had SHA-256:

`e44c7a85886b07d9757d8aa7f24ebcf08031b8d0e362268f399f59a077d09c78`

The source image should only be redistributed when permitted by the applicable MOPG-7 dataset terms.
