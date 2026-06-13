#!/usr/bin/env python3
"""Round 17 · Final checklist."""

import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


def main() -> None:
    base = Path.home() / "cli-lab" / "round17"
    base.mkdir(parents=True, exist_ok=True)
    markers = [base / f"week{n}" / "service_wrapup_week{n}.txt" for n in (1, 2, 3)]
    print("Round 17 收口检查")
    for path in markers:
        print(f"- {path.name}: {'OK' if path.exists() else 'MISSING'}")

    mark("r17-fin-comp")
    input("请检查 rounds/round_17/final/service_wrapup_cheatsheet.md 后按回车...")
    mark("r17-fin-sheet")
    input("请确认你能解释 Round 17 核心概念后按回车...")
    mark("r17-fin-acc1")


if __name__ == "__main__":
    main()
