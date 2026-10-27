#!/usr/bin/env python3
"""Local progress board server: static files + mark-done API."""

from __future__ import annotations

import argparse
import json
import re
import hmac
import secrets
import sys
from http import HTTPStatus
from hub_project_actions import ActionError
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse, unquote

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
LAB_ATTEMPT_API = re.compile(r"^/api/lab/attempts/([A-Za-z0-9_-]+)(?:/(input|resize|check|view|stop|reset))?$")
PUBLIC_FILES = {"index.html", "practice_ui.js", "practice_ui.css", "progress.html",
                "progress_ui.js", "progress_ui.css", "progress_data.js", "rounds_data.js"}



class ProgressRequestHandler(SimpleHTTPRequestHandler):
    repo_root: Path = repo_root()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(self.repo_root), **kwargs)

    def _local_request(self) -> bool:
        port = self.server.server_address[1]
        hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}
        values = self.headers.get_all("Host", [])
        if len(values) != 1 or values[0] not in hosts:
            self.end_json(HTTPStatus.FORBIDDEN, {"ok": False, "error": "invalid_host"})
            return False
        origin = self.headers.get("Origin")
        if (origin is not None and origin != f"http://{values[0]}") or self.headers.get("Sec-Fetch-Site") == "cross-site":
            self.end_json(HTTPStatus.FORBIDDEN, {"ok": False, "error": "cross_origin_denied"})
            return False
        return True

    def _lab_authorized(self) -> bool:
        supplied = self.headers.get("X-Lab-Token", "")
        expected = getattr(self.server, "lab_token", "")
        if not expected or not hmac.compare_digest(supplied.encode("utf-8"), expected.encode("utf-8")):
            self.end_json(HTTPStatus.FORBIDDEN, {"ok": False, "error": "lab_authorization_required"})
            return False
        return True

    def end_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        script_policy = "'self' 'unsafe-inline'" if urlparse(self.path).path == "/progress.html" else "'self'"
        self.send_header("Content-Security-Policy", f"default-src 'self'; script-src {script_policy}; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; object-src 'none'; frame-src 'none'; base-uri 'none'; form-action 'none'")
        super().end_headers()

    def _public_static(self) -> bool:
        raw = unquote(urlparse(self.path).path)
        rel = raw.lstrip("/") or "index.html"
        if "\\" in rel or any(p in {".", ".."} or p.startswith(".") for p in Path(rel).parts):
            return False
        candidate = self.repo_root / rel
        allowed = rel in PUBLIC_FILES or (rel.startswith("vendor/xterm/") and rel.split("/")[-1] in {"xterm.js", "xterm.css"})
        allowed |= rel in {"round_00.md", "round_01.md", "round_02.md", "round_06.md"}
        allowed |= rel.startswith(("rounds/round_00/", "rounds/round_01/", "rounds/round_02/", "rounds/round_06/", "rounds/stage_03_vps_remote_ops/", "plans/linux/", "content/courses/linux-foundations/")) and candidate.suffix in {".md", ".sh"}
        return bool(allowed and candidate.is_file() and candidate.resolve().is_relative_to(self.repo_root.resolve())
                    and not any(p.is_symlink() for p in [candidate, *candidate.parents] if p != self.repo_root.parent))

    def do_HEAD(self) -> None:
        if not self._local_request():
            return
        if not self._public_static():
            self.end_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "not_found"})
            return
        super().do_HEAD()

    def _lab_get(self, path: str) -> None:
        manager = getattr(self.server, "lab_manager", None)
        if manager is None:
            self.end_json(HTTPStatus.SERVICE_UNAVAILABLE, {"ok": False, "error": "lab_runtime_unavailable"})
            return
        if path == "/api/lab/bootstrap":
            self.end_json(HTTPStatus.OK, {"token": self.server.lab_token, "capabilities": manager.capabilities(), **manager.catalog()})
            return
        if not self._lab_authorized():
            return
        try:
            if path.startswith("/api/lab/exports/"):
                if not re.fullmatch(r"/api/lab/exports/[a-f0-9]{64}", path) or urlparse(self.path).query:
                    raise ActionError("invalid_export_request", 400)
                data = manager.download_wav(path.rsplit("/", 1)[1])
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "audio/wav")
                self.send_header("Content-Disposition", 'attachment; filename="tone.wav"')
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers(); self.wfile.write(data)
                return
            elif path == "/api/lab/locate":
                query = parse_qs(urlparse(self.path).query, keep_blank_values=True)
                if set(query) not in ({"scenario"}, {"scenario", "attempt"}) or any(len(v) != 1 for v in query.values()):
                    raise ActionError("invalid_location", 400)
                result = manager.locate(query["scenario"][0], query.get("attempt", [None])[0])
            elif re.fullmatch(r"/api/lab/attempts/[a-f0-9]{32}/wav", path):
                if urlparse(self.path).query: raise ActionError("invalid_artifact_request", 400)
                result = manager.prepare_wav(path.split("/")[4])
            elif path == "/api/lab/history":
                result = manager.history()
            else:
                match = LAB_ATTEMPT_API.fullmatch(path)
                query = parse_qs(urlparse(self.path).query)
                if not match or match.group(2) or set(query) - {"cursor"} or len(query.get("cursor", ["0"])) != 1:
                    raise ValueError("invalid_lab_request")
                cursor = int(query.get("cursor", ["0"])[0])
                result = manager.snapshot(match.group(1), cursor=cursor)
            self.end_json(HTTPStatus.OK, result)
        except ActionError as exc:
            self.end_json(exc.status, {"ok": False, "error": str(exc)})
        except (ValueError, KeyError) as exc:
            self.end_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(exc)})
        except RuntimeError as exc:
            self.end_json(HTTPStatus.CONFLICT, {"ok": False, "error": str(exc)})

    def _lab_post(self, path: str, payload: dict) -> None:
        if not self._lab_authorized():
            return
        manager = getattr(self.server, "lab_manager", None)
        if manager is None:
            self.end_json(HTTPStatus.SERVICE_UNAVAILABLE, {"ok": False, "error": "lab_runtime_unavailable"})
            return
        try:
            if re.fullmatch(r"/api/lab/attempts/[a-f0-9]{32}/export-wav", path):
                if set(payload) != {"operation_id", "binding"} or urlparse(self.path).query:
                    raise ActionError("invalid_export_payload", 400)
                result = manager.export_wav(path.split("/")[4], payload["operation_id"], payload["binding"])
            elif path == "/api/lab/start":
                if set(payload) != {"scenario_id", "operation_id"}:
                    raise ValueError("invalid_lab_payload")
                result = manager.start(payload["scenario_id"], payload["operation_id"])
            else:
                match = LAB_ATTEMPT_API.fullmatch(path)
                if not match or not match.group(2):
                    raise ValueError("invalid_lab_request")
                attempt, action = match.groups()
                expected = {"input": {"data", "operation_id"}, "resize": {"cols", "rows"},
                            "view": {"kind"}}.get(action, {"operation_id"})
                if set(payload) != expected:
                    raise ValueError("invalid_lab_payload")
                if action == "input":
                    result = manager.input(attempt, payload["data"], payload["operation_id"])
                elif action == "resize":
                    result = manager.resize(attempt, payload["cols"], payload["rows"])
                elif action == "view":
                    result = manager.view(attempt, payload["kind"])
                else:
                    result = getattr(manager, action)(attempt, payload["operation_id"])
            self.end_json(HTTPStatus.OK, result)
        except ActionError as exc:
            self.end_json(exc.status, {"ok": False, "error": str(exc)})
        except (ValueError, KeyError, TypeError) as exc:
            self.end_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(exc)})
        except RuntimeError as exc:
            self.end_json(HTTPStatus.CONFLICT, {"ok": False, "error": str(exc)})

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
        if not self._local_request():
            return
        path = urlparse(self.path).path
        if path.startswith("/api/lab/"):
            self._lab_get(path)
            return
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
        if not self._public_static():
            self.end_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "not_found"})
            return
        super().do_GET()

    def do_POST(self) -> None:
        if not self._local_request():
            return
        if self.headers.get_content_type() != "application/json" or self.headers.get("Transfer-Encoding"):
            self.end_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "json_body_required"})
            return
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

        if path.startswith("/api/lab/"):
            self._lab_post(path, payload)
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
    import signal
    parser = argparse.ArgumentParser(description="Serve the local problem practice workbench and legacy progress")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8777)
    parser.add_argument("--rr", action="store_true", help="Enable the fixed project RR sockets using the installed FD provider")
    args = parser.parse_args()
    if args.host != "127.0.0.1":
        parser.error("local owner workbench must bind to 127.0.0.1")
    root = repo_root()
    from lab_runtime import LabManager
    manager = server = rr = None
    transient_startup_type = ()
    previous = {}
    def stop(_number, _frame):
        raise KeyboardInterrupt
    try:
        for number in (signal.SIGTERM, signal.SIGINT):
            previous[number] = signal.signal(number, stop)
        manager = LabManager(root / "content/scenarios", root / ".lab-runtime")
        server = ThreadingHTTPServer((args.host, args.port), ProgressRequestHandler)
        server.lab_manager = manager
        server.lab_token = secrets.token_urlsafe(32)
        if args.rr:
            from rr_adapter import RunningAdapter, ProviderUnavailable
            transient_startup_type = ProviderUnavailable
            rr = RunningAdapter(manager)
        print(f"Serving {root}")
        print(f"Open: http://{args.host}:{args.port}/")
        print("Problem API: /api/lab/bootstrap | start | attempts/<id>/input/check/reset/stop; legacy: /progress.html")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        return 0
    except Exception as error:
        if not args.rr:
            raise
        if isinstance(error, transient_startup_type):
            print("RR startup waiting for its fixed provider prerequisite.", file=sys.stderr)
            return 75
        print("RR startup refused; project identity, protocol or source is invalid.", file=sys.stderr)
        return 78
    finally:
        # A repeated stop cannot interrupt exact-instance cleanup halfway through.
        for number in previous:
            signal.signal(number, signal.SIG_IGN)
        try:
            try:
                if rr is not None:
                    rr.close()
            finally:
                if server is not None:
                    server.server_close()
        finally:
            try:
                if manager is not None:
                    manager.close()
            finally:
                for number, handler in previous.items():
                    signal.signal(number, handler)


if __name__ == "__main__":
    raise SystemExit(main())
