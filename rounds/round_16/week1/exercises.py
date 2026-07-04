#!/usr/bin/env python3
"""Round 16 · Week 1: connect POST /run to core logic and SQLite."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round16" / "week1_auto" / "api_data_layer"

DB_PY = '''"""SQLite run storage for Round 16 Week 1."""

from __future__ import annotations

import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[1] / "runs.db"


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with connect() as conn:
        conn.execute(
            """
            create table if not exists runs (
                id integer primary key autoincrement,
                input_file text not null,
                output_file text not null,
                format text not null,
                original_count integer not null,
                processed_count integer not null,
                dedup integer not null,
                created_at text not null default current_timestamp
            )
            """
        )


def insert_run(
    *,
    input_file: str,
    output_file: str,
    fmt: str,
    original_count: int,
    processed_count: int,
    dedup: bool,
) -> int:
    init_db()
    with connect() as conn:
        cur = conn.execute(
            """
            insert into runs
                (input_file, output_file, format, original_count, processed_count, dedup)
            values (?, ?, ?, ?, ?, ?)
            """,
            (input_file, output_file, fmt, original_count, processed_count, int(dedup)),
        )
        return int(cur.lastrowid)


def count_runs() -> int:
    init_db()
    with connect() as conn:
        return int(conn.execute("select count(*) from runs").fetchone()[0])
'''

CORE_PY = '''"""Core processing functions for Round 16 Week 1."""

from __future__ import annotations


def filter_records(records: list[str]) -> list[str]:
    """Drop blank lines and comment rows."""
    return [item.strip() for item in records if item.strip() and not item.strip().startswith("#")]


def dedup_records(records: list[str]) -> list[str]:
    """Remove duplicates while preserving the original order."""
    seen: set[str] = set()
    result: list[str] = []
    for item in records:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result
'''

IO_UTILS_PY = '''"""Input readers for Round 16 Week 1."""

from __future__ import annotations

import csv
from pathlib import Path


def read_records(input_file: str | Path, fmt: str) -> list[str]:
    path = Path(input_file)
    if fmt == "txt":
        return path.read_text(encoding="utf-8").splitlines()
    if fmt == "csv":
        with path.open("r", encoding="utf-8", newline="") as f:
            return [row[0] for row in csv.reader(f) if row]
    raise ValueError(f"unsupported format: {fmt}")
'''

SCHEMAS_PY = '''"""Pydantic schemas used by the generated FastAPI router."""

from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    input_file: str = Field(..., examples=["input/demo.txt"])
    format: str = Field("txt", examples=["txt"])
    dedup: bool = Field(False)


class RunResponse(BaseModel):
    run_id: int
    status: str
    input_file: str
    processed_count: int
    message: str = ""
'''

JOBS_ROUTER_PY = '''"""POST /run router that calls real logic and writes SQLite records."""

from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.core import dedup_records, filter_records
from app.db import init_db, insert_run
from app.io_utils import read_records
from app.schemas import RunRequest, RunResponse


router = APIRouter(prefix="/run", tags=["jobs"])
init_db()


@router.post("", response_model=RunResponse)
def trigger_run(req: RunRequest) -> RunResponse:
    """Submit one data-processing job."""
    input_path = Path(req.input_file)
    if not input_path.exists():
        raise HTTPException(status_code=404, detail=f"Input file not found: {req.input_file}")

    try:
        records = read_records(input_path, req.format)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {exc}") from exc

    original_count = len(records)
    processed = filter_records(records)
    if req.dedup:
        processed = dedup_records(processed)

    output_path = Path("output") / f"{input_path.stem}_result.txt"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text("\\n".join(processed) + "\\n", encoding="utf-8")

    run_id = insert_run(
        input_file=req.input_file,
        output_file=str(output_path),
        fmt=req.format,
        original_count=original_count,
        processed_count=len(processed),
        dedup=req.dedup,
    )
    return RunResponse(
        run_id=run_id,
        status="completed",
        input_file=req.input_file,
        processed_count=len(processed),
        message=f"Removed {original_count - len(processed)} records",
    )
'''

RUN_FLOW_DEMO = '''#!/usr/bin/env python3
"""Run the Round 16 Week 1 flow without starting an HTTP server."""

from __future__ import annotations

import json
from pathlib import Path

from app.core import dedup_records, filter_records
from app.db import count_runs, insert_run
from app.io_utils import read_records


base = Path(__file__).resolve().parent
input_path = base / "input" / "demo.txt"
output_path = base / "output" / "demo_result.txt"
input_path.parent.mkdir(exist_ok=True)
output_path.parent.mkdir(exist_ok=True)
input_path.write_text("alpha\\n\\n# comment\\nbeta\\nalpha\\ngamma\\n", encoding="utf-8")

records = read_records(input_path, "txt")
filtered = filter_records(records)
processed = dedup_records(filtered)
output_path.write_text("\\n".join(processed) + "\\n", encoding="utf-8")
run_id = insert_run(
    input_file=str(input_path),
    output_file=str(output_path),
    fmt="txt",
    original_count=len(records),
    processed_count=len(processed),
    dedup=True,
)

report = {
    "run_id": run_id,
    "input_file": str(input_path),
    "output_file": str(output_path),
    "original_count": len(records),
    "processed_count": len(processed),
    "run_count": count_runs(),
    "output_preview": processed,
}
(base / "round16_week1_report.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\\n",
    encoding="utf-8",
)
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
'''

STATIC_CHECK = '''#!/usr/bin/env python3
"""Static checks for the generated Round 16 Week 1 files."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path


