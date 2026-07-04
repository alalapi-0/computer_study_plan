#!/usr/bin/env python3
"""Round 14 · Final: local HTTP/API design package."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round14" / "final_auto" / "ai_prep_api_design"


API_CONTRACT = {
    "service": "ai_prep_tool_api",
    "version": "0.1.0",
    "base_path": "/",
    "endpoints": [
        {"method": "GET", "path": "/health", "summary": "Health check", "success_status": 200},
        {"method": "GET", "path": "/runs", "summary": "List run records", "success_status": 200},
        {"method": "GET", "path": "/runs/{run_id}", "summary": "Get one run record", "success_status": 200, "not_found_status": 404},
        {"method": "POST", "path": "/run", "summary": "Submit one processing job", "success_status": 201, "bad_request_status": 400},
    ],
    "schemas": {
        "RunRequest": {"input_file": "str", "format": "str", "dedup": "bool"},
        "RunResponse": {"run_id": "int", "status": "str", "message": "str"},
        "ErrorResponse": {"error": "str", "message": "str"},
    },
}

MOCK_API = '''"""Round 14 final mock API using standard library only."""

from __future__ import annotations

import json
from urllib.parse import parse_qs, urlparse


RUNS = [
    {"id": 1, "input_file": "input/demo.txt", "format": "txt", "dedup": True, "status": "completed", "processed_count": 3},
]


def response(status: int, body: dict) -> dict:
    return {"status": status, "headers": {"content-type": "application/json"}, "body": body}


def handle_request(method: str, path: str, body: dict | None = None) -> dict:
    method = method.upper()
    parsed = urlparse(path)
    clean_path = parsed.path
    query = parse_qs(parsed.query)
    if method == "GET" and clean_path == "/health":
        return response(200, {"status": "ok", "version": "0.1.0"})
    if method == "GET" and clean_path == "/runs":
        skip = int(query.get("skip", ["0"])[0])
        limit = int(query.get("limit", ["20"])[0])
        return response(200, {"runs": RUNS[skip:skip + limit], "total": len(RUNS), "skip": skip, "limit": limit})
    if method == "GET" and clean_path.startswith("/runs/"):
        run_id = int(clean_path.rsplit("/", 1)[-1])
        for item in RUNS:
            if item["id"] == run_id:
                return response(200, item)
        return response(404, {"error": "run_not_found", "message": f"Run {run_id} was not found"})
    if method == "POST" and clean_path == "/run":
        payload = body or {}
        if not payload.get("input_file"):
            return response(400, {"error": "invalid_request", "message": "input_file is required"})
        return response(201, {"run_id": 2, "status": "accepted", "message": f"Will process {payload['input_file']}"})
    return response(404, {"error": "route_not_found", "message": f"{method} {clean_path} is not defined"})


def dumps_response(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)
'''

CLIENT_DEMO = '''#!/usr/bin/env python3
"""Client-style demo for the Round 14 final mock API."""

import json
from pathlib import Path
from mock_api import handle_request

base = Path(__file__).resolve().parent
calls = [
    {"name": "health", "response": handle_request("GET", "/health")},
    {"name": "list_runs", "response": handle_request("GET", "/runs?skip=0&limit=5")},
    {"name": "get_run", "response": handle_request("GET", "/runs/1")},
    {"name": "missing_run", "response": handle_request("GET", "/runs/999")},
    {"name": "submit_run", "response": handle_request("POST", "/run", {"input_file": "input/demo.txt", "format": "txt", "dedup": True})},
    {"name": "bad_request", "response": handle_request("POST", "/run", {})},
]
report = {"ok": True, "calls": calls, "status_codes": [item["response"]["status"] for item in calls]}
(base / "client_demo_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
'''

PREFLIGHT = '''#!/usr/bin/env python3
"""Preflight checks for the Round 14 API design package."""

import json
import subprocess
import sys
from pathlib import Path

base = Path(__file__).resolve().parent
contract = json.loads((base / "api_contract.json").read_text(encoding="utf-8"))
endpoints = contract["endpoints"]
expected = {("GET", "/health"), ("GET", "/runs"), ("GET", "/runs/{run_id}"), ("POST", "/run")}
actual = {(item["method"], item["path"]) for item in endpoints}
client = subprocess.run([sys.executable, str(base / "client_demo.py")], cwd=base, capture_output=True, text=True, check=False)
client_report = json.loads((base / "client_demo_report.json").read_text(encoding="utf-8"))
checks = {
    "contract_routes": expected.issubset(actual),
    "schemas": {"RunRequest", "RunResponse", "ErrorResponse"}.issubset(contract.get("schemas", {})),
    "client_returncode": client.returncode == 0,
    "status_201": 201 in client_report.get("status_codes", []),
    "status_404": 404 in client_report.get("status_codes", []),
    "status_400": 400 in client_report.get("status_codes", []),
}
report = {"ok": all(checks.values()), "checks": checks, "client_stdout": client.stdout.strip()}
(base / "round14_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
raise SystemExit(0 if report["ok"] else 1)
'''


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    (LAB / "docs").mkdir(parents=True)
    (LAB / "input").mkdir()


def write_package() -> dict:
    (LAB / "api_contract.json").write_text(json.dumps(API_CONTRACT, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (LAB / "mock_api.py").write_text(MOCK_API, encoding="utf-8")
    client = LAB / "client_demo.py"
    client.write_text(CLIENT_DEMO, encoding="utf-8")
    client.chmod(0o755)
    preflight = LAB / "preflight_check.py"
    preflight.write_text(PREFLIGHT, encoding="utf-8")
    preflight.chmod(0o755)
    (LAB / "input" / "demo.txt").write_text("alpha\nbeta\nalpha\n", encoding="utf-8")
    (LAB / "openapi_preview.json").write_text(
        json.dumps(
            {
                "openapi": "3.1.0-preview",
                "info": {"title": "AI Prep Tool API", "version": "0.1.0"},
                "paths": {item["path"]: {item["method"].lower(): {"summary": item["summary"]}} for item in API_CONTRACT["endpoints"]},
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (LAB / "README.md").write_text(
        "# Round 14 API design package\n\n"
        "This is a standard-library rehearsal for HTTP/API design. It does not install FastAPI or start a long-running server.\n\n"
        "Run `python3 preflight_check.py` to validate the contract and mock API.\n",
        encoding="utf-8",
    )
    proc = subprocess.run([sys.executable, str(preflight)], cwd=LAB, capture_output=True, text=True, check=False)
    summary = json.loads((LAB / "round14_summary.json").read_text(encoding="utf-8"))
    summary.update({"returncode": proc.returncode, "sandbox": str(LAB)})
    return summary


def main() -> None:
    reset_lab()
    summary = write_package()
    if summary["returncode"] != 0 or not summary["ok"]:
        raise RuntimeError(f"Round 14 final API design check failed: {summary}")
    print("Round 14 收口检查")
    print("sandbox:", LAB)
    print("contract:", LAB / "api_contract.json")
    print("mock_api:", LAB / "mock_api.py")
    print("summary:", LAB / "round14_summary.json")
    print("client_status_codes:", [200, 200, 200, 404, 201, 400])
    mark("r14-fin-comp")


if __name__ == "__main__":
    main()
