#!/usr/bin/env python3
"""Round 19 · Week 2: generate metric and overfitting examples."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round19" / "week2_auto" / "metrics_overfitting"

METRICS_DEMO = '''"""Classification metrics demo for imbalanced data."""

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
)


def main() -> None:
    X, y = make_classification(
        n_samples=1000,
        n_features=10,
        weights=[0.9, 0.1],
        random_state=42,
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("accuracy:", round(accuracy_score(y_test, y_pred), 3))
    print("precision:", round(precision_score(y_test, y_pred), 3))
    print("recall:", round(recall_score(y_test, y_pred), 3))
    print("f1:", round(f1_score(y_test, y_pred), 3))
    print(classification_report(y_test, y_pred))


if __name__ == "__main__":
    main()
'''

OVERFITTING_DEMO = '''"""Observe train/test score gap with decision tree depth."""

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


def main() -> None:
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    for depth in [1, 2, 3, 5, 10, None]:
        model = DecisionTreeClassifier(max_depth=depth, random_state=42)
        model.fit(X_train, y_train)
        train_acc = accuracy_score(y_train, model.predict(X_train))
        test_acc = accuracy_score(y_test, model.predict(X_test))
        print(f"max_depth={depth}: train={train_acc:.3f}, test={test_acc:.3f}")


if __name__ == "__main__":
    main()
'''

STDLIB_METRICS_DEMO = '''#!/usr/bin/env python3
"""Dependency-free metrics and overfitting intuition demo."""

from __future__ import annotations

import json
from pathlib import Path


tp, fp, fn, tn = 18, 4, 6, 72
accuracy = (tp + tn) / (tp + fp + fn + tn)
precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1 = 2 * precision * recall / (precision + recall)

depth_rows = [
    {"max_depth": 1, "train": 0.72, "test": 0.70},
    {"max_depth": 2, "train": 0.86, "test": 0.82},
    {"max_depth": 5, "train": 0.99, "test": 0.76},
    {"max_depth": "None", "train": 1.0, "test": 0.70},
]
for row in depth_rows:
    row["gap"] = round(row["train"] - row["test"], 3)

summary = {
    "confusion_counts": {"tp": tp, "fp": fp, "fn": fn, "tn": tn},
    "metrics": {
        "accuracy": round(accuracy, 3),
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
    },
    "depth_rows": depth_rows,
    "largest_gap": max(depth_rows, key=lambda row: row["gap"]),
}
base = Path(__file__).resolve().parent
(base / "metrics_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
'''

METRIC_EXAMPLES = {
    "round": 19,
    "week": 2,
    "confusion_counts": {"tp": 18, "fp": 4, "fn": 6, "tn": 72},
    "metric_roles": {
        "accuracy": "overall correctness",
        "precision": "how trustworthy positive predictions are",
        "recall": "how many actual positives are found",
        "f1": "balanced summary of precision and recall",
    },
    "overfitting_signal": "train score high while test score drops",
}

STATIC_CHECK = '''#!/usr/bin/env python3
"""Static checks for Round 19 Week 2 generated metric examples."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path


base = Path(__file__).resolve().parent
metrics = (base / "metrics_demo.py").read_text(encoding="utf-8")
overfit = (base / "overfitting_demo.py").read_text(encoding="utf-8")
stdlib = (base / "stdlib_metrics_demo.py").read_text(encoding="utf-8")
for source in (metrics, overfit, stdlib):
    ast.parse(source)

proc = subprocess.run([sys.executable, "stdlib_metrics_demo.py"], cwd=base, capture_output=True, text=True, check=False)
summary = {}
if proc.returncode == 0:
    summary = json.loads((base / "metrics_summary.json").read_text(encoding="utf-8"))

examples = json.loads((base / "metric_examples.json").read_text(encoding="utf-8"))
checks = {
    "metric_imports": all(name in metrics for name in ("accuracy_score", "precision_score", "recall_score", "f1_score", "classification_report")),
    "imbalanced_data": "weights=[0.9, 0.1]" in metrics and "stratify=y" in metrics,
    "metric_calls": all(name in metrics for name in ("accuracy_score(y_test, y_pred)", "precision_score(y_test, y_pred)", "recall_score(y_test, y_pred)", "f1_score(y_test, y_pred)")),
    "overfit_depths": all(text in overfit for text in ("max_depth", "train_acc", "test_acc", "[1, 2, 3, 5, 10, None]")),
    "stdlib_metrics": proc.returncode == 0 and summary.get("metrics", {}).get("f1") == 0.783,
    "gap_detected": summary.get("largest_gap", {}).get("gap", 0) >= 0.2,
    "examples": set(examples.get("metric_roles", {})) == {"accuracy", "precision", "recall", "f1"},
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


def main() -> None:
    reset_lab()
    (LAB / "metrics_demo.py").write_text(METRICS_DEMO, encoding="utf-8")
    (LAB / "overfitting_demo.py").write_text(OVERFITTING_DEMO, encoding="utf-8")
    (LAB / "stdlib_metrics_demo.py").write_text(STDLIB_METRICS_DEMO, encoding="utf-8")
    (LAB / "metric_examples.json").write_text(json.dumps(METRIC_EXAMPLES, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    check = LAB / "static_check.py"
    check.write_text(STATIC_CHECK, encoding="utf-8")
    check.chmod(0o755)
    proc = subprocess.run(["python3", str(check)], cwd=LAB, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    print("Round 19 Week 2 分类指标与过拟合观察")
    print("sandbox:", LAB)
    print("metrics:", LAB / "metrics_summary.json")
    print("report:", LAB / "static_check_report.json")
    mark("r19-w2-ex2")


if __name__ == "__main__":
    main()
