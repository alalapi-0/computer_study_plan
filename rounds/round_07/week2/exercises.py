#!/usr/bin/env python3
"""Round 07 · Week 2: argparse and logging demo runnable from Web UI."""

from __future__ import annotations

import argparse
import csv
import json
import logging
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round7" / "week2_auto"
DEFAULT_INPUT = LAB / "input" / "labels.txt"
DEFAULT_OUTPUT = LAB / "output" / "result.txt"
DEFAULT_LOG = LAB / "logs" / "week2.log"


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Round 07 Week 2 CLI demo")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Input file path")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output file path")
    parser.add_argument("--format", choices=["txt", "csv", "json", "jsonl"], default="txt", help="Input file format")
    parser.add_argument("--dedup", dest="dedup", action="store_true", default=True, help="Enable deduplication")
    parser.add_argument("--keep-duplicates", dest="dedup", action="store_false", help="Keep duplicate rows")
    return parser.parse_args()


def setup_lab() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    DEFAULT_INPUT.parent.mkdir(parents=True)
    DEFAULT_OUTPUT.parent.mkdir(parents=True)
    DEFAULT_LOG.parent.mkdir(parents=True)
    DEFAULT_INPUT.write_text("ok\nblur\nok\nbad\n", encoding="utf-8")
    (LAB / "input" / "labels.csv").write_text("id,label\n1,ok\n2,blur\n3,ok\n", encoding="utf-8")
    (LAB / "input" / "labels.json").write_text(
        json.dumps({"records": [{"id": 1, "label": "ok"}, {"id": 2, "label": "blur"}]}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    (LAB / "input" / "labels.jsonl").write_text(
        '{"id": 1, "label": "ok"}\n{"id": 2, "label": "blur"}\n{"id": 3, "label": "ok"}\n',
        encoding="utf-8",
    )


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(DEFAULT_LOG, encoding="utf-8"),
        ],
    )


def dedup_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def normalize_record(value: object) -> str:
    if isinstance(value, str):
        return value.strip()
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def load_records(path: Path, fmt: str) -> list[str]:
    if fmt == "txt":
        return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if fmt == "csv":
        with path.open(encoding="utf-8", newline="") as f:
            return [normalize_record(row) for row in csv.DictReader(f)]
    if fmt == "json":
        data = json.loads(path.read_text(encoding="utf-8"))
        rows = data.get("records", data) if isinstance(data, dict) else data
        if not isinstance(rows, list):
            raise ValueError("json_input_must_be_list_or_records")
        return [normalize_record(row) for row in rows]
    if fmt == "jsonl":
        return [
            normalize_record(json.loads(line))
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    raise ValueError(f"unsupported_format:{fmt}")


def main() -> None:
    setup_lab()
    setup_logging()
    args = parse_args()

    input_path = Path(args.input).expanduser()
    output_path = Path(args.output).expanduser()
    lines = load_records(input_path, args.format)
    processed = dedup_keep_order(lines) if args.dedup else lines
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(processed) + "\n", encoding="utf-8")

    logging.info("input=%s output=%s format=%s dedup=%s", input_path, output_path, args.format, args.dedup)
    logging.info("records=%d processed=%d", len(lines), len(processed))

    (LAB / "next_steps.txt").write_text(
        "\n".join(
            [
                "Week 2 自动练习已生成 input/labels.txt、output/result.txt 和 logs/week2.log。",
                "自测请在 Web UI 点击 r07-w2-self 的“终端”，自己写 cli_logger.py 并观察 --help 与日志文件。",
                "能解释 argparse 参数、默认值、store_true 和 logging 文件输出后，再手动点“记录 / 完成”。",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print("cli-output:", output_path)
    print("records:", len(lines))
    print("processed:", len(processed))
    print("dedup:", args.dedup)
    print("log-file:", DEFAULT_LOG)

    mark("r07-w2-ex2")
    print("Week 2 自动练习完成。请继续手动完成 r07-w2-self。")


if __name__ == "__main__":
    main()
