#!/usr/bin/env python3
"""Local learning server: static files + progress API for progress.html.

Default: http://127.0.0.1:8000/progress.html

PW-0 / PW-1 / PW-2 from docs/PROGRESS_WEB_LEARNING_ROADMAP.md
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import re
import sys
from http import HTTPStatus
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

sys.path.insert(0, str(SCRIPT_DIR))
from content_paths import markdown_to_html, resolve_content_path  # noqa: E402
from exercise_guide import build_guide, run_exercise  # noqa: E402
from progress_store import load_progress, set_task_done  # noqa: E402

TASK_API_RE = re.compile(r"^/api/tasks/([^/]+)/(done|undo)$")


class LearnHTTPRequestHandler(SimpleHTTPRequestHandler):
    server_version = "LearnServer/1.0"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(REPO_ROOT), **kwargs)

    def log_message(self, format: str, *args: Any) -> None:
        if args and str(args[0]).startswith("GET /api/"):
            return
        super().log_message(format, *args)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/health":
            self._json_response(
                HTTPStatus.OK,
                {
                    "ok": True,
                    "service": "learn_server",
                    "repo_root": str(REPO_ROOT),
                    "features": [
                        "progress_read",
                        "task_mark",
                        "content_read",
                        "exercise_guide",
                        "exercise_run",
                    ],
                },
            )
            return

        if path == "/api/progress":
            self._json_response(HTTPStatus.OK, load_progress(REPO_ROOT))
            return

        if path == "/api/content":
            params = parse_qs(parsed.query)
            rel = params.get("path", [""])[0]
            full = resolve_content_path(REPO_ROOT, rel)
            if not full:
                self._json_response(
                    HTTPStatus.BAD_REQUEST,
                    {"ok": False, "error": "invalid or missing path"},
                )
                return
            text = full.read_text(encoding="utf-8")
            fmt = params.get("format", ["json"])[0]
            if fmt == "html":
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                html = (
                    "<!DOCTYPE html><html><head><meta charset='utf-8'>"
                    "<title>" + rel + "</title></head><body>"
                    + markdown_to_html(text)
                    + "</body></html>"
                )
                self.wfile.write(html.encode("utf-8"))
                return
            self._json_response(
                HTTPStatus.OK,
                {
                    "ok": True,
                    "path": rel,
                    "markdown": text,
                    "html": markdown_to_html(text),
                },
            )
            return

        if path == "/api/exercise/guide":
            params = parse_qs(parsed.query)
            rel = params.get("path", [""])[0]
            try:
                guide = build_guide(REPO_ROOT, rel)
                self._json_response(HTTPStatus.OK, guide)
            except ValueError as exc:
                self._json_response(
                    HTTPStatus.BAD_REQUEST,
                    {"ok": False, "error": str(exc)},
                )
            return

        if path.startswith("/api/"):
            self._json_response(HTTPStatus.NOT_FOUND, {"ok": False, "error": "not found"})
            return

        super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/exercise/run":
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length else b"{}"
            try:
                body = json.loads(raw.decode("utf-8") or "{}")
            except json.JSONDecodeError:
                body = {}
            rel = body.get("path", "")
            try:
                result = run_exercise(REPO_ROOT, rel)
                # Shell/Python 脚本可能已调用 mark_done；刷新进度供前端同步
                if result.get("ok"):
                    result["progress"] = load_progress(REPO_ROOT)
                self._json_response(HTTPStatus.OK, result)
            except ValueError as exc:
                self._json_response(
                    HTTPStatus.BAD_REQUEST,
                    {"ok": False, "error": str(exc)},
                )
            return

        match = TASK_API_RE.match(parsed.path)
        if not match:
            self._json_response(HTTPStatus.NOT_FOUND, {"ok": False, "error": "not found"})
            return

        task_id = match.group(1)
        action = match.group(2)
        try:
            result = set_task_done(task_id, undo=action == "undo", root=REPO_ROOT)
            self._json_response(HTTPStatus.OK, result)
        except KeyError:
            self._json_response(
                HTTPStatus.BAD_REQUEST,
                {"ok": False, "error": f"unknown task_id: {task_id}"},
            )

    def _json_response(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> int:
    parser = argparse.ArgumentParser(description="Local learning server for progress.html")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host (default 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Bind port (default 8000)")
    args = parser.parse_args()

    if args.host not in ("127.0.0.1", "localhost"):
        print("⚠️  learn_server 仅建议在 127.0.0.1 使用（单用户本地）", file=sys.stderr)

    if not (REPO_ROOT / "progress.json").is_file():
        print(f"❌ 未找到 progress.json：{REPO_ROOT}", file=sys.stderr)
        return 1

    mimetypes.add_type("application/javascript", ".js")
    server = ThreadingHTTPServer((args.host, args.port), LearnHTTPRequestHandler)
    url = f"http://{args.host}:{args.port}/progress.html"
    print(f"Learn server at {url}")
    print(
        "API: /api/health /api/progress /api/tasks/<id>/done|undo "
        "/api/content?path=... /api/exercise/guide?path=... POST /api/exercise/run"
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
