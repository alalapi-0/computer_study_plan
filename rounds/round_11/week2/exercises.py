#!/usr/bin/env python3
"""Round 11 · Week 2 exercises: parameterized insert and query."""

import sqlite3
from pathlib import Path


def insert_run(
    conn: sqlite3.Connection,
    input_file: str,
    output_file: str,
    raw_count: int,
    final_count: int,
) -> None:
    conn.execute(
        """
        INSERT INTO runs (input_file, output_file, raw_count, final_count)
        VALUES (?, ?, ?, ?)
        """,
        (input_file, output_file, raw_count, final_count),
    )


def list_runs(conn: sqlite3.Connection) -> list[tuple]:
    cur = conn.execute(
        "SELECT id, input_file, output_file, raw_count, final_count, run_at FROM runs"
    )
    return cur.fetchall()


def main() -> None:
    db_path = Path.home() / "cli-lab" / "round11" / "week1" / "ai_prep_tool.db"
    if not db_path.exists():
        print("请先运行 week1/exercises.py 初始化数据库。")
        return

    with sqlite3.connect(db_path) as conn:
        insert_run(conn, "input/a.txt", "output/a.txt", 10, 8)
        conn.commit()
        rows = list_runs(conn)

    print(f"当前 runs 记录数: {len(rows)}")
    for row in rows[-3:]:
        print(row)


if __name__ == "__main__":
    main()
