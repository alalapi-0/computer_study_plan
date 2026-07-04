#!/usr/bin/env python3
"""Local progress board server: static files + mark-done API."""

from __future__ import annotations

import argparse
import json
import re
import sys
from http import HTTPStatus
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from progress_lib import (
    create_progress_save,
    events_by_task,
    list_progress_saves,
    list_status,
    load_action_events,
    load_progress,
    load_progress_save,
    mark_task,
    repo_root,
    run_task_script,
    run_terminal_command,
    sync_progress_data_js,
    terminal_state,
)

TASK_API = re.compile(r"^/api/tasks/([^/]+)/(done|undo)$")
TASK_RUN_API = re.compile(r"^/api/tasks/([^/]+)/run$")
SAVE_LOAD_API = re.compile(r"^/api/saves/([A-Za-z0-9._-]+)/load$")


class ProgressRequestHandler(SimpleHTTPRequestHandler):
    repo_root: Path = repo_root()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(self.repo_root), **kwargs)

    def log_message(self, fmt: str, *args) -> None:
        if self.path.startswith("/api/"):
            sys.stderr.write("[api] " + (fmt % args) + "\n")
        else:
            super().log_message(fmt, *args)

    def end_json(self, status: HTTPStatus, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/progress":
            self.end_json(HTTPStatus.OK, list_status(self.repo_root))
            return
        if path == "/api/events":
            events = load_action_events(self.repo_root)
            self.end_json(
                HTTPStatus.OK,
                {
                    "version": 1,
                    "events": events,
                    "by_task": events_by_task(events),
                },
            )
            return
        if path == "/api/feedback":
            fb_path = self.repo_root / "records/feedback/task_feedback.json"
            if fb_path.exists():
                payload = json.loads(fb_path.read_text(encoding="utf-8"))
            else:
                payload = {"version": 1, "feedback": {}}
            self.end_json(HTTPStatus.OK, payload)
            return
        if path == "/api/saves":
            self.end_json(
                HTTPStatus.OK,
                {
                    "version": 1,
                    "saves": list_progress_saves(self.repo_root),
                },
            )
            return
        if path == "/api/terminal":
            query = parse_qs(urlparse(self.path).query)
            cwd_value = query.get("cwd", [""])[0]
            try:
                self.end_json(HTTPStatus.OK, {"ok": True, "terminal": terminal_state(cwd_value)})
            except ValueError as exc:
                self.end_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(exc)})
            return
        if path == "/api/health":
            self.end_json(HTTPStatus.OK, {"ok": True, "service": "progress_server"})
            return
        super().do_GET()

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        payload = {}
        length = int(self.headers.get("Content-Length") or 0)
        if length:
            try:
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
            except json.JSONDecodeError:
                self.end_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "invalid_json"})
                return

        if path == "/api/sync":
            data = load_progress(self.repo_root)
            sync_progress_data_js(data, self.repo_root)
            self.end_json(HTTPStatus.OK, {"ok": True, "tasks": len(data.get("tasks", {}))})
            return
        if path == "/api/saves":
            result = create_progress_save(
                root=self.repo_root,
                label=str(payload.get("label", ""))[:120],
                personal=payload.get("personal") if isinstance(payload.get("personal"), dict) else {},
                reason="manual",
            )
            self.end_json(
                HTTPStatus.OK,
                {
                    "ok": True,
                    "save": result,
                    "saves": list_progress_saves(self.repo_root),
                },
            )
            return

        if path == "/api/terminal/run":
            try:
                result = run_terminal_command(
                    command=str(payload.get("command", ""))[:500],
                    cwd=str(payload.get("cwd", ""))[:500],
                    root=self.repo_root,
                    task_id=str(payload.get("task_id", ""))[:120],
                )
                self.end_json(HTTPStatus.OK, {"ok": True, "terminal": result})
            except ValueError as exc:
                self.end_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(exc)})
            except Exception as exc:  # pragma: no cover - safety net for local server
                self.end_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"ok": False, "error": str(exc)})
            return

        save_match = SAVE_LOAD_API.match(path)
        if save_match:
            try:
                result = load_progress_save(
                    save_match.group(1),
                    root=self.repo_root,
                    personal=payload.get("personal") if isinstance(payload.get("personal"), dict) else {},
                )
                self.end_json(
                    HTTPStatus.OK,
                    {
                        "ok": True,
                        "loaded": result,
                        "tasks": result.get("tasks", {}),
                        "lanes": result.get("lanes", {}),
                        "feedback": result.get("feedback", {}),
                        "saves": list_progress_saves(self.repo_root),
                    },
                )
            except FileNotFoundError:
                self.end_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "save_not_found"})
            except ValueError as exc:
                self.end_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(exc)})
            return

        run_match = TASK_RUN_API.match(path)
        if run_match:
            try:
                execution = run_task_script(run_match.group(1), root=self.repo_root)
                self.end_json(
                    HTTPStatus.OK,
                    {
                        "ok": True,
                        "execution": execution,
                        "tasks": execution.get("tasks", {}),
                        "lanes": execution.get("lanes", {}),
                        "feedback": execution.get("feedback", {}),
                    },
                )
            except KeyError:
                self.end_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": f"unknown task: {run_match.group(1)}"})
            except FileNotFoundError:
                self.end_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "script_not_found"})
            except ValueError as exc:
                self.end_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(exc)})
            except Exception as exc:  # pragma: no cover - safety net for local server
                self.end_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"ok": False, "error": str(exc)})
            return

        match = TASK_API.match(path)
        if not match:
            self.end_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "not_found"})
            return

        task_id = match.group(1)
        action = match.group(2)
        try:
            result = mark_task(
                task_id,
                undo=(action == "undo"),
                root=self.repo_root,
                note=str(payload.get("note", ""))[:500],
                evidence_path=str(payload.get("evidence_path", ""))[:500],
            )
            self.end_json(HTTPStatus.OK, result)
        except KeyError:
            self.end_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": f"unknown task: {task_id}"})
        except Exception as exc:  # pragma: no cover - safety net for local server
            self.end_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"ok": False, "error": str(exc)})


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve progress.html with write API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8777)
    args = parser.parse_args()

    root = repo_root()
    data = load_progress(root)
    sync_progress_data_js(data, root)

    server = ThreadingHTTPServer((args.host, args.port), ProgressRequestHandler)
    url = f"http://{args.host}:{args.port}/progress.html"
    print(f"Serving {root}")
    print(f"Open: {url}")
    print("API: POST /api/tasks/<id>/done | /undo | /run ; POST /api/terminal/run ; GET /api/progress")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
