#!/usr/bin/env python3
"""Round 08 · Week 2: sqlite3 run history persistence."""

from __future__ import annotations

import shutil
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round8" / "week2_auto"
DB_PATH = LAB / "runs.db"


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], check=True)


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


def insert_run(conn: sqlite3.Connection, input_file: str, output_file: str, original: int, processed: int) -> None:
    conn.execute(
        "INSERT INTO runs (input_file, output_file, original_count, processed_count, run_time) VALUES (?, ?, ?, ?, ?)",
        (input_file, output_file, original, processed, datetime.now().isoformat(timespec="seconds")),
    )
    conn.commit()


def fetch_runs(conn: sqlite3.Connection) -> list[tuple[object, ...]]:
    return conn.execute(
        "SELECT id, input_file, output_file, original_count, processed_count, run_time FROM runs ORDER BY id DESC"
    ).fetchall()


def main() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    LAB.mkdir(parents=True)

    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    insert_run(conn, "input/labels.txt", "output/result.txt", 4, 3)
    insert_run(conn, "input/labels.jsonl", "output/clean.jsonl", 8, 6)
    rows = fetch_runs(conn)
    conn.close()

    report = "\n".join(str(row) for row in rows) + "\n"
    (LAB / "runs_report.txt").write_text(report, encoding="utf-8")
    (LAB / "next_steps.txt").write_text(
        "Week 2 自动练习已生成 runs.db 和 runs_report.txt。\n"
        "自测请在 Web UI 点击 r08-w2-self 的“终端”，自己写 runs_db.py 完成建表、插入、查询。\n"
        "能解释参数化 SQL、commit 和数据库存放位置后，再手动点“记录 / 完成”。\n",
        encoding="utf-8",
    )

    print("database:", DB_PATH)
    print("runs-count:", len(rows))
    print("latest-run:", rows[0])

    mark("r08-w2-ex2")
    print("Week 2 自动练习完成。请继续手动完成 r08-w2-self。")


if __name__ == "__main__":
    main()
