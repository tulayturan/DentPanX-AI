from pathlib import Path
from collections import Counter
import json
import torch
from ultralytics import RTDETR

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent.parent

MODEL_PATH = PACKAGE / "model" / "DentPanX_AI_RTDETR_L_best.pt"
IMAGE_PATH = HERE / "0000568.jpg"
EXPECTED_JSON = HERE / "expected_output.json"

CONF = 0.55
IMGSZ = 640
MAX_DET = 300

def box_iou_xyxy(a, b):
    x1 = max(a[0], b[0])
    y1 = max(a[1], b[1])
    x2 = min(a[2], b[2])
    y2 = min(a[3], b[3])
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    area_a = max(0, a[2] - a[0]) * max(0, a[3] - a[1])
    area_b = max(0, b[2] - b[0]) * max(0, b[3] - b[1])
    union = area_a + area_b - inter
    return inter / union if union > 0 else 0.0

for p in [MODEL_PATH, IMAGE_PATH, EXPECTED_JSON]:
    if not p.exists():
        raise FileNotFoundError(p)

with open(EXPECTED_JSON, "r", encoding="utf-8") as f:
    expected = json.load(f)

expected_dets = expected["expected_detections"]
expected_count = expected["expected_number_of_detections"]
expected_classes = Counter(d["class_name"] for d in expected_dets)

device = 0 if torch.cuda.is_available() else "cpu"
model = RTDETR(str(MODEL_PATH))

results = model.predict(
    source=str(IMAGE_PATH),
    imgsz=IMGSZ,
    conf=CONF,
    max_det=MAX_DET,
    device=device,
    verbose=False,
)

r = results[0]
actual_dets = []

if r.boxes is not None and len(r.boxes) > 0:
    boxes = r.boxes.xyxy.cpu().numpy()
    confs = r.boxes.conf.cpu().numpy()
    classes = r.boxes.cls.cpu().numpy().astype(int)
    names = r.names

    for box, conf, cls in zip(boxes, confs, classes):
        actual_dets.append({
            "class_id": int(cls),
            "class_name": str(names[int(cls)]),
            "confidence": float(conf),
            "bbox_xyxy": [float(x) for x in box],
        })

actual_count = len(actual_dets)
actual_classes = Counter(d["class_name"] for d in actual_dets)

count_pass = actual_count == expected_count
class_pass = actual_classes == expected_classes

used_actual = set()
matches = []

for exp in expected_dets:
    candidates = []
    for j, act in enumerate(actual_dets):
        if j in used_actual or act["class_id"] != exp["class_id"]:
            continue
        iou = box_iou_xyxy(exp["bbox_xyxy"], act["bbox_xyxy"])
        candidates.append((iou, j, act))

    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        best_iou, best_j, best_act = candidates[0]
        used_actual.add(best_j)
        matches.append({
            "class_name": exp["class_name"],
            "iou": best_iou,
            "expected_confidence": exp["confidence"],
            "actual_confidence": best_act["confidence"],
        })
    else:
        matches.append({
            "class_name": exp["class_name"],
            "iou": 0.0,
            "expected_confidence": exp["confidence"],
            "actual_confidence": None,
        })

localization_pass = all(m["iou"] >= 0.85 for m in matches)
overall_pass = count_pass and class_pass and localization_pass

result = {
    "test_name": "DentPanX-AI minimal inference smoke test",
    "input_image": IMAGE_PATH.name,
    "confidence_threshold": CONF,
    "input_size": IMGSZ,
    "maximum_detections": MAX_DET,
    "expected_detection_count": expected_count,
    "actual_detection_count": actual_count,
    "expected_class_counts": dict(expected_classes),
    "actual_class_counts": dict(actual_classes),
    "localization_matches": matches,
    "count_pass": count_pass,
    "class_composition_pass": class_pass,
    "localization_pass": localization_pass,
    "overall_pass": overall_pass,
}

(HERE / "smoke_test_result.json").write_text(
    json.dumps(result, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

print("=" * 70)
print("DentPanX-AI Minimal Smoke Test")
print("=" * 70)
print("Detection count:", "PASS" if count_pass else "FAIL")
print("Class composition:", "PASS" if class_pass else "FAIL")
print("Localization consistency:", "PASS" if localization_pass else "FAIL")
print()
print("SMOKE TEST PASS" if overall_pass else "SMOKE TEST FAIL")
print("=" * 70)

raise SystemExit(0 if overall_pass else 1)
