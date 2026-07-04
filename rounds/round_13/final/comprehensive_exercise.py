#!/usr/bin/env python3
"""Round 13 · Final: environment reproducibility release package."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tomllib
import venv
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round13" / "final_auto" / "ai_prep_tool_release"


PYPROJECT = """[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "ai-prep-tool-release"
version = "0.1.0"
description = "Round 13 reproducible release rehearsal"
readme = "README.md"
requires-python = ">=3.10"
dependencies = []

[project.scripts]
ai-prep-release = "ai_prep_tool.cli:main"
"""

DOCKERFILE = """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p input output logs

CMD ["python", "-m", "ai_prep_tool.cli", "--help"]
"""

CLI = '''"""Tiny CLI used by the Round 13 final release rehearsal."""

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Round 13 release rehearsal CLI")
    parser.add_argument("--input", default="input/sample.txt")
    args = parser.parse_args()
    path = Path(args.input)
    print(f"input={path}")
    print(f"exists={path.exists()}")


if __name__ == "__main__":
    main()
'''

RELEASE_CHECK = '''"""Release preflight checks for the Round 13 final package."""

from pathlib import Path
import json
import tomllib


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    pyproject = tomllib.loads((base / "pyproject.toml").read_text(encoding="utf-8"))
    dockerfile = (base / "Dockerfile").read_text(encoding="utf-8")
    dockerignore = (base / ".dockerignore").read_text(encoding="utf-8").splitlines()
    required_files = [
        "README.md",
        "requirements.txt",
        "pyproject.toml",
        ".env.example",
        ".gitignore",
        ".dockerignore",
        "Dockerfile",
        "ai_prep_tool/cli.py",
    ]
    checks = {
        "required_files": all((base / item).exists() for item in required_files),
        "project_name": pyproject["project"]["name"] == "ai-prep-tool-release",
        "script_entry": "ai-prep-release" in pyproject["project"]["scripts"],
        "docker_from": "FROM python:" in dockerfile,
        "docker_cmd": "CMD [" in dockerfile,
        "dockerignore_venv": any(".venv" in line or "venv" in line for line in dockerignore),
        "dockerignore_git": ".git/" in dockerignore,
        "env_example": (base / ".env.example").read_text(encoding="utf-8").count("=") >= 3,
    }
    report = {"ok": all(checks.values()), "checks": checks, "required_files": required_files}
    (base / "release_preflight.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
'''


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    for rel in ("ai_prep_tool", "scripts", "input", "output", "logs", "dist"):
        (LAB / rel).mkdir(parents=True, exist_ok=True)


def write_release_package() -> None:
    (LAB / "README.md").write_text(
        "# ai-prep-tool release rehearsal\n\n"
        "This package demonstrates the minimum handoff files for rebuilding a Python tool.\n\n"
        "## Rebuild outline\n\n"
        "1. Create a virtual environment.\n"
        "2. Install from requirements.txt.\n"
        "3. Read pyproject.toml for package metadata.\n"
        "4. Copy .env.example to .env only on your own machine.\n"
        "5. Review Dockerfile before building an image.\n",
        encoding="utf-8",
    )
    (LAB / "requirements.txt").write_text("# no third-party dependencies for this offline rehearsal\n", encoding="utf-8")
    (LAB / "pyproject.toml").write_text(PYPROJECT, encoding="utf-8")
    (LAB / ".env.example").write_text(
        "APP_ENV=local\nLOG_LEVEL=INFO\nINPUT_DIR=input\nOUTPUT_DIR=output\n",
        encoding="utf-8",
    )
    (LAB / ".gitignore").write_text(".env\n.venv*/\n__pycache__/\n*.pyc\nlogs/\noutput/\ndist/\n", encoding="utf-8")
    (LAB / ".dockerignore").write_text(".env\n.venv*/\n__pycache__/\n*.pyc\n.git/\nlogs/\noutput/\ndist/\n", encoding="utf-8")
    (LAB / "Dockerfile").write_text(DOCKERFILE, encoding="utf-8")
    (LAB / "ai_prep_tool" / "__init__.py").write_text("", encoding="utf-8")
    (LAB / "ai_prep_tool" / "cli.py").write_text(CLI, encoding="utf-8")
    (LAB / "input" / "sample.txt").write_text("round13\nrelease\nrehearsal\n", encoding="utf-8")
    check = LAB / "scripts" / "release_check.py"
    check.write_text(RELEASE_CHECK, encoding="utf-8")
    check.chmod(0o755)
    (LAB / "RELEASE_CHECKLIST.md").write_text(
        "# Release checklist\n\n"
        "- [ ] requirements.txt exists and is intentionally small.\n"
        "- [ ] pyproject.toml has project metadata and script entry.\n"
        "- [ ] .env.example lists required variables without secrets.\n"
        "- [ ] .gitignore and .dockerignore exclude local generated files.\n"
        "- [ ] Dockerfile has been reviewed before build/run.\n",
        encoding="utf-8",
    )


def run_checks() -> tuple[subprocess.CompletedProcess[str], dict, Path]:
    venv_check = LAB.parent / ".venv_release_check"
    venv.EnvBuilder(with_pip=False, clear=True).create(venv_check)
    parsed = tomllib.loads((LAB / "pyproject.toml").read_text(encoding="utf-8"))
    proc = subprocess.run([sys.executable, str(LAB / "scripts" / "release_check.py")], cwd=LAB, capture_output=True, text=True, check=False)
    preflight = json.loads((LAB / "release_preflight.json").read_text(encoding="utf-8"))
    archive_tmp = Path(shutil.make_archive(str(LAB.parent / "ai_prep_tool_release"), "zip", LAB))
    archive = LAB / "dist" / "ai_prep_tool_release.zip"
    shutil.move(str(archive_tmp), archive)
    manifest = {
        "project_name": parsed["project"]["name"],
        "version": parsed["project"]["version"],
        "script_entry": parsed["project"]["scripts"]["ai-prep-release"],
        "preflight_ok": preflight["ok"],
        "archive": str(archive),
        "archive_exists": archive.exists(),
        "venv_cfg_exists": (venv_check / "pyvenv.cfg").exists(),
        "docker_build_executed": False,
        "note": "Dockerfile is generated and checked, but docker build/run is intentionally not executed by Web UI.",
    }
    (LAB / "handoff_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return proc, manifest, archive


def main() -> None:
    reset_lab()
    write_release_package()
    proc, manifest, archive = run_checks()
    if (
        proc.returncode != 0
        or not manifest["preflight_ok"]
        or not manifest["archive_exists"]
        or not manifest["venv_cfg_exists"]
    ):
        raise RuntimeError(f"Round 13 final release check failed: {manifest}; stderr={proc.stderr}")
    print("Round 13 收口检查")
    print("sandbox:", LAB)
    print("project_name:", manifest["project_name"])
    print("script_entry:", manifest["script_entry"])
    print("preflight_ok:", manifest["preflight_ok"])
    print("archive:", archive)
    print("docker_build_executed:", manifest["docker_build_executed"])
    print("manifest:", LAB / "handoff_manifest.json")
    mark("r13-fin-comp")


if __name__ == "__main__":
    main()
