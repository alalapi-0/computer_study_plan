#!/usr/bin/env python3
"""Round 07 · Week 1: pathlib plus txt/csv/json/jsonl reading."""

from __future__ import annotations

import csv
import json
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round7" / "week1_auto"


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], check=True)


def write_demo_files(base: Path) -> None:
    rows = [
        {"id": "1", "label": "ok", "score": "0.95"},
        {"id": "2", "label": "blur", "score": "0.42"},
        {"id": "3", "label": "ok", "score": "0.88"},
    ]
    (base / "labels.txt").write_text("ok\nblur\nok\n", encoding="utf-8")

    with (base / "labels.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "label", "score"])
        writer.writeheader()
        writer.writerows(rows)

    (base / "labels.json").write_text(
        json.dumps({"records": rows}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (base / "labels.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def read_demo_files(base: Path) -> dict[str, object]:
    txt_lines = [
        line.strip()
        for line in (base / "labels.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    with (base / "labels.csv").open(encoding="utf-8", newline="") as f:
        csv_rows = list(csv.DictReader(f))
    json_rows = json.loads((base / "labels.json").read_text(encoding="utf-8"))["records"]
    jsonl_rows = [
        json.loads(line)
        for line in (base / "labels.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    return {
        "formats": sorted(path.suffix.lstrip(".") for path in base.glob("labels.*")),
        "txt_count": len(txt_lines),
        "csv_labels": [row["label"] for row in csv_rows],
        "json_count": len(json_rows),
        "jsonl_count": len(jsonl_rows),
    }


def main() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    LAB.mkdir(parents=True)

    write_demo_files(LAB)
    result = read_demo_files(LAB)

    (LAB / "next_steps.txt").write_text(
        "\n".join(
            [
                "Week 1 自动练习已生成 labels.txt / labels.csv / labels.json / labels.jsonl。",
                "自测请在 Web UI 点击 r07-w1-self 的“终端练习”，进入 ~/cli-lab/round7 后自己写 read_formats.py。",
                "能解释 json 一次读取、jsonl 逐行读取、csv DictReader 后，再点击“记录并完成”。",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print("workdir:", LAB)
    print("formats:", ", ".join(result["formats"]))
    print("txt-count:", result["txt_count"])
    print("csv-labels:", ", ".join(result["csv_labels"]))
    print("json-count:", result["json_count"])
    print("jsonl-count:", result["jsonl_count"])

    mark("r07-w1-ex1")
    print("Week 1 自动练习完成。请继续在 Web UI 点击“记录并完成”保存 r07-w1-self。")


if __name__ == "__main__":
    main()
