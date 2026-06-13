#!/usr/bin/env python3
"""Round 08 · Final: consolidation checklist runner."""

import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


CHECKLIST = {
    "project_layout": ["README.md", "tests/test_basic.py"],
    "sqlite": ["week2/runs.db"],
    "api_rehearsal": ["week3/exercises.py"],
}


def scan(base: Path) -> dict[str, bool]:
    result: dict[str, bool] = {}
    for key, rel_files in CHECKLIST.items():
        result[key] = all((base / rel_file).exists() for rel_file in rel_files)
    return result


def main() -> None:
    base = Path.home() / "cli-lab" / "round8"
    base.mkdir(parents=True, exist_ok=True)

    summary = scan(base)
    print("Round 08 收口检查")
    for key, ok in summary.items():
        print(f"- {key}: {'OK' if ok else 'MISSING'}")

    mark("r08-fin-comp")
    input("请检查 rounds/round_08/final/upgrade_route_cheatsheet.md 后按回车...")
    mark("r08-fin-sheet")
    input("请确认你能解释 Round 08 核心概念后按回车...")
    mark("r08-fin-acc1")


if __name__ == "__main__":
    main()
