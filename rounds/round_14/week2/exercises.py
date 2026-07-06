#!/usr/bin/env python3
"""Round 14 · Week 2: JSON request/response contract rehearsal."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round14" / "week2_auto" / "json_contract"


CONTRACT = {
    "service": "ai_prep_tool_api",
    "version": "0.1.0",
    "endpoints": [
        {"method": "GET", "path": "/health", "response": {"status": 200, "body_schema": {"status": "str", "version": "str"}}},
        {"method": "GET", "path": "/runs", "query": {"skip": "int", "limit": "int"}, "response": {"status": 200, "body_schema": {"runs": "list", "total": "int"}}},
        {"method": "GET", "path": "/runs/{run_id}", "response": {"status": 200, "body_schema": {"id": "int", "status": "str"}}},
        {"method": "POST", "path": "/run", "request_body": {"input_file": "str", "format": "str", "dedup": "bool"}, "response": {"status": 201, "body_schema": {"run_id": "int", "status": "str"}}},
    ],
    "error_shape": {"error": "str", "message": "str"},
}

VALIDATE = '''#!/usr/bin/env python3
"""Validate the Round 14 JSON API contract with standard library only."""

import json
from pathlib import Path

base = Path(__file__).resolve().parent
contract = json.loads((base / "api_contract.json").read_text(encoding="utf-8"))
endpoints = contract.get("endpoints", [])
required = {
    "has_health": any(item.get("method") == "GET" and item.get("path") == "/health" for item in endpoints),
    "has_runs": any(item.get("method") == "GET" and item.get("path") == "/runs" for item in endpoints),
    "has_run_detail": any(item.get("method") == "GET" and item.get("path") == "/runs/{run_id}" for item in endpoints),
    "has_submit_run": any(item.get("method") == "POST" and item.get("path") == "/run" for item in endpoints),
    "has_error_shape": set(contract.get("error_shape", {})) == {"error", "message"},
}
samples = sorted((base / "responses").glob("*.json")) + [base / "request_run.json"]
sample_ok = True
for path in samples:
    json.loads(path.read_text(encoding="utf-8"))
report = {"ok": all(required.values()) and sample_ok, "required": required, "sample_count": len(samples)}
(base / "contract_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
raise SystemExit(0 if report["ok"] else 1)
'''


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    (LAB / "responses").mkdir(parents=True)


def write_contract() -> dict:
    (LAB / "api_contract.json").write_text(json.dumps(CONTRACT, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (LAB / "request_run.json").write_text(
        json.dumps({"input_file": "input/demo.txt", "format": "txt", "dedup": True}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    responses = {
        "health_ok.json": {"status": "ok", "version": "0.1.0"},
        "runs_list.json": {"runs": [{"id": 1, "status": "completed"}], "total": 1, "skip": 0, "limit": 20},
        "run_created.json": {"run_id": 2, "status": "accepted", "message": "queued"},
        "run_not_found.json": {"error": "run_not_found", "message": "No run with that id"},
    }
    for name, payload in responses.items():
        (LAB / "responses" / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    validator = LAB / "validate_contract.py"
    validator.write_text(VALIDATE, encoding="utf-8")
    validator.chmod(0o755)
    proc = subprocess.run([sys.executable, str(validator)], cwd=LAB, capture_output=True, text=True, check=False)
    report = json.loads((LAB / "contract_report.json").read_text(encoding="utf-8"))
    report.update({"returncode": proc.returncode, "sandbox": str(LAB)})
    (LAB / "next_steps.txt").write_text(
        "在浏览器终端写 request.json 和 error.json，用 python3 -m json.tool 检查，再点击“记录并完成”保存记录 r14-w2-self。\n",
        encoding="utf-8",
    )
    return report


def main() -> None:
    reset_lab()
    report = write_contract()
    if report["returncode"] != 0 or not report["ok"]:
        raise RuntimeError(f"Week 2 contract rehearsal failed: {report}")
    print("Round 14 Week 2 JSON API 合同")
    print("sandbox:", LAB)
    print("endpoint_count:", len(CONTRACT["endpoints"]))
    print("sample_count:", report["sample_count"])
    print("report:", LAB / "contract_report.json")
    mark("r14-w2-ex2")


if __name__ == "__main__":
    main()
