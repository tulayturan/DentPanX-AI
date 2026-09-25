# DentPanX-AI Application

DentPanX-AI: A Software System for Multi-Class Dental Finding Detection in Panoramic Radiographs

DentPanX-AI is an English-language research application for detecting seven dataset-defined dental findings in panoramic radiographs.

## Model

- Architecture: RT-DETR-L
- Input resolution: 640 × 640 pixels
- Default confidence threshold: 0.55
- Threshold selection: validation partition only
- Model-selection metric: mean validation mAP50–95 across three seeds
- Independent test used for model or threshold selection: no

## Detected classes

0. Missing
1. Dental Crown
2. Root Canal
3. Caries
4. Broken Down
5. Wisdom Teeth
6. Healthy

## Windows installation

1. Obtain the versioned release archive containing `model/best.pt`.
2. Extract the archive to a normal folder.
3. Install Python 3.10 or Python 3.11.
4. During Python installation, enable Add Python to PATH.
5. Double-click `install_and_run_windows.bat`.
6. Wait for package installation and model loading.
7. The application will open in the default web browser.

For later use, double-click `run_windows.bat`.

## Linux or macOS

Open a terminal in the extracted application folder.

Run:

`chmod +x install_and_run_linux_macos.sh`

Then:

`./install_and_run_linux_macos.sh`

## Application outputs

- Annotated panoramic image in PNG format
- Object-level detection table in CSV format
- Research report in PDF format

## Important limitations

This application is a research prototype and is not a medical device.

It must not be used for autonomous diagnosis, clinical screening, treatment planning, patient management, or replacement of a dentist.

The model does not perform ICDAS staging or caries severity classification. A confidence value is a model score and is not a calibrated clinical probability.

Internal evaluation showed class-dependent performance. Dental Crown and Wisdom Teeth were stronger classes, whereas Missing and Caries showed lower sensitivity and localization performance.

## Repository versus release archive

The Git repository contains source code, configuration, metadata, and reproducibility materials. The approximately 63 MB deployment checkpoint is intentionally excluded from normal Git tracking and is intended to be distributed through the versioned release/DOI archive.

The application expects the checkpoint at:

`application/model/best.pt`

The archived checkpoint SHA-256 is documented in the repository release materials.
