# DentPanX-AI Minimal Test Case

## Purpose

This directory provides a minimal functional test case for the DentPanX-AI research software.

The test case was selected from the validation partition and was not used as an independent-test performance estimate.

## Input

Image: `0000568.jpg`

Input size: 640

Confidence threshold: 0.55

Maximum detections: 300

## Expected functional output

Expected number of detections: 6

Expected class composition:

- Wisdom Teeth: 4
- Dental Crown: 1
- Root Canal: 1

The archived reference output is provided in:

- `expected_output.csv`
- `expected_output.json`

The corresponding dataset annotation is provided only as a reproducibility reference in:

- `ground_truth_reference.csv`

## Interpretation

This test case is intended only to verify that the packaged checkpoint can be loaded and can reproduce the expected type and composition of output under the documented operating settings.

It is not an additional validation experiment and should not be interpreted as evidence of diagnostic accuracy or clinical validity.

Minor floating-point differences in confidence scores or bounding-box coordinates may occur across software, CUDA, GPU, or operating-system environments. Functional verification should therefore prioritize successful inference, detection count, class composition, and approximately consistent localization rather than requiring bit-for-bit equality of floating-point outputs.

The source radiograph itself is not tracked in Git. Users should obtain it from the official MOPG-7 source when redistribution is not clearly permitted.
