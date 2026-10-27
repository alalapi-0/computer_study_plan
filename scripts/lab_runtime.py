"""Rootless, local problem-lab runtime.

The module deliberately has no host-shell fallback.  A lab is either running in
the probed Bubblewrap boundary or it is unavailable.
"""

from __future__ import annotations

import codecs
import copy
import datetime as dt
import fcntl
import hashlib
import json
import os
import pty
import queue
import re
import resource
import shutil
import signal
import select
import stat
import struct
import subprocess
import termios
import threading
import time
import uuid
from pathlib import Path
from typing import Any


_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,79}$")
_OP_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_OUTPUT_LIMIT = 512 * 1024
_INPUT_LIMIT = 12 * 1024
_LIFETIME_SECONDS = 30 * 60
_SETUP_TIMEOUT = 20
_CHECK_TIMEOUT = 15
_WORKSPACE_BYTES = 64 * 1024 * 1024
_WORKSPACE_ENTRIES = 10_000


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds")


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _fingerprint(value: Any) -> str:
    return _digest(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())


def _safe_root(path: Path, *, create: bool) -> Path:
    path = path.expanduser().absolute()
    chain = list(reversed((path,) + tuple(path.parents)))
    for component in chain:
        if component.is_symlink():
            raise ValueError("runtime root path may not contain symbolic links")
    if create:
        path.mkdir(parents=True, exist_ok=True, mode=0o700)
    if not path.is_dir() or path.is_symlink() or path.resolve() != path:
        raise ValueError("runtime root must be a real directory without symbolic links")
    return path


def _atomic_json(path: Path, value: Any) -> None:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode() + b"\n"
    temp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        try:
            temp.unlink()
        except FileNotFoundError:
            pass


if __package__:
    from . import hub_project_actions as project_actions
else:
    import hub_project_actions as project_actions


RUNTIME_CODE_VERSION = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


