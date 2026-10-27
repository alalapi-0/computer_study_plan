"""Pure-memory fixture for the problem workbench browser tests.

It serves repository UI files and synthetic scenarios only. It deliberately
does not import production lab/progress modules or touch real learning data.
"""
from __future__ import annotations

import json
import re
import threading
import time
from copy import deepcopy
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[2]
ATTEMPT_PATH = re.compile(r"^/api/lab/attempts/([A-Za-z0-9._-]+)$")
ACTION_PATH = re.compile(r"^/api/lab/attempts/([A-Za-z0-9._-]+)/(input|resize|check|stop|reset|view)$")


def _step(command: str) -> dict:
    return {"node": "lab", "shell": "bash", "command": command, "expected": "看到预期结果", "explanation": "用证据缩小原因", "recovery": "先复查当前路径和输出"}


SCENARIOS = [
    {
        "id": "missing-input", "version": "1", "playable": True, "publication_status": "fixture-verified", "title": "换目录后找不到输入文件",
        "summary": "脚本报 No such file，但文件确实存在。", "tags": ["文件", "Shell"],
        "symptom": "在 /workspace/app 运行脚本时，相对路径 data/input.txt 无法打开。",
        "goal": "让脚本从任意当前目录都读取题内输入，并保留输出内容。",
        "constraints": ["不得删除输入", "不得写宿主目录"],
        "environment": {"adapter": "fixture", "nodes": ["lab"], "shell": "bash", "required_tools": ["python3"]},
        "provenance": {"kind": "教学改编", "status": "合成夹具"},
        "hints": [_step("pwd"), _step("python3 app.py")],
        "solution": {"explanation": "以脚本文件位置构造输入路径。", "steps": [_step("sed -n '1,80p' app.py"), _step("printf fix")]},
    },
    {
        "id": "wrong-python", "version": "2", "playable": True, "publication_status": "fixture-verified", "title": "包已安装，程序仍说找不到",
        "summary": "安装包的解释器和运行程序的解释器不同。", "tags": ["依赖", "Python"],
        "symptom": "pip 显示已安装，python 启动仍抛出 ModuleNotFoundError。",
        "goal": "确认解释器身份并让程序使用题内已安装依赖。", "constraints": ["不联网安装", "不更改宿主 Python"],
        "environment": {"adapter": "fixture", "nodes": ["lab"], "shell": "bash", "required_tools": ["python3"]},
        "provenance": {"kind": "教学改编", "status": "合成夹具"},
        "hints": [_step("which python3"), _step("python3 -m pip --version")],
        "solution": {"explanation": "让安装和运行使用同一解释器。", "steps": [_step("python3 -m pip --version")]},
    },
    {
        "id": "awaiting-gate", "version": "1", "playable": False, "publication_status": "awaiting-revalidation", "title": "等待完整复验的草稿题",
        "summary": "题包存在，但尚未通过完整发布门禁。", "tags": ["草稿"], "symptom": "待复验", "goal": "待复验",
        "constraints": ["不得在发布前启动"], "environment": {"adapter": "fixture", "nodes": ["lab"], "shell": "bash", "required_tools": []},
        "provenance": {"kind": "测试草稿"}, "hints": [], "solution": {"explanation": "尚未发布", "steps": []},
    },
]


WAV_SCENARIO = {**deepcopy(SCENARIOS[0]), "id": "media-wav-quality", "title": "WAV 控件合成夹具", "hints": [], "solution": {"steps": [], "explanation": "合成控件测试"}}
WAV_FACTS = {"sha256": "a"*64, "size": 8044, "sample_rate_hz": 16000, "channels": 1, "sample_width_bytes": 2, "frames": 4000, "duration_seconds": .25}


