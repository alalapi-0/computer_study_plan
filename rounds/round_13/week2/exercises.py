#!/usr/bin/env python3
"""Round 13 · Week 2: pyproject.toml and configuration sample."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round13" / "week2_auto" / "project_config"


PYPROJECT = """[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "ai-prep-tool"
version = "0.1.0"
description = "Local AI data preparation rehearsal tool"
readme = "README.md"
requires-python = ">=3.10"
dependencies = []

[project.scripts]
ai-prep = "ai_prep_tool.settings:main"

[tool.round13]
stage = "environment-reproducibility"
web_ui_safe = true
"""

SETTINGS = '''"""Minimal settings reader for the Round 13 project config rehearsal."""

from pathlib import Path


def parse_env_example(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip()
    return values


def main() -> None:
    env_path = Path(__file__).resolve().parents[1] / ".env.example"
    values = parse_env_example(env_path)
    print(f"loaded={len(values)} keys")
    for key in sorted(values):
        print(f"{key}={values[key]}")


if __name__ == "__main__":
    main()
'''


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    (LAB / "ai_prep_tool").mkdir(parents=True)


def write_project() -> dict:
    (LAB / "pyproject.toml").write_text(PYPROJECT, encoding="utf-8")
    (LAB / ".env.example").write_text(
        "# Copy to .env locally if you need real overrides. Do not commit real .env files.\n"
        "APP_ENV=local\n"
        "LOG_LEVEL=INFO\n"
        "INPUT_DIR=input\n"
        "OUTPUT_DIR=output\n",
        encoding="utf-8",
    )
    (LAB / ".gitignore").write_text(".env\n.venv*/\n__pycache__/\n*.pyc\nlogs/\noutput/\n", encoding="utf-8")
    (LAB / "requirements.txt").write_text("# no third-party dependencies for this rehearsal\n", encoding="utf-8")
    (LAB / "README.md").write_text(
        "# ai-prep-tool config rehearsal\n\n"
        "Read pyproject.toml for project metadata and .env.example for required local settings.\n",
        encoding="utf-8",
    )
    (LAB / "ai_prep_tool" / "__init__.py").write_text("", encoding="utf-8")
    (LAB / "ai_prep_tool" / "settings.py").write_text(SETTINGS, encoding="utf-8")
    parsed = tomllib.loads((LAB / "pyproject.toml").read_text(encoding="utf-8"))
    proc = subprocess.run(
        [sys.executable, str(LAB / "ai_prep_tool" / "settings.py")],
        cwd=LAB,
        capture_output=True,
        text=True,
        check=False,
    )
    report = {
        "sandbox": str(LAB),
        "project_name": parsed["project"]["name"],
        "version": parsed["project"]["version"],
        "requires_python": parsed["project"]["requires-python"],
        "script_entry": parsed["project"]["scripts"]["ai-prep"],
        "settings_returncode": proc.returncode,
        "settings_stdout": proc.stdout.strip().splitlines(),
        "env_keys": ["APP_ENV", "INPUT_DIR", "LOG_LEVEL", "OUTPUT_DIR"],
    }
    (LAB / "config_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (LAB / "next_steps.txt").write_text(
        "在浏览器终端自己写一个小 pyproject.toml 或 .env.example 检查命令，再手动记录 r13-w2-self。\n",
        encoding="utf-8",
    )
    return report


def main() -> None:
    reset_lab()
    report = write_project()
    if (
        report["project_name"] != "ai-prep-tool"
        or report["settings_returncode"] != 0
        or "LOG_LEVEL=INFO" not in report["settings_stdout"]
    ):
        raise RuntimeError(f"Week 2 config rehearsal failed: {report}")
    print("Round 13 Week 2 pyproject 与配置样例")
    print("sandbox:", LAB)
    print("pyproject:", LAB / "pyproject.toml")
    print("env_example:", LAB / ".env.example")
    print("script_entry:", report["script_entry"])
    print("report:", LAB / "config_report.json")
    mark("r13-w2-ex2")


if __name__ == "__main__":
    main()
