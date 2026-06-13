#!/usr/bin/env python3
"""Round 11 · Week 1 exercises: create SQLite schema."""

import sqlite3
import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_file TEXT NOT NULL,
    output_file TEXT NOT NULL,
    raw_count INTEGER NOT NULL,
    final_count INTEGER NOT NULL,
    run_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


def main() -> None:
    base = Path.home() / "cli-lab" / "round11" / "week1"
    base.mkdir(parents=True, exist_ok=True)
    db_path = base / "ai_prep_tool.db"

    with sqlite3.connect(db_path) as conn:
        conn.executescript(SCHEMA)
        conn.commit()

    print("已初始化 SQLite:", db_path)
    print("runs 表已创建（若不存在）。")

    mark("r11-w1-ex1")
    input("请手动完成第1周自测后按回车继续...")
    mark("r11-w1-self")


if __name__ == "__main__":
    main()
