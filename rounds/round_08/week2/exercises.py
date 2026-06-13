#!/usr/bin/env python3
"""Round 08 · Week 2 exercises: sqlite3 basics."""

import sqlite3
from datetime import datetime
import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


DB_PATH = Path.home() / "cli-lab" / "round8" / "week2" / "runs.db"


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_file TEXT,
            output_file TEXT,
            original_count INTEGER,
            processed_count INTEGER,
            run_time TEXT
        )
        """
    )
    conn.commit()


def insert_demo(conn: sqlite3.Connection) -> None:
    conn.execute(
        "INSERT INTO runs (input_file, output_file, original_count, processed_count, run_time) VALUES (?, ?, ?, ?, ?)",
        ("input/demo.txt", "output/demo.txt", 12, 10, datetime.now().isoformat(timespec="seconds")),
    )
    conn.commit()


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    insert_demo(conn)
    count = conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
    conn.close()

    print("数据库位置:", DB_PATH)
    print("当前 runs 记录数:", count)

    mark("r08-w2-ex2")
    input("请手动完成第2周自测后按回车继续...")
    mark("r08-w2-self")


if __name__ == "__main__":
    main()