class LabManager:
    """Own one isolated interactive lab and a durable attempt history."""

    def __init__(self, catalog_root: Path, state_root: Path, validation_mode: bool = False):
        self._catalog_root = _safe_root(Path(catalog_root), create=False)
        self._state_root = _safe_root(Path(state_root), create=True)
        self._validation_mode = bool(validation_mode)
        self._lock_fd = os.open(self._state_root / ".manager.lock", os.O_RDWR | os.O_CREAT | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0), 0o600)
        try:
            fcntl.flock(self._lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            os.close(self._lock_fd)
            raise RuntimeError("another lab manager already owns this state") from exc

        try:
            self._mutex = threading.RLock()
            self._closed = False
            self._processes: dict[str, subprocess.Popen[bytes]] = {}
            self._masters: dict[str, int] = {}
            self._catalog_data, self._packages = self._load_catalog()
            self._state_file = self._state_root / "attempts.json"
            self._state = self._load_state()
            self._validate_state()
            changed = False
            for attempt in self._state["attempts"]:
                if attempt.get("status") == "active":
                    self._cleanup_workspace(attempt)
                    attempt["status"] = "lost"
                    attempt["ended_at"] = _now()
                    attempt["end_reason"] = "manager_restart"
                    changed = True
            if changed:
                self._save()
            self._capability = self._probe_capability()
            self._apply_publication()
            self._launch_queue: queue.Queue[Any] = queue.Queue()
            self._launcher = threading.Thread(target=self._launcher_loop, name="lab-runtime-launcher", daemon=True)
            self._launcher.start()
            self._monitor = threading.Thread(target=self._monitor_loop, name="lab-runtime-monitor", daemon=True)
            self._monitor.start()
        except Exception:
            if hasattr(self, "_launch_queue"):
                self._launch_queue.put(None)
                self._launcher.join(timeout=2)
            fcntl.flock(self._lock_fd, fcntl.LOCK_UN)
            os.close(self._lock_fd)
            raise

    # ---------- public API ----------

    def catalog(self) -> dict[str, Any]:
        return {"scenarios": copy.deepcopy(self._catalog_data)}

    def capabilities(self) -> dict[str, Any]:
        return copy.deepcopy(self._capability)

    def start(self, scenario_id: str, operation_id: str) -> dict[str, Any]:
        with self._mutex:
            self._ensure_open()
            scenario = self._scenario(scenario_id)
            if not scenario.get("playable", False) and not self._validation_mode:
                raise RuntimeError("scenario is not admitted by the current publication receipt")
            replay = self._operation(operation_id, {"action": "start", "scenario_id": scenario_id})
            if replay:
                return self.snapshot(replay["attempt_id"])
            if not self._capability["available"]:
                raise RuntimeError("isolated lab runtime is unavailable")
            for previous in self._state["attempts"]:
                if previous["status"] == "active":
                    self._stop_internal(previous, "replaced")

            attempt_id = uuid.uuid4().hex
            attempt_root = self._state_root / "attempts" / attempt_id
            workspace = attempt_root / "workspace"
            workspace.mkdir(parents=True, mode=0o700)
            package = self._packages[scenario_id]
            self._assert_package_hash(scenario, package)
            attempt = {
                "id": attempt_id,
                "scenario_id": scenario_id,
                "scenario_version": scenario["version"],
                "scenario_hash": scenario["content_hash"],
                "status": "active",
                "started_at": _now(),
                "ended_at": None,
                "end_reason": None,
                "hints_viewed": False,
                "solution_viewed": False,
                "view_events": [],
                "checks": [],
                "inputs": [],
                "tool_versions": copy.deepcopy(self._capability["versions"]),
                "output": "",
                "output_base": 0,
                "output_truncated": False,
                "workspace_name": attempt_id,
            }
            self._state["attempts"].append(attempt)
            self._remember_operation(operation_id, {"action": "start", "scenario_id": scenario_id}, attempt_id)
            self._save()
            try:
                self._run_trusted(package, workspace, ["/bin/bash", "/package/setup.sh"], _SETUP_TIMEOUT)
                ready = self._run_checker(package, workspace, "ready")
                if ready.get("ready") is not True:
                    raise RuntimeError("scenario readiness check failed")
                self._launch(attempt, workspace)
            except Exception:
                attempt["status"] = "stopped"
                attempt["ended_at"] = _now()
                attempt["end_reason"] = "infrastructure_error"
                self._cleanup_workspace(attempt)
                self._save()
                raise
            return self.snapshot(attempt_id)

    def snapshot(self, attempt_id: str, cursor: int = 0) -> dict[str, Any]:
        with self._mutex:
            self._ensure_open()
            attempt = self._attempt(attempt_id)
            self._refresh(attempt)
            if not isinstance(cursor, int) or cursor < 0:
                raise ValueError("cursor must be a non-negative integer")
            base = int(attempt.get("output_base", 0))
            text = attempt.get("output", "")
            end = base + len(text)
            start = max(cursor, base)
            output = text[start - base :] if start <= end else ""
            public_attempt = {k: copy.deepcopy(v) for k, v in attempt.items() if k not in {"output", "output_base", "workspace_name"}}
            public_attempt["output_truncated"] = bool(attempt.get("output_truncated")) or cursor < base
            return {
                "attempt": public_attempt,
                "output": output,
                "cursor": end,
                "environment": self._environment(attempt),
                "revision": self._state["revision"],
            }

    def input(self, attempt_id: str, data: str, operation_id: str) -> dict[str, Any]:
        if not isinstance(data, str):
            raise ValueError("input data must be text")
        raw = data.encode("utf-8")
        if not raw or len(raw) > _INPUT_LIMIT:
            raise ValueError("input data must be between 1 byte and 12 KiB")
        with self._mutex:
            attempt = self._active_attempt(attempt_id)
            payload = {"action": "input", "attempt_id": attempt_id, "data_hash": _digest(raw)}
            if self._operation(operation_id, payload):
                return self.snapshot(attempt_id)
            # Persist the replay guard before the non-repeatable PTY write.
            self._remember_operation(operation_id, payload, attempt_id, status="pending")
            input_record = {
                "operation_id": operation_id, "data_hash": payload["data_hash"],
                "bytes": len(raw), "status": "pending_uncertain", "at": _now(),
            }
            attempt["inputs"].append(input_record)
            self._save()
            try:
                view = memoryview(raw)
                delivered = 0
                while delivered < len(view):
                    written = os.write(self._masters[attempt_id], view[delivered:])
                    if written <= 0:
                        raise OSError("PTY write made no progress")
                    delivered += written
            except OSError as exc:
                self._state["operations"][operation_id]["status"] = "pending_uncertain"
                input_record["status"] = "pending_uncertain"
                self._save()
                self._refresh(attempt)
                raise RuntimeError("lab input delivery is uncertain") from exc
            self._state["operations"][operation_id]["status"] = "delivered"
            input_record["status"] = "delivered"
            self._save()
            return self.snapshot(attempt_id)

    def resize(self, attempt_id: str, cols: int, rows: int) -> dict[str, Any]:
        if not isinstance(cols, int) or not isinstance(rows, int) or not (20 <= cols <= 400 and 5 <= rows <= 200):
            raise ValueError("terminal size is outside the supported range")
        with self._mutex:
            self._active_attempt(attempt_id)
            fd = self._masters[attempt_id]
            fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0))
            process = self._processes[attempt_id]
            try:
                os.killpg(process.pid, signal.SIGWINCH)
            except ProcessLookupError:
                pass
            return self.snapshot(attempt_id)

    def execute(self, attempt_id: str, command: str, operation_id: str) -> dict[str, Any]:
        """Run a trusted publication-gate command outside the learner PTY.

        This method exists only for repository-owned scenario validation.  It
        is unavailable to normal product managers and is not a host fallback.
        """
        if not self._validation_mode:
            raise RuntimeError("batch execution is restricted to scenario validation")
        if not isinstance(command, str) or not command or len(command.encode("utf-8")) > _INPUT_LIMIT:
            raise ValueError("validation command is empty or too large")
        with self._mutex:
            attempt = self._active_attempt(attempt_id)
            payload = {"action": "validation_execute", "attempt_id": attempt_id, "command_hash": _digest(command.encode("utf-8"))}
            replay = self._operation(operation_id, payload)
            if replay:
                return copy.deepcopy(replay["result"])
            try:
                result = subprocess.run(
                    self._base_bwrap(self._workspace(attempt), None) + ["/bin/bash", "--noprofile", "--norc", "-c", command],
                    stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    timeout=20, check=False, env={},
                )
            except subprocess.TimeoutExpired as exc:
                raise RuntimeError("validation command timed out") from exc
            if len(result.stdout) + len(result.stderr) > _OUTPUT_LIMIT:
                raise RuntimeError("validation command output exceeded its limit")
            response = {
                "exit_code": result.returncode,
                "stdout": result.stdout.decode("utf-8", errors="replace"),
                "stderr": result.stderr.decode("utf-8", errors="replace"),
            }
            self._remember_operation(operation_id, payload, attempt_id)
            self._state["operations"][operation_id]["result"] = copy.deepcopy(response)
            self._save()
            return response

    def check(self, attempt_id: str, operation_id: str) -> dict[str, Any]:
        with self._mutex:
            attempt = self._active_attempt(attempt_id)
            payload = {"action": "check", "attempt_id": attempt_id, "scenario_id": attempt["scenario_id"]}
            if self._operation(operation_id, payload):
                return self.snapshot(attempt_id)
            package = self._packages[attempt["scenario_id"]]
            self._assert_package_hash(self._scenario(attempt["scenario_id"]), package)
            workspace = self._workspace(attempt)
            record: dict[str, Any] = {"at": _now(), "status": "infra_error", "passed": False, "evidence": [], "details": "checker did not complete"}
            try:
                before_artifact = None
                if attempt["scenario_id"] == project_actions.SCENARIO:
                    try: before_artifact = project_actions.inspect_tone(project_actions.read_tone(workspace))
                    except project_actions.ActionError: pass
                result = self._run_checker(package, workspace, "check")
                if result.get("ready") is not True:
                    raise RuntimeError("checker reported that scenario infrastructure is not ready")
                if not isinstance(result.get("passed"), bool):
                    raise RuntimeError("checker result did not contain a boolean passed field")
                record = {
                    "at": _now(),
                    "status": "passed" if result["passed"] else "failed",
                    "passed": result["passed"],
                    "evidence": self._json_value(result.get("evidence", [])),
                    "details": self._json_value(result.get("details", "")),
                    "operation_id": operation_id,
                }
            except Exception as exc:
                record["details"] = str(exc) if str(exc) else "checker infrastructure error"
                record["operation_id"] = operation_id
            if record["passed"] and attempt["scenario_id"] == project_actions.SCENARIO:
                try:
                    artifact = project_actions.inspect_tone(project_actions.read_tone(workspace))
                    if artifact == before_artifact:
                        record["artifact_binding"] = artifact
                        record["artifact_action_code"] = project_actions.CODE_VERSION
                        record["artifact_runtime_code"] = RUNTIME_CODE_VERSION
                    else:
                        record["artifact_export_error"] = "artifact_changed_during_check"
                except project_actions.ActionError:
                    record["artifact_export_error"] = "artifact_unavailable"
            attempt["checks"].append(record)
            self._remember_operation(operation_id, payload, attempt_id)
            self._save()
            return self.snapshot(attempt_id)

    def locate(self, scenario_id, attempt_id=None):
        """Read-only identity lookup: deliberately no refresh, start or view."""
        with self._mutex:
            self._scenario(scenario_id)
            if attempt_id is not None and self._attempt(attempt_id)["scenario_id"] != scenario_id:
                raise project_actions.ActionError("scenario_attempt_mismatch")
            result = {"url": project_actions.location(scenario_id, attempt_id)}
            if attempt_id is not None:
                attempt = self._attempt(attempt_id)
                result["attempt"] = {k: copy.deepcopy(attempt[k]) for k in ("id", "scenario_id", "scenario_version", "scenario_hash", "status", "hints_viewed", "solution_viewed", "started_at")}
                result["attempt"]["checks"] = [{k: copy.deepcopy(c[k]) for k in ("at", "passed", "status", "artifact_binding") if k in c} for c in attempt["checks"]]
            return result

    def prepare_wav(self, attempt_id):
        """Read-only: no refresh or operation reservation on GET."""
        with self._mutex:
            try: attempt = self._attempt(attempt_id)
            except ValueError as exc: raise project_actions.ActionError("attempt_removed", 410) from exc
            if attempt["status"] != "active": raise project_actions.ActionError("attempt_ended", 410)
            scenario = self._scenario(attempt["scenario_id"])
            self._assert_package_hash(scenario, self._packages[scenario["id"]])
            if (scenario["version"], scenario["content_hash"]) != (attempt["scenario_version"], attempt["scenario_hash"]):
                raise project_actions.ActionError("scenario_version_changed")
            return project_actions.prepare(attempt, self._workspace(attempt), RUNTIME_CODE_VERSION)

    def export_wav(self, attempt_id, operation_id, binding):
        with self._mutex:
            binding_json = project_actions.canonical_export_binding(binding)
            # Only this action normalizes numeric identity; global fingerprints
            # and every other persisted operation retain their original ABI.
            payload = {"action": "export_wav", "attempt_id": attempt_id,
                       "binding": json.loads(binding_json)}
            if not isinstance(operation_id, str) or not _OP_RE.fullmatch(operation_id):
                raise project_actions.ActionError("invalid_operation_id", 400)
            existing = self._state["operations"].get(operation_id)
            if existing and existing["fingerprint"] != _fingerprint(payload):
                raise project_actions.ActionError("operation_id_conflict")
            if existing and "artifact_receipt" in existing:
                prior = existing["artifact_receipt"]["binding"]
                if project_actions.canonical_export_binding(prior) != binding_json:
                    raise project_actions.ActionError("operation_id_conflict")
                if (prior.get("code_version") != project_actions.CODE_VERSION or
                        prior.get("runtime_code_version") != RUNTIME_CODE_VERSION or
                        prior.get("action_version") != project_actions.ACTION_VERSION or
                        prior.get("permission_version") != project_actions.PERMISSION_VERSION):
                    raise project_actions.ActionError("receipt_code_version_changed")
                scenario = self._scenario(prior["scenario_id"])
                self._assert_package_hash(scenario, self._packages[scenario["id"]])
                if (scenario["version"], scenario["content_hash"]) != (prior["scenario_version"], prior["scenario_hash"]):
                    raise project_actions.ActionError("receipt_scenario_version_changed")
                project_actions.read_export(self._state_root, existing["artifact_receipt"])
                return copy.deepcopy(existing["artifact_receipt"])
            current = self.prepare_wav(attempt_id)
            if binding_json != project_actions.canonical_export_binding(current):
                raise project_actions.ActionError("stale_artifact_binding")
            data = project_actions.read_tone(self._workspace(self._attempt(attempt_id)))
            if project_actions.inspect_tone(data) != current["artifact"]:
                raise project_actions.ActionError("artifact_changed_since_check")
            identity = project_actions.receipt_id(operation_id, current)
            if not existing:
                self._remember_operation(operation_id, payload, attempt_id, status="pending")
                self._save()
            project_actions.store_export(self._state_root, identity, data)
            if self.prepare_wav(attempt_id) != current: raise project_actions.ActionError("artifact_changed_during_export")
            receipt = {"receipt_id": identity, "operation_id": operation_id, "binding": current,
                       "download_url": "/api/lab/exports/" + identity, "hearing_accepted": None}
            self._state["operations"][operation_id].update(status="completed", artifact_receipt=receipt)
            self._save()
            return copy.deepcopy(receipt)

    def download_wav(self, identity):
        with self._mutex:
            for operation in self._state["operations"].values():
                receipt = operation.get("artifact_receipt")
                if receipt and receipt["receipt_id"] == identity:
                    attempt = self._attempt(operation["attempt_id"])
                    if attempt["status"] != "active": raise project_actions.ActionError("attempt_ended", 410)
                    if self.prepare_wav(attempt["id"]) != receipt["binding"]:
                        raise project_actions.ActionError("stale_artifact_binding")
                    return project_actions.read_export(self._state_root, receipt)
            raise project_actions.ActionError("unknown_export", 410)

    def view(self, attempt_id: str, kind: str) -> dict[str, Any]:
        if kind not in {"hints", "solution"}:
            raise ValueError("view kind must be hints or solution")
        with self._mutex:
            attempt = self._attempt(attempt_id)
            key = "hints_viewed" if kind == "hints" else "solution_viewed"
            if not attempt[key]:
                attempt[key] = True
                attempt["view_events"].append({"kind": kind, "at": _now()})
                self._save()
            return self.snapshot(attempt_id)

    def stop(self, attempt_id: str, operation_id: str) -> dict[str, Any]:
        with self._mutex:
            attempt = self._attempt(attempt_id)
            payload = {"action": "stop", "attempt_id": attempt_id}
            if not self._operation(operation_id, payload):
                if attempt["status"] == "active":
                    self._stop_internal(attempt, "user_stop")
                self._remember_operation(operation_id, payload, attempt_id)
                self._save()
            return self.snapshot(attempt_id)

    def reset(self, attempt_id: str, operation_id: str) -> dict[str, Any]:
        with self._mutex:
            previous = self._attempt(attempt_id)
            payload = {"action": "reset", "attempt_id": attempt_id, "scenario_id": previous["scenario_id"]}
            replay = self._operation(operation_id, payload)
            if replay:
                return self.snapshot(replay["attempt_id"])
            if previous["status"] == "active":
                self._stop_internal(previous, "reset")
            # Reserve the reset operation with the new start operation.  start()
            # performs all state mutation and preserves the old attempt.
            child_operation = f"reset-start:{operation_id}"
            result = self.start(previous["scenario_id"], child_operation)
            new_id = result["attempt"]["id"]
            self._remember_operation(operation_id, payload, new_id)
            self._save()
            return result

    def history(self) -> dict[str, Any]:
        with self._mutex:
            self._ensure_open()
            for attempt in self._state["attempts"]:
                self._refresh(attempt)
            return {"attempts": [
                {k: copy.deepcopy(v) for k, v in item.items() if k not in {"output", "output_base", "workspace_name"}}
                for item in self._state["attempts"]
            ], "revision": self._state["revision"]}

    def close(self) -> None:
        with self._mutex:
            if self._closed:
                return
            for attempt in self._state["attempts"]:
                if attempt["status"] == "active":
                    self._stop_internal(attempt, "manager_close")
            self._closed = True
            self._launch_queue.put(None)
            self._launcher.join(timeout=2)
            try:
                fcntl.flock(self._lock_fd, fcntl.LOCK_UN)
            finally:
                os.close(self._lock_fd)

    # ---------- catalog and durable state ----------

    def _load_catalog(self) -> tuple[list[dict[str, Any]], dict[str, Path]]:
        scenarios: list[dict[str, Any]] = []
        packages: dict[str, Path] = {}
        required = {"id", "version", "title", "summary", "tags", "symptom", "goal", "constraints", "environment", "provenance", "hints", "solution"}
        for descriptor in sorted(self._catalog_root.glob("*/scenario.json")):
            package = descriptor.parent
            if package.is_symlink() or descriptor.is_symlink():
                raise ValueError("scenario packages may not use symbolic links")
            for child in package.rglob("*"):
                if child.is_symlink():
                    raise ValueError("scenario packages may not use symbolic links")
            try:
                scenario = json.loads(descriptor.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise ValueError("scenario catalog contains invalid JSON") from exc
            if not isinstance(scenario, dict) or not required.issubset(scenario):
                raise ValueError("scenario descriptor is missing required fields")
            scenario_id = scenario.get("id")
            if not isinstance(scenario_id, str) or not _ID_RE.fullmatch(scenario_id) or package.name != scenario_id:
                raise ValueError("scenario id is invalid or does not match its directory")
            if scenario_id in packages or not (package / "setup.sh").is_file() or not (package / "check.py").is_file():
                raise ValueError("scenario package is incomplete or duplicated")
            environment = scenario.get("environment")
            if not isinstance(environment, dict) or not {"adapter", "nodes", "shell", "required_tools"}.issubset(environment):
                raise ValueError("scenario environment is incomplete")
            if environment.get("adapter") != "bwrap-userland" or environment.get("nodes") != ["lab"]:
                raise ValueError("scenario requires an unsupported environment")
            public = copy.deepcopy(scenario)
            public["content_hash"] = self._package_hash(package)
            scenarios.append(public)
            packages[scenario_id] = package
        return scenarios, packages

    @staticmethod
    def _package_hash(package: Path) -> str:
        content_hash = hashlib.sha256()
        for file in sorted(p for p in package.rglob("*") if p.is_file()):
            content_hash.update(file.relative_to(package).as_posix().encode() + b"\0")
            content_hash.update(file.read_bytes())
        return content_hash.hexdigest()

    def _assert_package_hash(self, scenario: dict[str, Any], package: Path) -> None:
        if self._package_hash(package) != scenario["content_hash"]:
            raise RuntimeError("scenario package changed after catalog load")

    def _apply_publication(self) -> None:
        if self._validation_mode:
            for scenario in self._catalog_data:
                scenario["playable"] = True
                scenario["publication_status"] = "validation_mode"
            return
        receipt_path = self._catalog_root / "publication.json"
        receipt: dict[str, Any] | None = None
        status = "publication receipt missing"
        if receipt_path.exists() and not receipt_path.is_symlink():
            try:
                parsed = json.loads(receipt_path.read_text(encoding="utf-8"))
                if (
                    isinstance(parsed, dict) and parsed.get("schema_version") == 1
                    and parsed.get("adapter") == "bwrap-userland"
                    and isinstance(parsed.get("runtime_versions"), dict)
                    and isinstance(parsed.get("scenarios"), dict)
                    and isinstance(parsed.get("gate"), dict)
                    and parsed["gate"].get("cycles", 0) >= 2
                    and parsed["gate"].get("negative") is True
                ):
                    receipt = parsed
                    status = "runtime version mismatch"
                else:
                    status = "publication receipt invalid"
            except (OSError, json.JSONDecodeError):
                status = "publication receipt invalid"
        versions_match = receipt is not None and receipt["runtime_versions"] == self._capability["versions"]
        for scenario in self._catalog_data:
            admitted = receipt["scenarios"].get(scenario["id"]) if versions_match and receipt else None
            playable = bool(
                isinstance(admitted, dict)
                and admitted.get("version") == scenario["version"]
                and admitted.get("content_hash") == scenario["content_hash"]
            )
            scenario["playable"] = playable
            scenario["publication_status"] = "published" if playable else ("package changed or not admitted" if versions_match else status)

    def _load_state(self) -> dict[str, Any]:
        if not self._state_file.exists():
            return {"schema_version": 1, "revision": 0, "attempts": [], "operations": {}}
        if self._state_file.is_symlink():
            raise ValueError("runtime state file may not be a symbolic link")
        try:
            fd = os.open(self._state_file, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
            with os.fdopen(fd, "r", encoding="utf-8") as stream:
                state = json.load(stream)
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError("lab state is unreadable") from exc
        if not isinstance(state, dict) or state.get("schema_version") != 1 or not isinstance(state.get("revision"), int) or state["revision"] < 0 or not isinstance(state.get("attempts"), list) or not isinstance(state.get("operations"), dict):
            raise RuntimeError("lab state has an unsupported shape")
        return state

    def _validate_state(self) -> None:
        valid_statuses = {"active", "stopped", "lost", "expired"}
        seen: set[str] = set()
        for attempt in self._state["attempts"]:
            if not isinstance(attempt, dict):
                raise RuntimeError("lab state contains an invalid attempt")
            attempt_id = attempt.get("id")
            fields = {
                "scenario_id": str, "scenario_version": int, "scenario_hash": str,
                "started_at": str, "hints_viewed": bool, "solution_viewed": bool,
                "view_events": list, "checks": list, "inputs": list, "tool_versions": dict,
                "output": str, "output_base": int, "output_truncated": bool,
            }
            if (
                not isinstance(attempt_id, str) or re.fullmatch(r"[0-9a-f]{32}", attempt_id) is None
                or attempt_id in seen or attempt.get("workspace_name") != attempt_id
                or attempt.get("status") not in valid_statuses
                or not isinstance(attempt.get("scenario_id"), str)
                or _ID_RE.fullmatch(attempt["scenario_id"]) is None
                or any(not isinstance(attempt.get(key), kind) for key, kind in fields.items())
                or attempt.get("output_base", -1) < 0
            ):
                raise RuntimeError("lab state contains an invalid attempt")
            seen.add(attempt_id)
        for operation_id, operation in self._state["operations"].items():
            if (
                not isinstance(operation_id, str) or _OP_RE.fullmatch(operation_id) is None
                or not isinstance(operation, dict) or operation.get("attempt_id") not in seen
                or not isinstance(operation.get("fingerprint"), str)
                or re.fullmatch(r"[0-9a-f]{64}", operation["fingerprint"]) is None
                or operation.get("status", "completed") not in {"pending", "pending_uncertain", "delivered", "completed"}
                or (
                    "result" in operation and (
                        not isinstance(operation["result"], dict)
                        or not isinstance(operation["result"].get("exit_code"), int)
                        or not isinstance(operation["result"].get("stdout"), str)
                        or not isinstance(operation["result"].get("stderr"), str)
                    )
                )
            ):
                raise RuntimeError("lab state contains an invalid operation")

    def _save(self) -> None:
        self._state["revision"] += 1
        _atomic_json(self._state_file, self._state)

    # ---------- isolation ----------

    def _base_bwrap(
        self, workspace: Path, package: Path | None, *, workspace_write: bool = True,
        input_workspace: Path | None = None, verifier_access: bool = False,
    ) -> list[str]:
        self._assert_mount_source(workspace, self._state_root)
        command = [
            "bwrap", "--die-with-parent", "--unshare-all", "--unshare-user", "--disable-userns", "--cap-drop", "ALL",
        ]
        if verifier_access:
            command += ["--cap-add", "CAP_DAC_OVERRIDE"]
        command += [
            "--ro-bind", "/usr", "/usr", "--symlink", "usr/bin", "/bin", "--symlink", "usr/lib", "/lib",
            "--symlink", "usr/lib64", "/lib64", "--symlink", "usr/sbin", "/sbin",
            "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp", "--dir", "/workspace",
            "--bind" if workspace_write else "--ro-bind", str(workspace), "/workspace",
        ]
        if package is not None:
            self._assert_mount_source(package, self._catalog_root)
            command += ["--dir", "/package", "--ro-bind", str(package), "/package"]
        if input_workspace is not None:
            self._assert_mount_source(input_workspace, self._state_root)
            command += ["--dir", "/input", "--ro-bind", str(input_workspace), "/input"]
        command += [
            "--chdir", "/workspace", "--clearenv", "--setenv", "HOME", "/workspace",
            "--setenv", "PATH", "/usr/bin:/bin", "--setenv", "LANG", "C.UTF-8",
            "--setenv", "TERM", "xterm-256color", "--setenv", "PS1", "lab:\\w\\$ ",
            "--hostname", "problem-lab", "--",
            "/usr/bin/prlimit", "--cpu=900", "--as=536870912", "--fsize=16777216",
            f"--nproc={self._nproc_ceiling()}", "--nofile=256", "--",
        ]
        return command

    def _run_trusted(
        self, package: Path, workspace: Path, command: list[str], timeout: int, *,
        workspace_write: bool = True, input_workspace: Path | None = None, verifier_access: bool = False,
    ) -> subprocess.CompletedProcess[bytes]:
        try:
            result = subprocess.run(
                self._base_bwrap(
                    workspace, package, workspace_write=workspace_write,
                    input_workspace=input_workspace, verifier_access=verifier_access,
                ) + command,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
                check=False,
                env={},
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("scenario infrastructure timed out") from exc
        if result.returncode != 0:
            raise RuntimeError("scenario infrastructure command failed")
        if len(result.stdout) > _OUTPUT_LIMIT or len(result.stderr) > _OUTPUT_LIMIT:
            raise RuntimeError("scenario infrastructure output exceeded its limit")
        return result

    def _run_checker(self, package: Path, workspace: Path, mode: str) -> dict[str, Any]:
        verification_root = self._state_root / "verifications" / uuid.uuid4().hex
        verification = verification_root / "workspace"
        verification.mkdir(parents=True, mode=0o700)
        try:
            self._copy_workspace_snapshot(workspace, verification)
            result = self._run_trusted(
                package, verification, ["/usr/bin/python3", "/package/check.py", mode], _CHECK_TIMEOUT,
                workspace_write=True, input_workspace=workspace, verifier_access=True,
            )
            try:
                value = json.loads(result.stdout.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise RuntimeError("checker returned malformed JSON") from exc
        finally:
            if verification_root.exists() and not verification_root.is_symlink():
                shutil.rmtree(verification_root)
        if not isinstance(value, dict):
            raise RuntimeError("checker returned malformed JSON")
        return value

    def _copy_workspace_snapshot(self, source: Path, destination: Path) -> None:
        self._assert_mount_source(source, self._state_root)
        totals = {"entries": 0, "bytes": 0}
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
        root_fd = os.open(source, flags)
        try:
            self._copy_directory_fd(root_fd, destination, totals)
        finally:
            os.close(root_fd)

    def _copy_directory_fd(self, source_fd: int, destination: Path, totals: dict[str, int]) -> None:
        for name in os.listdir(source_fd):
            if name in {".", ".."}:
                continue
            totals["entries"] += 1
            if totals["entries"] > _WORKSPACE_ENTRIES:
                raise RuntimeError("workspace snapshot exceeded its entry limit")
            metadata = os.stat(name, dir_fd=source_fd, follow_symlinks=False)
            target = destination / name
            mode = stat.S_IMODE(metadata.st_mode)
            if stat.S_ISDIR(metadata.st_mode):
                target.mkdir(mode=0o700)
                child_fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0), dir_fd=source_fd)
                try:
                    self._copy_directory_fd(child_fd, target, totals)
                finally:
                    os.close(child_fd)
                os.chmod(target, mode)
            elif stat.S_ISREG(metadata.st_mode):
                totals["bytes"] += metadata.st_size
                if totals["bytes"] > _WORKSPACE_BYTES:
                    raise RuntimeError("workspace snapshot exceeded its byte limit")
                temporarily_readable = False
                try:
                    file_fd = os.open(name, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0), dir_fd=source_fd)
                except PermissionError:
                    # The manager owns this disposable workspace.  Open an
                    # intentionally unreadable learner file through a narrowly
                    # verified, immediately restored mode change so the
                    # independent checker can preserve and inspect the fault.
                    os.chmod(name, mode | stat.S_IRUSR, dir_fd=source_fd, follow_symlinks=False)
                    temporarily_readable = True
                    try:
                        file_fd = os.open(name, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0), dir_fd=source_fd)
                    except Exception:
                        current = os.stat(name, dir_fd=source_fd, follow_symlinks=False)
                        if current.st_ino == metadata.st_ino and stat.S_IMODE(current.st_mode) == (mode | stat.S_IRUSR):
                            os.chmod(name, mode, dir_fd=source_fd, follow_symlinks=False)
                        raise
                try:
                    opened = os.fstat(file_fd)
                    if not stat.S_ISREG(opened.st_mode) or opened.st_ino != metadata.st_ino or opened.st_dev != metadata.st_dev:
                        raise RuntimeError("workspace changed while creating verification snapshot")
                    with os.fdopen(file_fd, "rb", closefd=False) as input_stream, target.open("xb") as output_stream:
                        shutil.copyfileobj(input_stream, output_stream, length=1024 * 1024)
                finally:
                    if temporarily_readable:
                        current = os.fstat(file_fd)
                        if stat.S_IMODE(current.st_mode) == (mode | stat.S_IRUSR):
                            os.fchmod(file_fd, mode)
                    os.close(file_fd)
                os.chmod(target, mode)
            elif stat.S_ISLNK(metadata.st_mode):
                link_target = os.readlink(name, dir_fd=source_fd)
                if len(os.fsencode(link_target)) > 4096:
                    raise RuntimeError("workspace link target exceeded its limit")
                target.symlink_to(link_target)
            else:
                raise RuntimeError("workspace contains an unsupported special file")

    def _launch(self, attempt: dict[str, Any], workspace: Path) -> None:
        master, slave = pty.openpty()
        fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", 30, 100, 0, 0))
        command = self._base_bwrap(workspace, None) + [
            "/usr/bin/script", "-qefc", "/bin/bash --noprofile --norc", "/dev/null"
        ]
        completed = threading.Event()
        result: dict[str, Any] = {}
        self._launch_queue.put((command, slave, completed, result))
        if not completed.wait(timeout=5):
            os.close(master)
            raise RuntimeError("interactive shell launch timed out")
        if "error" in result:
            os.close(master)
            raise RuntimeError("interactive shell failed to launch") from result["error"]
        process = result["process"]
        self._processes[attempt["id"]] = process
        self._masters[attempt["id"]] = master
        decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
        deadline = time.monotonic() + 2
        while time.monotonic() < deadline:
            ready, _, _ = select.select([master], [], [], 0.1)
            if not ready:
                if process.poll() is not None:
                    raise RuntimeError("interactive shell failed to start")
                continue
            chunk = os.read(master, 8192)
            attempt["output"] += decoder.decode(chunk)
            if "lab:" in attempt["output"]:
                break
        else:
            self._stop_internal(attempt, "shell_start_timeout")
            raise RuntimeError("interactive shell did not become ready")
        self._save()
        reader = threading.Thread(target=self._read_output, args=(attempt["id"], master, decoder), name=f"lab-output-{attempt['id'][:8]}", daemon=True)
        reader.start()

    def _launcher_loop(self) -> None:
        while True:
            request = self._launch_queue.get()
            if request is None:
                return
            command, slave, completed, result = request
            try:
                result["process"] = subprocess.Popen(
                    command,
                    stdin=slave,
                    stdout=slave,
                    stderr=slave,
                    close_fds=True,
                    start_new_session=True,
                    env={},
                )
            except Exception as exc:
                result["error"] = exc
            finally:
                os.close(slave)
                completed.set()

    def _probe_capability(self) -> dict[str, Any]:
        versions = {"bubblewrap": self._version(["bwrap", "--version"]), "userland": self._host_userland()}
        available = bool(shutil.which("bwrap") and shutil.which("prlimit") and shutil.which("script"))
        if available:
            probe = self._state_root / ".probe"
            probe.mkdir(exist_ok=True, mode=0o700)
            try:
                probe_code = (
                    "import json,platform,subprocess;"
                    "v=lambda c:subprocess.check_output(c,text=True,stderr=subprocess.DEVNULL).splitlines()[0];"
                    "print(json.dumps({'python':platform.python_version(),'bash':v(['/bin/bash','--version']),"
                    "'git':v(['/usr/bin/git','--version']),'stat':v(['/usr/bin/stat','--version']),"
                    "'architecture':platform.machine()}))"
                )
                result = subprocess.run(
                    self._base_bwrap(probe, None) + ["/usr/bin/python3", "-c", probe_code],
                    stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                    timeout=5, check=False, env={},
                )
                available = result.returncode == 0
                if available:
                    versions.update(json.loads(result.stdout.decode("utf-8")))
            except (OSError, subprocess.TimeoutExpired, UnicodeDecodeError, json.JSONDecodeError):
                available = False
            finally:
                try:
                    probe.rmdir()
                except OSError:
                    pass
        return {
            "available": available,
            "label": f"Rootless Bubblewrap {versions['userland']} userland ({versions.get('architecture', 'unknown')}, host tools)",
            "adapter": "bwrap-userland",
            "versions": versions,
            "limitations": [
                "single-node host userland, not a separate distribution image",
                "no network, systemd, kernel administration, VM, macOS, or Windows semantics",
                "workspace is disposable and limited to one active lab",
                "workspace size and entry limits are monitored; CPU and memory rlimits are per process, not cgroup aggregates",
            ],
        }

    # ---------- process and output lifecycle ----------

    def _read_output(self, attempt_id: str, fd: int, decoder: codecs.IncrementalDecoder) -> None:
        while True:
            try:
                chunk = os.read(fd, 8192)
            except OSError:
                break
            if not chunk:
                break
            text = decoder.decode(chunk)
            with self._mutex:
                if self._closed:
                    break
                try:
                    attempt = self._attempt(attempt_id)
                except ValueError:
                    break
                attempt["output"] += text
                encoded_output = attempt["output"].encode("utf-8")
                if len(encoded_output) > _OUTPUT_LIMIT:
                    old_length = len(attempt["output"])
                    attempt["output"] = encoded_output[-(_OUTPUT_LIMIT // 2):].decode("utf-8", errors="ignore")
                    attempt["output_base"] += old_length - len(attempt["output"])
                    attempt["output_truncated"] = True
                    if attempt["status"] == "active":
                        self._stop_internal(attempt, "output_limit", from_reader=True)
                self._save()
        tail = decoder.decode(b"", final=True)
        if tail:
            with self._mutex:
                if not self._closed:
                    try:
                        attempt = self._attempt(attempt_id)
                    except ValueError:
                        return
                    attempt["output"] += tail
                    self._save()

    def _monitor_loop(self) -> None:
        while True:
            time.sleep(0.2)
            with self._mutex:
                if self._closed:
                    return
                for attempt in self._state["attempts"]:
                    if attempt["status"] != "active":
                        continue
                    started = dt.datetime.fromisoformat(attempt["started_at"])
                    if (dt.datetime.now(dt.timezone.utc) - started).total_seconds() > _LIFETIME_SECONDS:
                        self._stop_internal(attempt, "lifetime_limit", expired=True)
                    elif self._workspace_over_limit(attempt):
                        self._stop_internal(attempt, "workspace_limit", expired=True)
                    else:
                        self._refresh(attempt)

    def _refresh(self, attempt: dict[str, Any]) -> None:
        if attempt["status"] != "active":
            return
        process = self._processes.get(attempt["id"])
        if process is None:
            self._cleanup_workspace(attempt)
            attempt["status"] = "lost"
            attempt["ended_at"] = _now()
            attempt["end_reason"] = "process_missing"
            self._save()
        elif process.poll() is not None:
            self._cleanup_workspace(attempt)
            attempt["status"] = "stopped"
            attempt["ended_at"] = _now()
            attempt["end_reason"] = "shell_exit"
            self._close_master(attempt["id"])
            self._save()

    def _stop_internal(self, attempt: dict[str, Any], reason: str, *, expired: bool = False, from_reader: bool = False) -> None:
        process = self._processes.pop(attempt["id"], None)
        if process is not None and process.poll() is None:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            if not from_reader:
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    process.wait(timeout=2)
            else:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    pass
        self._close_master(attempt["id"])
        self._cleanup_workspace(attempt)
        attempt["status"] = "expired" if expired or reason in {"output_limit", "lifetime_limit"} else "stopped"
        attempt["ended_at"] = _now()
        attempt["end_reason"] = reason
        self._save()

    def _close_master(self, attempt_id: str) -> None:
        fd = self._masters.pop(attempt_id, None)
        if fd is not None:
            try:
                os.close(fd)
            except OSError:
                pass

    def _cleanup_workspace(self, attempt: dict[str, Any]) -> None:
        attempt_id = attempt.get("id")
        if not isinstance(attempt_id, str) or re.fullmatch(r"[0-9a-f]{32}", attempt_id) is None:
            raise RuntimeError("refusing cleanup for invalid attempt identity")
        attempt_root = self._state_root / "attempts" / attempt_id
        try:
            attempt_root.relative_to(self._state_root / "attempts")
        except ValueError as exc:
            raise RuntimeError("refusing cleanup outside runtime state") from exc
        if attempt_root.is_symlink():
            raise RuntimeError("refusing cleanup through a symbolic link")
        if attempt_root.exists():
            shutil.rmtree(attempt_root)

    def _workspace_over_limit(self, attempt: dict[str, Any]) -> bool:
        try:
            root = self._workspace(attempt)
        except RuntimeError:
            return True
        entries = 0
        total = 0
        pending = [root]
        while pending:
            directory = pending.pop()
            try:
                children = list(os.scandir(directory))
            except OSError:
                return True
            for child in children:
                entries += 1
                if entries > _WORKSPACE_ENTRIES:
                    return True
                try:
                    stat_result = child.stat(follow_symlinks=False)
                except OSError:
                    return True
                total += stat_result.st_size if child.is_file(follow_symlinks=False) else 0
                if total > _WORKSPACE_BYTES:
                    return True
                if child.is_dir(follow_symlinks=False):
                    pending.append(Path(child.path))
        return False

    # ---------- validation helpers ----------

    def _scenario(self, scenario_id: str) -> dict[str, Any]:
        if not isinstance(scenario_id, str):
            raise ValueError("scenario id must be text")
        for scenario in self._catalog_data:
            if scenario["id"] == scenario_id:
                return scenario
        raise ValueError("unknown scenario")

    def _attempt(self, attempt_id: str) -> dict[str, Any]:
        if not isinstance(attempt_id, str):
            raise ValueError("attempt id must be text")
        for attempt in self._state["attempts"]:
            if attempt["id"] == attempt_id:
                return attempt
        raise ValueError("unknown attempt")

    def _active_attempt(self, attempt_id: str) -> dict[str, Any]:
        self._ensure_open()
        attempt = self._attempt(attempt_id)
        self._refresh(attempt)
        if attempt["status"] != "active":
            raise RuntimeError("attempt is not active")
        return attempt

    def _workspace(self, attempt: dict[str, Any]) -> Path:
        workspace = self._state_root / "attempts" / attempt["workspace_name"] / "workspace"
        self._assert_mount_source(workspace, self._state_root)
        return workspace

    @staticmethod
    def _assert_mount_source(path: Path, root: Path) -> None:
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise RuntimeError("mount source is outside its owned root") from exc
        if not path.is_dir() or path.is_symlink() or path.resolve() != path:
            raise RuntimeError("mount source is not a safe real directory")

    def _operation(self, operation_id: str, payload: dict[str, Any]) -> dict[str, Any] | None:
        if not isinstance(operation_id, str) or not _OP_RE.fullmatch(operation_id):
            raise ValueError("operation id is invalid")
        existing = self._state["operations"].get(operation_id)
        if existing and existing["fingerprint"] != _fingerprint(payload):
            raise ValueError("operation id was already used for a different request")
        if existing and existing.get("status") in {"pending", "pending_uncertain"}:
            raise RuntimeError("previous operation outcome is uncertain")
        return existing

    def _remember_operation(self, operation_id: str, payload: dict[str, Any], attempt_id: str, *, status: str = "completed") -> None:
        self._state["operations"][operation_id] = {
            "fingerprint": _fingerprint(payload), "attempt_id": attempt_id, "at": _now(), "status": status
        }

    def _environment(self, attempt: dict[str, Any]) -> dict[str, Any]:
        scenario = self._scenario(attempt["scenario_id"])
        return {
            "adapter": "bwrap-userland",
            "label": self._capability["label"],
            "nodes": copy.deepcopy(scenario["environment"]["nodes"]),
            "shell": scenario["environment"]["shell"],
            "required_tools": copy.deepcopy(scenario["environment"]["required_tools"]),
            "versions": copy.deepcopy(attempt["tool_versions"]),
            "network": "isolated",
            "workspace": "/workspace",
            "limits": {
                "lifetime_seconds": _LIFETIME_SECONDS, "output_bytes": _OUTPUT_LIMIT,
                "workspace_bytes": _WORKSPACE_BYTES, "workspace_entries": _WORKSPACE_ENTRIES,
                "per_process_memory_bytes": 536870912, "aggregate_enforcement": "monitored workspace; per-process rlimits",
            },
        }

    @staticmethod
    def _nproc_ceiling() -> int:
        current = 0
        uid = os.getuid()
        for entry in Path("/proc").iterdir():
            if not entry.name.isdigit():
                continue
            try:
                status = (entry / "status").read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            owner = None
            threads = 1
            for line in status.splitlines():
                if line.startswith("Uid:"):
                    owner = int(line.split()[1])
                elif line.startswith("Threads:"):
                    threads = int(line.split()[1])
            if owner == uid:
                current += threads
        hard = resource.getrlimit(resource.RLIMIT_NPROC)[1]
        proposed = current + 128
        return proposed if hard == resource.RLIM_INFINITY else min(proposed, hard)

    @staticmethod
    def _host_userland() -> str:
        try:
            values = {}
            for line in Path("/etc/os-release").read_text(encoding="utf-8").splitlines():
                if "=" in line:
                    key, value = line.split("=", 1)
                    values[key] = value.strip().strip('"')
            return values.get("PRETTY_NAME") or values.get("NAME") or "host"
        except OSError:
            return "host"

    @staticmethod
    def _json_value(value: Any) -> Any:
        try:
            encoded = json.dumps(value, ensure_ascii=False)
            if len(encoded.encode("utf-8")) > 64 * 1024:
                return "checker detail exceeded its limit"
            return json.loads(encoded)
        except (TypeError, ValueError):
            return "checker returned a non-JSON detail"

    @staticmethod
    def _version(command: list[str], *, first_line: bool = False) -> str:
        try:
            text = subprocess.check_output(command, stderr=subprocess.DEVNULL, timeout=3, text=True).strip()
            return text.splitlines()[0] if first_line else text
        except (OSError, subprocess.SubprocessError):
            return "unavailable"

    def _ensure_open(self) -> None:
        if self._closed:
            raise RuntimeError("lab manager is closed")

    def __enter__(self) -> "LabManager":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
