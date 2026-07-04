#!/usr/bin/env python3
"""Round 07 · Final: small AI data prep tool runnable from Web UI."""

from __future__ import annotations

import argparse
import csv
import json
import logging
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round7" / "final_auto"
DEFAULT_INPUT = LAB / "input" / "labels.txt"
DEFAULT_OUTPUT = LAB / "output" / "result.txt"
DEFAULT_LOG = LAB / "logs" / "round7_final.log"


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI prep tool minimal demo")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Input path")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output path")
    parser.add_argument("--format", choices=["txt", "csv", "json", "jsonl"], default="txt", help="Input format")
    parser.add_argument("--dedup", dest="dedup", action="store_true", default=True, help="Enable deduplication")
    parser.add_argument("--keep-duplicates", dest="dedup", action="store_false", help="Keep duplicate records")
    return parser.parse_args()


def setup_lab() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    (LAB / "input").mkdir(parents=True)
    (LAB / "output").mkdir()
    (LAB / "logs").mkdir()
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


def maybe_dedup(lines: list[str], enabled: bool) -> list[str]:
    if not enabled:
        return lines
    seen: set[str] = set()
    result: list[str] = []
    for line in lines:
        if line not in seen:
            seen.add(line)
            result.append(line)
    return result


def dump_lines(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    setup_lab()
    setup_logging()
    args = parse_args()

    src = Path(args.input).expanduser()
    dst = Path(args.output).expanduser()
    original = load_records(src, args.format)
    processed = maybe_dedup(original, args.dedup)
    dump_lines(dst, processed)

    summary = {
        "input": str(src),
        "format": args.format,
        "output": str(dst),
        "original": len(original),
        "processed": len(processed),
        "removed": len(original) - len(processed),
        "dedup": args.dedup,
        "log": str(DEFAULT_LOG),
    }
    (LAB / "output" / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    logging.info(
        "input=%s format=%s original=%d output=%s processed=%d dedup=%s",
        src,
        args.format,
        len(original),
        dst,
        len(processed),
        args.dedup,
    )

    print("Summary")
    print("- original:", summary["original"])
    print("- processed:", summary["processed"])
    print("- removed:", summary["removed"])
    print("- output:", dst)
    print("- log:", DEFAULT_LOG)

    mark("r07-fin-comp")
    print("Round 07 Final 自动练习完成。请继续手动完成 r07-fin-sheet 与 r07-fin-acc1。")


if __name__ == "__main__":
    main()