class _Server(ThreadingHTTPServer):
    daemon_threads = True


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    @property
    def fixture(self):
        return self.server.fixture  # type: ignore[attr-defined]

    def log_message(self, _format, *_args):
        return

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _json(self, status: int, value: dict):
        body = json.dumps(value, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _auth(self) -> bool:
        if self.headers.get("X-Lab-Token") == "fixture-token":
            return True
        self._json(HTTPStatus.UNAUTHORIZED, {"ok": False, "error": "缺少夹具令牌"})
        return False

    def _record(self, method: str, path: str, payload=None):
        with self.fixture["lock"]:
            self.fixture["requests"].append((method, path, deepcopy(payload)))

    def _snapshot(self, attempt: dict, cursor: int = 0) -> dict:
        output = attempt["output"][cursor:] if attempt["status"] == "active" else ""
        return {"attempt": deepcopy({key: value for key, value in attempt.items() if key not in {"output", "_revision"}}), "output": output, "cursor": len(attempt["output"]), "revision": attempt["_revision"], "environment": {"adapter": "memory-fixture", "node": "lab", "shell": "bash", "network": "offline"}}

    def send_head(self):
        path = urlparse(self.path).path
        allowed = {"/", "/index.html", "/practice_ui.js", "/practice_ui.css", "/progress.html", "/progress_ui.js", "/progress.css", "/progress_ui.css", "/progress_data.js", "/rounds_data.js", "/vendor/xterm/xterm.js", "/vendor/xterm/xterm.css"}
        notes = re.fullmatch(r"/rounds/(?:round_00|round_01|round_02|round_06)/[A-Za-z0-9_/-]+\.md", path)
        target = ROOT / ("index.html" if path == "/" else path.lstrip("/"))
        if (path not in allowed and not notes) or ".." in target.parts or any(p.is_symlink() for p in [target, *target.parents]) or not target.is_file():
            self.send_error(404); return None
        return super().send_head()

    def do_GET(self):  # noqa: N802
        parsed = urlparse(self.path); path = parsed.path; self._record("GET", path)
        if path == "/api/lab/bootstrap":
            self._json(HTTPStatus.OK, {"token": "fixture-token", "capabilities": {"available": True, "label": "测试隔离环境", "adapter": "memory", "versions": {"fixture": "1"}, "limitations": ["只在内存中模拟"]}, "scenarios": deepcopy(SCENARIOS + ([WAV_SCENARIO] if self.fixture.get("wav_enabled") else []))})
            return
        if path.startswith("/api/lab/") and not self._auth():
            return
        if path.startswith("/api/lab/exports/fixture-"):
            self._json(410, {"error": "fixture_export_stale"}); return
        wav = re.fullmatch(r"/api/lab/attempts/(attempt-[0-9]+)/wav", path)
        if wav:
            with self.fixture["lock"]:
                attempt = self.fixture["attempts"].get(wav[1])
                if not attempt or attempt["status"] != "active" or not attempt.get("checks") or not attempt["checks"][-1].get("passed"):
                    self._json(409, {"error": "fixture_check_required"}); return
                self.fixture["wav_prepares"] += 1
                binding = {"attempt_id": wav[1], "revision": attempt["_revision"], "artifact": deepcopy(WAV_FACTS), "code_version": "internal-code-do-not-display", "permission_version": "internal-permission-do-not-display"}
            self._json(200, binding); return
        if path == "/api/lab/history":
            with self.fixture["lock"]:
                attempts = [{key: deepcopy(value) for key, value in attempt.items() if key not in {"output", "_revision"}} for attempt in reversed(self.fixture["attempts"].values())]
            self._json(HTTPStatus.OK, {"attempts": attempts}); return
        match = ATTEMPT_PATH.match(path)
        if match:
            with self.fixture["lock"]:
                attempt = self.fixture["attempts"].get(match.group(1))
                if not attempt:
                    self._json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "Attempt 不存在"}); return
                delay = self.fixture["poll_delays"].pop(0) if self.fixture["poll_delays"] else 0
            if delay: time.sleep(delay)
            cursor = int(parse_qs(parsed.query).get("cursor", ["0"])[0])
            with self.fixture["lock"]:
                self._json(HTTPStatus.OK, self._snapshot(attempt, cursor))
            return
        super().do_GET()

    def do_POST(self):  # noqa: N802
        path = urlparse(self.path).path
        try:
            length = int(self.headers.get("Content-Length", "0")); payload = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            self._json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "JSON 无效"}); return
        self._record("POST", path, payload)
        if not self._auth(): return
        wav = re.fullmatch(r"/api/lab/attempts/(attempt-[0-9]+)/export-wav", path)
        if wav:
            if set(payload) != {"operation_id", "binding"}:
                self._json(400, {"error": "fixture_payload"}); return
            with self.fixture["lock"]:
                plan = self.fixture["wav_plan"].pop(0) if self.fixture["wav_plan"] else {}
            if plan.get("delay"): time.sleep(plan["delay"])
            if plan.get("status"):
                self._json(plan["status"], {"error": "fixture_stale" if plan["status"] == 409 else "fixture_transient"}); return
            self._json(200, {"receipt_id": "fixture-"+wav[1], "binding": payload["binding"], "download_url": "/api/lab/exports/fixture-"+wav[1]}); return
        action_match = ACTION_PATH.match(path)
        action_name = "start" if path == "/api/lab/start" else (action_match.group(2) if action_match else "")
        expected = {"start": {"scenario_id", "operation_id"}, "input": {"data", "operation_id"}, "resize": {"cols", "rows"}, "check": {"operation_id"}, "stop": {"operation_id"}, "reset": {"operation_id"}, "view": {"kind"}}.get(action_name)
        if expected is None or set(payload) != expected:
            self._json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "夹具请求字段不符"}); return
        if path == "/api/lab/start":
            scenario = next((item for item in SCENARIOS + ([WAV_SCENARIO] if self.fixture.get("wav_enabled") else []) if item["id"] == payload.get("scenario_id")), None)
            if not scenario:
                self._json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "场景不存在"}); return
            with self.fixture["lock"]:
                for old in self.fixture["attempts"].values():
                    if old["status"] == "active": old["status"] = "stopped"
                self.fixture["sequence"] += 1; attempt_id = f"attempt-{self.fixture['sequence']}"
                attempt = {"id": attempt_id, "scenario_id": scenario["id"], "scenario_version": scenario["version"], "status": "active", "hints_viewed": False, "solution_viewed": False, "checks": [], "started_at": "2026-10-13T10:00:00Z", "output": "$ ", "_revision": 1}
                self.fixture["attempts"][attempt_id] = attempt
                snapshot = self._snapshot(attempt)
            self._json(HTTPStatus.OK, snapshot); return
        match = ACTION_PATH.match(path)
        if not match:
            self._json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "未知操作"}); return
        attempt_id, action = match.groups()
        with self.fixture["lock"]:
            attempt = self.fixture["attempts"].get(attempt_id)
            if not attempt:
                self._json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "Attempt 不存在"}); return
            if action == "resize" and attempt["status"] != "active":
                self._json(HTTPStatus.CONFLICT, {"ok": False, "error": "Attempt 已结束"}); return
            if action == "input":
                attempt["output"] += payload.get("data", "")
                if "fix" in payload.get("data", ""): attempt["fixed"] = True
            elif action == "check":
                passed = bool(attempt.get("fixed"))
                attempt["checks"] = [{"id": "goal", "name": "目标状态", "ready": True, "passed": passed, "evidence": "fixture verifier" if passed else "初始故障仍存在"}]
                if passed and attempt["scenario_id"] == "media-wav-quality":
                    attempt["checks"][-1]["artifact_binding"] = deepcopy(WAV_FACTS)
                    attempt["checks"][-1]["fixture_revision"] = attempt["_revision"]
            elif action == "stop": attempt["status"] = "stopped"
            elif action == "reset":
                attempt["status"] = "stopped"
                self.fixture["sequence"] += 1; new_id = f"attempt-{self.fixture['sequence']}"
                attempt = {"id": new_id, "scenario_id": attempt["scenario_id"], "scenario_version": attempt["scenario_version"], "status": "active", "hints_viewed": False, "solution_viewed": False, "checks": [], "started_at": "2026-10-13T10:01:00Z", "output": "$ ", "_revision": 1}
                self.fixture["attempts"][new_id] = attempt
            elif action == "view": attempt[f"{payload.get('kind')}_viewed"] = True
            if action != "reset": attempt["_revision"] += 1
            snapshot = self._snapshot(attempt, len(attempt["output"]) if action in {"input", "resize", "view"} else 0)
            delay = self.fixture["response_delays"].get(action, []).pop(0) if self.fixture["response_delays"].get(action) else 0
        if delay: time.sleep(delay)
        self._json(HTTPStatus.OK, snapshot)


class ProblemFixture:
    def __init__(self):
        self.state = {"lock": threading.RLock(), "requests": [], "attempts": {}, "sequence": 0, "poll_delays": [], "response_delays": {}, "wav_enabled": False, "wav_prepares": 0, "wav_plan": []}
        self.server = None
        self.thread = None

    def __enter__(self):
        self.server = _Server(("127.0.0.1", 0), Handler); self.server.fixture = self.state
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True); self.thread.start()
        return self

    def __exit__(self, *_args):
        self.server.shutdown(); self.server.server_close(); self.thread.join(timeout=2)

    @property
    def url(self):
        return f"http://127.0.0.1:{self.server.server_port}"

    def lose(self, attempt_id: str):
        with self.state["lock"]:
            self.state["attempts"][attempt_id]["status"] = "lost"; self.state["attempts"][attempt_id]["_revision"] += 1
