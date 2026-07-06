#!/usr/bin/env python3
"""Round 11 · Week 1: create SQLite schema and insert first rows."""

from __future__ import annotations

import sqlite3
import subprocess
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round11" / "week1_auto" / "ai_prep_tool"


SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_file TEXT NOT NULL,
    output_file TEXT NOT NULL,
    format TEXT NOT NULL,
    original_count INTEGER NOT NULL,
    processed_count INTEGER NOT NULL,
    dedup INTEGER NOT NULL DEFAULT 0,
    run_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], check=True)


def main() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    LAB.mkdir(parents=True)
    db_path = LAB / "runs.db"

    with sqlite3.connect(db_path) as conn:
        conn.execute(SCHEMA)
        conn.execute(
            """
            INSERT INTO runs
            (input_file, output_file, format, original_count, processed_count, dedup)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            ("input/sample.txt", "output/result.txt", "txt", 5, 3, 1),
        )
        conn.commit()
        rows = conn.execute(
            "SELECT id, input_file, output_file, format, original_count, processed_count, dedup FROM runs"
        ).fetchall()
        schema = conn.execute("PRAGMA table_info(runs)").fetchall()

    report = [
        "Round 11 Week 1 SQLite 初始化报告",
        f"db_path: {db_path}",
        f"schema_columns: {', '.join(col[1] for col in schema)}",
        f"row_count: {len(rows)}",
        f"first_row: {rows[0] if rows else 'NONE'}",
    ]
    (LAB / "schema_report.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    (LAB / "next_steps.txt").write_text(
        "Week 1 自动练习已创建 runs.db、runs 表并插入第一条参数化记录。\n"
        "自测请在 Web UI 点击 r11-w1-self 的“终端练习”，自己写 sqlite3 建表和插入脚本。\n"
        "能解释 ? 占位符和 conn.commit() 后，再点击“记录并完成”。\n",
        encoding="utf-8",
    )

    print("db:", db_path)
    print("schema_columns:", ", ".join(col[1] for col in schema))
    print("row_count:", len(rows))

    mark("r11-w1-ex1")
    print("Week 1 自动练习完成。请继续在 Web UI 点击“记录并完成”保存 r11-w1-self。")


if __name__ == "__main__":
    main()
