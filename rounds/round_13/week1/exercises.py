#!/usr/bin/env python3
"""Round 13 · Week 1: venv structure and requirements rehearsal."""

from __future__ import annotations

import json
import subprocess
import sys
import venv
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round13" / "week1_auto" / "env_basics"


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> None:
    LAB.mkdir(parents=True, exist_ok=True)
    for path in LAB.glob("*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir() and path.name != ".venv_demo":
            for child in sorted(path.rglob("*"), reverse=True):
                if child.is_file() or child.is_symlink():
                    child.unlink()
                elif child.is_dir():
                    child.rmdir()
            path.rmdir()
    venv_dir = LAB / ".venv_demo"
    if venv_dir.exists():
        for child in sorted(venv_dir.rglob("*"), reverse=True):
            if child.is_file() or child.is_symlink():
                child.unlink()
            elif child.is_dir():
                child.rmdir()
        venv_dir.rmdir()


def write_files() -> dict:
    venv_dir = LAB / ".venv_demo"
    venv.EnvBuilder(with_pip=False, clear=True).create(venv_dir)
    requirements = LAB / "requirements.txt"
    requirements.write_text(
        "# Round 13 offline rehearsal: no third-party runtime dependencies yet.\n"
        "# Add pinned packages only when you intentionally install them.\n",
        encoding="utf-8",
    )
    (LAB / ".gitignore").write_text(
        ".venv*/\n"
        "__pycache__/\n"
        "*.pyc\n"
        "logs/\n"
        "output/\n",
        encoding="utf-8",
    )
    (LAB / "README.md").write_text(
        "# Round 13 Week 1 sandbox\n\n"
        "This directory demonstrates the files needed to rebuild a Python environment.\n",
        encoding="utf-8",
    )
    pyvenv_cfg = venv_dir / "pyvenv.cfg"
    report = {
        "sandbox": str(LAB),
        "python": sys.executable,
        "venv_exists": venv_dir.exists(),
        "pyvenv_cfg_exists": pyvenv_cfg.exists(),
        "requirements_lines": len(requirements.read_text(encoding="utf-8").splitlines()),
        "ignored": [".venv*/", "__pycache__/", "*.pyc", "logs/", "output/"],
        "rebuild_hint": "python3 -m venv .venv && python3 -m pip install -r requirements.txt",
    }
    (LAB / "env_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (LAB / "next_steps.txt").write_text(
        "在浏览器终端自己创建 week1_self/.venv_self，并点击“记录并完成”保存记录 r13-w1-self。\n",
        encoding="utf-8",
    )
    return report


def main() -> None:
    reset_lab()
    report = write_files()
    if not report["venv_exists"] or not report["pyvenv_cfg_exists"] or report["requirements_lines"] < 2:
        raise RuntimeError(f"Week 1 environment rehearsal failed: {report}")
    print("Round 13 Week 1 环境复现基础")
    print("sandbox:", LAB)
    print("venv:", LAB / ".venv_demo")
    print("requirements:", LAB / "requirements.txt")
    print("report:", LAB / "env_report.json")
    print("rebuild_hint:", report["rebuild_hint"])
    mark("r13-w1-ex1")


if __name__ == "__main__":
    main()
