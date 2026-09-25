# Installation and Environment Notes

## Portable application installation

The application-facing `application/requirements.txt` retains bounded dependency ranges so that the research interface can be installed on supported CPU or GPU systems.

## Exact v1.0.0 verification environment

For reproducibility auditing, the exact direct package versions verified during preparation of the v1.0.0 release are recorded in:

- `application/requirements_release_exact.txt`
- `reproducibility/environment/release_environment_exact.json`

Verified environment:

| Component | Version |
|---|---|
| Python | 3.13.15 |
| Streamlit | 1.61.1 |
| Ultralytics | 8.4.115 |
| PyTorch | 2.11.0+cu128 |
| torchvision | 0.26.0+cu128 |
| Pillow | 11.3.0 |
| pandas | 2.2.3 |
| NumPy | 2.1.3 |
| ReportLab | 4.5.1 |
| CUDA runtime | 12.8 |
| GPU used for release verification | Tesla T4 |

These versions describe the **release/reproduction verification environment**, not a retroactive claim about the exact package versions used in the historical training runs.

## PyTorch build note

The `+cu128` PyTorch and torchvision builds are CUDA 12.8 builds. Installation of those exact builds may require the corresponding official PyTorch package index rather than the default PyPI index. CPU-only users can install an appropriate CPU PyTorch build, but such an environment is not bit-for-bit identical to the recorded GPU verification environment.

## Reproducibility interpretation

Three layers are kept separate:

1. archived training arguments — original experiment configuration;
2. exact release environment — package versions verified during manuscript revision;
3. portable application dependencies — bounded versions intended to facilitate installation across systems.

This separation avoids claiming unverified historical package versions while still providing an exact, auditable release environment.
