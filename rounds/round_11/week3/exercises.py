#!/usr/bin/env python3
"""Round 11 · Week 3: connect persistence to a tiny ai_prep_tool."""

from __future__ import annotations

import sqlite3
import subprocess
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round11" / "week3_auto" / "ai_prep_tool"


DB_TEMPLATE = '''"""SQLite helpers for ai_prep_tool sandbox."""

import sqlite3
from datetime import datetime

DEFAULT_DB_PATH = "runs.db"


def connect(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    with connect(db_path) as conn:
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


def insert_run(input_file: str, output_file: str, fmt: str, original_count: int, processed_count: int, dedup: bool = False, db_path: str = DEFAULT_DB_PATH) -> int:
    with connect(db_path) as conn:
        cursor = conn.execute(
            """INSERT INTO runs
               (input_file, output_file, format, original_count, processed_count, dedup, run_time)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (input_file, output_file, fmt, original_count, processed_count, int(dedup), datetime.now().isoformat(timespec="seconds")),
        )
        conn.commit()
        return int(cursor.lastrowid)


def get_all_runs(db_path: str = DEFAULT_DB_PATH) -> list[dict]:
    with connect(db_path) as conn:
        rows = conn.execute("SELECT * FROM runs ORDER BY id DESC").fetchall()
    return [dict(row) for row in rows]
'''

APP_TEMPLATE = '''"""Tiny processing tool that records each run into SQLite."""

import argparse
from pathlib import Path

from db import get_all_runs, init_db, insert_run


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai_prep_tool")
    parser.add_argument("--input", default="input/sample.txt")
    parser.add_argument("--output", default="output/result.txt")
    parser.add_argument("--format", default="txt")
    parser.add_argument("--dedup", action="store_true")
    return parser


def read_records(path: str) -> list[str]:
    return [line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def write_records(records: list[str], path: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\\n".join(records) + "\\n", encoding="utf-8")


def main() -> None:
    args = build_parser().parse_args()
    init_db()
    original = read_records(args.input)
    records = list(dict.fromkeys(original)) if args.dedup else original
    write_records(records, args.output)
    run_id = insert_run(args.input, args.output, args.format, len(original), len(records), args.dedup)
    print("run_id:", run_id)
    print("total_runs:", len(get_all_runs()))


if __name__ == "__main__":
    main()
'''

CHECK_TEMPLATE = '''"""Show recent saved runs."""

from db import get_all_runs

for run in get_all_runs()[:5]:
    print(f"[{run['id']}] {run['input_file']} -> {run['output_file']} processed={run['processed_count']}")
'''


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], check=True)


def main() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    (LAB / "input").mkdir(parents=True)
    (LAB / "output").mkdir()
    (LAB / "db.py").write_text(DB_TEMPLATE, encoding="utf-8")
    (LAB / "ai_prep_tool.py").write_text(APP_TEMPLATE, encoding="utf-8")
    (LAB / "check_runs.py").write_text(CHECK_TEMPLATE, encoding="utf-8")
    (LAB / "input" / "sample.txt").write_text("alpha\nbeta\nalpha\n", encoding="utf-8")

    first = subprocess.run(["python3", "ai_prep_tool.py", "--dedup"], cwd=LAB, check=True, capture_output=True, text=True)
    second = subprocess.run(
        ["python3", "ai_prep_tool.py", "--input", "input/sample.txt", "--output", "output/again.txt"],
        cwd=LAB,
        check=True,
        capture_output=True,
        text=True,
    )
    listing = subprocess.run(["python3", "check_runs.py"], cwd=LAB, check=True, capture_output=True, text=True)
    with sqlite3.connect(LAB / "runs.db") as conn:
        count = conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
    assert count == 2, count
    assert "total_runs: 2" in second.stdout, second.stdout

    report = "first:\n" + first.stdout + "\nsecond:\n" + second.stdout + "\nrecent:\n" + listing.stdout
    (LAB / "persistence_report.txt").write_text(report, encoding="utf-8")
    (LAB / "next_steps.txt").write_text(
        "Week 3 自动练习已生成 db.py、ai_prep_tool.py、check_runs.py，并验证每次运行都会写入 runs.db。\n"
        "自测请在 Web UI 点击 r11-w3-self 的“终端练习”，自己把 insert_run 接入一个小脚本。\n"
        "能解释一条 runs 记录代表一次运行后，再点击“记录并完成”。\n",
        encoding="utf-8",
    )

    print("project:", LAB)
    print(second.stdout.strip())
    print("recent:")
    print(listing.stdout.strip())

    mark("r11-w3-ex3")
    print("Week 3 自动练习完成。请继续在 Web UI 点击“记录并完成”保存 r11-w3-self。")


if __name__ == "__main__":
    main()
