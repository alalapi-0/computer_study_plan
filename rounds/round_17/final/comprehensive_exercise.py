#!/usr/bin/env python3
"""Round 17 · Final: generate a service wrap-up project package."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round17" / "final_auto" / "service_wrapup_project"

CONFIG_PY = '''"""Service settings loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Prep Tool API"
    app_version: str = "0.3.0"
    db_path: str = "data/runs.db"
    log_level: str = "INFO"
    debug: bool = False
    api_token: str = "secret-dev-token"
    allowed_origins: list[str] = ["http://localhost:3000"]
    docs_url: str = "/docs"
    openapi_url: str = "/openapi.json"

    class Config:
        env_file = ".env"


settings = Settings()
'''

LOG_UTILS_PY = '''"""Logging setup for the service."""

from __future__ import annotations

import logging
from pathlib import Path

from api.config import settings


def setup_logging() -> None:
    Path("logs").mkdir(exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        handlers=[
            logging.FileHandler("logs/service.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def get_logger(name: str) -> logging.Logger:
    setup_logging()
    return logging.getLogger(name)
'''

AUTH_PY = '''"""Concept-level Bearer token authentication."""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from api.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    if token != settings.api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": "dev-user"}
'''

SCHEMAS_PY = '''"""Shared schemas."""

from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    input_file: str = Field(..., examples=["input/demo.txt"])
    format: str = Field("txt", examples=["txt", "csv"])
    dedup: bool = False


class RunResponse(BaseModel):
    run_id: int
    status: str
    processed_count: int
    message: str = ""
'''

HEALTH_ROUTER = '''"""Health routes."""

from fastapi import APIRouter

from api.config import settings


router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": settings.app_version}
'''

RUNS_ROUTER = '''"""Run history routes."""

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

JOBS_ROUTER = '''"""Protected job submission routes."""

from fastapi import APIRouter, Depends

from api.auth import get_current_user
from api.log_utils import get_logger
from api.schemas import RunRequest, RunResponse


router = APIRouter(prefix="/run", tags=["jobs"])
logger = get_logger(__name__)


@router.post("", response_model=RunResponse)
def trigger_run(req: RunRequest, current_user: dict = Depends(get_current_user)) -> RunResponse:
    logger.info("accepted run request")
    return RunResponse(
        run_id=1001,
        status="accepted",
        processed_count=0,
        message=f"queued {req.input_file} for {current_user['username']}",
    )
'''

MAIN_PY = '''"""FastAPI service wrap-up entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import settings
from api.log_utils import get_logger
from api.routers import health, jobs, runs


logger = get_logger(__name__)
logger.info("building service application")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI data-prep API with routers, settings, logging, auth, CORS, and deployment files.",
    docs_url=settings.docs_url if settings.debug else None,
    openapi_url=settings.openapi_url if settings.debug else None,
    openapi_tags=[
        {"name": "health", "description": "Service status"},
        {"name": "runs", "description": "Read run history"},
        {"name": "jobs", "description": "Submit processing jobs"},
    ],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else settings.allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
app.include_router(health.router)
app.include_router(runs.router)
app.include_router(jobs.router)
'''

DOCKERFILE = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p input output logs data
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

REQUIREMENTS = """fastapi
uvicorn
pydantic
pydantic-settings
"""

ENV_EXAMPLE = """APP_NAME=AI Prep Tool API
APP_VERSION=0.3.0
DB_PATH=data/runs.db
LOG_LEVEL=INFO
DEBUG=false
API_TOKEN=replace-this-token
ALLOWED_ORIGINS=["http://localhost:3000"]
DOCS_URL=/docs
OPENAPI_URL=/openapi.json
"""

SERVICE_CONTRACT = {
    "routes": [
        {"method": "GET", "path": "/health", "auth": False},
        {"method": "GET", "path": "/runs", "auth": False},
        {"method": "GET", "path": "/runs/{run_id}", "auth": False},
        {"method": "POST", "path": "/run", "auth": True},
    ],
    "runtime": {
        "command": "uvicorn api.main:app --host 0.0.0.0 --port 8000",
        "docker_port": 8000,
    },
}

CHECK_SCRIPT = '''#!/usr/bin/env python3
"""Final static contract check for Round 17 service wrap-up."""

from __future__ import annotations

import ast
import json
from pathlib import Path


base = Path(__file__).resolve().parent
files = {
    "main": base / "api" / "main.py",
    "config": base / "api" / "config.py",
    "log_utils": base / "api" / "log_utils.py",
    "auth": base / "api" / "auth.py",
    "schemas": base / "api" / "schemas.py",
    "health": base / "api" / "routers" / "health.py",
    "runs": base / "api" / "routers" / "runs.py",
    "jobs": base / "api" / "routers" / "jobs.py",
}
sources = {name: path.read_text(encoding="utf-8") for name, path in files.items()}
for source in sources.values():
    ast.parse(source)

contract = json.loads((base / "service_contract.json").read_text(encoding="utf-8"))
dockerfile = (base / "Dockerfile").read_text(encoding="utf-8")
requirements = (base / "requirements.txt").read_text(encoding="utf-8")
checklist = (base / "deployment_checklist.md").read_text(encoding="utf-8")
routes = {(item["method"], item["path"], item["auth"]) for item in contract["routes"]}

checks = {
    "metadata": "title=settings.app_name" in sources["main"] and "openapi_tags" in sources["main"],
    "router_split": sources["main"].count("include_router") == 3 and "from api.routers import health, jobs, runs" in sources["main"],
    "settings": "class Settings(BaseSettings)" in sources["config"] and "api_token" in sources["config"] and "allowed_origins" in sources["config"],
    "logging": "logging.basicConfig" in sources["log_utils"] and "FileHandler" in sources["log_utils"],
    "auth": "OAuth2PasswordBearer" in sources["auth"] and "HTTP_401_UNAUTHORIZED" in sources["auth"] and "WWW-Authenticate" in sources["auth"],
    "protected_job": "Depends(get_current_user)" in sources["jobs"] and "response_model=RunResponse" in sources["jobs"],
    "cors": "CORSMiddleware" in sources["main"] and "allow_origins" in sources["main"],
    "docker": "EXPOSE 8000" in dockerfile and '"uvicorn", "api.main:app"' in dockerfile,
    "requirements": all(name in requirements for name in ("fastapi", "uvicorn", "pydantic-settings")),
    "contract_routes": routes == {("GET", "/health", False), ("GET", "/runs", False), ("GET", "/runs/{run_id}", False), ("POST", "/run", True)},
    "checklist": all(text in checklist for text in ("Health endpoint", "Debug mode", "Bearer token", "CORS", "Dockerfile")),
}
summary = {"ok": all(checks.values()), "checks": checks, "files": {name: str(path.relative_to(base)) for name, path in files.items()}}
(base / "round17_final_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
raise SystemExit(0 if summary["ok"] else 1)
'''


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    (LAB / "api" / "routers").mkdir(parents=True)
    (LAB / "tests").mkdir(parents=True)


def main() -> None:
    reset_lab()
    (LAB / "api" / "__init__.py").write_text("", encoding="utf-8")
    (LAB / "api" / "routers" / "__init__.py").write_text("", encoding="utf-8")
    (LAB / "api" / "config.py").write_text(CONFIG_PY, encoding="utf-8")
    (LAB / "api" / "log_utils.py").write_text(LOG_UTILS_PY, encoding="utf-8")
    (LAB / "api" / "auth.py").write_text(AUTH_PY, encoding="utf-8")
    (LAB / "api" / "schemas.py").write_text(SCHEMAS_PY, encoding="utf-8")
    (LAB / "api" / "routers" / "health.py").write_text(HEALTH_ROUTER, encoding="utf-8")
    (LAB / "api" / "routers" / "runs.py").write_text(RUNS_ROUTER, encoding="utf-8")
    (LAB / "api" / "routers" / "jobs.py").write_text(JOBS_ROUTER, encoding="utf-8")
    (LAB / "api" / "main.py").write_text(MAIN_PY, encoding="utf-8")
    (LAB / "Dockerfile").write_text(DOCKERFILE, encoding="utf-8")
    (LAB / "requirements.txt").write_text(REQUIREMENTS, encoding="utf-8")
    (LAB / ".env.example").write_text(ENV_EXAMPLE, encoding="utf-8")
    (LAB / "service_contract.json").write_text(json.dumps(SERVICE_CONTRACT, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (LAB / "deployment_checklist.md").write_text(
        "# Deployment preflight checklist\n\n"
        "- [ ] Health endpoint returns `ok`.\n"
        "- [ ] Debug mode is off outside local development.\n"
        "- [ ] Bearer token is replaced outside demos.\n"
        "- [ ] CORS origins are explicit in production.\n"
        "- [ ] Dockerfile exposes port 8000 and runs uvicorn.\n",
        encoding="utf-8",
    )
    (LAB / "README.md").write_text(
        "# Round 17 service wrap-up package\n\n"
        "Generated by the Web UI exercise. Static checks validate service structure without installing dependencies or running Docker.\n",
        encoding="utf-8",
    )
    check = LAB / "final_contract_check.py"
    check.write_text(CHECK_SCRIPT, encoding="utf-8")
    check.chmod(0o755)
    proc = subprocess.run(["python3", str(check)], cwd=LAB, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    print("Round 17 综合练习：服务化收口项目包")
    print("sandbox:", LAB)
    print("summary:", LAB / "round17_final_summary.json")
    print("contract:", LAB / "service_contract.json")
    mark("r17-fin-comp")


if __name__ == "__main__":
    main()
