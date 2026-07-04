#!/usr/bin/env python3
"""Round 17 · Week 2: generate settings, metadata, and logging examples."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round17" / "week2_auto" / "settings_logging"

CONFIG_PY = '''"""Environment-based service settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Prep Tool API"
    app_version: str = "0.3.0"
    db_path: str = "runs.db"
    log_level: str = "INFO"
    debug: bool = False
    docs_url: str = "/docs"
    openapi_url: str = "/openapi.json"

    class Config:
        env_file = ".env"


settings = Settings()
'''

LOG_UTILS_PY = '''"""Logging utilities shared by API modules."""

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

MAIN_PY = '''"""Service entrypoint with metadata and logging setup."""

from fastapi import FastAPI

from api.config import settings
from api.log_utils import get_logger


logger = get_logger(__name__)
logger.info("starting service", extra={"app_version": settings.app_version})

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI data-prep API with environment settings and unified logging.",
    docs_url=settings.docs_url if settings.debug else None,
    openapi_url=settings.openapi_url if settings.debug else None,
)
'''

ENV_EXAMPLE = """APP_NAME=AI Prep Tool API
APP_VERSION=0.3.0
DB_PATH=runs.db
LOG_LEVEL=DEBUG
DEBUG=true
DOCS_URL=/docs
OPENAPI_URL=/openapi.json
"""

LOGGING_DEMO = '''#!/usr/bin/env python3
"""Standard-library logging demo for Round 17 Week 2."""

from __future__ import annotations

import json
import logging
from pathlib import Path


base = Path(__file__).resolve().parent
env = {}
for line in (base / ".env.example").read_text(encoding="utf-8").splitlines():
    if "=" in line:
        key, value = line.split("=", 1)
        env[key] = value

log_dir = base / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "round17_week2.log"
logging.basicConfig(
    filename=log_file,
    level=getattr(logging, env.get("LOG_LEVEL", "INFO")),
    format="%(levelname)s:%(name)s:%(message)s",
    force=True,
)
logger = logging.getLogger("round17.week2")
logger.debug("debug mode is enabled")
logger.info("service metadata loaded")

report = {
    "app_name": env.get("APP_NAME"),
    "debug": env.get("DEBUG") == "true",
    "log_file": str(log_file),
    "log_contains_debug": "debug mode is enabled" in log_file.read_text(encoding="utf-8"),
}
(base / "round17_week2_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
'''

STATIC_CHECK = '''#!/usr/bin/env python3
"""Static checks for settings and logging examples."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path


base = Path(__file__).resolve().parent
config = (base / "api" / "config.py").read_text(encoding="utf-8")
log_utils = (base / "api" / "log_utils.py").read_text(encoding="utf-8")
main = (base / "api" / "main.py").read_text(encoding="utf-8")
for source in (config, log_utils, main):
    ast.parse(source)

proc = subprocess.run([sys.executable, "logging_demo.py"], cwd=base, capture_output=True, text=True, check=False)
demo = {}
if proc.returncode == 0:
    demo = json.loads((base / "round17_week2_report.json").read_text(encoding="utf-8"))

checks = {
    "settings_class": "class Settings(BaseSettings)" in config and 'env_file = ".env"' in config,
    "important_fields": all(field in config for field in ("app_name", "app_version", "db_path", "log_level", "debug")),
    "metadata_uses_settings": "title=settings.app_name" in main and "version=settings.app_version" in main,
    "docs_gate": "docs_url=settings.docs_url if settings.debug else None" in main,
    "logging_setup": "logging.basicConfig" in log_utils and "FileHandler" in log_utils and "StreamHandler" in log_utils,
    "logger_used": "get_logger(__name__)" in main and "logger.info" in main,
    "env_example": "LOG_LEVEL=DEBUG" in (base / ".env.example").read_text(encoding="utf-8"),
    "demo_ok": demo.get("debug") is True and demo.get("log_contains_debug") is True,
}
report = {"ok": all(checks.values()) and proc.returncode == 0, "checks": checks, "demo_stdout": proc.stdout.strip(), "demo_stderr": proc.stderr.strip()}
(base / "static_check_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
raise SystemExit(0 if report["ok"] else 1)
'''


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    (LAB / "api").mkdir(parents=True)


def main() -> None:
    reset_lab()
    (LAB / "api" / "__init__.py").write_text("", encoding="utf-8")
    (LAB / "api" / "config.py").write_text(CONFIG_PY, encoding="utf-8")
    (LAB / "api" / "log_utils.py").write_text(LOG_UTILS_PY, encoding="utf-8")
    (LAB / "api" / "main.py").write_text(MAIN_PY, encoding="utf-8")
    (LAB / ".env.example").write_text(ENV_EXAMPLE, encoding="utf-8")
    demo = LAB / "logging_demo.py"
    demo.write_text(LOGGING_DEMO, encoding="utf-8")
    demo.chmod(0o755)
    check = LAB / "static_check.py"
    check.write_text(STATIC_CHECK, encoding="utf-8")
    check.chmod(0o755)
    proc = subprocess.run(["python3", str(check)], cwd=LAB, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    print("Round 17 Week 2 配置、元数据与日志")
    print("sandbox:", LAB)
    print("config:", LAB / "api" / "config.py")
    print("report:", LAB / "static_check_report.json")
    mark("r17-w2-ex2")


if __name__ == "__main__":
    main()
