#!/usr/bin/env python3
"""Round 16 · Week 3: generate error contracts and API test examples."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round16" / "week3_auto" / "errors_and_tests"

JOBS_ROUTER_PY = '''"""Error-handled /run route for Round 16 Week 3."""

from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.schemas import RunRequest, RunResponse


router = APIRouter(prefix="/run", tags=["jobs"])
SUPPORTED_FORMATS = {"txt", "csv"}


@router.post("", response_model=RunResponse)
def trigger_run(req: RunRequest) -> RunResponse:
    """Return clear HTTP errors before entering the processing pipeline."""
    if req.format not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail={"code": "unsupported_format", "message": f"Unsupported format: {req.format}"},
        )
    if not Path(req.input_file).exists():
        raise HTTPException(
            status_code=404,
            detail={"code": "input_not_found", "message": f"Input file not found: {req.input_file}"},
        )
    return RunResponse(run_id=1, status="completed", input_file=req.input_file, processed_count=0)
'''

SCHEMAS_PY = '''"""Schemas for static API tests."""

from pydantic import BaseModel


class RunRequest(BaseModel):
    input_file: str
    format: str = "txt"
    dedup: bool = False


class RunResponse(BaseModel):
    run_id: int
    status: str
    input_file: str
    processed_count: int
'''

MAIN_PY = '''"""Round 16 Week 3 FastAPI app."""

from fastapi import FastAPI

from app.routers import jobs


app = FastAPI(title="Round 16 Error Contract API")
app.include_router(jobs.router)
'''

TEST_API = '''"""TestClient examples for Round 16 Week 3."""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_missing_file_returns_404():
    response = client.post("/run", json={"input_file": "missing.txt", "format": "txt"})
    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "input_not_found"


def test_unsupported_format_returns_400():
    response = client.post("/run", json={"input_file": "input/demo.md", "format": "md"})
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "unsupported_format"


def test_request_validation_returns_422():
    response = client.post("/run", json={"format": "txt"})
    assert response.status_code == 422
'''

ERROR_SIMULATOR = '''#!/usr/bin/env python3
"""Simulate the API error contract using only the standard library."""

from __future__ import annotations

import json
from pathlib import Path


def response_for(payload: dict) -> dict:
    if "input_file" not in payload:
        return {"status_code": 422, "detail": {"code": "validation_error"}}
    if payload.get("format", "txt") not in {"txt", "csv"}:
        return {"status_code": 400, "detail": {"code": "unsupported_format"}}
    if not Path(payload["input_file"]).exists():
        return {"status_code": 404, "detail": {"code": "input_not_found"}}
    return {"status_code": 200, "detail": {"code": "ok"}}


cases = [
    {"name": "missing_file", "payload": {"input_file": "missing.txt", "format": "txt"}, "expected": 404},
    {"name": "bad_format", "payload": {"input_file": "input/demo.md", "format": "md"}, "expected": 400},
    {"name": "validation", "payload": {"format": "txt"}, "expected": 422},
]
results = []
for case in cases:
    actual = response_for(case["payload"])
    results.append({**case, "actual": actual, "ok": actual["status_code"] == case["expected"]})

report = {"ok": all(item["ok"] for item in results), "results": results}
Path("round16_week3_error_report.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\\n",
    encoding="utf-8",
)
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
'''

STATIC_CHECK = '''#!/usr/bin/env python3
"""Static checks for Round 16 Week 3 error handling and tests."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path


base = Path(__file__).resolve().parent
jobs_source = (base / "app" / "routers" / "jobs.py").read_text(encoding="utf-8")
test_source = (base / "tests" / "test_api_contract.py").read_text(encoding="utf-8")
ast.parse(jobs_source)
ast.parse(test_source)
proc = subprocess.run(
    [sys.executable, "error_simulator.py"],
    cwd=base,
    capture_output=True,
    text=True,
    check=False,
)
sim_report = {}
if proc.returncode == 0:
    sim_report = json.loads((base / "round16_week3_error_report.json").read_text(encoding="utf-8"))

checks = {
    "uses_httpexception": "HTTPException" in jobs_source,
    "unsupported_format_400": "status_code=400" in jobs_source and "unsupported_format" in jobs_source,
    "missing_file_404": "status_code=404" in jobs_source and "input_not_found" in jobs_source,
    "structured_detail": '"code":' in jobs_source and '"message":' in jobs_source,
    "testclient_import": "from fastapi.testclient import TestClient" in test_source,
    "tests_400_404_422": all(text in test_source for text in ("status_code == 400", "status_code == 404", "status_code == 422")),
    "tests_check_error_codes": "input_not_found" in test_source and "unsupported_format" in test_source,
    "simulation_ok": sim_report.get("ok") is True,
}
report = {
    "ok": all(checks.values()) and proc.returncode == 0,
    "checks": checks,
    "simulator_stdout": proc.stdout.strip(),
    "simulator_stderr": proc.stderr.strip(),
    "files": [
        "app/routers/jobs.py",
        "tests/test_api_contract.py",
        "round16_week3_error_report.json",
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
    (LAB / "tests").mkdir(parents=True)


def main() -> None:
    reset_lab()
    (LAB / "app" / "__init__.py").write_text("", encoding="utf-8")
    (LAB / "app" / "routers" / "__init__.py").write_text("", encoding="utf-8")
    (LAB / "app" / "schemas.py").write_text(SCHEMAS_PY, encoding="utf-8")
    (LAB / "app" / "main.py").write_text(MAIN_PY, encoding="utf-8")
    (LAB / "app" / "routers" / "jobs.py").write_text(JOBS_ROUTER_PY, encoding="utf-8")
    (LAB / "tests" / "test_api_contract.py").write_text(TEST_API, encoding="utf-8")
    simulator = LAB / "error_simulator.py"
    simulator.write_text(ERROR_SIMULATOR, encoding="utf-8")
    simulator.chmod(0o755)
    (LAB / "error_contract.json").write_text(
        json.dumps(
            {
                "errors": [
                    {"case": "unsupported_format", "status_code": 400},
                    {"case": "input_not_found", "status_code": 404},
                    {"case": "request_validation", "status_code": 422},
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
    print("Round 16 Week 3 错误响应 + API 测试")
    print("sandbox:", LAB)
    print("router:", LAB / "app" / "routers" / "jobs.py")
    print("tests:", LAB / "tests" / "test_api_contract.py")
    print("report:", LAB / "static_check_report.json")
    mark("r16-w3-ex3")


if __name__ == "__main__":
    main()
