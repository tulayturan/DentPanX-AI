# Archived Training Configuration

The original experiment outputs preserve Ultralytics `args.yaml` files for the three RT-DETR-L 640-pixel runs used in the repeated-seed analysis.

Common recorded settings include:

| Setting | Value |
|---|---|
| Task | detect |
| Architecture | RT-DETR-L |
| Pretrained checkpoint | `rtdetr-l.pt` |
| Input size | 640 |
| Maximum epochs | 150 |
| Early-stopping patience | 30 |
| Physical batch size | 2 |
| Optimizer | auto |
| Cosine learning-rate schedule | enabled |
| AMP | enabled |
| Deterministic mode | enabled |
| Close mosaic | 10 |
| Validation IoU | 0.70 |
| Maximum detections | 300 |
| Workers | 2 |

Repeated seeds:

- 42
- 123
- 2026

The seed-42 run originated from the exploratory 640-pixel architecture-screening stage and was subsequently retained as one of the three RT-DETR-L checkpoints. Seeds 123 and 2026 were trained during the repeated-seed validation stage.

The complete original `args.yaml` files and run materials are retained in the versioned reproducibility archive. This GitHub document is a human-readable summary and should not be substituted for the archived configuration files when exact field-level reproduction is required.
