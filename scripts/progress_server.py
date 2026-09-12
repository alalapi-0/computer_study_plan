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
    RunInProgressError,
    RunOutcomeUncertainError,
    create_progress_save,
    events_by_task,
    list_progress_saves,
    list_status,
    load_action_events,
    load_progress,
    load_progress_save,
    mark_task,
    progress_write_lock,
    read_feedback_payload,
    recover_pending_operations,
    repo_root,
    run_task_script,
    run_terminal_command,
    sync_progress_state,
    terminal_state,
)

TASK_ID_PATTERN = r"[A-Za-z0-9._-]+"
TASK_API = re.compile(rf"^/api/tasks/({TASK_ID_PATTERN})/(done|undo)$")
TASK_RUN_API = re.compile(rf"^/api/tasks/({TASK_ID_PATTERN})/run$")
SAVE_LOAD_API = re.compile(r"^/api/saves/([A-Za-z0-9._-]+)/load$")
MAX_JSON_BODY_BYTES = 16 * 1024


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
            with progress_write_lock(self.repo_root):
                recover_pending_operations(self.repo_root)
                payload = list_status(self.repo_root)
            self.end_json(HTTPStatus.OK, payload)
            return
        if path == "/progress.json":
            with progress_write_lock(self.repo_root):
                recover_pending_operations(self.repo_root)
                payload = load_progress(self.repo_root)
            self.end_json(HTTPStatus.OK, payload)
            return
        if path == "/api/events":
            with progress_write_lock(self.repo_root):
                recover_pending_operations(self.repo_root)
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
            with progress_write_lock(self.repo_root):
                recover_pending_operations(self.repo_root)
                payload = read_feedback_payload(self.repo_root)
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
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            self.end_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "invalid_content_length"})
            return
        if length < 0:
            self.end_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "invalid_content_length"})
            return
        if length > MAX_JSON_BODY_BYTES:
            self.close_connection = True
            self.end_json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"ok": False, "error": "payload_too_large"})
            return
        if length:
            try:
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                self.end_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "invalid_json"})
                return
        if not isinstance(payload, dict):
            self.end_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "invalid_payload"})
            return

        if path == "/api/sync":
            data = sync_progress_state(self.repo_root)
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
                        "revision": result.get("revision", 0),
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
            if set(payload) != {"operation_id"}:
                self.end_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "invalid_run_payload"})
                return
            operation_id = payload.get("operation_id")
            if not isinstance(operation_id, str):
                self.end_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "invalid_operation_id_type"})
                return
            if not operation_id:
                self.end_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "missing_operation_id"})
                return
            try:
                result = run_task_script(
                    run_match.group(1),
                    root=self.repo_root,
                    operation_id=operation_id,
                )
                self.end_json(HTTPStatus.OK, result)
            except KeyError:
                self.end_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": f"unknown task: {run_match.group(1)}"})
            except FileNotFoundError:
                self.end_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "script_not_found"})
            except RunInProgressError as exc:
                self.end_json(HTTPStatus.CONFLICT, {"ok": False, "error": str(exc)})
            except RunOutcomeUncertainError as exc:
                self.end_json(HTTPStatus.CONFLICT, {"ok": False, "error": str(exc)})
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
        operation_id = payload.get("operation_id", "")
        if not isinstance(operation_id, str):
            self.end_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "invalid_operation_id_type"})
            return
        if not operation_id:
            self.end_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "missing_operation_id"})
            return
        note = payload.get("note", "")
        evidence_path = payload.get("evidence_path", "")
        if not isinstance(note, str) or not isinstance(evidence_path, str):
            self.end_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "invalid_task_action_text"})
            return
        try:
            result = mark_task(
                task_id,
                undo=(action == "undo"),
                root=self.repo_root,
                note=note,
                evidence_path=evidence_path,
                operation_id=operation_id,
            )
            self.end_json(HTTPStatus.OK, result)
        except KeyError:
            self.end_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": f"unknown task: {task_id}"})
        except ValueError as exc:
            self.end_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(exc)})
        except Exception as exc:  # pragma: no cover - safety net for local server
            self.end_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"ok": False, "error": str(exc)})


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve progress.html with write API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8777)
    args = parser.parse_args()

    root = repo_root()
    sync_progress_state(root)

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
