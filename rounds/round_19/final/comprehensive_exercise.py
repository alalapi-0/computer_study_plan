#!/usr/bin/env python3
"""Round 19 · Final checklist."""

import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


def main() -> None:
    base = Path.home() / "cli-lab" / "round19"
    base.mkdir(parents=True, exist_ok=True)
    markers = [base / f"week{n}" / "ml_minimal_loop_week{n}.txt" for n in (1, 2, 3)]
    print("Round 19 收口检查")
    for path in markers:
        print(f"- {path.name}: {'OK' if path.exists() else 'MISSING'}")

    mark("r19-fin-comp")
    input("请检查 rounds/round_19/final/ml_minimal_loop_cheatsheet.md 后按回车...")
    mark("r19-fin-sheet")
    input("请确认你能解释 Round 19 核心概念后按回车...")
    mark("r19-fin-acc1")


if __name__ == "__main__":
    main()
