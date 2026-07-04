#!/usr/bin/env python3
"""Round 19 · Week 1: generate train/test split and minimal ML loop examples."""

from __future__ import annotations

import ast
import csv
import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round19" / "week1_auto" / "train_test_split"

MINIMAL_CLASSIFIER = '''"""Minimal scikit-learn classification loop."""

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


def main() -> None:
    iris = load_iris()
    X = iris.data
    y = iris.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print("X shape:", X.shape)
    print("y shape:", y.shape)
    print("train rows:", len(X_train))
    print("test rows:", len(X_test))
    print("accuracy:", round(accuracy, 3))


if __name__ == "__main__":
    main()
'''

HOLDOUT_SPLIT_DEMO = '''#!/usr/bin/env python3
"""Dependency-free holdout split demo used by the Web UI exercise."""

from __future__ import annotations

import csv
import json
from pathlib import Path


base = Path(__file__).resolve().parent
with (base / "toy_samples.csv").open("r", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

X = [[float(row["length"]), float(row["score"])] for row in rows]
y = [row["label"] for row in rows]
split_at = int(len(rows) * 0.8)
X_train, X_test = X[:split_at], X[split_at:]
y_train, y_test = y[:split_at], y[split_at:]

label_scores = {}
for features, label in zip(X_train, y_train):
    label_scores.setdefault(label, []).append(sum(features))
centroids = {
    label: sum(values) / len(values)
    for label, values in label_scores.items()
}

def predict(features: list[float]) -> str:
    score = sum(features)
    return min(centroids, key=lambda label: abs(score - centroids[label]))

predictions = [predict(features) for features in X_test]
correct = sum(1 for expected, actual in zip(y_test, predictions) if expected == actual)
accuracy = correct / len(y_test)
summary = {
    "sample_rows": len(rows),
    "feature_count": len(X[0]),
    "train_rows": len(X_train),
    "test_rows": len(X_test),
    "labels": sorted(set(y)),
    "predictions": predictions,
    "accuracy": round(accuracy, 3),
}
(base / "split_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
'''

CONCEPTS = {
    "round": 19,
    "week": 1,
    "workflow": ["prepare X/y", "train_test_split", "fit", "predict", "evaluate"],
    "rules": [
        "X is a two-dimensional feature matrix",
        "y is a one-dimensional label vector",
        "test data is held out for evaluation",
        "random_state makes the split reproducible",
    ],
}

TOY_ROWS = [
    {"id": 1, "length": "1.0", "score": "0.10", "label": "low"},
    {"id": 2, "length": "1.2", "score": "0.20", "label": "low"},
    {"id": 3, "length": "1.4", "score": "0.15", "label": "low"},
    {"id": 4, "length": "2.0", "score": "0.70", "label": "mid"},
    {"id": 5, "length": "2.2", "score": "0.80", "label": "mid"},
    {"id": 6, "length": "2.4", "score": "0.75", "label": "mid"},
    {"id": 7, "length": "3.0", "score": "1.40", "label": "high"},
    {"id": 8, "length": "3.1", "score": "1.50", "label": "high"},
    {"id": 9, "length": "3.2", "score": "1.55", "label": "high"},
    {"id": 10, "length": "2.3", "score": "0.85", "label": "mid"},
]

STATIC_CHECK = '''#!/usr/bin/env python3
"""Static checks for Round 19 Week 1 generated ML examples."""

from __future__ import annotations

import ast
import csv
import json
import subprocess
import sys
from pathlib import Path


base = Path(__file__).resolve().parent
minimal = (base / "minimal_classifier.py").read_text(encoding="utf-8")
holdout = (base / "holdout_split_demo.py").read_text(encoding="utf-8")
ast.parse(minimal)
ast.parse(holdout)

with (base / "toy_samples.csv").open("r", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

proc = subprocess.run([sys.executable, "holdout_split_demo.py"], cwd=base, capture_output=True, text=True, check=False)
summary = {}
if proc.returncode == 0:
    summary = json.loads((base / "split_summary.json").read_text(encoding="utf-8"))

checks = {
    "sklearn_imports": all(text in minimal for text in ("load_iris", "train_test_split", "DecisionTreeClassifier", "accuracy_score")),
    "split_contract": all(text in minimal for text in ("test_size=0.2", "random_state=42", "stratify=y")),
    "fit_predict_evaluate": all(text in minimal for text in (".fit(", ".predict(", "accuracy_score(y_test, y_pred)")),
    "x_y_names": all(text in minimal for text in ("X_train", "X_test", "y_train", "y_test")),
    "toy_data": len(rows) == 10 and set(rows[0]) == {"id", "length", "score", "label"},
    "stdlib_demo_runs": proc.returncode == 0 and summary.get("train_rows") == 8 and summary.get("test_rows") == 2,
    "concepts": len(json.loads((base / "ml_concepts.json").read_text(encoding="utf-8")).get("workflow", [])) == 5,
}
report = {"ok": all(checks.values()), "checks": checks, "summary": summary, "stderr": proc.stderr.strip()}
(base / "static_check_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
raise SystemExit(0 if report["ok"] else 1)
'''


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    LAB.mkdir(parents=True)


def write_csv(path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "length", "score", "label"])
        writer.writeheader()
        writer.writerows(TOY_ROWS)


def main() -> None:
    reset_lab()
    (LAB / "minimal_classifier.py").write_text(MINIMAL_CLASSIFIER, encoding="utf-8")
    (LAB / "holdout_split_demo.py").write_text(HOLDOUT_SPLIT_DEMO, encoding="utf-8")
    (LAB / "ml_concepts.json").write_text(json.dumps(CONCEPTS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(LAB / "toy_samples.csv")
    check = LAB / "static_check.py"
    check.write_text(STATIC_CHECK, encoding="utf-8")
    check.chmod(0o755)
    proc = subprocess.run(["python3", str(check)], cwd=LAB, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    print("Round 19 Week 1 X/y 切分与最小分类闭环")
    print("sandbox:", LAB)
    print("demo:", LAB / "minimal_classifier.py")
    print("report:", LAB / "static_check_report.json")
    mark("r19-w1-ex1")


if __name__ == "__main__":
    main()
