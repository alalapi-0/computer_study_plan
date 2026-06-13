#!/usr/bin/env python3
"""Round 20 · Final checklist."""

import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


def main() -> None:
    base = Path.home() / "cli-lab" / "round20"
    base.mkdir(parents=True, exist_ok=True)
    markers = [base / f"week{n}" / "pytorch_intro_week{n}.txt" for n in (1, 2, 3)]
    print("Round 20 收口检查")
    for path in markers:
        print(f"- {path.name}: {'OK' if path.exists() else 'MISSING'}")

    mark("r20-fin-comp")
    input("请检查 rounds/round_20/final/pytorch_intro_cheatsheet.md 后按回车...")
    mark("r20-fin-sheet")
    input("请确认你能解释 Round 20 核心概念后按回车...")
    mark("r20-fin-acc1")


if __name__ == "__main__":
    main()
