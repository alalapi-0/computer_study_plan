#!/usr/bin/env python3
"""Round 18 · Week 2: generate pandas CSV exploration exercises."""

from __future__ import annotations

import ast
import csv
import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round18" / "week2_auto" / "pandas_csv"

CREATE_TEST_DATA = '''"""Create deterministic sample data for pandas practice."""

import numpy as np
import pandas as pd


def main() -> None:
    rng = np.random.default_rng(42)
    n = 200
    df = pd.DataFrame({
        "id": range(1, n + 1),
        "label": rng.choice(["ok", "blur", "bad", "good"], n),
        "score": rng.uniform(0, 1, n).round(3),
        "length": rng.integers(5, 500, n),
        "source": rng.choice(["web", "mobile", "api"], n),
    })
    df.to_csv("sample_data.csv", index=False)
    print("Created sample_data.csv")


if __name__ == "__main__":
    main()
'''

PANDAS_BASICS = '''"""Read a CSV and inspect the DataFrame surface."""

import pandas as pd


def main() -> None:
    df = pd.read_csv("sample_data.csv")
    print("shape:", df.shape)
    print("head:")
    print(df.head())
    print("dtypes:")
    print(df.dtypes)
    print("describe:")
    print(df.describe())
    print("info:")
    df.info()


if __name__ == "__main__":
    main()
'''

SELECT_FILTER = '''"""Select columns and filter rows with pandas."""

import pandas as pd


def main() -> None:
    df = pd.read_csv("sample_data.csv")
    scores = df["score"]
    subset = df[["label", "score"]]
    high_score = df[df["score"] > 0.8]
    ok_or_good = df[df["label"].isin(["ok", "good"])]
    web_high = df[(df["source"] == "web") & (df["score"] > 0.7)]

    print("score_count:", len(scores))
    print("subset_columns:", list(subset.columns))
    print("high_score_rows:", len(high_score))
    print("ok_or_good_rows:", len(ok_or_good))
    print("web_high_rows:", len(web_high))


if __name__ == "__main__":
    main()
'''

STATS_GROUPBY = '''"""Aggregate numeric columns by label."""

import pandas as pd


def main() -> None:
    df = pd.read_csv("sample_data.csv")
    print("score_stats:")
    print(df["score"].describe())
    label_stats = df.groupby("label").agg(
        count=("id", "count"),
        avg_score=("score", "mean"),
        avg_length=("length", "mean"),
    ).round(3)
    print("label_stats:")
    print(label_stats)
    print("missing_values:")
    print(df.isna().sum())


if __name__ == "__main__":
    main()
'''

SAMPLE_ROWS = [
    {"id": 1, "label": "ok", "score": "0.91", "length": "120", "source": "web"},
    {"id": 2, "label": "bad", "score": "0.18", "length": "42", "source": "api"},
    {"id": 3, "label": "good", "score": "0.83", "length": "310", "source": "mobile"},
    {"id": 4, "label": "blur", "score": "0.44", "length": "88", "source": "web"},
    {"id": 5, "label": "ok", "score": "0.76", "length": "224", "source": "api"},
    {"id": 6, "label": "good", "score": "0.95", "length": "175", "source": "web"},
]

STATIC_CHECK = '''#!/usr/bin/env python3
"""Static checks for Round 18 Week 2 generated pandas examples."""

from __future__ import annotations

import ast
import csv
import json
from pathlib import Path


base = Path(__file__).resolve().parent
sources = {
    name: (base / name).read_text(encoding="utf-8")
    for name in ("create_test_data.py", "pandas_basics.py", "select_filter.py", "stats_groupby.py")
}
for source in sources.values():
    ast.parse(source)

with (base / "sample_data.csv").open("r", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
scores = [float(row["score"]) for row in rows]
labels = sorted({row["label"] for row in rows})

basic = sources["pandas_basics.py"]
select = sources["select_filter.py"]
stats = sources["stats_groupby.py"]

checks = {
    "csv_shape": len(rows) >= 6 and set(rows[0]) == {"id", "label", "score", "length", "source"},
    "score_range": min(scores) >= 0 and max(scores) <= 1,
    "labels_present": labels == ["bad", "blur", "good", "ok"],
    "read_csv": all("pd.read_csv" in source for source in (basic, select, stats)),
    "inspect_methods": all(text in basic for text in ("df.shape", "df.head()", "df.dtypes", "df.describe()", "df.info()")),
    "select_columns": 'df["score"]' in select and 'df[["label", "score"]]' in select,
    "filter_rows": 'df["score"] > 0.8' in select and ".isin(" in select and "&" in select,
    "groupby_agg": "df.groupby" in stats and ".agg(" in stats and "df.isna().sum()" in stats,
}
report = {"ok": all(checks.values()), "checks": checks, "row_count": len(rows), "labels": labels}
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


def write_sample_csv(path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "label", "score", "length", "source"])
        writer.writeheader()
        writer.writerows(SAMPLE_ROWS)


def main() -> None:
    reset_lab()
    (LAB / "create_test_data.py").write_text(CREATE_TEST_DATA, encoding="utf-8")
    (LAB / "pandas_basics.py").write_text(PANDAS_BASICS, encoding="utf-8")
    (LAB / "select_filter.py").write_text(SELECT_FILTER, encoding="utf-8")
    (LAB / "stats_groupby.py").write_text(STATS_GROUPBY, encoding="utf-8")
    write_sample_csv(LAB / "sample_data.csv")
    check = LAB / "static_check.py"
    check.write_text(STATIC_CHECK, encoding="utf-8")
    check.chmod(0o755)
    proc = subprocess.run(["python3", str(check)], cwd=LAB, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    print("Round 18 Week 2 pandas CSV 基础")
    print("sandbox:", LAB)
    print("sample:", LAB / "sample_data.csv")
    print("report:", LAB / "static_check_report.json")
    mark("r18-w2-ex2")


if __name__ == "__main__":
    main()
