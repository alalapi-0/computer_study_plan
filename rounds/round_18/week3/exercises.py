#!/usr/bin/env python3
"""Round 18 · Week 3: generate a small data-analysis pipeline exercise."""

from __future__ import annotations

import ast
import csv
import json
import shutil
import statistics
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round18" / "week3_auto" / "analysis_pipeline"

DATA_ANALYSIS = '''"""Mini analysis pipeline: read, explore, clean, analyze, export."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


def load_and_explore(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print("shape:", df.shape)
    print("columns:", list(df.columns))
    print("missing_values:")
    print(df.isna().sum())
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    clean = df.dropna().copy()
    clean = clean[(clean["score"] >= 0) & (clean["score"] <= 1)]
    return clean


def analyze(df: pd.DataFrame) -> dict:
    scores = df["score"].to_numpy()
    percentiles = np.percentile(scores, [25, 50, 75])
    return {
        "total_records": int(len(df)),
        "label_distribution": df["label"].value_counts().to_dict(),
        "avg_score_by_label": df.groupby("label")["score"].mean().round(3).to_dict(),
        "score_percentiles": {
            "p25": round(float(percentiles[0]), 3),
            "p50": round(float(percentiles[1]), 3),
            "p75": round(float(percentiles[2]), 3),
        },
    }


def main() -> None:
    Path("output").mkdir(exist_ok=True)
    raw = load_and_explore("messy_sample_data.csv")
    clean = clean_data(raw)
    report = analyze(clean)
    clean.to_csv("output/clean_data.csv", index=False)
    Path("output/analysis_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
'''

PREVIEW = '''#!/usr/bin/env python3
"""Dependency-free preview of the expected analysis flow."""

from __future__ import annotations

import csv
import json
import statistics
from pathlib import Path


base = Path(__file__).resolve().parent
with (base / "messy_sample_data.csv").open("r", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

clean_rows = []
for row in rows:
    if not row["score"] or not row["length"]:
        continue
    score = float(row["score"])
    if 0 <= score <= 1:
        row["score"] = score
        row["length"] = int(row["length"])
        clean_rows.append(row)

label_distribution = {}
scores_by_label = {}
for row in clean_rows:
    label = row["label"]
    label_distribution[label] = label_distribution.get(label, 0) + 1
    scores_by_label.setdefault(label, []).append(row["score"])

avg_score_by_label = {
    label: round(statistics.mean(scores), 3)
    for label, scores in sorted(scores_by_label.items())
}
scores = sorted(row["score"] for row in clean_rows)
percentiles = {
    "p25": scores[len(scores) // 4],
    "p50": statistics.median(scores),
    "p75": scores[(len(scores) * 3) // 4],
}

report = {
    "raw_records": len(rows),
    "total_records": len(clean_rows),
    "label_distribution": label_distribution,
    "avg_score_by_label": avg_score_by_label,
    "score_percentiles": {key: round(value, 3) for key, value in percentiles.items()},
}
(base / "analysis_preview_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
'''

MESSY_ROWS = [
    {"id": 1, "label": "ok", "score": "0.91", "length": "120", "source": "web"},
    {"id": 2, "label": "bad", "score": "-0.10", "length": "42", "source": "api"},
    {"id": 3, "label": "good", "score": "0.83", "length": "310", "source": "mobile"},
    {"id": 4, "label": "blur", "score": "", "length": "88", "source": "web"},
    {"id": 5, "label": "ok", "score": "0.76", "length": "", "source": "api"},
    {"id": 6, "label": "good", "score": "0.95", "length": "175", "source": "web"},
    {"id": 7, "label": "blur", "score": "0.52", "length": "260", "source": "mobile"},
    {"id": 8, "label": "ok", "score": "1.20", "length": "99", "source": "web"},
]

CONTRACT = {
    "pipeline_steps": ["load", "explore", "clean", "analyze", "export"],
    "required_outputs": ["output/clean_data.csv", "output/analysis_report.json"],
    "cleaning_rules": ["drop missing score or length", "keep score between 0 and 1"],
    "metrics": ["label_distribution", "avg_score_by_label", "score_percentiles"],
}

STATIC_CHECK = '''#!/usr/bin/env python3
"""Static checks for Round 18 Week 3 generated analysis pipeline."""

from __future__ import annotations

import ast
import csv
import json
import subprocess
import sys
from pathlib import Path


base = Path(__file__).resolve().parent
analysis = (base / "data_analysis.py").read_text(encoding="utf-8")
preview = (base / "stdlib_preview.py").read_text(encoding="utf-8")
ast.parse(analysis)
ast.parse(preview)

with (base / "messy_sample_data.csv").open("r", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
contract = json.loads((base / "analysis_contract.json").read_text(encoding="utf-8"))

proc = subprocess.run([sys.executable, "stdlib_preview.py"], cwd=base, capture_output=True, text=True, check=False)
preview_report = {}
if proc.returncode == 0:
    preview_report = json.loads((base / "analysis_preview_report.json").read_text(encoding="utf-8"))

checks = {
    "imports": "import numpy as np" in analysis and "import pandas as pd" in analysis,
    "pipeline_functions": all(name in analysis for name in ("load_and_explore", "clean_data", "analyze", "main")),
    "cleaning_rules": ".dropna()" in analysis and 'clean["score"] >= 0' in analysis and 'clean["score"] <= 1' in analysis,
    "analysis_metrics": "value_counts()" in analysis and ".groupby(" in analysis and "np.percentile" in analysis,
    "exports": 'to_csv("output/clean_data.csv"' in analysis and "analysis_report.json" in analysis,
    "messy_rows": len(rows) == 8 and any(not row["score"] for row in rows) and any(float(row["score"] or 0) > 1 for row in rows),
    "contract": contract["pipeline_steps"] == ["load", "explore", "clean", "analyze", "export"],
    "preview_ok": proc.returncode == 0 and preview_report.get("total_records") == 4,
}
report = {"ok": all(checks.values()), "checks": checks, "preview": preview_report, "preview_stderr": proc.stderr.strip()}
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


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "label", "score", "length", "source"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    reset_lab()
    (LAB / "data_analysis.py").write_text(DATA_ANALYSIS, encoding="utf-8")
    (LAB / "stdlib_preview.py").write_text(PREVIEW, encoding="utf-8")
    (LAB / "analysis_contract.json").write_text(json.dumps(CONTRACT, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(LAB / "messy_sample_data.csv", MESSY_ROWS)
    check = LAB / "static_check.py"
    check.write_text(STATIC_CHECK, encoding="utf-8")
    check.chmod(0o755)
    proc = subprocess.run(["python3", str(check)], cwd=LAB, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    print("Round 18 Week 3 综合数据分析")
    print("sandbox:", LAB)
    print("contract:", LAB / "analysis_contract.json")
    print("report:", LAB / "static_check_report.json")
    mark("r18-w3-ex3")


if __name__ == "__main__":
    main()
