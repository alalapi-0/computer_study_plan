#!/usr/bin/env python3
"""Round 09 · Final: repo readiness checklist runner."""

import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


CHECKLIST = {
    "week1_layout": ["week1/ai_prep_tool/README.md", "week1/ai_prep_tool/.gitignore"],
    "week2_practice": ["week2/workflow_demo"],
    "week3_logic": ["week3/exercises.py"],
}


def scan(base: Path) -> dict[str, bool]:
    result: dict[str, bool] = {}
    for key, rel_paths in CHECKLIST.items():
        result[key] = all((base / rel_path).exists() for rel_path in rel_paths)
    return result


def main() -> None:
    base = Path.home() / "cli-lab" / "round9"
    base.mkdir(parents=True, exist_ok=True)

    summary = scan(base)
    print("Round 09 收口检查")
    for key, ok in summary.items():
        print(f"- {key}: {'OK' if ok else 'MISSING'}")

    mark("r09-fin-comp")
    input("请检查 rounds/round_09/final/repo_testing_cheatsheet.md 后按回车...")
    mark("r09-fin-sheet")
    input("请确认你能解释 Round 09 核心概念后按回车...")
    mark("r09-fin-acc1")


if __name__ == "__main__":
    main()
