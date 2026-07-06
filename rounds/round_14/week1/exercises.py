#!/usr/bin/env python3
"""Round 14 · Week 1: HTTP method and status-code rehearsal."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round14" / "week1_auto" / "http_basics"


METHODS = [
    {"method": "GET", "meaning": "read resource", "safe": True, "idempotent": True, "ai_prep_example": "list runs"},
    {"method": "POST", "meaning": "submit or create", "safe": False, "idempotent": False, "ai_prep_example": "submit a processing job"},
    {"method": "PUT", "meaning": "replace whole resource", "safe": False, "idempotent": True, "ai_prep_example": "replace run metadata"},
    {"method": "PATCH", "meaning": "partially update resource", "safe": False, "idempotent": False, "ai_prep_example": "mark one run as reviewed"},
    {"method": "DELETE", "meaning": "delete resource", "safe": False, "idempotent": True, "ai_prep_example": "delete a draft job"},
]

STATUSES = [
    {"status": 200, "name": "OK", "group": "2xx", "use": "successful read or action"},
    {"status": 201, "name": "Created", "group": "2xx", "use": "new resource created"},
    {"status": 400, "name": "Bad Request", "group": "4xx", "use": "invalid input payload"},
    {"status": 404, "name": "Not Found", "group": "4xx", "use": "run id does not exist"},
    {"status": 500, "name": "Internal Server Error", "group": "5xx", "use": "unexpected server failure"},
]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    LAB.mkdir(parents=True)


def write_report() -> dict:
    examples = [
        {
            "request": {"method": "GET", "path": "/health", "body": None},
            "response": {"status": 200, "body": {"status": "ok", "version": "0.1.0"}},
        },
        {
            "request": {"method": "POST", "path": "/run", "body": {"input_file": "input/demo.txt", "format": "txt"}},
            "response": {"status": 201, "body": {"run_id": 1, "status": "accepted"}},
        },
        {
            "request": {"method": "GET", "path": "/runs/999", "body": None},
            "response": {"status": 404, "body": {"error": "run_not_found"}},
        },
    ]
    (LAB / "method_matrix.json").write_text(json.dumps(METHODS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (LAB / "status_matrix.json").write_text(json.dumps(STATUSES, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (LAB / "request_response_examples.json").write_text(json.dumps(examples, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = {
        "method_count": len(METHODS),
        "status_count": len(STATUSES),
        "has_get": any(item["method"] == "GET" and item["safe"] for item in METHODS),
        "has_post": any(item["method"] == "POST" and not item["safe"] for item in METHODS),
        "has_404": any(item["status"] == 404 for item in STATUSES),
        "example_count": len(examples),
        "next_step": "Use the browser terminal to write method_quiz.txt, then manually mark r14-w1-self.",
    }
    (LAB / "http_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (LAB / "next_steps.txt").write_text(
        "自己在浏览器终端写 method_quiz.txt，解释 GET/POST/404/500，再点击“记录并完成”保存记录 r14-w1-self。\n",
        encoding="utf-8",
    )
    return report


def main() -> None:
    reset_lab()
    report = write_report()
    if not (report["has_get"] and report["has_post"] and report["has_404"] and report["example_count"] >= 3):
        raise RuntimeError(f"Week 1 HTTP rehearsal failed: {report}")
    print("Round 14 Week 1 HTTP 方法与状态码")
    print("sandbox:", LAB)
    print("method_count:", report["method_count"])
    print("status_count:", report["status_count"])
    print("report:", LAB / "http_report.json")
    mark("r14-w1-ex1")


if __name__ == "__main__":
    main()
