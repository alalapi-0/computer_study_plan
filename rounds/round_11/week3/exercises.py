#!/usr/bin/env python3
"""Round 11 · Week 3 exercises: db helper module."""

from pathlib import Path


DB_TEMPLATE = '''"""SQLite helpers for ai_prep_tool sandbox."""

import sqlite3
from pathlib import Path


def connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def count_runs(conn: sqlite3.Connection) -> int:
    cur = conn.execute("SELECT COUNT(*) AS c FROM runs")
    row = cur.fetchone()
    return int(row["c"]) if row else 0
'''


def main() -> None:
    base = Path.home() / "cli-lab" / "round11" / "week3" / "ai_prep_tool"
    base.mkdir(parents=True, exist_ok=True)
    (base / "db.py").write_text(DB_TEMPLATE, encoding="utf-8")
    print("已生成 db.py:", base / "db.py")


if __name__ == "__main__":
    main()
