#!/usr/bin/env python3
"""Round 16 · Final: generate a complete API + data-layer project package."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round16" / "final_auto" / "api_data_layer_project"

DB_PY = '''"""SQLite storage layer for the Round 16 final project."""

from __future__ import annotations

import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[1] / "data" / "runs.db"


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
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


def row_to_dict(row: sqlite3.Row) -> dict:
    return dict(row)


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


def get_all_runs() -> list[dict]:
    init_db()
    with connect() as conn:
        rows = conn.execute("select * from runs order by id desc").fetchall()
    return [row_to_dict(row) for row in rows]


def get_run(run_id: int) -> dict | None:
    init_db()
    with connect() as conn:
        row = conn.execute("select * from runs where id = ?", (run_id,)).fetchone()
    return row_to_dict(row) if row else None


def get_runs_by_format(fmt: str) -> list[dict]:
    init_db()
    with connect() as conn:
        rows = conn.execute("select * from runs where format = ? order by id desc", (fmt,)).fetchall()
    return [row_to_dict(row) for row in rows]
'''

CORE_PY = '''"""Core processing rules used by API routes."""

from __future__ import annotations


def filter_records(records: list[str]) -> list[str]:
    return [item.strip() for item in records if item.strip() and not item.strip().startswith("#")]


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

IO_UTILS_PY = '''"""Input readers for text and CSV files."""

from __future__ import annotations

import csv
from pathlib import Path


SUPPORTED_FORMATS = {"txt", "csv"}


def read_records(input_file: str | Path, fmt: str) -> list[str]:
    path = Path(input_file)
    if fmt == "txt":
        return path.read_text(encoding="utf-8").splitlines()
    if fmt == "csv":
        with path.open("r", encoding="utf-8", newline="") as f:
            return [row[0] for row in csv.reader(f) if row]
    raise ValueError(f"unsupported format: {fmt}")
'''

SCHEMAS_PY = '''"""Pydantic schemas for the Round 16 final project."""

from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    input_file: str = Field(..., examples=["input/demo.txt"])
    format: str = Field("txt", examples=["txt", "csv"])
    dedup: bool = Field(False)


class RunResponse(BaseModel):
    run_id: int
    status: str
    input_file: str
    processed_count: int
    message: str = ""


class RunRecord(BaseModel):
    id: int
    input_file: str
    output_file: str
    format: str
    original_count: int
    processed_count: int
    dedup: bool
'''

JOBS_ROUTER_PY = '''"""Write routes: POST /run and POST /run/upload."""

import os
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core import dedup_records, filter_records
from app.db import init_db, insert_run
from app.io_utils import SUPPORTED_FORMATS, read_records
from app.schemas import RunRequest, RunResponse


router = APIRouter(prefix="/run", tags=["jobs"])
init_db()


def process_file(input_file: str, fmt: str, dedup: bool, display_name: str | None = None) -> RunResponse:
    if fmt not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail={"code": "unsupported_format", "message": f"Unsupported format: {fmt}"},
        )

    input_path = Path(input_file)
    if not input_path.exists():
        raise HTTPException(
            status_code=404,
            detail={"code": "input_not_found", "message": f"Input file not found: {input_file}"},
        )

    try:
        records = read_records(input_path, fmt)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail={"code": "read_failed", "message": str(exc)},
        ) from exc

    original_count = len(records)
    processed = filter_records(records)
    if dedup:
        processed = dedup_records(processed)

    output_path = Path("output") / f"{input_path.stem}_result.txt"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text("\\n".join(processed) + "\\n", encoding="utf-8")
    run_id = insert_run(
        input_file=display_name or input_file,
        output_file=str(output_path),
        fmt=fmt,
        original_count=original_count,
        processed_count=len(processed),
        dedup=dedup,
    )
    return RunResponse(
        run_id=run_id,
        status="completed",
        input_file=display_name or input_file,
        processed_count=len(processed),
        message=f"Removed {original_count - len(processed)} records",
    )


@router.post("", response_model=RunResponse)
def trigger_run(req: RunRequest) -> RunResponse:
    return process_file(req.input_file, req.format, req.dedup)


@router.post("/upload", response_model=RunResponse)
async def upload_and_run(
    file: UploadFile = File(...),
    format: str = "txt",
    dedup: bool = False,
) -> RunResponse:
    with tempfile.NamedTemporaryFile(mode="wb", suffix=f".{format}", delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    try:
        return process_file(tmp_path, format, dedup, display_name=file.filename or "uploaded")
    finally:
        os.unlink(tmp_path)
'''

RUNS_ROUTER_PY = '''"""Read routes backed by SQLite."""

from fastapi import APIRouter, HTTPException

from app.db import get_all_runs, get_run, get_runs_by_format


router = APIRouter(prefix="/runs", tags=["runs"])


@router.get("")
def list_runs(skip: int = 0, limit: int = 20, format: str | None = None) -> dict:
    limit = min(max(limit, 1), 100)
    runs = get_runs_by_format(format) if format else get_all_runs()
    return {"runs": runs[skip: skip + limit], "total": len(runs), "skip": skip, "limit": limit}


@router.get("/{run_id}")
def get_run_detail(run_id: int) -> dict:
    run = get_run(run_id)
    if run is None:
        raise HTTPException(
            status_code=404,
            detail={"code": "run_not_found", "message": f"Run {run_id} not found"},
        )
    return run
'''

MAIN_PY = '''"""FastAPI entrypoint for the Round 16 final project."""

from fastapi import FastAPI

from app.routers import jobs, runs


app = FastAPI(title="Round 16 API Data Layer", version="0.2.0")
app.include_router(jobs.router)
app.include_router(runs.router)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "round16_api_data_layer"}
'''

TEST_API = '''"""TestClient contract examples for the final project."""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    assert client.get("/health").status_code == 200


def test_missing_input_returns_404():
    response = client.post("/run", json={"input_file": "missing.txt", "format": "txt"})
    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "input_not_found"


def test_bad_format_returns_400():
    response = client.post("/run", json={"input_file": "input/demo.md", "format": "md"})
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "unsupported_format"


def test_list_runs_shape():
    response = client.get("/runs?skip=0&limit=20")
    assert response.status_code == 200
    assert "runs" in response.json()
'''

RUN_DEMO = '''#!/usr/bin/env python3
"""Exercise the final data layer without importing FastAPI."""

from __future__ import annotations

import json
from pathlib import Path

from app.core import dedup_records, filter_records
from app.db import get_all_runs, get_run, insert_run
from app.io_utils import read_records


base = Path(__file__).resolve().parent
input_path = base / "input" / "demo.txt"
output_path = base / "output" / "demo_result.txt"
input_path.parent.mkdir(exist_ok=True)
output_path.parent.mkdir(exist_ok=True)
input_path.write_text("alpha\\n# ignored\\nbeta\\nalpha\\ngamma\\n", encoding="utf-8")

records = read_records(input_path, "txt")
processed = dedup_records(filter_records(records))
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
    "processed_count": len(processed),
    "output_file": str(output_path),
    "detail": get_run(run_id),
    "total": len(get_all_runs()),
}
(base / "round16_final_demo.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\\n",
    encoding="utf-8",
)
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
'''

CONTRACT_CHECK = '''#!/usr/bin/env python3
"""Final static contract checks for Round 16."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path


