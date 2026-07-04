#!/usr/bin/env python3
"""Round 16 · Week 2: generate list/detail routes and an upload endpoint."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round16" / "week2_auto" / "read_upload_api"

DB_PY = '''"""SQLite read helpers for Round 16 Week 2."""

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
                processed_count integer not null,
                dedup integer not null,
                created_at text not null default current_timestamp
            )
            """
        )


def row_to_dict(row: sqlite3.Row) -> dict:
    return dict(row)


def insert_run(input_file: str, output_file: str, fmt: str, processed_count: int, dedup: bool) -> int:
    init_db()
    with connect() as conn:
        cur = conn.execute(
            """
            insert into runs (input_file, output_file, format, processed_count, dedup)
            values (?, ?, ?, ?, ?)
            """,
            (input_file, output_file, fmt, processed_count, int(dedup)),
        )
        return int(cur.lastrowid)


def get_all_runs() -> list[dict]:
    init_db()
    with connect() as conn:
        rows = conn.execute("select * from runs order by id").fetchall()
    return [row_to_dict(row) for row in rows]


def get_run(run_id: int) -> dict | None:
    init_db()
    with connect() as conn:
        row = conn.execute("select * from runs where id = ?", (run_id,)).fetchone()
    return row_to_dict(row) if row else None


def get_runs_by_format(fmt: str) -> list[dict]:
    init_db()
    with connect() as conn:
        rows = conn.execute("select * from runs where format = ? order by id", (fmt,)).fetchall()
    return [row_to_dict(row) for row in rows]
'''

RUNS_ROUTER_PY = '''"""GET routes backed by SQLite."""

from fastapi import APIRouter, HTTPException

from app.db import get_all_runs, get_run, get_runs_by_format


router = APIRouter(prefix="/runs", tags=["runs"])


@router.get("")
def list_runs(skip: int = 0, limit: int = 20, format: str | None = None) -> dict:
    """List stored runs from SQLite."""
    limit = min(max(limit, 1), 100)
    runs = get_runs_by_format(format) if format else get_all_runs()
    return {"runs": runs[skip: skip + limit], "total": len(runs), "skip": skip, "limit": limit}


@router.get("/{run_id}")
def get_run_detail(run_id: int) -> dict:
    """Read one stored run from SQLite."""
    run = get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")
    return run
'''

CORE_PY = '''"""Core helpers reused by the upload route."""

from __future__ import annotations


def filter_records(records: list[str]) -> list[str]:
    return [item.strip() for item in records if item.strip()]


