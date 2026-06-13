#!/usr/bin/env python3
"""Round 11 · Final: persistence checklist."""

import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


CHECKLIST = {
    "week1_db": ["week1/ai_prep_tool.db"],
    "week3_db_module": ["week3/ai_prep_tool/db.py"],
}


def scan(base: Path) -> dict[str, bool]:
    result: dict[str, bool] = {}
    for key, rel_paths in CHECKLIST.items():
        result[key] = all((base / rel_path).exists() for rel_path in rel_paths)
    return result


def main() -> None:
    base = Path.home() / "cli-lab" / "round11"
    base.mkdir(parents=True, exist_ok=True)

    summary = scan(base)
    print("Round 11 收口检查")
    for key, ok in summary.items():
        print(f"- {key}: {'OK' if ok else 'MISSING'}")

    mark("r11-fin-comp")
    input("请检查 rounds/round_11/final/sqlite_persistence_cheatsheet.md 后按回车...")
    mark("r11-fin-sheet")
    input("请确认你能解释 Round 11 核心概念后按回车...")
    mark("r11-fin-acc1")


if __name__ == "__main__":
    main()
