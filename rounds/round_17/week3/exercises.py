#!/usr/bin/env python3
"""Round 17 · Week 3: generate auth, CORS, Docker, and preflight examples."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round17" / "week3_auto" / "security_deploy"

CONFIG_PY = '''"""Deployment-facing settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = False
    allowed_origins: list[str] = ["http://localhost:3000"]
    api_token: str = "secret-dev-token"

    class Config:
        env_file = ".env"


settings = Settings()
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

MAIN_PY = '''"""Service entrypoint with CORS and routers."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import settings
from api.routers import jobs


app = FastAPI(title="Round 17 Service Wrapup", version="0.3.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else settings.allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
app.include_router(jobs.router)
'''

JOBS_ROUTER = '''"""Protected job route."""

from fastapi import APIRouter, Depends

from api.auth import get_current_user


router = APIRouter(prefix="/run", tags=["jobs"])


@router.post("")
def trigger_run(current_user: dict = Depends(get_current_user)) -> dict:
    return {"status": "accepted", "user": current_user["username"]}
'''

DOCKERFILE = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p input output logs
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

REQUIREMENTS = """fastapi
uvicorn
pydantic
pydantic-settings
"""

PREFLIGHT = '''#!/usr/bin/env python3
"""Deployment preflight checks without running Docker."""

from __future__ import annotations

import json
from pathlib import Path


base = Path(__file__).resolve().parent
dockerfile = (base / "Dockerfile").read_text(encoding="utf-8")
requirements = (base / "requirements.txt").read_text(encoding="utf-8")
checks = {
    "workdir": "WORKDIR /app" in dockerfile,
    "dependencies": "pip install --no-cache-dir -r requirements.txt" in dockerfile,
    "port": "EXPOSE 8000" in dockerfile,
    "uvicorn_cmd": '"uvicorn", "api.main:app"' in dockerfile,
    "requirements": all(name in requirements for name in ("fastapi", "uvicorn", "pydantic-settings")),
}
report = {"ok": all(checks.values()), "checks": checks}
(base / "deployment_preflight_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
raise SystemExit(0 if report["ok"] else 1)
'''

STATIC_CHECK = '''#!/usr/bin/env python3
"""Static checks for auth, CORS, and deployment files."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path


base = Path(__file__).resolve().parent
auth = (base / "api" / "auth.py").read_text(encoding="utf-8")
main = (base / "api" / "main.py").read_text(encoding="utf-8")
jobs = (base / "api" / "routers" / "jobs.py").read_text(encoding="utf-8")
for source in (auth, main, jobs, (base / "api" / "config.py").read_text(encoding="utf-8")):
    ast.parse(source)

proc = subprocess.run([sys.executable, "preflight_check.py"], cwd=base, capture_output=True, text=True, check=False)
preflight = {}
if proc.returncode == 0:
    preflight = json.loads((base / "deployment_preflight_report.json").read_text(encoding="utf-8"))

checks = {
    "oauth2_bearer": "OAuth2PasswordBearer" in auth and 'tokenUrl="token"' in auth,
    "unauthorized_401": "HTTP_401_UNAUTHORIZED" in auth and "WWW-Authenticate" in auth and "Bearer" in auth,
    "protected_route": "Depends(get_current_user)" in jobs,
    "cors_middleware": "CORSMiddleware" in main and "allow_origins" in main and "allow_methods" in main,
    "dockerfile": (base / "Dockerfile").exists(),
    "preflight_ok": preflight.get("ok") is True,
    "checklist": (base / "deployment_checklist.md").exists(),
}
report = {"ok": all(checks.values()) and proc.returncode == 0, "checks": checks, "preflight_stdout": proc.stdout.strip(), "preflight_stderr": proc.stderr.strip()}
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
    (LAB / "api" / "auth.py").write_text(AUTH_PY, encoding="utf-8")
    (LAB / "api" / "main.py").write_text(MAIN_PY, encoding="utf-8")
    (LAB / "api" / "routers" / "jobs.py").write_text(JOBS_ROUTER, encoding="utf-8")
    (LAB / "Dockerfile").write_text(DOCKERFILE, encoding="utf-8")
    (LAB / "requirements.txt").write_text(REQUIREMENTS, encoding="utf-8")
    (LAB / "deployment_checklist.md").write_text(
        "# Deployment preflight checklist\n\n"
        "- [ ] Health endpoint exists.\n"
        "- [ ] Debug mode is off outside local development.\n"
        "- [ ] Bearer token is not the sample token in real deployment.\n"
        "- [ ] CORS origins are explicit in production.\n"
        "- [ ] Dockerfile exposes and runs port 8000.\n",
        encoding="utf-8",
    )
    preflight = LAB / "preflight_check.py"
    preflight.write_text(PREFLIGHT, encoding="utf-8")
    preflight.chmod(0o755)
    check = LAB / "static_check.py"
    check.write_text(STATIC_CHECK, encoding="utf-8")
    check.chmod(0o755)
    proc = subprocess.run(["python3", str(check)], cwd=LAB, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    print("Round 17 Week 3 认证、CORS 与部署检查")
    print("sandbox:", LAB)
    print("auth:", LAB / "api" / "auth.py")
    print("report:", LAB / "static_check_report.json")
    mark("r17-w3-ex3")


if __name__ == "__main__":
    main()
