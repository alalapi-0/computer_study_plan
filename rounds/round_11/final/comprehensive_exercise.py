#!/usr/bin/env python3
"""Round 11 · Final: persistence checklist."""

from __future__ import annotations

import json
import shutil
import sqlite3
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round11" / "final_auto" / "ai_prep_tool"


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], check=True)


DB_TEMPLATE = '''"""SQLite persistence helpers."""

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


def get_runs_by_format(fmt: str, db_path: str = DEFAULT_DB_PATH) -> list[dict]:
    with connect(db_path) as conn:
        rows = conn.execute("SELECT * FROM runs WHERE format = ? ORDER BY id DESC", (fmt,)).fetchall()
    return [dict(row) for row in rows]
'''

APP_TEMPLATE = '''"""Round 11 final ai_prep_tool with SQLite run history."""

import argparse
from pathlib import Path

from db import get_all_runs, init_db, insert_run


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai_prep_tool")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
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
    processed = list(dict.fromkeys(original)) if args.dedup else original
    write_records(processed, args.output)
    run_id = insert_run(args.input, args.output, args.format, len(original), len(processed), args.dedup)
    print("run_id:", run_id)
    print("total_runs:", len(get_all_runs()))


if __name__ == "__main__":
    main()
'''

CHECK_TEMPLATE = '''"""Query saved run history."""

from db import get_all_runs, get_runs_by_format

all_runs = get_all_runs()
txt_runs = get_runs_by_format("txt")
print("all_runs:", len(all_runs))
print("txt_runs:", len(txt_runs))
for run in all_runs:
    print(f"[{run['id']}] {run['format']} {run['input_file']} -> {run['output_file']}")
'''


def write_project(base: Path) -> None:
    (base / "input").mkdir(parents=True)
    (base / "output").mkdir()
    (base / "README.md").write_text(
        "# AI Prep Tool\n\nRound 11 SQLite persistence final sandbox.\n",
        encoding="utf-8",
    )
    (base / ".gitignore").write_text("__pycache__/\n*.py[cod]\noutput/\n*.db\n", encoding="utf-8")
    (base / "db.py").write_text(DB_TEMPLATE, encoding="utf-8")
    (base / "ai_prep_tool.py").write_text(APP_TEMPLATE, encoding="utf-8")
    (base / "check_runs.py").write_text(CHECK_TEMPLATE, encoding="utf-8")
    (base / "input" / "sample.txt").write_text("alpha\nbeta\nalpha\n", encoding="utf-8")
    (base / "input" / "other.txt").write_text("gamma\ndelta\n", encoding="utf-8")


def scan(base: Path) -> dict[str, bool]:
    required = ["db.py", "ai_prep_tool.py", "check_runs.py", "runs.db", ".gitignore", "README.md"]
    return {name: (base / name).exists() for name in required}


def main() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    write_project(LAB)

    first = subprocess.run(
        ["python3", "ai_prep_tool.py", "--input", "input/sample.txt", "--output", "output/result.txt", "--format", "txt", "--dedup"],
        cwd=LAB,
        check=True,
        capture_output=True,
        text=True,
    )
    second = subprocess.run(
        ["python3", "ai_prep_tool.py", "--input", "input/other.txt", "--output", "output/other.txt", "--format", "txt"],
        cwd=LAB,
        check=True,
        capture_output=True,
        text=True,
    )
    listing = subprocess.run(["python3", "check_runs.py"], cwd=LAB, check=True, capture_output=True, text=True)
    with sqlite3.connect(LAB / "runs.db") as conn:
        count = conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
        txt_count = conn.execute("SELECT COUNT(*) FROM runs WHERE format = ?", ("txt",)).fetchone()[0]
        processed_sum = conn.execute("SELECT SUM(processed_count) FROM runs").fetchone()[0]
    checks = scan(LAB)
    assert all(checks.values()), checks
    assert count == 2, count
    assert txt_count == 2, txt_count
    assert processed_sum == 4, processed_sum
    assert "*.db" in (LAB / ".gitignore").read_text(encoding="utf-8")

    summary = {
        "layout": checks,
        "run_count": count,
        "txt_count": txt_count,
        "processed_sum": processed_sum,
        "first_stdout": first.stdout.strip(),
        "second_stdout": second.stdout.strip(),
        "query_stdout": listing.stdout.strip(),
        "sandbox": str(LAB),
    }
    (LAB / "round11_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("Round 11 收口检查")
    print("- layout:", "OK")
    print("- run_count:", count)
    print("- txt_count:", txt_count)
    print("- processed_sum:", processed_sum)
    print("- summary:", LAB / "round11_summary.json")

    mark("r11-fin-comp")
    print("Round 11 Final 自动练习完成。请继续在 Web UI 点击“记录并完成”保存 r11-fin-sheet 与 r11-fin-acc1。")


if __name__ == "__main__":
    main()
