#!/usr/bin/env python3
"""Round 08 · Final: consolidation checklist runner."""

from __future__ import annotations

import importlib.util
import json
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round8" / "final_auto"


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], check=True)


def write_project(base: Path) -> int:
    project = base / "ai_prep_tool"
    (project / "tests").mkdir(parents=True)
    (project / "README.md").write_text("# ai_prep_tool\n\nRound 08 final consolidation sandbox.\n", encoding="utf-8")
    (project / "ai_prep_tool.py").write_text(
        "def dedup_records(items):\n"
        "    return list(dict.fromkeys(items))\n\n"
        "def build_summary(original, processed):\n"
        "    return {'original_count': len(original), 'processed_count': len(processed), 'removed_count': len(original) - len(processed)}\n",
        encoding="utf-8",
    )
    (project / "tests" / "test_basic.py").write_text(
        "from ai_prep_tool import build_summary, dedup_records\n\n"
        "def test_dedup_records():\n"
        "    assert dedup_records(['ok', 'blur', 'ok']) == ['ok', 'blur']\n\n"
        "def test_summary_counts():\n"
        "    assert build_summary(['a', 'a'], ['a'])['removed_count'] == 1\n",
        encoding="utf-8",
    )
    spec = importlib.util.spec_from_file_location("test_basic", project / "tests" / "test_basic.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot_load_final_tests")
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(project))
    spec.loader.exec_module(module)
    names = sorted(name for name in dir(module) if name.startswith("test_"))
    for name in names:
        getattr(module, name)()
    sys.path.pop(0)
    return len(names)


def write_sqlite(base: Path) -> int:
    db_path = base / "runs.db"
    conn = sqlite3.connect(db_path)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS runs (id INTEGER PRIMARY KEY AUTOINCREMENT, input_file TEXT, output_file TEXT, original_count INTEGER, processed_count INTEGER, run_time TEXT)"
    )
    conn.execute(
        "INSERT INTO runs (input_file, output_file, original_count, processed_count, run_time) VALUES (?, ?, ?, ?, ?)",
        ("input/final.txt", "output/final.txt", 5, 4, datetime.now().isoformat(timespec="seconds")),
    )
    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
    conn.close()
    return int(count)


def write_api_contract(base: Path) -> dict[str, object]:
    payload = {
        "GET /health": {"status": "ok"},
        "POST /run": {"status": "accepted", "input_file": "input/final.txt", "dedup": True},
        "GET /runs": {"runs": [], "count": 0},
    }
    (base / "api_contract.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    LAB.mkdir(parents=True)

    tests_passed = write_project(LAB)
    sqlite_runs = write_sqlite(LAB)
    api_contract = write_api_contract(LAB)
    summary = {
        "project_layout": True,
        "tests_passed": tests_passed,
        "sqlite_runs": sqlite_runs,
        "api_contract_endpoints": list(api_contract),
        "recommended_next_route": "A 工程化深入，再进入 B 服务化，最后进入 C AI/ML",
    }
    (LAB / "round08_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("Round 08 收口检查")
    print("- project_layout: OK")
    print("- tests_passed:", tests_passed)
    print("- sqlite_runs:", sqlite_runs)
    print("- api_contract:", ", ".join(api_contract))
    print("- summary:", LAB / "round08_summary.json")

    mark("r08-fin-comp")
    print("Round 08 Final 自动练习完成。请继续手动完成 r08-fin-sheet 与 r08-fin-acc1。")


if __name__ == "__main__":
    main()
