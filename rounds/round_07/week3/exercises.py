#!/usr/bin/env python3
"""Round 07 · Week 3: integrate read, dedup, stats, and output."""

from __future__ import annotations

import json
import shutil
import subprocess
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round7" / "week3_auto"


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], check=True)


def write_jsonl(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def read_jsonl(path: Path) -> list[dict[str, str]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def dedup_records(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    result: list[dict[str, str]] = []
    for row in rows:
        key = (row["text"], row["label"])
        if key not in seen:
            seen.add(key)
            result.append(row)
    return result


def main() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    LAB.mkdir(parents=True)

    input_file = LAB / "input" / "records.jsonl"
    output_file = LAB / "output" / "processed.jsonl"
    report_file = LAB / "output" / "summary.json"
    rows = [
        {"id": "1", "text": "clean image", "label": "ok"},
        {"id": "2", "text": "blurred image", "label": "blur"},
        {"id": "3", "text": "clean image", "label": "ok"},
        {"id": "4", "text": "too dark", "label": "bad"},
    ]

    write_jsonl(input_file, rows)
    loaded = read_jsonl(input_file)
    deduped = dedup_records(loaded)
    stats = Counter(row["label"] for row in deduped)
    write_jsonl(output_file, deduped)
    report_file.write_text(
        json.dumps(
            {
                "input_count": len(loaded),
                "processed_count": len(deduped),
                "label_stats": dict(stats),
                "output": str(output_file),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    (LAB / "next_steps.txt").write_text(
        "\n".join(
            [
                "Week 3 自动练习已生成 records.jsonl、processed.jsonl 和 summary.json。",
                "自测请在 Web UI 点击 r07-w3-self 的“终端”，自己写 mini_prep_tool.py。",
                "能解释读取、去重 key、Counter 统计、输出文件后，再手动点“记录 / 完成”。",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print("input:", input_file)
    print("deduped:", f"{len(loaded)} -> {len(deduped)}")
    print("label-stats:", dict(stats))
    print("summary:", report_file)

    mark("r07-w3-ex3")
    print("Week 3 自动练习完成。请继续手动完成 r07-w3-self。")


if __name__ == "__main__":
    main()
