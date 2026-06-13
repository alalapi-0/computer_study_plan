#!/usr/bin/env python3
"""Round 15 · Final checklist."""

import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


def main() -> None:
    base = Path.home() / "cli-lab" / "round15"
    base.mkdir(parents=True, exist_ok=True)
    markers = [base / f"week{n}" / "fastapi_basics_week{n}.txt" for n in (1, 2, 3)]
    print("Round 15 收口检查")
    for path in markers:
        print(f"- {path.name}: {'OK' if path.exists() else 'MISSING'}")

    mark("r15-fin-comp")
    input("请检查 rounds/round_15/final/fastapi_basics_cheatsheet.md 后按回车...")
    mark("r15-fin-sheet")
    input("请确认你能解释 Round 15 核心概念后按回车...")
    mark("r15-fin-acc1")


if __name__ == "__main__":
    main()
