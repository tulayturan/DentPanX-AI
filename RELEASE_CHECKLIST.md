# v1.0.0 Release Checklist

## Already prepared

- [x] Public GitHub repository
- [x] README
- [x] AGPL-3.0 source-code license
- [x] CITATION.cff
- [x] MODEL_NOTICE.md
- [x] DATASET_NOTICE.md
- [x] PACKAGE_VERSION.json
- [x] REPRODUCIBILITY.md
- [x] frozen split metadata
- [x] dataset YAML
- [x] current reproduction-environment record
- [x] seed-level test summary
- [x] class-level mean performance summary
- [x] validation-selected threshold summary
- [x] fixed-threshold micro bootstrap summary
- [x] fixed-threshold class bootstrap summary
- [x] minimal smoke-test script
- [x] expected smoke-test outputs
- [x] draft v1.0.0 release notes

## Still required before publishing v1.0.0

- [x] import the actual DentPanX-AI application source files and launch scripts
- [x] add the final exact v1.0.0 release dependency snapshot
- [ ] place the deployment checkpoint in the versioned binary archive
- [x] include complete archived run configuration files in GitHub; retain full split assignments in the binary reproducibility archive
- [ ] include full evaluation/PR/confusion-matrix and bootstrap-distribution materials in the DOI archive
- [ ] regenerate SHA256SUMS.csv after the archive is frozen
- [ ] verify whether the minimal MOPG-7 source image may be redistributed; omit it if redistribution is uncertain
- [ ] create GitHub tag/release `v1.0.0`
- [ ] archive the release in Zenodo and obtain a DOI
- [ ] add the Zenodo DOI to CITATION.cff, README, manuscript, and reviewer response