base = Path(__file__).resolve().parent
jobs_source = (base / "app" / "routers" / "jobs.py").read_text(encoding="utf-8")
db_source = (base / "app" / "db.py").read_text(encoding="utf-8")
ast.parse(jobs_source)
ast.parse(db_source)

proc = subprocess.run(
    [sys.executable, "run_flow_demo.py"],
    cwd=base,
    capture_output=True,
    text=True,
    check=False,
)
demo = {}
if proc.returncode == 0:
    demo = json.loads((base / "round16_week1_report.json").read_text(encoding="utf-8"))

checks = {
    "router_post_run": '@router.post("", response_model=RunResponse)' in jobs_source,
    "request_body": "req: RunRequest" in jobs_source,
    "missing_file_404": "HTTPException(status_code=404" in jobs_source,
    "read_error_400": "HTTPException(status_code=400" in jobs_source,
    "calls_core_logic": "filter_records(records)" in jobs_source and "dedup_records(processed)" in jobs_source,
    "writes_output_file": "output_path.write_text" in jobs_source,
    "writes_sqlite_run": "insert_run(" in jobs_source,
    "sqlite_table": "create table if not exists runs" in db_source,
    "demo_processed_count": demo.get("processed_count") == 3,
    "demo_inserted_run": int(demo.get("run_count", 0)) >= 1,
}
report = {
    "ok": all(checks.values()) and proc.returncode == 0,
    "checks": checks,
    "demo_stdout": proc.stdout.strip(),
    "demo_stderr": proc.stderr.strip(),
    "files": [
        "app/routers/jobs.py",
        "app/db.py",
        "app/core.py",
        "app/io_utils.py",
        "round16_week1_report.json",
    ],
}
(base / "static_check_report.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\\n",
    encoding="utf-8",
)
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
raise SystemExit(0 if report["ok"] else 1)
'''


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    (LAB / "app" / "routers").mkdir(parents=True)


def main() -> None:
    reset_lab()
    (LAB / "app" / "__init__.py").write_text("", encoding="utf-8")
    (LAB / "app" / "routers" / "__init__.py").write_text("", encoding="utf-8")
    (LAB / "app" / "db.py").write_text(DB_PY, encoding="utf-8")
    (LAB / "app" / "core.py").write_text(CORE_PY, encoding="utf-8")
    (LAB / "app" / "io_utils.py").write_text(IO_UTILS_PY, encoding="utf-8")
    (LAB / "app" / "schemas.py").write_text(SCHEMAS_PY, encoding="utf-8")
    (LAB / "app" / "routers" / "jobs.py").write_text(JOBS_ROUTER_PY, encoding="utf-8")
    demo = LAB / "run_flow_demo.py"
    demo.write_text(RUN_FLOW_DEMO, encoding="utf-8")
    demo.chmod(0o755)
    check = LAB / "static_check.py"
    check.write_text(STATIC_CHECK, encoding="utf-8")
    check.chmod(0o755)
    proc = subprocess.run(["python3", str(check)], cwd=LAB, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    print("Round 16 Week 1 API + SQLite 主链")
    print("sandbox:", LAB)
    print("router:", LAB / "app" / "routers" / "jobs.py")
    print("report:", LAB / "static_check_report.json")
    mark("r16-w1-ex1")


if __name__ == "__main__":
    main()
