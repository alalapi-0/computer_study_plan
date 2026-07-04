#!/usr/bin/env python3
"""Round 10 · Week 1: split CLI, core logic, and IO helpers."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round10" / "week1_auto" / "ai_prep_tool"


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], check=True)


CLI_TEMPLATE = '''"""CLI entry for ai_prep_tool sandbox."""

import argparse

from core import build_summary, dedup_records, filter_records
from io_utils import read_records, write_records


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai_prep_tool", description="AI prep tool sandbox")
    parser.add_argument("--input", default="input/sample.txt", help="input txt file")
    parser.add_argument("--output", default="output/result.txt", help="output txt file")
    parser.add_argument("--min-length", type=int, default=1, help="minimum stripped record length")
    parser.add_argument("--dedup", action="store_true", help="remove duplicate records while preserving order")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    original = read_records(args.input)
    records = filter_records(original, min_length=args.min_length)
    if args.dedup:
        records = dedup_records(records)
    write_records(records, args.output)
    summary = build_summary(original, records)
    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
'''

CORE_TEMPLATE = '''"""Core processing for ai_prep_tool sandbox."""


def filter_records(records: list[str], min_length: int = 1) -> list[str]:
    return [item.strip() for item in records if len(item.strip()) >= min_length]


def dedup_records(records: list[str]) -> list[str]:
    return list(dict.fromkeys(records))


def build_summary(original: list[str], processed: list[str]) -> dict[str, int]:
    return {
        "original_count": len(original),
        "processed_count": len(processed),
        "removed_count": len(original) - len(processed),
    }
'''

IO_TEMPLATE = '''"""IO helpers for ai_prep_tool sandbox."""

from pathlib import Path


def read_records(path: str) -> list[str]:
    return [line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def write_records(records: list[str], path: str) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\\n".join(records) + "\\n", encoding="utf-8")
'''


def main() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    (LAB / "input").mkdir(parents=True)
    (LAB / "output").mkdir()

    (LAB / "cli.py").write_text(CLI_TEMPLATE, encoding="utf-8")
    (LAB / "core.py").write_text(CORE_TEMPLATE, encoding="utf-8")
    (LAB / "io_utils.py").write_text(IO_TEMPLATE, encoding="utf-8")
    (LAB / "input" / "sample.txt").write_text("alpha\nb\nalpha\n\nteam\n", encoding="utf-8")
    (LAB / "README.md").write_text(
        "# Week 1 Split Modules\n\n"
        "Run: `python3 cli.py --input input/sample.txt --output output/result.txt --min-length 2 --dedup`.\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            "python3",
            "cli.py",
            "--input",
            "input/sample.txt",
            "--output",
            "output/result.txt",
            "--min-length",
            "2",
            "--dedup",
        ],
        cwd=LAB,
        check=True,
        capture_output=True,
        text=True,
    )
    output = (LAB / "output" / "result.txt").read_text(encoding="utf-8").splitlines()
    assert output == ["alpha", "team"], output
    (LAB / "week1_report.txt").write_text(result.stdout, encoding="utf-8")
    (LAB / "next_steps.txt").write_text(
        "Week 1 自动练习已生成 cli.py、core.py、io_utils.py 并跑通样例。\n"
        "自测请在 Web UI 点击 r10-w1-self 的“终端”，自己写一个薄 CLI 调用核心函数。\n"
        "能解释入口、核心逻辑和 IO 三者职责后，再手动点“记录 / 完成”。\n",
        encoding="utf-8",
    )

    print("project:", LAB)
    print(result.stdout.strip())
    print("output:", LAB / "output" / "result.txt")

    mark("r10-w1-ex1")
    print("Week 1 自动练习完成。请继续手动完成 r10-w1-self。")


if __name__ == "__main__":
    main()
