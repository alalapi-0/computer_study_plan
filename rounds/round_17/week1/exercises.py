#!/usr/bin/env python3
"""Round 17 · Week 1: generate an APIRouter service layout."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round17" / "week1_auto" / "router_layout"

CONFIG_PY = '''"""Configuration object used by generated service entrypoint."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Prep Tool API"
    app_version: str = "0.3.0"
    debug: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
'''

SCHEMAS_PY = '''"""Shared response schemas for Round 17 Week 1."""

from pydantic import BaseModel


class RunResponse(BaseModel):
    run_id: int
    status: str
    processed_count: int
'''

HEALTH_ROUTER = '''"""Health routes."""

from fastapi import APIRouter

from api.config import settings


router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    """Return service health and version."""
    return {"status": "ok", "version": settings.app_version}
'''

RUNS_ROUTER = '''"""Read routes for run history."""

from fastapi import APIRouter, HTTPException


router = APIRouter(prefix="/runs", tags=["runs"])
FAKE_RUNS = {
    1: {"id": 1, "format": "txt", "processed_count": 3},
    2: {"id": 2, "format": "csv", "processed_count": 42},
}


@router.get("")
def list_runs(skip: int = 0, limit: int = 20) -> dict:
    runs = list(FAKE_RUNS.values())
    return {"runs": runs[skip: skip + limit], "total": len(runs)}


@router.get("/{run_id}")
def get_run(run_id: int) -> dict:
    if run_id not in FAKE_RUNS:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")
    return FAKE_RUNS[run_id]
'''

JOBS_ROUTER = '''"""Write routes for processing jobs."""

from fastapi import APIRouter

from api.schemas import RunResponse


router = APIRouter(prefix="/run", tags=["jobs"])


@router.post("", response_model=RunResponse)
def trigger_run() -> RunResponse:
    return RunResponse(run_id=1001, status="accepted", processed_count=0)
'''

MAIN_PY = '''"""FastAPI service entrypoint split across APIRouter modules."""

from fastapi import FastAPI

from api.config import settings
from api.routers import health, jobs, runs


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI data-prep service wrapped as a multi-file API.",
    openapi_tags=[
        {"name": "health", "description": "Service status"},
        {"name": "runs", "description": "Read run history"},
        {"name": "jobs", "description": "Submit processing jobs"},
    ],
)
app.include_router(health.router)
app.include_router(runs.router)
app.include_router(jobs.router)
'''

STATIC_CHECK = '''#!/usr/bin/env python3
"""Static checks for the generated APIRouter service layout."""

from __future__ import annotations

import ast
import json
from pathlib import Path


base = Path(__file__).resolve().parent
files = {
    "main": base / "api" / "main.py",
    "health": base / "api" / "routers" / "health.py",
    "runs": base / "api" / "routers" / "runs.py",
    "jobs": base / "api" / "routers" / "jobs.py",
    "config": base / "api" / "config.py",
    "schemas": base / "api" / "schemas.py",
}
sources = {name: path.read_text(encoding="utf-8") for name, path in files.items()}
for source in sources.values():
    ast.parse(source)

inventory = json.loads((base / "route_inventory.json").read_text(encoding="utf-8"))
routes = {(item["method"], item["path"], item["module"]) for item in inventory["routes"]}
checks = {
    "main_uses_fastapi_metadata": "app = FastAPI(" in sources["main"] and "openapi_tags" in sources["main"],
    "routers_are_imported": "from api.routers import health, jobs, runs" in sources["main"],
    "routers_are_included": sources["main"].count("include_router") == 3,
    "health_router": 'APIRouter(tags=["health"])' in sources["health"] and '@router.get("/health")' in sources["health"],
    "runs_router": 'APIRouter(prefix="/runs", tags=["runs"])' in sources["runs"],
    "jobs_router": 'APIRouter(prefix="/run", tags=["jobs"])' in sources["jobs"],
    "response_model": "response_model=RunResponse" in sources["jobs"],
    "settings_used": "settings.app_name" in sources["main"] and "settings.app_version" in sources["main"],
    "inventory_routes": routes == {("GET", "/health", "health"), ("GET", "/runs", "runs"), ("GET", "/runs/{run_id}", "runs"), ("POST", "/run", "jobs")},
}
report = {"ok": all(checks.values()), "checks": checks, "files": {name: str(path.relative_to(base)) for name, path in files.items()}}
(base / "static_check_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
raise SystemExit(0 if report["ok"] else 1)
'''


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    (LAB / "api" / "routers").mkdir(parents=True)


def main() -> None:
    reset_lab()
    (LAB / "api" / "__init__.py").write_text("", encoding="utf-8")
    (LAB / "api" / "routers" / "__init__.py").write_text("", encoding="utf-8")
    (LAB / "api" / "config.py").write_text(CONFIG_PY, encoding="utf-8")
    (LAB / "api" / "schemas.py").write_text(SCHEMAS_PY, encoding="utf-8")
    (LAB / "api" / "routers" / "health.py").write_text(HEALTH_ROUTER, encoding="utf-8")
    (LAB / "api" / "routers" / "runs.py").write_text(RUNS_ROUTER, encoding="utf-8")
    (LAB / "api" / "routers" / "jobs.py").write_text(JOBS_ROUTER, encoding="utf-8")
    (LAB / "api" / "main.py").write_text(MAIN_PY, encoding="utf-8")
    (LAB / "route_inventory.json").write_text(
        json.dumps(
            {
                "routes": [
                    {"method": "GET", "path": "/health", "module": "health"},
                    {"method": "GET", "path": "/runs", "module": "runs"},
                    {"method": "GET", "path": "/runs/{run_id}", "module": "runs"},
                    {"method": "POST", "path": "/run", "module": "jobs"},
                ]
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    check = LAB / "static_check.py"
    check.write_text(STATIC_CHECK, encoding="utf-8")
    check.chmod(0o755)
    proc = subprocess.run(["python3", str(check)], cwd=LAB, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    print("Round 17 Week 1 APIRouter 服务拆分")
    print("sandbox:", LAB)
    print("entrypoint:", LAB / "api" / "main.py")
    print("report:", LAB / "static_check_report.json")
    mark("r17-w1-ex1")


if __name__ == "__main__":
    main()
