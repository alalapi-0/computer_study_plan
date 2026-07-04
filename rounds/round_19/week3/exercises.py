#!/usr/bin/env python3
"""Round 19 · Week 3: generate preprocessing, Pipeline, and leakage checks."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round19" / "week3_auto" / "pipeline_leakage"

PREPROCESSING_CORRECT = '''"""Correct preprocessing: fit on train, transform train and test."""

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def main() -> None:
    X, y = load_breast_cancer(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train_scaled, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test_scaled))
    print("accuracy:", round(accuracy, 3))


if __name__ == "__main__":
    main()
'''

PIPELINE_DEMO = '''"""Pipeline wraps preprocessing and model training together."""

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def main() -> None:
    X, y = load_breast_cancer(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000, random_state=42)),
    ])
    pipe.fit(X_train, y_train)
    print("test_score:", round(pipe.score(X_test, y_test), 3))
    scores = cross_val_score(pipe, X, y, cv=5)
    print("cv_mean:", round(scores.mean(), 3))


if __name__ == "__main__":
    main()
'''

LEAKAGE_NOTES = '''"""Data leakage examples: wrong pattern vs correct pattern."""


WRONG_PATTERN = "scaler.fit(X) before train_test_split leaks test distribution"
RIGHT_PATTERN = "split first, scaler.fit(X_train), scaler.transform(X_train), scaler.transform(X_test)"


def explain() -> dict:
    return {
        "wrong": WRONG_PATTERN,
        "right": RIGHT_PATTERN,
        "why_pipeline_helps": "Pipeline keeps preprocessing inside the estimator workflow.",
    }
'''

STDLIB_SCALER_CHECK = '''#!/usr/bin/env python3
"""Dependency-free scaler rule check."""

from __future__ import annotations

import json
from pathlib import Path


train = [10.0, 12.0, 14.0, 16.0]
test = [30.0, 32.0]
train_mean = sum(train) / len(train)
train_variance = sum((value - train_mean) ** 2 for value in train) / len(train)
train_scale = train_variance ** 0.5
full = train + test
full_mean = sum(full) / len(full)

train_scaled = [(value - train_mean) / train_scale for value in train]
test_scaled = [(value - train_mean) / train_scale for value in test]
summary = {
    "train_mean": round(train_mean, 3),
    "full_mean": round(full_mean, 3),
    "means_differ": train_mean != full_mean,
    "train_scaled_first": round(train_scaled[0], 3),
    "test_scaled_first": round(test_scaled[0], 3),
    "rule": "fit on train, transform train and test",
}
base = Path(__file__).resolve().parent
(base / "preprocessing_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
'''

CONTRACT = {
    "round": 19,
    "week": 3,
    "rules": [
        "split before fit",
        "fit preprocessing on training data",
        "transform training and test data with the training-fitted transformer",
        "prefer Pipeline for preprocessing plus model chains",
    ],
    "forbidden_in_correct_path": ["scaler.fit(X)", "fit_transform(X_test)"],
}

STATIC_CHECK = '''#!/usr/bin/env python3
"""Static checks for Round 19 Week 3 generated preprocessing examples."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path


base = Path(__file__).resolve().parent
correct = (base / "preprocessing_correct.py").read_text(encoding="utf-8")
pipeline = (base / "pipeline_demo.py").read_text(encoding="utf-8")
leakage = (base / "leakage_notes.py").read_text(encoding="utf-8")
stdlib = (base / "stdlib_scaler_check.py").read_text(encoding="utf-8")
for source in (correct, pipeline, leakage, stdlib):
    ast.parse(source)

proc = subprocess.run([sys.executable, "stdlib_scaler_check.py"], cwd=base, capture_output=True, text=True, check=False)
summary = {}
if proc.returncode == 0:
    summary = json.loads((base / "preprocessing_summary.json").read_text(encoding="utf-8"))

contract = json.loads((base / "preprocessing_contract.json").read_text(encoding="utf-8"))
checks = {
    "correct_imports": all(text in correct for text in ("StandardScaler", "LogisticRegression", "accuracy_score", "train_test_split")),
    "fit_on_train_only": "scaler.fit_transform(X_train)" in correct and "scaler.transform(X_test)" in correct and "scaler.fit(X)" not in correct,
    "pipeline_imports": all(text in pipeline for text in ("Pipeline", "cross_val_score", "StandardScaler", "LogisticRegression")),
    "pipeline_steps": '("scaler", StandardScaler())' in pipeline and '("model", LogisticRegression' in pipeline,
    "leakage_notes": "scaler.fit(X) before train_test_split" in leakage and "scaler.fit(X_train)" in leakage,
    "stdlib_rule": proc.returncode == 0 and summary.get("means_differ") is True and summary.get("rule") == "fit on train, transform train and test",
    "contract_rules": len(contract.get("rules", [])) >= 4 and "scaler.fit(X)" in contract.get("forbidden_in_correct_path", []),
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
    (LAB / "preprocessing_correct.py").write_text(PREPROCESSING_CORRECT, encoding="utf-8")
    (LAB / "pipeline_demo.py").write_text(PIPELINE_DEMO, encoding="utf-8")
    (LAB / "leakage_notes.py").write_text(LEAKAGE_NOTES, encoding="utf-8")
    (LAB / "stdlib_scaler_check.py").write_text(STDLIB_SCALER_CHECK, encoding="utf-8")
    (LAB / "preprocessing_contract.json").write_text(json.dumps(CONTRACT, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    check = LAB / "static_check.py"
    check.write_text(STATIC_CHECK, encoding="utf-8")
    check.chmod(0o755)
    proc = subprocess.run(["python3", str(check)], cwd=LAB, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    print("Round 19 Week 3 预处理、Pipeline 与泄漏检查")
    print("sandbox:", LAB)
    print("summary:", LAB / "preprocessing_summary.json")
    print("report:", LAB / "static_check_report.json")
    mark("r19-w3-ex3")


if __name__ == "__main__":
    main()
