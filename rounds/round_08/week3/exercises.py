#!/usr/bin/env python3
"""Round 08 · Week 3: API contract rehearsal without starting a server."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round8" / "week3_auto"


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], check=True)


def build_health() -> dict[str, str]:
    return {"status": "ok"}


def build_run_response(request: dict[str, object]) -> dict[str, object]:
    return {
        "status": "accepted",
        "input_file": str(request["input_file"]),
        "format": str(request.get("format", "txt")),
        "dedup": bool(request.get("dedup", False)),
        "next": "write run summary into sqlite",
    }


def build_runs_response(rows: list[dict[str, object]]) -> dict[str, object]:
    return {"runs": rows, "count": len(rows)}


def main() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    LAB.mkdir(parents=True)

    contract_file = LAB / "api_contract.py"
    contract_file.write_text(
        "def health():\n"
        "    return {'status': 'ok'}\n\n"
        "def trigger_run(req):\n"
        "    return {\n"
        "        'status': 'accepted',\n"
        "        'input_file': req['input_file'],\n"
        "        'format': req.get('format', 'txt'),\n"
        "        'dedup': bool(req.get('dedup', False)),\n"
        "    }\n\n"
        "def list_runs(rows):\n"
        "    return {'runs': rows, 'count': len(rows)}\n\n"
        "if __name__ == '__main__':\n"
        "    print('GET /health', health())\n"
        "    print('POST /run', trigger_run({'input_file': 'input/demo.txt', 'dedup': True}))\n"
        "    print('GET /runs', list_runs([]))\n",
        encoding="utf-8",
    )

    demo = {
        "GET /health": build_health(),
        "POST /run": build_run_response({"input_file": "input/demo.txt", "format": "txt", "dedup": True}),
        "GET /runs": build_runs_response([]),
    }
    (LAB / "api_demo_output.json").write_text(json.dumps(demo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (LAB / "fastapi_next_steps.md").write_text(
        "# FastAPI next steps\n\n"
        "- Keep this round dependency-free in Web UI.\n"
        "- Later wrap health/trigger_run/list_runs with FastAPI routes.\n"
        "- Connect trigger_run to the SQLite runs table from Week 2.\n",
        encoding="utf-8",
    )

    print("contract:", contract_file)
    print("health:", demo["GET /health"])
    print("run:", demo["POST /run"])
    print("runs:", demo["GET /runs"])

    mark("r08-w3-ex3")
    print("Week 3 自动练习完成。请继续在 Web UI 点击“记录并完成”保存 r08-w3-self。")


if __name__ == "__main__":
    main()
