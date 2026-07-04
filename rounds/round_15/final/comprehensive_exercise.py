#!/usr/bin/env python3
"""Round 15 · Final: generate a static-checkable FastAPI project skeleton."""

from __future__ import annotations

import ast
import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round15" / "final_auto" / "fastapi_project"

SCHEMAS = '''"""Round 15 final Pydantic schemas."""

from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    input_file: str = Field(..., description="Input file path", examples=["input/demo.txt"])
    format: str = Field("txt", description="Input format", examples=["txt"])
    dedup: bool = Field(False, description="Whether to remove duplicates")

    model_config = {
        "json_schema_extra": {
            "example": {"input_file": "input/demo.txt", "format": "txt", "dedup": True}
        }
    }


class RunResponse(BaseModel):
    run_id: int
    status: str
    input_file: str
    processed_count: int | None = None
    message: str | None = None


class RunRecord(BaseModel):
    id: int
    input_file: str
    format: str
    processed_count: int
    dedup: bool
'''

RUNS_ROUTER = '''"""Read routes for Round 15 final FastAPI project."""

from fastapi import APIRouter, HTTPException
from app.schemas import RunRecord

router = APIRouter(prefix="/runs", tags=["runs"])

FAKE_RUNS = {
    1: RunRecord(id=1, input_file="input/demo.txt", format="txt", processed_count=3, dedup=True),
    2: RunRecord(id=2, input_file="input/labels.csv", format="csv", processed_count=42, dedup=False),
}


@router.get("/{run_id}", response_model=RunRecord, summary="Get one run")
def get_run(run_id: int) -> RunRecord:
    """Get one run by integer path parameter."""
    if run_id not in FAKE_RUNS:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")
    return FAKE_RUNS[run_id]


@router.get("", summary="List runs")
def list_runs(skip: int = 0, limit: int = 20, format: str | None = None) -> dict:
    """List runs with query parameters."""
    limit = min(max(limit, 1), 100)
    runs = list(FAKE_RUNS.values())
    if format:
        runs = [item for item in runs if item.format == format]
    return {"runs": runs[skip: skip + limit], "total": len(runs), "skip": skip, "limit": limit}
'''

JOBS_ROUTER = '''"""Job routes for Round 15 final FastAPI project."""

from fastapi import APIRouter
from app.schemas import RunRequest, RunResponse

router = APIRouter(tags=["jobs"])


@router.post("/run", response_model=RunResponse, summary="Submit one run")
def trigger_run(req: RunRequest) -> RunResponse:
    """Submit one data-processing request and return a structured result."""
    return RunResponse(
        run_id=1001,
        status="completed",
        input_file=req.input_file,
        processed_count=3,
        message=f"Processed {req.input_file} with format={req.format}, dedup={req.dedup}",
    )
'''

MAIN = '''"""Round 15 final FastAPI application entrypoint."""

from fastapi import FastAPI
from app.routers import jobs, runs

app = FastAPI(title="AI Prep Tool API", version="0.1.0")
app.include_router(runs.router)
app.include_router(jobs.router)


@app.get("/health", tags=["system"], summary="Health check")
def health() -> dict[str, str]:
    """Return a minimal health signal."""
    return {"status": "ok", "service": "ai_prep_tool_api"}
'''

CONTRACT_CHECK = '''#!/usr/bin/env python3
"""Static contract checks for the Round 15 final FastAPI project."""

import ast
import json
from pathlib import Path

base = Path(__file__).resolve().parent
files = {
    "main": base / "app" / "main.py",
    "schemas": base / "app" / "schemas.py",
    "runs": base / "app" / "routers" / "runs.py",
    "jobs": base / "app" / "routers" / "jobs.py",
}
sources = {name: path.read_text(encoding="utf-8") for name, path in files.items()}
schema_tree = ast.parse(sources["schemas"])
classes = {node.name for node in ast.walk(schema_tree) if isinstance(node, ast.ClassDef)}
checks = {
    "app_entry": "app = FastAPI(" in sources["main"] and "include_router" in sources["main"],
    "health_route": '@app.get("/health"' in sources["main"],
    "routers": 'APIRouter(prefix="/runs"' in sources["runs"] and 'APIRouter(tags=["jobs"])' in sources["jobs"],
    "path_parameter": '@router.get("/{run_id}"' in sources["runs"] and "run_id: int" in sources["runs"],
    "query_parameters": "skip: int = 0" in sources["runs"] and "limit: int = 20" in sources["runs"],
    "request_body": "req: RunRequest" in sources["jobs"] and '@router.post("/run"' in sources["jobs"],
    "response_models": "response_model=RunRecord" in sources["runs"] and "response_model=RunResponse" in sources["jobs"],
    "pydantic_models": {"RunRequest", "RunResponse", "RunRecord"}.issubset(classes),
    "examples": "json_schema_extra" in sources["schemas"],
}
contract = json.loads((base / "api_contract.json").read_text(encoding="utf-8"))
checks["contract_routes"] = {item["path"] for item in contract["endpoints"]} == {"/health", "/runs", "/runs/{run_id}", "/run"}
report = {"ok": all(checks.values()), "checks": checks, "files": {name: str(path) for name, path in files.items()}}
(base / "round15_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
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
    (LAB / "app" / "schemas.py").write_text(SCHEMAS, encoding="utf-8")
    (LAB / "app" / "main.py").write_text(MAIN, encoding="utf-8")
    (LAB / "app" / "routers" / "runs.py").write_text(RUNS_ROUTER, encoding="utf-8")
    (LAB / "app" / "routers" / "jobs.py").write_text(JOBS_ROUTER, encoding="utf-8")
    contract = {
        "endpoints": [
            {"method": "GET", "path": "/health", "parameter_source": "none"},
            {"method": "GET", "path": "/runs", "parameter_source": "query"},
            {"method": "GET", "path": "/runs/{run_id}", "parameter_source": "path"},
            {"method": "POST", "path": "/run", "parameter_source": "body"},
        ]
    }
    (LAB / "api_contract.json").write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (LAB / "requirements.txt").write_text("fastapi\nuvicorn\npydantic\n", encoding="utf-8")
    (LAB / "README.md").write_text(
        "# Round 15 FastAPI project skeleton\n\n"
        "This package is generated for code reading and static contract checks in the Web UI flow.\n"
        "Optional local run outside the Web UI: install dependencies, then run uvicorn app.main:app --reload.\n",
        encoding="utf-8",
    )
    check = LAB / "static_contract_test.py"
    check.write_text(CONTRACT_CHECK, encoding="utf-8")
    check.chmod(0o755)
    proc = subprocess.run(["python3", str(check)], cwd=LAB, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    print("Round 15 收口检查")
    print("sandbox:", LAB)
    print("app:", LAB / "app" / "main.py")
    print("schemas:", LAB / "app" / "schemas.py")
    print("summary:", LAB / "round15_summary.json")
    mark("r15-fin-comp")


if __name__ == "__main__":
    main()
