#!/usr/bin/env python3
"""Round 10 · Final: engineering layout checklist."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round10" / "final_auto" / "ai_prep_tool"


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], check=True)


FILES = {
    "cli.py": '''"""CLI parser."""

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai_prep_tool")
    parser.add_argument("--input", default="input/sample.txt")
    parser.add_argument("--output", default="")
    parser.add_argument("--config", default="config.ini")
    parser.add_argument("--dedup", action="store_true")
    return parser
''',
    "config.py": '''"""Configuration helpers."""

import configparser
from pathlib import Path


def load_config(path: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    if Path(path).exists():
        config.read(path)
    return config


def output_dir(config: configparser.ConfigParser) -> str:
    return config.get("defaults", "output_dir", fallback="output")


def log_dir(config: configparser.ConfigParser) -> str:
    return config.get("defaults", "log_dir", fallback="logs")


def min_length(config: configparser.ConfigParser) -> int:
    return config.getint("defaults", "min_length", fallback=1)
''',
    "errors.py": '''"""Domain errors."""


class PrepToolError(Exception):
    """Base error for controlled failures."""


class InputMissingError(PrepToolError):
    """Input file does not exist."""
''',
    "log_utils.py": '''"""Logging setup."""

import logging
from pathlib import Path


def setup_logging(log_dir: str) -> None:
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(Path(log_dir) / "app.log", encoding="utf-8"),
        ],
        force=True,
    )
''',
    "io_utils.py": '''"""File IO helpers."""

from pathlib import Path

from errors import InputMissingError


def read_records(path: str) -> list[str]:
    target = Path(path)
    if not target.exists():
        raise InputMissingError(f"input file not found: {path}")
    return [line.strip() for line in target.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_records(records: list[str], path: str) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\\n".join(records) + "\\n", encoding="utf-8")
''',
    "core.py": '''"""Core processing helpers."""

import logging

logger = logging.getLogger(__name__)


def filter_records(records: list[str], min_length: int) -> list[str]:
    result = [item for item in records if len(item.strip()) >= min_length]
    logger.info("filter_records: %s -> %s", len(records), len(result))
    return result


def dedup_records(records: list[str]) -> list[str]:
    result = list(dict.fromkeys(records))
    logger.info("dedup_records: %s -> %s", len(records), len(result))
    return result


def build_summary(original: list[str], processed: list[str]) -> dict[str, int]:
    return {
        "original_count": len(original),
        "processed_count": len(processed),
        "removed_count": len(original) - len(processed),
    }
''',
    "ai_prep_tool.py": '''"""Thin entry point wiring the Round 10 modules."""

from cli import build_parser
from config import load_config, log_dir, min_length, output_dir
from core import build_summary, dedup_records, filter_records
from errors import PrepToolError
from io_utils import read_records, write_records
from log_utils import setup_logging


def main() -> int:
    args = build_parser().parse_args()
    config = load_config(args.config)
    setup_logging(log_dir(config))
    try:
        original = read_records(args.input)
        records = filter_records(original, min_length(config))
        if args.dedup:
            records = dedup_records(records)
        output = args.output or f"{output_dir(config)}/result.txt"
        write_records(records, output)
    except PrepToolError as exc:
        print(f"error: {exc}")
        return 2
    summary = build_summary(original, records)
    print("summary:", summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''',
}


def write_project(base: Path) -> None:
    (base / "input").mkdir(parents=True)
    (base / "output").mkdir()
    (base / "logs").mkdir()
    (base / "README.md").write_text(
        "# AI Prep Tool\n\n"
        "Round 10 final sandbox: split CLI, config, logging, IO, core, and controlled errors.\n",
        encoding="utf-8",
    )
    (base / "config.ini").write_text(
        "[defaults]\noutput_dir = output\nlog_dir = logs\nmin_length = 3\n",
        encoding="utf-8",
    )
    (base / "pyproject.toml").write_text(
        "[project]\nname = \"ai-prep-tool-round10\"\nversion = \"0.1.0\"\nrequires-python = \">=3.10\"\n",
        encoding="utf-8",
    )
    (base / "input" / "sample.txt").write_text("ai\nprep\nprep\ntool\n", encoding="utf-8")
    for name, content in FILES.items():
        (base / name).write_text(content, encoding="utf-8")


def scan(base: Path) -> dict[str, bool]:
    required = [
        "cli.py",
        "core.py",
        "io_utils.py",
        "config.py",
        "log_utils.py",
        "errors.py",
        "ai_prep_tool.py",
        "config.ini",
        "pyproject.toml",
        "README.md",
    ]
    return {name: (base / name).exists() for name in required}


def main() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    write_project(LAB)

    success = subprocess.run(
        ["python3", "ai_prep_tool.py", "--input", "input/sample.txt", "--dedup"],
        cwd=LAB,
        check=True,
        capture_output=True,
        text=True,
    )
    missing = subprocess.run(
        ["python3", "ai_prep_tool.py", "--input", "input/missing.txt"],
        cwd=LAB,
        check=False,
        capture_output=True,
        text=True,
    )
    checks = scan(LAB)
    output = (LAB / "output" / "result.txt").read_text(encoding="utf-8").splitlines()
    log_text = (LAB / "logs" / "app.log").read_text(encoding="utf-8")
    assert all(checks.values()), checks
    assert output == ["prep", "tool"], output
    assert missing.returncode == 2, missing.returncode
    assert "filter_records" in log_text and "dedup_records" in log_text, log_text
    summary = {
        "layout": checks,
        "success_stdout": success.stdout.strip(),
        "missing_returncode": missing.returncode,
        "output_records": output,
        "log_file": str(LAB / "logs" / "app.log"),
    }
    (LAB / "round10_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("Round 10 收口检查")
    print("- layout:", "OK")
    print("- output_records:", len(output))
    print("- missing_returncode:", missing.returncode)
    print("- summary:", LAB / "round10_summary.json")

    mark("r10-fin-comp")
    print("Round 10 Final 自动练习完成。请继续在 Web UI 点击“记录并完成”保存 r10-fin-sheet 与 r10-fin-acc1。")


if __name__ == "__main__":
    main()
