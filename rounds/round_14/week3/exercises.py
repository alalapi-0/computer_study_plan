#!/usr/bin/env python3
"""Round 14 · Week 3: REST route sketch and mock API rehearsal."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round14" / "week3_auto" / "rest_routes"


ROUTES = [
    {"method": "GET", "path": "/health", "description": "service health check", "success_status": 200},
    {"method": "GET", "path": "/runs", "description": "list run records", "success_status": 200},
    {"method": "GET", "path": "/runs/{run_id}", "description": "get one run record", "success_status": 200},
    {"method": "POST", "path": "/run", "description": "submit processing job", "success_status": 201},
]

MOCK_API = '''"""Standard-library mock API for Round 14 route design."""

from __future__ import annotations

import json
from urllib.parse import parse_qs, urlparse


RUNS = [
    {"id": 1, "input_file": "input/demo.txt", "status": "completed", "processed_count": 3},
]


def json_response(status: int, body: dict) -> dict:
    return {"status": status, "body": body}


def handle_request(method: str, path: str, body: dict | None = None) -> dict:
    method = method.upper()
    parsed = urlparse(path)
    clean_path = parsed.path
    query = parse_qs(parsed.query)
    if method == "GET" and clean_path == "/health":
        return json_response(200, {"status": "ok", "version": "0.1.0"})
    if method == "GET" and clean_path == "/runs":
        skip = int(query.get("skip", ["0"])[0])
        limit = int(query.get("limit", ["20"])[0])
        return json_response(200, {"runs": RUNS[skip:skip + limit], "total": len(RUNS), "skip": skip, "limit": limit})
    if method == "GET" and clean_path.startswith("/runs/"):
        run_id = int(clean_path.rsplit("/", 1)[-1])
        for item in RUNS:
            if item["id"] == run_id:
                return json_response(200, item)
        return json_response(404, {"error": "run_not_found", "message": f"Run {run_id} was not found"})
    if method == "POST" and clean_path == "/run":
        payload = body or {}
        if not payload.get("input_file"):
            return json_response(400, {"error": "invalid_request", "message": "input_file is required"})
        return json_response(201, {"run_id": 2, "status": "accepted", "input_file": payload["input_file"]})
    return json_response(404, {"error": "route_not_found", "message": f"{method} {clean_path} is not defined"})


def main() -> None:
    demo = [
        handle_request("GET", "/health"),
        handle_request("GET", "/runs?skip=0&limit=5"),
        handle_request("GET", "/runs/999"),
        handle_request("POST", "/run", {"input_file": "input/demo.txt", "format": "txt"}),
    ]
    print(json.dumps(demo, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
'''

ROUTE_TESTS = '''#!/usr/bin/env python3
"""In-process route tests for the Round 14 mock API."""

import json
from pathlib import Path
from mock_api import handle_request

base = Path(__file__).resolve().parent
cases = [
    ("GET health", handle_request("GET", "/health"), 200),
    ("GET runs", handle_request("GET", "/runs?skip=0&limit=5"), 200),
    ("GET missing run", handle_request("GET", "/runs/999"), 404),
    ("POST run", handle_request("POST", "/run", {"input_file": "input/demo.txt"}), 201),
    ("POST invalid", handle_request("POST", "/run", {}), 400),
]
results = [
    {"case": name, "expected": expected, "actual": response["status"], "ok": response["status"] == expected}
    for name, response, expected in cases
]
report = {"ok": all(item["ok"] for item in results), "case_count": len(results), "results": results}
(base / "route_test_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
raise SystemExit(0 if report["ok"] else 1)
'''


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    LAB.mkdir(parents=True)


def write_routes() -> dict:
    (LAB / "routes.json").write_text(json.dumps(ROUTES, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (LAB / "mock_api.py").write_text(MOCK_API, encoding="utf-8")
    tests = LAB / "route_tests.py"
    tests.write_text(ROUTE_TESTS, encoding="utf-8")
    tests.chmod(0o755)
    proc = subprocess.run([sys.executable, str(tests)], cwd=LAB, capture_output=True, text=True, check=False)
    report = json.loads((LAB / "route_test_report.json").read_text(encoding="utf-8"))
    report.update({"returncode": proc.returncode, "sandbox": str(LAB)})
    (LAB / "next_steps.txt").write_text(
        "在浏览器终端写 mini_router.py，说明 GET health / POST run / 404 的判断，再手动记录 r14-w3-self。\n",
        encoding="utf-8",
    )
    return report


def main() -> None:
    reset_lab()
    report = write_routes()
    if report["returncode"] != 0 or not report["ok"] or report["case_count"] < 5:
        raise RuntimeError(f"Week 3 REST route rehearsal failed: {report}")
    print("Round 14 Week 3 REST 路由草图")
    print("sandbox:", LAB)
    print("route_count:", len(ROUTES))
    print("case_count:", report["case_count"])
    print("report:", LAB / "route_test_report.json")
    mark("r14-w3-ex3")


if __name__ == "__main__":
    main()
