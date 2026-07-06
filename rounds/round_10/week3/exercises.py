#!/usr/bin/env python3
"""Round 10 · Week 3: controlled errors and entry-point checks."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round10" / "week3_auto" / "ai_prep_tool"


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], check=True)


ERRORS_TEMPLATE = '''"""Domain errors for ai_prep_tool sandbox."""


class PrepToolError(Exception):
    """Base domain error for controlled user-facing failures."""


class InputMissingError(PrepToolError):
    """Raised when the input file does not exist."""
'''

CORE_TEMPLATE = '''"""Core helpers with explicit domain errors."""

from pathlib import Path

from errors import InputMissingError, PrepToolError


def read_required_text(path: str) -> str:
    target = Path(path)
    if not target.exists():
        raise InputMissingError(f"input file not found: {path}")
    text = target.read_text(encoding="utf-8")
    if not text.strip():
        raise PrepToolError("input file is empty")
    return text


def normalize_records(text: str) -> list[str]:
    records = [line.strip() for line in text.splitlines() if line.strip()]
    if not records:
        raise PrepToolError("records must not be empty")
    return records
'''

APP_TEMPLATE = '''"""Thin entry point with controlled error handling."""

import argparse
import logging

from core import normalize_records, read_required_text
from errors import PrepToolError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai_prep_tool")
    parser.add_argument("--input", default="input/sample.txt")
    return parser


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")
    args = build_parser().parse_args()
    try:
        records = normalize_records(read_required_text(args.input))
    except PrepToolError as exc:
        logging.error("%s", exc)
        print(f"error: {exc}")
        return 2
    print(f"records: {len(records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''

PYPROJECT_TEMPLATE = """[project]
name = "ai-prep-tool-sandbox"
version = "0.1.0"
description = "Round 10 entry point and error handling sandbox"
requires-python = ">=3.10"
"""


def main() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    (LAB / "input").mkdir(parents=True)
    (LAB / "errors.py").write_text(ERRORS_TEMPLATE, encoding="utf-8")
    (LAB / "core.py").write_text(CORE_TEMPLATE, encoding="utf-8")
    (LAB / "ai_prep_tool.py").write_text(APP_TEMPLATE, encoding="utf-8")
    (LAB / "pyproject.toml").write_text(PYPROJECT_TEMPLATE, encoding="utf-8")
    (LAB / "input" / "sample.txt").write_text("alpha\nbeta\n", encoding="utf-8")

    ok = subprocess.run(
        ["python3", "ai_prep_tool.py", "--input", "input/sample.txt"],
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
    assert "records: 2" in ok.stdout, ok.stdout
    assert missing.returncode == 2, missing.returncode
    assert "error: input file not found" in missing.stdout, missing.stdout
    report = (
        "success_stdout:\n" + ok.stdout
        + "\nmissing_returncode: " + str(missing.returncode)
        + "\nmissing_stdout:\n" + missing.stdout
        + "\nmissing_stderr:\n" + missing.stderr
    )
    (LAB / "error_report.txt").write_text(report, encoding="utf-8")
    (LAB / "next_steps.txt").write_text(
        "Week 3 自动练习已生成 errors.py、core.py、ai_prep_tool.py 和 pyproject.toml。\n"
        "自测请在 Web UI 点击 r10-w3-self 的“终端练习”，自己写一个返回码可控的入口脚本。\n"
        "能解释 try/except、返回码和 __main__ 入口后，再点击“记录并完成”。\n",
        encoding="utf-8",
    )

    print("project:", LAB)
    print(ok.stdout.strip())
    print("missing_returncode:", missing.returncode)
    print("report:", LAB / "error_report.txt")

    mark("r10-w3-ex3")
    print("Week 3 自动练习完成。请继续在 Web UI 点击“记录并完成”保存 r10-w3-self。")


if __name__ == "__main__":
    main()
