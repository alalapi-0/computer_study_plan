#!/usr/bin/env python3
"""Round 11 · Week 2: parameterized insert and query helpers."""

from __future__ import annotations

import sqlite3
import subprocess
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round11" / "week2_auto" / "ai_prep_tool"

DB_TEMPLATE = '''"""SQLite helpers for Round 11 sandbox."""

import sqlite3
from datetime import datetime

DEFAULT_DB_PATH = "runs.db"


def get_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    with get_connection(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_file TEXT NOT NULL,
                output_file TEXT NOT NULL,
                format TEXT NOT NULL,
                original_count INTEGER NOT NULL,
                processed_count INTEGER NOT NULL,
                dedup INTEGER NOT NULL DEFAULT 0,
                run_time TEXT NOT NULL
            )
        """)
        conn.commit()


def insert_run(
    input_file: str,
    output_file: str,
    fmt: str,
    original_count: int,
    processed_count: int,
    dedup: bool = False,
    db_path: str = DEFAULT_DB_PATH,
) -> int:
    with get_connection(db_path) as conn:
        cursor = conn.execute(
            """INSERT INTO runs
               (input_file, output_file, format, original_count, processed_count, dedup, run_time)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (input_file, output_file, fmt, original_count, processed_count, int(dedup), datetime.now().isoformat(timespec="seconds")),
        )
        conn.commit()
        return int(cursor.lastrowid)


def get_all_runs(db_path: str = DEFAULT_DB_PATH) -> list[dict]:
    with get_connection(db_path) as conn:
        rows = conn.execute("SELECT * FROM runs ORDER BY id DESC").fetchall()
    return [dict(row) for row in rows]


def get_runs_by_format(fmt: str, db_path: str = DEFAULT_DB_PATH) -> list[dict]:
    with get_connection(db_path) as conn:
        rows = conn.execute("SELECT * FROM runs WHERE format = ? ORDER BY id DESC", (fmt,)).fetchall()
    return [dict(row) for row in rows]
'''

CHECK_TEMPLATE = '''"""Exercise db.py helpers."""

from db import get_all_runs, get_runs_by_format, init_db, insert_run

init_db()
insert_run("input/a.txt", "output/a.txt", "txt", 5, 3, True)
insert_run("input/b.csv", "output/b.txt", "csv", 4, 4, False)
insert_run("input/c.txt", "output/c.txt", "txt", 2, 2, False)

all_runs = get_all_runs()
txt_runs = get_runs_by_format("txt")
print("all_runs:", len(all_runs))
print("txt_runs:", len(txt_runs))
print("latest:", all_runs[0]["format"], all_runs[0]["processed_count"])
'''


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], check=True)


def main() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    LAB.mkdir(parents=True)
    (LAB / "db.py").write_text(DB_TEMPLATE, encoding="utf-8")
    (LAB / "check_runs.py").write_text(CHECK_TEMPLATE, encoding="utf-8")

    result = subprocess.run(["python3", "check_runs.py"], cwd=LAB, check=True, capture_output=True, text=True)
    with sqlite3.connect(LAB / "runs.db") as conn:
        count = conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
        txt_count = conn.execute("SELECT COUNT(*) FROM runs WHERE format = ?", ("txt",)).fetchone()[0]
    assert count == 3, count
    assert txt_count == 2, txt_count

    (LAB / "query_report.txt").write_text(result.stdout, encoding="utf-8")
    (LAB / "next_steps.txt").write_text(
        "Week 2 自动练习已生成 db.py、check_runs.py，并验证全部查询和按 format 查询。\n"
        "自测请在 Web UI 点击 r11-w2-self 的“终端”，自己封装 insert_run/get_all_runs。\n"
        "能解释参数化 SELECT 和 sqlite3.Row 后，再手动点“记录 / 完成”。\n",
        encoding="utf-8",
    )

    print("project:", LAB)
    print(result.stdout.strip())
    print("db:", LAB / "runs.db")

    mark("r11-w2-ex2")
    print("Week 2 自动练习完成。请继续手动完成 r11-w2-self。")


if __name__ == "__main__":
    main()
