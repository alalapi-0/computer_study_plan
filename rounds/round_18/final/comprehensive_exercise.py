#!/usr/bin/env python3
"""Round 18 · Final checklist."""

import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


def main() -> None:
    base = Path.home() / "cli-lab" / "round18"
    base.mkdir(parents=True, exist_ok=True)
    markers = [base / f"week{n}" / "numerics_analytics_week{n}.txt" for n in (1, 2, 3)]
    print("Round 18 收口检查")
    for path in markers:
        print(f"- {path.name}: {'OK' if path.exists() else 'MISSING'}")

    mark("r18-fin-comp")
    input("请检查 rounds/round_18/final/numerics_analytics_cheatsheet.md 后按回车...")
    mark("r18-fin-sheet")
    input("请确认你能解释 Round 18 核心概念后按回车...")
    mark("r18-fin-acc1")


if __name__ == "__main__":
    main()