def dedup_records(records: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in records:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result
'''

IO_UTILS_PY = '''"""Input readers reused by upload route."""

from __future__ import annotations

from pathlib import Path


def read_records(input_file: str | Path, fmt: str) -> list[str]:
    if fmt not in {"txt", "csv"}:
        raise ValueError(f"unsupported format: {fmt}")
    return Path(input_file).read_text(encoding="utf-8").splitlines()
'''

SCHEMAS_PY = '''"""Pydantic schema names used by the generated route."""

from pydantic import BaseModel


class RunResponse(BaseModel):
    run_id: int
    status: str
    input_file: str
    processed_count: int
'''

JOBS_UPLOAD_PY = '''"""Upload route that stores a temporary file, processes it, then cleans up."""

import os
import tempfile

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core import dedup_records, filter_records
from app.db import insert_run
from app.io_utils import read_records
from app.schemas import RunResponse


router = APIRouter(prefix="/run", tags=["jobs"])


@router.post("/upload", response_model=RunResponse)
async def upload_and_run(
    file: UploadFile = File(...),
    format: str = "txt",
    dedup: bool = False,
) -> RunResponse:
    """Upload a file and run the same processing pipeline."""
    if format not in {"txt", "csv"}:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {format}")

    with tempfile.NamedTemporaryFile(mode="wb", suffix=f".{format}", delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        records = read_records(tmp_path, format)
        processed = filter_records(records)
        if dedup:
            processed = dedup_records(processed)
        run_id = insert_run(
            input_file=file.filename or "uploaded",
            output_file="",
            fmt=format,
            processed_count=len(processed),
            dedup=dedup,
        )
        return RunResponse(
            run_id=run_id,
            status="completed",
            input_file=file.filename or "uploaded",
            processed_count=len(processed),
        )
    finally:
        os.unlink(tmp_path)
'''

SEED_AND_QUERY = '''#!/usr/bin/env python3
"""Seed SQLite and prove list/detail/filter behavior without an HTTP server."""

from __future__ import annotations

import json
from pathlib import Path

from app.db import get_all_runs, get_run, get_runs_by_format, insert_run


base = Path(__file__).resolve().parent
run1 = insert_run("input/demo.txt", "output/demo_result.txt", "txt", 3, True)
run2 = insert_run("input/labels.csv", "output/labels_result.txt", "csv", 42, False)
report = {
    "inserted": [run1, run2],
    "all_total": len(get_all_runs()),
    "txt_total": len(get_runs_by_format("txt")),
    "detail": get_run(run2),
}
(base / "round16_week2_query_report.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\\n",
    encoding="utf-8",
)
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
'''

STATIC_CHECK = '''#!/usr/bin/env python3
"""Static checks for Round 16 Week 2 generated files."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path


base = Path(__file__).resolve().parent
runs_source = (base / "app" / "routers" / "runs.py").read_text(encoding="utf-8")
jobs_source = (base / "app" / "routers" / "jobs.py").read_text(encoding="utf-8")
db_source = (base / "app" / "db.py").read_text(encoding="utf-8")
for source in (runs_source, jobs_source, db_source):
    ast.parse(source)

proc = subprocess.run(
    [sys.executable, "seed_and_query.py"],
    cwd=base,
    capture_output=True,
    text=True,
    check=False,
)
query_report = {}
if proc.returncode == 0:
    query_report = json.loads((base / "round16_week2_query_report.json").read_text(encoding="utf-8"))

checks = {
    "list_route": '@router.get("")' in runs_source and "skip: int = 0" in runs_source,
    "detail_route": '@router.get("/{run_id}")' in runs_source and "run_id: int" in runs_source,
    "format_filter": "get_runs_by_format(format)" in runs_source,
    "detail_404": "HTTPException(status_code=404" in runs_source,
    "upload_route": '@router.post("/upload", response_model=RunResponse)' in jobs_source,
    "uploadfile_and_file": "UploadFile" in jobs_source and "File(...)" in jobs_source,
    "tempfile_cleanup": "NamedTemporaryFile" in jobs_source and "finally:" in jobs_source and "os.unlink(tmp_path)" in jobs_source,
    "upload_writes_sqlite": "insert_run(" in jobs_source,
    "db_read_helpers": all(name in db_source for name in ("get_all_runs", "get_run", "get_runs_by_format")),
    "seeded_two_runs": query_report.get("all_total") == 2,
    "detail_from_db": (query_report.get("detail") or {}).get("format") == "csv",
}
report = {
    "ok": all(checks.values()) and proc.returncode == 0,
    "checks": checks,
    "query_stdout": proc.stdout.strip(),
    "query_stderr": proc.stderr.strip(),
    "files": [
        "app/routers/runs.py",
        "app/routers/jobs.py",
        "app/db.py",
        "round16_week2_query_report.json",
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
    (LAB / "app" / "routers" / "runs.py").write_text(RUNS_ROUTER_PY, encoding="utf-8")
    (LAB / "app" / "routers" / "jobs.py").write_text(JOBS_UPLOAD_PY, encoding="utf-8")
    seed = LAB / "seed_and_query.py"
    seed.write_text(SEED_AND_QUERY, encoding="utf-8")
    seed.chmod(0o755)
    check = LAB / "static_check.py"
    check.write_text(STATIC_CHECK, encoding="utf-8")
    check.chmod(0o755)
    proc = subprocess.run(["python3", str(check)], cwd=LAB, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    print("Round 16 Week 2 读接口 + 上传入口")
    print("sandbox:", LAB)
    print("runs_router:", LAB / "app" / "routers" / "runs.py")
    print("upload_router:", LAB / "app" / "routers" / "jobs.py")
    print("report:", LAB / "static_check_report.json")
    mark("r16-w2-ex2")


if __name__ == "__main__":
    main()
