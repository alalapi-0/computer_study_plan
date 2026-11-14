#!/usr/bin/env python3
"""Freeze explicit public application bytes; never includes learning state or credentials."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ID = "computer-study-plan"
ORIGIN = "https://rr-computer-study-plan.invalid:9419"
BROWSER_SOCKET = "/run/rr-projects/computer-study-plan/browser.sock"
OWNER_SOCKET = "/run/rr-projects/computer-study-plan/owner.sock"
SCENARIOS = ("access-permission", "api-payload-errors", "git-preserve-work",
             "media-wav-quality", "path-cwd-input", "persistent-data-restart",
             "retry-no-duplicates", "script-output")
ASSETS = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/practice_ui.js": ("practice_ui.js", "text/javascript; charset=utf-8"),
    "/practice_ui.css": ("practice_ui.css", "text/css; charset=utf-8"),
    "/rr_feedback.js": ("rr_feedback.js", "text/javascript; charset=utf-8"),
    "/rr_feedback.css": ("rr_feedback.css", "text/css; charset=utf-8"),
    "/vendor/xterm/xterm.js": ("vendor/xterm/xterm.js", "text/javascript; charset=utf-8"),
    "/vendor/xterm/xterm.css": ("vendor/xterm/xterm.css", "text/css; charset=utf-8"),
}
CODE = ("scripts/rr_manifest.py", "scripts/rr_adapter.py", "scripts/rr_feedback_cli.py",
        "scripts/progress_server.py", "scripts/lab_runtime.py", "scripts/progress_lib.py",
        "tests/test_rr_adapter.py", "packaging/computer-study-plan-rr.service.in")
INPUTS = tuple(sorted(set([x[0] for x in ASSETS.values()] + list(CODE) +
    ["content/scenarios/publication.json"] +
    [f"content/scenarios/{s}/{n}" for s in SCENARIOS for n in ("scenario.json", "setup.sh", "check.py")])))

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")

def digest(value):
    return hashlib.sha256(value).hexdigest()

def read_regular(root, relative):
    root = Path(root).absolute()
    path = root / relative
    if path.is_symlink() or any(q.is_symlink() for q in path.parents):
        raise ValueError("source_link_refused")
    info = path.stat()
    if not stat.S_ISREG(info.st_mode):
        raise ValueError("source_not_regular")
    return path.read_bytes()

def catalog_members(root):
    """Fail closed on new runtime inputs until the explicit manifest is updated."""
    catalog = Path(root) / "content/scenarios"
    expected = set(SCENARIOS) | {"publication.json"}
    if catalog.is_symlink() or {p.name for p in catalog.iterdir()} != expected:
        raise ValueError("catalog_members_changed")
    for name in SCENARIOS:
        directory = catalog / name
        if directory.is_symlink() or not directory.is_dir():
            raise ValueError("catalog_members_changed")
        children = list(directory.iterdir())
        if {p.name for p in children} != {"scenario.json", "setup.sh", "check.py"} or any(p.is_symlink() or not p.is_file() for p in children):
            raise ValueError("catalog_members_changed")

def source_inputs(root=ROOT):
    catalog_members(root)
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    def git(*args):
        return subprocess.check_output(["git", "-C", str(root), *args], env=env).decode().strip()
    if Path(git("rev-parse", "--show-toplevel")).resolve() != Path(root).resolve():
        raise ValueError("source_git_root_mismatch")
    commit = git("rev-parse", "HEAD")
    dirty = bool(git("status", "--porcelain=v1", "--untracked-files=all"))
    inputs = {p: digest(read_regular(root, p)) for p in INPUTS}
    source = {"commit": commit, "dirty": dirty,
              "build_id": digest(canonical({"commit": commit, "dirty": dirty, "inputs": inputs}))}
    return source, inputs

class FrozenApplication:
    def __init__(self, root=ROOT):
        self.root = Path(root)
        self.source, self.inputs = source_inputs(self.root)
        self.assets = {path: read_regular(self.root, item[0]) for path, item in ASSETS.items()}
        resources = []
        for path, data in self.assets.items():
            resources.append({"id": "csp-" + digest(path.encode())[:24],
                              "sha256": digest(data), "size": len(data),
                              "content_type": ASSETS[path][1], "mode": "readonly",
                              "preview_version": "source-v1"})
        self.resources = {path: r for path, r in zip(self.assets, resources)}
        self.manifest = {
            "schema": 1, "project_id": PROJECT_ID, "source": self.source, "page_paths": ["/"], "resources": resources,
            "transport": {"websocket": False, "sse": False}, "purpose": "readonly-review",
            "routes": {
                "pages": [{"method": "GET", "path": "/", "resource_id": self.resources["/"]["id"]}],
                "resources": [{"method": "GET", "path": path, "resource_id": self.resources[path]["id"]}
                              for path in self.assets if path != "/"],
                "data": [{"method": "GET", "path": "/__rr/v1/workbench"}],
                "feedback": [
                    {"method": "POST", "path": "/__rr/v1/feedback"},
                    {"method": "GET", "path": "/__rr/v1/feedback/by-request/{client_request_id}"},
                    {"method": "GET", "path": "/__rr/v1/feedback/{feedback_id}"},
                    {"method": "GET", "path": "/__rr/v1/feedback/{feedback_id}/attachments/{attachment_id}"},
                ],
            },
        }
        self.check()

    def check(self):
        source, inputs = source_inputs(self.root)
        if source != self.source or inputs != self.inputs:
            raise ValueError("source_changed")
        if self.root.is_symlink() or self.root.stat().st_uid != os.getuid() or self.root.stat().st_mode & 0o022:
            raise ValueError("project_root_untrusted")
        return True

    def package(self):
        self.check()
        parent = self.root / ".rr-candidates"
        if parent.is_symlink():
            raise ValueError("candidate_link_refused")
        parent.mkdir(mode=0o700, exist_ok=True)
        if parent.stat().st_uid != os.getuid() or parent.stat().st_mode & 0o077:
            raise ValueError("candidate_directory_untrusted")
        target = parent / self.source["build_id"]
        expected = {"manifest.json": canonical(self.manifest),
                    "inputs.json": canonical(self.inputs)}
        for path, data in self.assets.items():
            expected[self.resources[path]["id"]] = data
        if target.exists():
            if target.is_symlink() or set(x.name for x in target.iterdir()) != set(expected):
                raise ValueError("candidate_collision")
            for name, data in expected.items():
                if read_regular(target, name) != data:
                    raise ValueError("candidate_collision")
            return target
        with tempfile.TemporaryDirectory(prefix=".building-", dir=parent) as temp:
            stage = Path(temp) / "package"
            stage.mkdir(mode=0o700)
            for name, data in expected.items():
                fd = os.open(stage / name, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
                with os.fdopen(fd, "wb") as stream:
                    stream.write(data); stream.flush(); os.fsync(stream.fileno())
            self.check()
            os.rename(stage, target)
        return target

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("inspect", "package"))
    args = parser.parse_args()
    app = FrozenApplication()
    if args.action == "package":
        print(app.package())
    else:
        print(json.dumps({"project_id": PROJECT_ID, "origin": ORIGIN,
                          "browser_socket": BROWSER_SOCKET, "source": app.source,
                          "manifest_sha256": digest(canonical(app.manifest)),
                          "inputs": app.inputs}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