base = Path(__file__).resolve().parent
files = {
    "main": base / "app" / "main.py",
    "jobs": base / "app" / "routers" / "jobs.py",
    "runs": base / "app" / "routers" / "runs.py",
    "db": base / "app" / "db.py",
    "io": base / "app" / "io_utils.py",
    "core": base / "app" / "core.py",
    "tests": base / "tests" / "test_api_contract.py",
}
sources = {name: path.read_text(encoding="utf-8") for name, path in files.items()}
for source in sources.values():
    ast.parse(source)

proc = subprocess.run(
    [sys.executable, "run_demo.py"],
    cwd=base,
    capture_output=True,
    text=True,
    check=False,
)
demo = {}
if proc.returncode == 0:
    demo = json.loads((base / "round16_final_demo.json").read_text(encoding="utf-8"))

contract = json.loads((base / "api_contract.json").read_text(encoding="utf-8"))
endpoint_set = {(item["method"], item["path"]) for item in contract["endpoints"]}
checks = {
    "fastapi_entry": "app = FastAPI(" in sources["main"] and "include_router" in sources["main"],
    "write_routes": '@router.post("", response_model=RunResponse)' in sources["jobs"] and '@router.post("/upload", response_model=RunResponse)' in sources["jobs"],
    "read_routes": '@router.get("")' in sources["runs"] and '@router.get("/{run_id}")' in sources["runs"],
    "sqlite_layer": all(name in sources["db"] for name in ("init_db", "insert_run", "get_all_runs", "get_run", "get_runs_by_format")),
    "core_pipeline": "filter_records" in sources["jobs"] and "dedup_records" in sources["jobs"],
    "file_upload": "UploadFile" in sources["jobs"] and "NamedTemporaryFile" in sources["jobs"] and "os.unlink(tmp_path)" in sources["jobs"],
    "clear_errors": "status_code=400" in sources["jobs"] and "status_code=404" in sources["jobs"] and "run_not_found" in sources["runs"],
    "testclient_examples": "TestClient" in sources["tests"] and "status_code == 404" in sources["tests"] and "status_code == 400" in sources["tests"],
    "contract_endpoints": endpoint_set == {("GET", "/health"), ("POST", "/run"), ("POST", "/run/upload"), ("GET", "/runs"), ("GET", "/runs/{run_id}")},
    "demo_ok": demo.get("processed_count") == 3 and demo.get("total", 0) >= 1,
}
summary = {
    "ok": all(checks.values()) and proc.returncode == 0,
    "checks": checks,
    "demo_stdout": proc.stdout.strip(),
    "demo_stderr": proc.stderr.strip(),
    "files": {name: str(path.relative_to(base)) for name, path in files.items()},
}
(base / "round16_final_summary.json").write_text(
    json.dumps(summary, ensure_ascii=False, indent=2) + "\\n",
    encoding="utf-8",
)
print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
raise SystemExit(0 if summary["ok"] else 1)
'''


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    (LAB / "app" / "routers").mkdir(parents=True)
    (LAB / "tests").mkdir(parents=True)


def main() -> None:
    reset_lab()
    (LAB / "app" / "__init__.py").write_text("", encoding="utf-8")
    (LAB / "app" / "routers" / "__init__.py").write_text("", encoding="utf-8")
    (LAB / "app" / "db.py").write_text(DB_PY, encoding="utf-8")
    (LAB / "app" / "core.py").write_text(CORE_PY, encoding="utf-8")
    (LAB / "app" / "io_utils.py").write_text(IO_UTILS_PY, encoding="utf-8")
    (LAB / "app" / "schemas.py").write_text(SCHEMAS_PY, encoding="utf-8")
    (LAB / "app" / "main.py").write_text(MAIN_PY, encoding="utf-8")
    (LAB / "app" / "routers" / "jobs.py").write_text(JOBS_ROUTER_PY, encoding="utf-8")
    (LAB / "app" / "routers" / "runs.py").write_text(RUNS_ROUTER_PY, encoding="utf-8")
    (LAB / "tests" / "test_api_contract.py").write_text(TEST_API, encoding="utf-8")
    (LAB / "api_contract.json").write_text(
        json.dumps(
            {
                "endpoints": [
                    {"method": "GET", "path": "/health"},
                    {"method": "POST", "path": "/run"},
                    {"method": "POST", "path": "/run/upload"},
                    {"method": "GET", "path": "/runs"},
                    {"method": "GET", "path": "/runs/{run_id}"},
                ],
                "storage": "SQLite runs table",
                "errors": ["unsupported_format", "input_not_found", "read_failed", "run_not_found"],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (LAB / "requirements.txt").write_text("fastapi\nuvicorn\npydantic\npytest\n", encoding="utf-8")
    (LAB / "README.md").write_text(
        "# Round 16 API + data layer project\n\n"
        "Generated from the Web UI exercise. Static checks run without installing FastAPI; "
        "optional local server use requires the dependencies in requirements.txt.\n",
        encoding="utf-8",
    )
    demo = LAB / "run_demo.py"
    demo.write_text(RUN_DEMO, encoding="utf-8")
    demo.chmod(0o755)
    check = LAB / "final_contract_check.py"
    check.write_text(CONTRACT_CHECK, encoding="utf-8")
    check.chmod(0o755)
    proc = subprocess.run(["python3", str(check)], cwd=LAB, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    print("Round 16 综合练习：API + SQLite + 上传 + 错误 + 测试")
    print("sandbox:", LAB)
    print("summary:", LAB / "round16_final_summary.json")
    print("contract:", LAB / "api_contract.json")
    mark("r16-fin-comp")


if __name__ == "__main__":
    main()
