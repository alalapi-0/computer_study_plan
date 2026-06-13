#!/usr/bin/env python3
"""Round 07 · Week 2 exercises: argparse and logging."""

import argparse
import logging
import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Round 07 Week 2 CLI demo")
    parser.add_argument("--input", required=True, help="Input file path")
    parser.add_argument("--output", default="output/result.txt", help="Output file path")
    parser.add_argument("--format", choices=["txt", "csv", "json", "jsonl"], default="txt")
    parser.add_argument("--dedup", action="store_true", help="Enable deduplication")
    return parser.parse_args()


def main() -> None:
    Path("logs").mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler("logs/week2.log", encoding="utf-8")],
    )

    args = parse_args()
    logging.info("input=%s output=%s format=%s dedup=%s", args.input, args.output, args.format, args.dedup)
    print("运行成功，下一步把本周参数解析接入综合工具。")

    mark("r07-w2-ex2")
    input("请手动完成第2周自测后按回车继续...")
    mark("r07-w2-self")


if __name__ == "__main__":
    main()
