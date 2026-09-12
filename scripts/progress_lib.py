#!/usr/bin/env python3
"""Shared progress read/write helpers for mark_done.sh and progress_server.py."""

from __future__ import annotations

import datetime
import fcntl
import hashlib
import json
import os
import re
import signal
import shlex
import subprocess
import sys
import tempfile
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Any

ACTIVE_COURSE_ID = "linux-foundations"
OPERATION_ID_RE = re.compile(r"^[A-Za-z0-9._:-]{1,120}$")
MAX_TASK_ACTION_TEXT_CODEPOINTS = 500

DEFAULT_LANES: dict[str, dict[str, str]] = {
    ACTIVE_COURSE_ID: {
        "title": "Linux 基础与工程实践",
        "description": "当前唯一正式课程 linux-foundations：终端、文件系统、Shell、自动化与远程实操",
        "course_id": ACTIVE_COURSE_ID,
    },
}


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def progress_json_path(root: Path | None = None) -> Path:
    return (root or repo_root()) / "progress.json"


def progress_js_path(root: Path | None = None) -> Path:
    return (root or repo_root()) / "progress_data.js"


def action_log_path(root: Path | None = None) -> Path:
    return (root or repo_root()) / "records/action_logs/events.jsonl"


def feedback_json_path(root: Path | None = None) -> Path:
    return (root or repo_root()) / "records/feedback/task_feedback.json"


def saves_dir_path(root: Path | None = None) -> Path:
    return (root or repo_root()) / "records/saves"


def rounds_js_path(root: Path | None = None) -> Path:
    return (root or repo_root()) / "rounds_data.js"


def terminal_log_path(root: Path | None = None) -> Path:
    return (root or repo_root()) / "records/terminal/commands.jsonl"


def task_operations_path(root: Path | None = None) -> Path:
    return (root or repo_root()) / "records/action_logs/task_operations.json"


def run_operations_path(root: Path | None = None) -> Path:
    return (root or repo_root()) / "records/action_logs/run_operations.json"


def _atomic_write_bytes(path: Path, content: bytes) -> None:
    """Replace one state file and persist its directory entry before returning."""
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        os.fchmod(fd, mode)
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except Exception:
        try:
            os.close(fd)
        except OSError:
            pass
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass
        raise


def _atomic_write_text(path: Path, content: str) -> None:
    """Replace one generated/state text file without exposing a partial body."""
    _atomic_write_bytes(path, content.encode("utf-8"))


def _capture_file_preimages(paths: list[Path]) -> dict[Path, bytes | None]:
    return {path: path.read_bytes() if path.exists() else None for path in paths}


def _restore_file_preimages(preimages: dict[Path, bytes | None]) -> None:
    """Best-effort rollback for a caught multi-file write failure."""
    restored: list[Path] = []
    try:
        for path, content in preimages.items():
            if content is None:
                if path.exists():
                    path.unlink()
                    directory_fd = os.open(path.parent, os.O_RDONLY)
                    try:
                        os.fsync(directory_fd)
                    finally:
                        os.close(directory_fd)
            else:
                _atomic_write_bytes(path, content)
            restored.append(path)
    except Exception as exc:
        names = ", ".join(str(path) for path in restored)
        raise RuntimeError(f"task_transaction_rollback_failed:{names}") from exc


@contextmanager
def progress_write_lock(root: Path | None = None):
    """Serialize progress mutations across the local server and CLI processes."""
    resolved_root = (root or repo_root()).resolve()
    digest = hashlib.sha256(str(resolved_root).encode("utf-8")).hexdigest()[:20]
    lock_path = Path(tempfile.gettempdir()) / f"computer-study-plan-progress-{digest}.lock"
    with lock_path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


@contextmanager
def task_mutation_lock(task_id: str, root: Path | None = None):
    """Serialize a run and explicit completion changes for the same task."""
    resolved_root = (root or repo_root()).resolve()
    digest = hashlib.sha256(f"{resolved_root}\0{task_id}".encode("utf-8")).hexdigest()[:20]
    lock_path = Path(tempfile.gettempdir()) / f"computer-study-plan-task-{digest}.lock"
    with lock_path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


class RunInProgressError(RuntimeError):
    pass


class RunOutcomeUncertainError(RuntimeError):
    pass


@contextmanager
def run_execution_lock(sandbox: Path, root: Path | None = None):
    """Prevent concurrent scripts from mutating the same course sandbox."""
    resolved_root = (root or repo_root()).resolve()
    digest = hashlib.sha256(f"{resolved_root}\0{sandbox.resolve()}".encode("utf-8")).hexdigest()[:20]
    lock_path = Path(tempfile.gettempdir()) / f"computer-study-plan-run-{digest}.lock"
    with lock_path.open("a+", encoding="utf-8") as handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RunInProgressError("run_in_progress") from exc
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def load_progress(root: Path | None = None) -> dict[str, Any]:
    path = progress_json_path(root)
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return normalize_progress(data)


def normalize_progress(data: dict[str, Any]) -> dict[str, Any]:
    revision = data.get("revision", 0)
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 0:
        raise ValueError("invalid_progress_revision")
    data["version"] = 2
    data["revision"] = revision
    data["active_course_id"] = ACTIVE_COURSE_ID
    # Single-course stage: drop legacy multi-lane metadata if present.
    data["lanes"] = {key: dict(meta) for key, meta in DEFAULT_LANES.items()}
    tasks = data.setdefault("tasks", {})
    if not isinstance(tasks, dict):
        raise ValueError("invalid_progress_tasks")
    for task_id, info in tasks.items():
        if not isinstance(task_id, str) or not isinstance(info, dict):
            raise ValueError("invalid_progress_task")
        done = info.get("done")
        done_at = info.get("done_at")
        if not isinstance(done, bool):
            raise ValueError(f"invalid_task_done:{task_id}")
        if done:
            if not isinstance(done_at, str) or not done_at:
                raise ValueError(f"invalid_task_done_at:{task_id}")
        elif done_at is not None:
            raise ValueError(f"invalid_task_done_at:{task_id}")
        else:
            info["done_at"] = None
        info["lane"] = ACTIVE_COURSE_ID
    return data


def save_progress(data: dict[str, Any], root: Path | None = None) -> None:
    path = progress_json_path(root)
    validated = normalize_progress(data)
    _atomic_write_text(path, json.dumps(validated, ensure_ascii=False, indent=2))


def read_feedback_payload(root: Path | None = None) -> dict[str, Any]:
    path = feedback_json_path(root)
    if not path.exists():
        progress = load_progress(root)
        return build_feedback_payload(progress, load_action_events(root))
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def sync_progress_data_js(data: dict[str, Any], root: Path | None = None) -> None:
    js_path = progress_js_path(root)
    payload = {
        "version": data.get("version", 2),
        "revision": max(0, int(data.get("revision") or 0)),
        "lanes": data.get("lanes", {}),
        "tasks": data.get("tasks", {}),
    }
    body = json.dumps(payload, ensure_ascii=False, indent=2)
    content = (
        "// Auto-generated — DO NOT edit manually\n"
        "// Source of truth: progress.json\n"
        f"window.PROGRESS_DATA = {body};\n"
    )
    _atomic_write_text(js_path, content)


def load_task_operations(root: Path | None = None) -> dict[str, Any]:
    path = task_operations_path(root)
    if not path.exists():
        return {"version": 1, "operations": {}}
    payload = json.loads(path.read_text(encoding="utf-8"))
    operations = payload.get("operations") if isinstance(payload, dict) else None
    if not isinstance(operations, dict):
        raise ValueError("invalid_task_operations")
    return {"version": 1, "operations": operations}


def save_task_operations(payload: dict[str, Any], root: Path | None = None) -> None:
    operations = payload.get("operations") if isinstance(payload, dict) else None
    if not isinstance(operations, dict):
        raise ValueError("invalid_task_operations")
    for operation_key, record in operations.items():
        _validated_task_operation_record(operation_key, record)
    _atomic_write_text(
        task_operations_path(root),
        json.dumps({"version": 1, "operations": operations}, ensure_ascii=False, indent=2) + "\n",
    )


RUN_RESULTS = {"ok", "failed", "timeout"}
RUN_RECORD_STATUSES = {"executing", "interrupted", "pending", "committed"}


def run_operation_request(task_id: str, script_path: str, sandbox_path: str) -> dict[str, Any]:
    if not isinstance(task_id, str) or not task_id:
        raise ValueError("invalid_run_request")
    if not isinstance(script_path, str) or not script_path:
        raise ValueError("invalid_run_request")
    if not isinstance(sandbox_path, str) or not sandbox_path:
        raise ValueError("invalid_run_request")
    return {
        "task_id": task_id,
        "action": "run",
        "script_path": script_path,
        "sandbox_path": sandbox_path,
    }


def run_operation_fingerprint(request: dict[str, Any]) -> str:
    canonical = json.dumps(request, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def progress_snapshot_fingerprint(data: dict[str, Any]) -> str:
    canonical = json.dumps(
        {"lanes": data.get("lanes", {}), "tasks": data.get("tasks", {})},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _validated_iso_timestamp(value: Any, error: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(error)
    try:
        datetime.datetime.fromisoformat(value)
    except ValueError:
        raise ValueError(error) from None
    return value


def _validated_canonical_uuid(value: Any, error: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(error)
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError):
        raise ValueError(error) from None
    if str(parsed) != value:
        raise ValueError(error)
    return value


def _validated_run_request(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("invalid_pending_run_request")
    canonical = run_operation_request(
        value.get("task_id"),
        value.get("script_path"),
        value.get("sandbox_path"),
    )
    if value != canonical:
        raise ValueError("invalid_pending_run_request")
    return canonical


def _validated_run_execution(value: Any) -> dict[str, Any]:
    required = {
        "result",
        "execution_ok",
        "returncode",
        "timed_out",
        "duration_ms",
        "script_path",
        "sandbox_path",
        "stdout",
        "stderr",
        "verification_reached",
        "completion_applied",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise ValueError("invalid_pending_run_execution")
    result = value.get("result")
    returncode = value.get("returncode")
    timed_out = value.get("timed_out")
    facts_match = (
        result == "ok" and returncode == 0 and timed_out is False
    ) or (
        result == "failed"
        and isinstance(returncode, int)
        and not isinstance(returncode, bool)
        and returncode != 0
        and timed_out is False
    ) or (
        result == "timeout" and returncode is None and timed_out is True
    )
    if (
        result not in RUN_RESULTS
        or not isinstance(value.get("execution_ok"), bool)
        or value.get("execution_ok") != (result == "ok")
        or not isinstance(timed_out, bool)
        or not facts_match
        or not isinstance(value.get("duration_ms"), int)
        or isinstance(value.get("duration_ms"), bool)
        or value.get("duration_ms") < 0
        or not isinstance(value.get("script_path"), str)
        or not value.get("script_path")
        or not isinstance(value.get("sandbox_path"), str)
        or not value.get("sandbox_path")
        or not isinstance(value.get("stdout"), str)
        or not isinstance(value.get("stderr"), str)
        or not isinstance(value.get("verification_reached"), bool)
        or not isinstance(value.get("completion_applied"), bool)
        or (value.get("completion_applied") and (result != "ok" or not value.get("verification_reached")))
    ):
        raise ValueError("invalid_pending_run_execution")
    return value


def _validated_run_event(
    value: Any,
    request: dict[str, Any],
    execution: dict[str, Any],
    operation_id: str,
) -> dict[str, Any]:
    required = {
        "action_id",
        "task_id",
        "round_id",
        "lane",
        "action_type",
        "timestamp",
        "result",
        "note",
        "evidence_path",
        "details",
        "operation_id",
    }
    detail_keys = {
        "script_path",
        "sandbox_path",
        "returncode",
        "timed_out",
        "duration_ms",
        "stdout_excerpt",
        "stderr_excerpt",
        "verification_reached",
        "completion_applied",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise ValueError("invalid_pending_run_event")
    details = value.get("details")
    if not isinstance(details, dict) or set(details) != detail_keys:
        raise ValueError("invalid_pending_run_event")
    _validated_canonical_uuid(value.get("action_id"), "invalid_pending_run_event")
    _validated_iso_timestamp(value.get("timestamp"), "invalid_pending_run_event")
    if (
        value.get("task_id") != request["task_id"]
        or value.get("round_id") != resolve_round_id(request["task_id"])
        or value.get("lane") != ACTIVE_COURSE_ID
        or value.get("action_type") != "run_exercise"
        or value.get("result") != execution["result"]
        or value.get("note") != f"Web UI 执行练习脚本：{request['script_path']}；结果：{execution['result']}"
        or value.get("evidence_path") != request["sandbox_path"]
        or value.get("operation_id") != operation_id
        or details.get("script_path") != execution["script_path"]
        or details.get("sandbox_path") != execution["sandbox_path"]
        or details.get("returncode") != execution["returncode"]
        or details.get("timed_out") != execution["timed_out"]
        or details.get("duration_ms") != execution["duration_ms"]
        or details.get("stdout_excerpt") != execution["stdout"]
        or details.get("stderr_excerpt") != execution["stderr"]
        or details.get("verification_reached") != execution["verification_reached"]
        or details.get("completion_applied") != execution["completion_applied"]
    ):
        raise ValueError("invalid_pending_run_event")
    return value


def _validated_run_operation_record(
    operation_id: str,
    value: Any,
    *,
    required_status: str | None = None,
) -> dict[str, Any]:
    if not isinstance(operation_id, str) or not OPERATION_ID_RE.fullmatch(operation_id):
        raise ValueError("invalid_pending_run_operation")
    if not isinstance(value, dict):
        raise ValueError("invalid_pending_run_operation")
    status = value.get("status")
    if required_status is not None and status != required_status:
        raise ValueError("invalid_pending_run_operation")
    if status not in RUN_RECORD_STATUSES:
        raise ValueError("invalid_pending_run_operation")
    request = _validated_run_request(value.get("request"))
    if value.get("request_fingerprint") != run_operation_fingerprint(request):
        raise ValueError("invalid_pending_run_fingerprint")
    _validated_iso_timestamp(value.get("started_at"), "invalid_pending_run_operation")

    common = {"status", "request", "request_fingerprint", "started_at"}
    if status == "executing":
        if set(value) != common:
            raise ValueError("invalid_pending_run_operation")
        return {"request": request}
    if status == "interrupted":
        if set(value) != common | {"interrupted_at"}:
            raise ValueError("invalid_pending_run_operation")
        _validated_iso_timestamp(value.get("interrupted_at"), "invalid_pending_run_operation")
        return {"request": request}

    required = common | {
        "base_revision",
        "target_revision",
        "base_task_state",
        "task_state",
        "base_progress_fingerprint",
        "target_progress_fingerprint",
        "execution",
        "event",
        "prepared_at",
    }
    if status == "committed":
        required.add("committed_at")
    if set(value) != required:
        raise ValueError("invalid_pending_run_operation")
    base_revision = value.get("base_revision")
    target_revision = value.get("target_revision")
    if (
        not isinstance(base_revision, int)
        or isinstance(base_revision, bool)
        or base_revision < 0
        or not isinstance(target_revision, int)
        or isinstance(target_revision, bool)
        or target_revision != base_revision + 1
    ):
        raise ValueError("invalid_pending_run_revision")
    for field in ("base_progress_fingerprint", "target_progress_fingerprint"):
        if not isinstance(value.get(field), str) or not re.fullmatch(r"[0-9a-f]{64}", value[field]):
            raise ValueError("invalid_pending_run_progress_fingerprint")
    execution = _validated_run_execution(value.get("execution"))
    if (
        execution["script_path"] != request["script_path"]
        or execution["sandbox_path"] != request["sandbox_path"]
    ):
        raise ValueError("invalid_pending_run_execution")
    event = _validated_run_event(value.get("event"), request, execution, operation_id)
    base_state = _validated_transaction_task_state(request["task_id"], value.get("base_task_state"))
    target_state = _validated_transaction_task_state(request["task_id"], value.get("task_state"))
    expected_target = dict(base_state)
    expected_applied = execution["result"] == "ok" and execution["verification_reached"] and not base_state["done"]
    if expected_applied:
        expected_target["done"] = True
        expected_target["done_at"] = target_state.get("done_at")
    if execution["completion_applied"] != expected_applied or target_state != expected_target:
        raise ValueError("invalid_pending_run_transition")
    _validated_iso_timestamp(value.get("prepared_at"), "invalid_pending_run_operation")
    if status == "committed":
        _validated_iso_timestamp(value.get("committed_at"), "invalid_pending_run_operation")
    return {
        "request": request,
        "execution": execution,
        "event": event,
        "base_revision": base_revision,
        "target_revision": target_revision,
        "base_task_state": base_state,
        "task_state": target_state,
        "base_progress_fingerprint": value["base_progress_fingerprint"],
        "target_progress_fingerprint": value["target_progress_fingerprint"],
    }


def load_run_operations(root: Path | None = None) -> dict[str, Any]:
    path = run_operations_path(root)
    if not path.exists():
        return {"version": 1, "operations": {}}
    payload = json.loads(path.read_text(encoding="utf-8"))
    operations = payload.get("operations") if isinstance(payload, dict) else None
    if (
        not isinstance(payload, dict)
        or set(payload) != {"version", "operations"}
        or payload.get("version") != 1
        or not isinstance(operations, dict)
    ):
        raise ValueError("invalid_run_operations")
    return {"version": 1, "operations": operations}


def save_run_operations(payload: dict[str, Any], root: Path | None = None) -> None:
    operations = payload.get("operations") if isinstance(payload, dict) else None
    if not isinstance(operations, dict):
        raise ValueError("invalid_run_operations")
    for operation_id, record in operations.items():
        _validated_run_operation_record(operation_id, record)
    _atomic_write_text(
        run_operations_path(root),
        json.dumps({"version": 1, "operations": operations}, ensure_ascii=False, indent=2) + "\n",
    )


def task_operation_request(
    task_id: str,
    undo: bool,
    note: str,
    evidence_path: str,
) -> dict[str, Any]:
    if not isinstance(note, str) or not isinstance(evidence_path, str):
        raise ValueError("invalid_task_action_text")
    if len(note) > MAX_TASK_ACTION_TEXT_CODEPOINTS:
        raise ValueError("note_too_long")
    if len(evidence_path) > MAX_TASK_ACTION_TEXT_CODEPOINTS:
        raise ValueError("evidence_path_too_long")
    return {
        "task_id": task_id,
        "action": "undo" if undo else "done",
        "note": note,
        "evidence_path": evidence_path,
    }


def task_operation_fingerprint(request: dict[str, Any]) -> str:
    canonical = json.dumps(request, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _validated_task_action_request(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("invalid_pending_task_request")
    task_id = value.get("task_id")
    action = value.get("action")
    if not isinstance(task_id, str) or not task_id or action not in {"done", "undo"}:
        raise ValueError("invalid_pending_task_request")
    canonical = task_operation_request(
        task_id,
        action == "undo",
        value.get("note"),
        value.get("evidence_path"),
    )
    if value != canonical:
        raise ValueError("invalid_pending_task_request")
    return canonical


def _validated_task_action_event(
    value: Any,
    request: dict[str, Any],
    operation_id: str,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("invalid_pending_action_event")
    action_id = value.get("action_id")
    timestamp = value.get("timestamp")
    if not isinstance(action_id, str) or not action_id:
        raise ValueError("invalid_pending_action_event")
    try:
        parsed_action_id = uuid.UUID(action_id)
    except (ValueError, AttributeError):
        raise ValueError("invalid_pending_action_event") from None
    if str(parsed_action_id) != action_id:
        raise ValueError("invalid_pending_action_event")
    if not isinstance(timestamp, str) or not timestamp:
        raise ValueError("invalid_pending_action_event")
    try:
        datetime.datetime.fromisoformat(timestamp)
    except ValueError:
        raise ValueError("invalid_pending_action_event") from None

    action = request["action"]
    expected_action_type = "undo_done" if action == "undo" else "mark_done"
    allowed_results = {"ok", "noop_already_undone"} if action == "undo" else {"ok", "noop_already_done"}
    required = {
        "action_id",
        "task_id",
        "round_id",
        "lane",
        "action_type",
        "timestamp",
        "result",
        "note",
        "evidence_path",
    }
    if operation_id:
        required.add("operation_id")
    if set(value) != required:
        raise ValueError("invalid_pending_action_event")
    if (
        value.get("task_id") != request["task_id"]
        or value.get("round_id") != resolve_round_id(request["task_id"])
        or value.get("lane") != ACTIVE_COURSE_ID
        or value.get("action_type") != expected_action_type
        or value.get("result") not in allowed_results
        or value.get("note") != request["note"]
        or value.get("evidence_path") != request["evidence_path"]
    ):
        raise ValueError("invalid_pending_action_event")
    if operation_id:
        if not OPERATION_ID_RE.fullmatch(operation_id) or value.get("operation_id") != operation_id:
            raise ValueError("invalid_pending_action_event")
    elif "operation_id" in value:
        raise ValueError("invalid_pending_action_event")
    return value


def _validated_transaction_task_state(task_id: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or value.get("lane") != ACTIVE_COURSE_ID:
        raise ValueError("invalid_pending_task_state")
    done = value.get("done")
    done_at = value.get("done_at")
    if not isinstance(done, bool):
        raise ValueError("invalid_pending_task_state")
    if done:
        if not isinstance(done_at, str) or not done_at:
            raise ValueError(f"invalid_task_done_at:{task_id}")
    elif done_at is not None:
        raise ValueError(f"invalid_task_done_at:{task_id}")
    return value


def _validated_task_operation_record(
    operation_key: str,
    value: Any,
    *,
    required_status: str | None = None,
) -> dict[str, Any]:
    if not isinstance(operation_key, str) or not isinstance(value, dict):
        raise ValueError("invalid_pending_task_operation")
    status = value.get("status")
    if required_status is not None and status != required_status:
        raise ValueError("invalid_pending_task_operation")
    if status not in {"pending", "committed"}:
        raise ValueError("invalid_pending_task_operation")
    request = _validated_task_action_request(value.get("request"))
    request_fingerprint = value.get("request_fingerprint")
    if request_fingerprint != task_operation_fingerprint(request):
        raise ValueError("invalid_pending_task_fingerprint")

    event_value = value.get("event")
    action_id = event_value.get("action_id") if isinstance(event_value, dict) else ""
    if operation_key.startswith("legacy:"):
        if operation_key != f"legacy:{action_id}":
            raise ValueError("invalid_pending_operation_key")
        event_operation_id = ""
    else:
        if not OPERATION_ID_RE.fullmatch(operation_key):
            raise ValueError("invalid_pending_operation_key")
        event_operation_id = operation_key
    event = _validated_task_action_event(event_value, request, event_operation_id)

    base_revision = value.get("base_revision")
    target_revision = value.get("target_revision")
    if (
        not isinstance(base_revision, int)
        or isinstance(base_revision, bool)
        or base_revision < 0
        or not isinstance(target_revision, int)
        or isinstance(target_revision, bool)
        or target_revision != base_revision + 1
    ):
        raise ValueError("invalid_pending_task_revision")

    task_id = request["task_id"]
    base_task_state = _validated_transaction_task_state(task_id, value.get("base_task_state"))
    task_state = _validated_transaction_task_state(task_id, value.get("task_state"))
    expected_state = dict(base_task_state)
    if request["action"] == "undo":
        expected_result = "ok" if base_task_state["done"] else "noop_already_undone"
        expected_state["done"] = False
        expected_state["done_at"] = None
    else:
        expected_result = "noop_already_done" if base_task_state["done"] else "ok"
        expected_state["done"] = True
        expected_state["done_at"] = (
            base_task_state["done_at"] if base_task_state["done"] else task_state["done_at"]
        )
    if event["result"] != expected_result or task_state != expected_state:
        raise ValueError("invalid_pending_task_transition")
    return {
        "request": request,
        "event": event,
        "base_task_state": base_task_state,
        "task_state": task_state,
        "base_revision": base_revision,
        "target_revision": target_revision,
    }


def resolve_round_id(task_id: str) -> str:
    if task_id.startswith(("w1-", "w2-", "w3-", "fin-")):
        return "round_00"
    if task_id.startswith("r") and len(task_id) >= 4 and task_id[1:3].isdigit():
        return f"round_{int(task_id[1:3]):02d}"
    if task_id.startswith(("linux-", "linux_")):
        return "linux"
    if task_id.startswith("vps-"):
        return "vps"
    return "unknown"


def build_action_event(
    task_id: str,
    lane: str,
    action_type: str,
    result: str,
    root: Path | None = None,
    note: str = "",
    evidence_path: str = "",
    details: dict[str, Any] | None = None,
    operation_id: str = "",
    action_id: str = "",
    timestamp: str = "",
) -> dict[str, Any]:
    action_id = action_id or str(uuid.uuid4())
    event = {
        "action_id": action_id,
        "task_id": task_id,
        "round_id": resolve_round_id(task_id),
        "lane": lane,
        "action_type": action_type,
        "timestamp": timestamp or datetime.datetime.now().isoformat(timespec="seconds"),
        "result": result,
        "note": note,
        "evidence_path": evidence_path,
    }
    if details:
        event["details"] = details
    if operation_id:
        event["operation_id"] = operation_id
    return event


def write_action_events(events: list[dict[str, Any]], root: Path | None = None) -> None:
    body = "".join(json.dumps(event, ensure_ascii=False) + "\n" for event in events)
    _atomic_write_text(action_log_path(root), body)


def append_action_event(
    task_id: str,
    lane: str,
    action_type: str,
    result: str,
    root: Path | None = None,
    note: str = "",
    evidence_path: str = "",
    details: dict[str, Any] | None = None,
    operation_id: str = "",
) -> str:
    event = build_action_event(
        task_id,
        lane,
        action_type,
        result,
        root=root,
        note=note,
        evidence_path=evidence_path,
        details=details,
        operation_id=operation_id,
    )
    with progress_write_lock(root):
        recover_pending_operations(root)
        events = load_action_events(root)
        events.append(event)
        write_action_events(events, root)
    return str(event["action_id"])


def load_action_events(root: Path | None = None) -> list[dict[str, Any]]:
    path = action_log_path(root)
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def events_by_task(events: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for event in events:
        task_id = event.get("task_id")
        if not task_id:
            continue
        grouped.setdefault(str(task_id), []).append(event)
    return grouped


def load_rounds_metadata(root: Path | None = None) -> list[dict[str, Any]]:
    path = rounds_js_path(root)
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    marker = "window.ROUNDS_DATA = "
    if marker not in text:
        return []
    raw = text.split(marker, 1)[1].strip()
    if raw.endswith(";"):
        raw = raw[:-1].strip()
    payload = json.loads(raw)
    return payload if isinstance(payload, list) else []


def task_metadata(task_id: str, root: Path | None = None) -> dict[str, Any] | None:
    for round_item in load_rounds_metadata(root):
        for week in round_item.get("weeks", []):
            for task in week.get("tasks", []):
                if task.get("id") == task_id:
                    return {
                        "round": round_item,
                        "week": week,
                        "task": task,
                    }
    return None


def task_metadata_map(root: Path | None = None) -> dict[str, dict[str, Any]]:
    items: dict[str, dict[str, Any]] = {}
    for round_item in load_rounds_metadata(root):
        for week in round_item.get("weeks", []):
            for task in week.get("tasks", []):
                task_id = task.get("id")
                if not task_id:
                    continue
                items[str(task_id)] = {
                    "round": round_item,
                    "week": week,
                    "task": task,
                }
    return items


RUNNABLE_SCRIPT_RE = re.compile(
    r"^rounds/round_(\d{2})/(week[1-3]|final)/(exercises|comprehensive_exercise)\.(sh|py)$"
)
RUN_TIMEOUT_SECONDS = 20
MAX_RUN_OUTPUT_CHARS = 8000


def safe_runnable_script(file_path: str, root: Path | None = None) -> tuple[Path, int]:
    match = RUNNABLE_SCRIPT_RE.match(file_path)
    if not match:
        raise ValueError("script_not_whitelisted")
    root = root or repo_root()
    script = (root / file_path).resolve()
    root_resolved = root.resolve()
    if root_resolved not in script.parents:
        raise ValueError("script_outside_repo")
    if not script.exists() or not script.is_file():
        raise FileNotFoundError(file_path)
    return script, int(match.group(1))


def runnable_task_execution_plan(task_id: str, root: Path | None = None) -> dict[str, Any]:
    meta = task_metadata(task_id, root)
    if not meta:
        raise ValueError("task_metadata_not_found")
    task = meta["task"]
    if task.get("type") != "exercise":
        raise ValueError("task_not_runnable")
    file_path = str(task.get("file") or "")
    script, round_num = safe_runnable_script(file_path, root)
    sandbox = Path.home() / "cli-lab" / f"round{round_num}"
    suffix = script.suffix.lower()
    if suffix == ".sh":
        command = ["/bin/bash", str(script)]
    elif suffix == ".py":
        command = [sys.executable, str(script)]
    else:
        raise ValueError("unsupported_script_type")
    return {
        "task_id": task_id,
        "title": str(task.get("title") or task_id),
        "file": file_path,
        "script": script,
        "round_id": str(meta["round"].get("id") or resolve_round_id(task_id)),
        "sandbox": sandbox,
        "command": command,
    }


def output_excerpt(value: Any, limit: int = MAX_RUN_OUTPUT_CHARS) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        text = value.decode("utf-8", errors="replace")
    else:
        text = str(value)
    if len(text) <= limit:
        return text
    return text[:limit] + "\n...[output truncated]"


def _terminate_run_process(proc: subprocess.Popen[str]) -> tuple[str, str]:
    """Terminate and reap the complete script process group."""
    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        # macOS can report EPERM after the session leader has exited and the
        # process group is already being torn down. The follow-up communicate
        # still reaps the owned process and closes its pipes.
        pass
    try:
        stdout, stderr = proc.communicate(timeout=1)
    except subprocess.TimeoutExpired:
        stdout = stderr = ""
    # The shell may already have exited while a detached descendant in the
    # same process group remains alive with its stdio closed. Always clear the
    # complete group before accepting a receipt or returning an outcome.
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass
    try:
        tail_stdout, tail_stderr = proc.communicate(timeout=1)
        stdout = tail_stdout or stdout
        stderr = tail_stderr or stderr
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("run_process_group_not_stopped") from exc
    except ValueError:
        pass
    return stdout or "", stderr or ""


def execute_run_plan(plan: dict[str, Any], env: dict[str, str]) -> dict[str, Any]:
    """Execute one trusted course script without ever holding the progress lock."""
    started = time.monotonic()
    proc = subprocess.Popen(
        plan["command"],
        cwd=plan["sandbox"],
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    try:
        stdout, stderr = proc.communicate(timeout=RUN_TIMEOUT_SECONDS)
        returncode: int | None = proc.returncode
        timed_out = False
        result = "ok" if returncode == 0 else "failed"
        # A successful shell exit is not proof that background descendants
        # stopped. Clear the process group before reading the capability receipt.
        _terminate_run_process(proc)
    except subprocess.TimeoutExpired:
        stdout, stderr = _terminate_run_process(proc)
        returncode = None
        timed_out = True
        result = "timeout"
    except BaseException:
        try:
            _terminate_run_process(proc)
        except Exception:
            pass
        raise
    return {
        "result": result,
        "execution_ok": result == "ok",
        "returncode": returncode,
        "timed_out": timed_out,
        "duration_ms": int((time.monotonic() - started) * 1000),
        "script_path": plan["file"],
        "sandbox_path": str(plan["sandbox"]),
        "stdout": output_excerpt(stdout),
        "stderr": output_excerpt(stderr),
    }


def _run_receipt_reached(
    receipt_path: Path,
    token: str,
    task_id: str,
    script_path: str,
) -> bool:
    """Accept only the private capability record created for this exact run."""
    try:
        info = receipt_path.lstat()
        if not receipt_path.is_file() or receipt_path.is_symlink() or info.st_uid != os.getuid():
            return False
        if info.st_size > 4096:
            return False
        rows = []
        for line in receipt_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict) or set(value) != {"token", "task_id", "script_path"}:
                return False
            rows.append(value)
        expected = {"token": token, "task_id": task_id, "script_path": script_path}
        return bool(rows) and all(row == expected for row in rows)
    except (FileNotFoundError, OSError, UnicodeDecodeError, json.JSONDecodeError):
        return False


def _run_operation_response(
    record: dict[str, Any],
    data: dict[str, Any],
    feedback: dict[str, Any],
    *,
    replayed: bool,
) -> dict[str, Any]:
    operation_id = str(record["event"]["operation_id"])
    execution = dict(record["execution"])
    execution.update(
        {
            "task_id": record["request"]["task_id"],
            "action_id": record["event"]["action_id"],
            "event": dict(record["event"]),
            "operation_id": operation_id,
            "replayed_operation": replayed,
            "revision": max(0, int(data.get("revision") or 0)),
            "total": len(data.get("tasks", {})),
            "done_count": sum(1 for item in data.get("tasks", {}).values() if item.get("done")),
        }
    )
    return {
        "ok": True,
        "execution": execution,
        "tasks": data.get("tasks", {}),
        "lanes": data.get("lanes", {}),
        "feedback": feedback.get("feedback", {}),
        "revision": max(0, int(data.get("revision") or 0)),
    }


def run_task_script(
    task_id: str,
    root: Path | None = None,
    *,
    operation_id: str,
) -> dict[str, Any]:
    root = root or repo_root()
    if not isinstance(operation_id, str) or not OPERATION_ID_RE.fullmatch(operation_id):
        raise ValueError("invalid_operation_id")
    plan = runnable_task_execution_plan(task_id, root)
    sandbox_path = str(plan["sandbox"])
    request = run_operation_request(task_id, plan["file"], sandbox_path)
    request_fingerprint = run_operation_fingerprint(request)

    with run_execution_lock(plan["sandbox"], root), task_mutation_lock(task_id, root):
        with progress_write_lock(root):
            recover_pending_operations(root)
            data = load_progress(root)
            if task_id not in data["tasks"]:
                raise KeyError(task_id)
            ledger = load_run_operations(root)
            for key, record in ledger["operations"].items():
                _validated_run_operation_record(key, record)

            changed = False
            for record in ledger["operations"].values():
                if record.get("status") == "executing" and record.get("request", {}).get("sandbox_path") == sandbox_path:
                    record["status"] = "interrupted"
                    record["interrupted_at"] = datetime.datetime.now().isoformat(timespec="seconds")
                    changed = True
            if changed:
                save_run_operations(ledger, root)

            existing = ledger["operations"].get(operation_id)
            if existing and existing.get("request_fingerprint") != request_fingerprint:
                raise ValueError("operation_id_conflict")
            if existing and existing.get("status") == "committed":
                validated = _validated_run_operation_record(operation_id, existing, required_status="committed")
                matches = [
                    event for event in load_action_events(root)
                    if event.get("action_id") == validated["event"]["action_id"]
                ]
                if len(matches) != 1 or matches[0] != validated["event"]:
                    raise ValueError("run_operation_event_not_in_current_history")
                return _run_operation_response(existing, data, read_feedback_payload(root), replayed=True)
            if existing:
                raise RunOutcomeUncertainError("run_execution_state_uncertain")

            # Validate/recover every durable operation before creating any
            # sandbox state. Directory creation itself is short and remains
            # inside the sandbox/task/progress lock ordering.
            plan["sandbox"].mkdir(parents=True, exist_ok=True)
            ledger["operations"][operation_id] = {
                "status": "executing",
                "request": request,
                "request_fingerprint": request_fingerprint,
                "started_at": datetime.datetime.now().isoformat(timespec="seconds"),
            }
            save_run_operations(ledger, root)

        token = str(uuid.uuid4())
        with tempfile.TemporaryDirectory(prefix=".progress-ui-run-", dir=plan["sandbox"]) as receipt_dir:
            os.chmod(receipt_dir, 0o700)
            receipt_path = Path(receipt_dir) / "receipt.jsonl"
            fd = os.open(receipt_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            os.close(fd)
            env = os.environ.copy()
            env.update(
                {
                    "PROGRESS_UI_RUN": "1",
                    "PROGRESS_UI_RUN_TASK_ID": task_id,
                    "PROGRESS_UI_RUN_SCRIPT": plan["file"],
                    "PROGRESS_UI_RUN_RECEIPT": str(receipt_path),
                    "PROGRESS_UI_RUN_TOKEN": token,
                    "COMPUTER_STUDY_PLAN_ROOT": str(root),
                    "PYTHONUNBUFFERED": "1",
                }
            )
            execution = execute_run_plan(plan, env)
            verification_reached = _run_receipt_reached(receipt_path, token, task_id, plan["file"])

        with progress_write_lock(root):
            recover_pending_operations(root)
            ledger = load_run_operations(root)
            executing = ledger["operations"].get(operation_id)
            _validated_run_operation_record(operation_id, executing, required_status="executing")
            latest = load_progress(root)
            if task_id not in latest["tasks"]:
                raise ValueError("run_task_scope_changed")
            base_state = dict(latest["tasks"][task_id])
            target = json.loads(json.dumps(latest))
            target_state = target["tasks"][task_id]
            completion_applied = (
                execution["result"] == "ok" and verification_reached and not base_state["done"]
            )
            if completion_applied:
                target_state["done"] = True
                target_state["done_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            execution.update(
                {
                    "verification_reached": verification_reached,
                    "completion_applied": completion_applied,
                }
            )
            target["revision"] = max(0, int(latest.get("revision") or 0)) + 1
            event = build_action_event(
                task_id,
                base_state.get("lane", ACTIVE_COURSE_ID),
                "run_exercise",
                execution["result"],
                root=root,
                note=f"Web UI 执行练习脚本：{plan['file']}；结果：{execution['result']}",
                evidence_path=sandbox_path,
                operation_id=operation_id,
                details={
                    "script_path": execution["script_path"],
                    "sandbox_path": execution["sandbox_path"],
                    "returncode": execution["returncode"],
                    "timed_out": execution["timed_out"],
                    "duration_ms": execution["duration_ms"],
                    "stdout_excerpt": execution["stdout"],
                    "stderr_excerpt": execution["stderr"],
                    "verification_reached": execution["verification_reached"],
                    "completion_applied": execution["completion_applied"],
                },
            )
            ledger["operations"][operation_id] = {
                "status": "pending",
                "request": request,
                "request_fingerprint": request_fingerprint,
                "started_at": executing["started_at"],
                "base_revision": latest["revision"],
                "target_revision": target["revision"],
                "base_task_state": base_state,
                "task_state": dict(target_state),
                "base_progress_fingerprint": progress_snapshot_fingerprint(latest),
                "target_progress_fingerprint": progress_snapshot_fingerprint(target),
                "execution": execution,
                "event": event,
                "prepared_at": datetime.datetime.now().isoformat(timespec="seconds"),
            }
            save_run_operations(ledger, root)
            committed, feedback = _apply_pending_run_operation(ledger, operation_id, root)
            return _run_operation_response(
                ledger["operations"][operation_id],
                committed,
                feedback,
                replayed=False,
            )


TERMINAL_TIMEOUT_SECONDS = 10
MAX_TERMINAL_OUTPUT_CHARS = 6000
TERMINAL_ALLOWED_COMMANDS = {
    "awk",
    "bash",
    "cat",
    "chmod",
    "cp",
    "date",
    "echo",
    "find",
    "git",
    "grep",
    "head",
    "less",
    "ls",
    "man",
    "mkdir",
    "mv",
    "ps",
    "printf",
    "pwd",
    "python3",
    "rm",
    "sed",
    "sh",
    "sort",
    "tail",
    "touch",
    "uniq",
    "wc",
    "whoami",
}
TERMINAL_DENIED_PATTERNS = [
    r"`",
    r"\$\(",
    r";",
    r"&&",
    r"\|\|",
    r"\b(?:sudo|su|ssh|scp|rsync|curl|wget|nc|netcat)\b",
    r"\brmdir\b",
    r"\brm\s+-",
    r"\brm\b[^\n]*(?:~|\$HOME|\*)",
    r"\bless\s+[-+]",
    r"\bman\s+-",
    r"\b(?:bash|sh)\s+-c\b",
    r"\b(?:python|python3)\s+-c\b",
    r"\bgit\s+(?:clone|fetch|pull|push|remote)\b",
    r"\b(?:chmod|mv|cp)\b[^\n]*(?:/Users/|/etc/|/var/|/System/|/Applications/)",
    r"(?:^|[\s\"'])/(?!dev/null(?:$|[\s\"']))",
    r"\.\.",
    r"<",
]


def terminal_root() -> Path:
    root = Path.home() / "cli-lab"
    root.mkdir(parents=True, exist_ok=True)
    return root.resolve()


def terminal_path_candidate(raw: str, root: Path, current: Path | None = None) -> Path:
    """Resolve user-facing terminal paths into the ~/cli-lab sandbox."""
    text = raw.strip() or "~"
    if text in {"~", "$HOME"}:
        return root
    for prefix in ("~/cli-lab", "$HOME/cli-lab"):
        if text == prefix:
            return root
        if text.startswith(prefix + "/"):
            return root / text[len(prefix) + 1 :]
    if text.startswith("~/"):
        return root / text[2:]
    if text.startswith("$HOME/"):
        return root / text[len("$HOME/") :]
    if text.startswith("/"):
        return Path(text)
    return (current or root) / text


def clamp_terminal_cwd(cwd: str | None = None) -> Path:
    root = terminal_root()
    if not cwd:
        return root
    candidate = terminal_path_candidate(str(cwd), root)
    resolved = candidate.resolve()
    if resolved != root and root not in resolved.parents:
        raise ValueError("terminal_cwd_outside_sandbox")
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def resolve_terminal_cd(current: Path, target: str | None) -> Path:
    root = terminal_root()
    candidate = terminal_path_candidate(target or "~", root, current=current)
    resolved = candidate.resolve()
    if resolved != root and root not in resolved.parents:
        raise ValueError("terminal_path_outside_sandbox")
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def terminal_command_words(command: str) -> list[str]:
    normalized = command.replace("|", " | ").replace(">>", " >> ").replace(">", " > ")
    try:
        tokens = shlex.split(normalized)
    except ValueError as exc:
        raise ValueError(f"terminal_parse_error:{exc}") from exc
    words: list[str] = []
    expect_command = True
    for token in tokens:
        if token in {"|", ">", ">>"}:
            expect_command = token == "|"
            continue
        if expect_command:
            words.append(token)
            expect_command = False
    return words


def validate_terminal_command(command: str) -> None:
    if not command.strip():
        raise ValueError("terminal_empty_command")
    if len(command) > 500:
        raise ValueError("terminal_command_too_long")
    if any(ord(ch) < 32 and ch not in "\t\n" for ch in command):
        raise ValueError("terminal_control_character")
    for pattern in TERMINAL_DENIED_PATTERNS:
        if re.search(pattern, command):
            raise ValueError("terminal_command_blocked")
    words = terminal_command_words(command)
    if not words:
        raise ValueError("terminal_no_command")
    for word in words:
        base = Path(word).name
        if base not in TERMINAL_ALLOWED_COMMANDS:
            raise ValueError(f"terminal_command_not_allowed:{base}")


def append_terminal_command_event(
    command: str,
    cwd: Path,
    result: str,
    root: Path | None = None,
    task_id: str = "",
    returncode: int | None = None,
    stdout: str = "",
    stderr: str = "",
    duration_ms: int = 0,
) -> str:
    command_id = str(uuid.uuid4())
    payload = {
        "command_id": command_id,
        "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
        "cwd": str(cwd),
        "command": command,
        "result": result,
        "task_id": task_id,
        "returncode": returncode,
        "duration_ms": duration_ms,
        "stdout_excerpt": output_excerpt(stdout, MAX_TERMINAL_OUTPUT_CHARS),
        "stderr_excerpt": output_excerpt(stderr, MAX_TERMINAL_OUTPUT_CHARS),
    }
    with progress_write_lock(root):
        recover_pending_operations(root)
        commands = load_terminal_commands(root)
        commands.append(payload)
        write_terminal_commands(commands, root)
    return command_id


def load_terminal_commands(root: Path | None = None) -> list[dict[str, Any]]:
    path = terminal_log_path(root)
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def write_terminal_commands(commands: list[dict[str, Any]], root: Path | None = None) -> None:
    path = terminal_log_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_text(
        path,
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in commands),
    )


def terminal_state(cwd: str | None = None) -> dict[str, Any]:
    root = terminal_root()
    current = clamp_terminal_cwd(cwd)
    cwd_display = "~/cli-lab" if current == root else "~/cli-lab/" + str(current.relative_to(root))
    return {
        "root": str(root),
        "cwd": str(current),
        "cwd_display": cwd_display,
        "allowed": sorted(TERMINAL_ALLOWED_COMMANDS),
        "timeout_seconds": TERMINAL_TIMEOUT_SECONDS,
    }


def run_terminal_command(
    command: str,
    cwd: str | None = None,
    root: Path | None = None,
    task_id: str = "",
) -> dict[str, Any]:
    root = root or repo_root()
    current = clamp_terminal_cwd(cwd)
    command = command.strip()

    if command == "clear":
        state = terminal_state(str(current))
        return {
            "ok": True,
            "result": "ok",
            "command": command,
            "cwd": state["cwd"],
            "cwd_display": state["cwd_display"],
            "stdout": "",
            "stderr": "",
            "clear": True,
        }

    if command.startswith("cd") and (command == "cd" or command.startswith("cd ")):
        try:
            parts = shlex.split(command)
        except ValueError as exc:
            raise ValueError(f"terminal_parse_error:{exc}") from exc
        if len(parts) > 2:
            raise ValueError("terminal_cd_too_many_args")
        new_cwd = resolve_terminal_cd(current, parts[1] if len(parts) == 2 else "~")
        command_id = append_terminal_command_event(
            command,
            new_cwd,
            "ok",
            root=root,
            task_id=task_id,
            returncode=0,
            stdout="",
            stderr="",
            duration_ms=0,
        )
        state = terminal_state(str(new_cwd))
        return {
            "ok": True,
            "result": "ok",
            "command_id": command_id,
            "command": command,
            "cwd": state["cwd"],
            "cwd_display": state["cwd_display"],
            "returncode": 0,
            "stdout": "",
            "stderr": "",
        }

    validate_terminal_command(command)
    env = os.environ.copy()
    lab_root = terminal_root()
    env.update(
        {
            "HOME": str(lab_root),
            "PWD": str(current),
            "COMPUTER_STUDY_PLAN_TERMINAL": "1",
            "LESS": "FRX",
            "MANPAGER": "cat",
            "PAGER": "cat",
            "PYTHONUNBUFFERED": "1",
            "TERM": "xterm-256color",
        }
    )

    started = time.monotonic()
    timed_out = False
    returncode: int | None = None
    stdout = ""
    stderr = ""
    try:
        proc = subprocess.run(
            ["/bin/zsh", "-lc", command],
            cwd=current,
            env=env,
            input="",
            capture_output=True,
            text=True,
            timeout=TERMINAL_TIMEOUT_SECONDS,
            check=False,
        )
        returncode = proc.returncode
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
        result = "ok" if proc.returncode == 0 else "failed"
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        stdout = output_excerpt(exc.stdout, MAX_TERMINAL_OUTPUT_CHARS)
        stderr = output_excerpt(exc.stderr, MAX_TERMINAL_OUTPUT_CHARS)
        result = "timeout"

    duration_ms = int((time.monotonic() - started) * 1000)
    command_id = append_terminal_command_event(
        command,
        current,
        result,
        root=root,
        task_id=task_id,
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
        duration_ms=duration_ms,
    )
    state = terminal_state(str(current))
    return {
        "ok": True,
        "result": result,
        "command_id": command_id,
        "command": command,
        "cwd": state["cwd"],
        "cwd_display": state["cwd_display"],
        "returncode": returncode,
        "timed_out": timed_out,
        "duration_ms": duration_ms,
        "stdout": output_excerpt(stdout, MAX_TERMINAL_OUTPUT_CHARS),
        "stderr": output_excerpt(stderr, MAX_TERMINAL_OUTPUT_CHARS),
    }


def build_feedback_payload(progress: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
    tasks = progress.get("tasks", {})
    grouped = events_by_task(events)

    def not_started_suggestion(lane: str) -> str:
        if lane == ACTIVE_COURSE_ID:
            return "先阅读 Linux 资料，或完成一条最小终端练习。"
        return "先阅读资料，或完成一条最小练习。"

    feedback_items: dict[str, dict[str, Any]] = {}
    for task_id, info in tasks.items():
        task_events = grouped.get(task_id, [])
        action_count = len(task_events)
        last_event = task_events[-1] if task_events else {}
        done = bool(info.get("done"))
        lane = info.get("lane", ACTIVE_COURSE_ID)

        if done:
            feedback_type = "completed"
            message = "已完成，建议进入复盘或继续下一个任务。"
            next_suggestion = "继续同主线下一个任务，或安排 10 分钟复盘。"
        elif action_count == 0:
            feedback_type = "not_started"
            message = "尚未开始，建议先做一个 15 分钟启动动作。"
            next_suggestion = not_started_suggestion(lane)
        elif last_event.get("action_type") == "undo_done":
            feedback_type = "not_started"
            message = "最近一次动作是撤销完成，当前任务未完成。"
            next_suggestion = "重新阅读资料后，再用网页按钮完成记录。"
        else:
            feedback_type = "in_progress"
            message = "已产生学习动作但尚未完成，建议收敛到最小闭环。"
            next_suggestion = "先把当前任务推进到完成，再切换任务。"

        feedback_items[task_id] = {
            "task_id": task_id,
            "lane": lane,
            "done": done,
            "action_count": action_count,
            "last_action_type": last_event.get("action_type"),
            "last_action_at": last_event.get("timestamp"),
            "feedback_type": feedback_type,
            "message": message,
            "next_suggestion": next_suggestion,
        }

    return {
        "version": 1,
        "source": {
            "progress_file": "progress.json",
            "action_log_file": "records/action_logs/events.jsonl",
        },
        "feedback": feedback_items,
    }


def write_feedback_payload(
    progress: dict[str, Any],
    root: Path | None = None,
    events: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    events = load_action_events(root) if events is None else events
    payload = build_feedback_payload(progress, events)
    path = feedback_json_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return payload


def save_id_from_label(label: str, fallback: str = "save") -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", label.strip()).strip("-._").lower()
    return (slug or fallback)[:48]


def summarize_save_payload(payload: dict[str, Any]) -> dict[str, Any]:
    progress = payload.get("progress") or {}
    tasks = progress.get("tasks") or {}
    events = payload.get("events") or []
    terminal_commands = payload.get("terminal_commands") or []
    done_count = sum(1 for item in tasks.values() if isinstance(item, dict) and item.get("done"))
    return {
        "total": len(tasks),
        "done_count": done_count,
        "event_count": len(events) if isinstance(events, list) else 0,
        "terminal_command_count": len(terminal_commands) if isinstance(terminal_commands, list) else 0,
    }


def _create_progress_save_unlocked(
    root: Path | None = None,
    label: str = "",
    personal: dict[str, Any] | None = None,
    reason: str = "manual",
) -> dict[str, Any]:
    root = root or repo_root()
    data = load_progress(root)
    events = load_action_events(root)
    feedback = read_feedback_payload(root)
    terminal_commands = load_terminal_commands(root)
    created_at = datetime.datetime.now().isoformat(timespec="seconds")
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    slug = save_id_from_label(label or reason, fallback=reason or "save")
    save_id = f"{stamp}-{slug}"
    save_dir = saves_dir_path(root)
    save_dir.mkdir(parents=True, exist_ok=True)
    path = save_dir / f"{save_id}.json"
    if path.exists():
        save_id = f"{save_id}-{uuid.uuid4().hex[:6]}"
        path = save_dir / f"{save_id}.json"

    payload = {
        "version": 1,
        "save_id": save_id,
        "label": label.strip() or ("读档前自动恢复点" if reason == "auto-before-load" else "手动存档"),
        "reason": reason,
        "created_at": created_at,
        "summary": {},
        "progress": data,
        "events": events,
        "feedback": feedback,
        "terminal_commands": terminal_commands,
        "personal": personal or {},
    }
    payload["summary"] = summarize_save_payload(payload)
    _atomic_write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return {
        "save_id": save_id,
        "label": payload["label"],
        "reason": reason,
        "created_at": created_at,
        "path": str(path.relative_to(root)),
        "summary": payload["summary"],
    }


def create_progress_save(
    root: Path | None = None,
    label: str = "",
    personal: dict[str, Any] | None = None,
    reason: str = "manual",
) -> dict[str, Any]:
    root = root or repo_root()
    with progress_write_lock(root):
        recover_pending_operations(root)
        return _create_progress_save_unlocked(root, label, personal, reason)


def list_progress_saves(root: Path | None = None) -> list[dict[str, Any]]:
    root = root or repo_root()
    save_dir = saves_dir_path(root)
    if not save_dir.exists():
        return []
    rows: list[dict[str, Any]] = []
    for path in save_dir.glob("*.json"):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            rows.append(
                {
                    "save_id": str(payload.get("save_id") or path.stem),
                    "label": str(payload.get("label") or path.stem),
                    "reason": str(payload.get("reason") or "manual"),
                    "created_at": str(payload.get("created_at") or ""),
                    "path": str(path.relative_to(root)),
                    "summary": payload.get("summary") or summarize_save_payload(payload),
                }
            )
        except Exception:
            rows.append(
                {
                    "save_id": path.stem,
                    "label": path.stem,
                    "reason": "unreadable",
                    "created_at": "",
                    "path": str(path.relative_to(root)),
                    "summary": {},
                    "error": "invalid_save_file",
                }
            )
    return sorted(rows, key=lambda row: row.get("created_at", ""), reverse=True)


def progress_save_path(save_id: str, root: Path | None = None) -> Path:
    if not re.match(r"^[A-Za-z0-9._-]+$", save_id):
        raise ValueError("invalid_save_id")
    path = saves_dir_path(root) / f"{save_id}.json"
    save_dir = saves_dir_path(root).resolve()
    resolved = path.resolve()
    if save_dir not in resolved.parents:
        raise ValueError("invalid_save_path")
    return path


def load_progress_save(
    save_id: str,
    root: Path | None = None,
    personal: dict[str, Any] | None = None,
) -> dict[str, Any]:
    root = root or repo_root()
    with progress_write_lock(root):
        recover_pending_operations(root)
        path = progress_save_path(save_id, root)
        if not path.exists():
            raise FileNotFoundError(save_id)
        payload = json.loads(path.read_text(encoding="utf-8"))
        progress = payload.get("progress")
        if not isinstance(progress, dict) or not isinstance(progress.get("tasks"), dict):
            raise ValueError("invalid_save_payload")

        restored = normalize_progress(json.loads(json.dumps(progress)))
        current = load_progress(root)
        backup = _create_progress_save_unlocked(
            root=root,
            label=f"读档前恢复点 · {save_id}",
            personal=personal,
            reason="auto-before-load",
        )
        restored["revision"] = max(0, int(current.get("revision") or 0)) + 1
        events = payload.get("events") if isinstance(payload.get("events"), list) else []
        terminal_commands = (
            payload.get("terminal_commands")
            if isinstance(payload.get("terminal_commands"), list)
            else []
        )
        paths = [
            progress_json_path(root),
            progress_js_path(root),
            action_log_path(root),
            feedback_json_path(root),
            terminal_log_path(root),
        ]
        preimages = _capture_file_preimages(paths)
        try:
            save_progress(restored, root)
            sync_progress_data_js(restored, root)
            write_action_events(events, root)
            if "terminal_commands" in payload:
                write_terminal_commands(terminal_commands, root)
            feedback = write_feedback_payload(restored, root, events=events)
        except Exception:
            _restore_file_preimages(preimages)
            raise
        return {
            "save_id": save_id,
            "label": str(payload.get("label") or save_id),
            "created_at": str(payload.get("created_at") or ""),
            "backup": backup,
            "summary": summarize_save_payload(payload),
            "personal": payload.get("personal") or {},
            "revision": restored["revision"],
            "tasks": restored.get("tasks", {}),
            "lanes": restored.get("lanes", {}),
            "feedback": feedback.get("feedback", {}),
        }


def task_transaction_paths(root: Path | None = None) -> list[Path]:
    return [
        progress_json_path(root),
        progress_js_path(root),
        action_log_path(root),
        feedback_json_path(root),
        task_operations_path(root),
    ]


def _apply_pending_task_operation(
    ledger: dict[str, Any],
    operation_id: str,
    root: Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Roll one durable pending task operation forward to a coherent snapshot."""
    record = ledger.get("operations", {}).get(operation_id)
    validated = _validated_task_operation_record(operation_id, record, required_status="pending")
    request = validated["request"]
    event = validated["event"]
    task_state = validated["task_state"]
    target_revision = validated["target_revision"]

    data = load_progress(root)
    task_id = request["task_id"]
    if task_id not in data.get("tasks", {}):
        raise ValueError("pending_task_scope_changed")
    current_revision = max(0, int(data.get("revision") or 0))
    base_revision = validated["base_revision"]
    if current_revision not in {base_revision, target_revision}:
        raise ValueError("pending_task_revision_conflict")
    expected_current_task = validated["base_task_state"] if current_revision == base_revision else task_state
    if data["tasks"][task_id] != expected_current_task:
        raise ValueError("pending_task_state_conflict")
    events = load_action_events(root)
    matching_events = [item for item in events if item.get("action_id") == event["action_id"]]
    if len(matching_events) > 1:
        raise ValueError("pending_action_event_conflict")
    matching_event = matching_events[0] if matching_events else None
    if matching_event and matching_event != event:
        raise ValueError("pending_action_event_conflict")
    if current_revision == base_revision and matching_event:
        raise ValueError("pending_action_event_order")
    if current_revision == base_revision:
        data["tasks"][task_id] = dict(task_state)
        data["revision"] = target_revision
        save_progress(data, root)
    sync_progress_data_js(data, root)
    if not matching_event:
        events.append(event)
        write_action_events(events, root)
    feedback = write_feedback_payload(data, root, events=events)
    record["status"] = "committed"
    record["committed_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    save_task_operations(ledger, root)
    return data, feedback


def _apply_pending_run_operation(
    ledger: dict[str, Any],
    operation_id: str,
    root: Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Roll one durable run outcome forward without executing its script again."""
    record = ledger.get("operations", {}).get(operation_id)
    validated = _validated_run_operation_record(operation_id, record, required_status="pending")
    request = validated["request"]
    event = validated["event"]
    target_revision = validated["target_revision"]
    base_revision = validated["base_revision"]
    data = load_progress(root)
    task_id = request["task_id"]
    if task_id not in data.get("tasks", {}):
        raise ValueError("pending_run_scope_changed")
    current_revision = max(0, int(data.get("revision") or 0))
    if current_revision not in {base_revision, target_revision}:
        raise ValueError("pending_run_revision_conflict")
    expected_fingerprint = (
        validated["base_progress_fingerprint"]
        if current_revision == base_revision
        else validated["target_progress_fingerprint"]
    )
    if progress_snapshot_fingerprint(data) != expected_fingerprint:
        raise ValueError("pending_run_progress_conflict")
    expected_task = (
        validated["base_task_state"]
        if current_revision == base_revision
        else validated["task_state"]
    )
    if data["tasks"][task_id] != expected_task:
        raise ValueError("pending_run_task_conflict")

    events = load_action_events(root)
    matches = [item for item in events if item.get("action_id") == event["action_id"]]
    if len(matches) > 1 or (matches and matches[0] != event):
        raise ValueError("pending_run_event_conflict")
    if current_revision == base_revision and matches:
        raise ValueError("pending_run_event_order")
    if current_revision == base_revision:
        data["tasks"][task_id] = dict(validated["task_state"])
        data["revision"] = target_revision
        save_progress(data, root)
    sync_progress_data_js(data, root)
    if not matches:
        events.append(event)
        write_action_events(events, root)
    feedback = write_feedback_payload(data, root, events=events)
    record["status"] = "committed"
    record["committed_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    save_run_operations(ledger, root)
    return data, feedback


def recover_pending_task_operations(root: Path | None = None) -> None:
    """Complete the only kind of interrupted state transaction under the caller's lock."""
    ledger = load_task_operations(root)
    for operation_id, record in ledger.get("operations", {}).items():
        _validated_task_operation_record(operation_id, record)
    pending = [
        operation_id
        for operation_id, record in ledger.get("operations", {}).items()
        if isinstance(record, dict) and record.get("status") == "pending"
    ]
    if len(pending) > 1:
        raise ValueError("multiple_pending_task_operations")
    if pending:
        _apply_pending_task_operation(ledger, pending[0], root)


def recover_pending_run_operations(root: Path | None = None) -> None:
    """Validate every run record and roll a durable known outcome forward once."""
    ledger = load_run_operations(root)
    for operation_id, record in ledger.get("operations", {}).items():
        _validated_run_operation_record(operation_id, record)
    pending = [
        operation_id
        for operation_id, record in ledger.get("operations", {}).items()
        if isinstance(record, dict) and record.get("status") == "pending"
    ]
    if len(pending) > 1:
        raise ValueError("multiple_pending_run_operations")
    if pending:
        _apply_pending_run_operation(ledger, pending[0], root)


def recover_pending_operations(root: Path | None = None) -> None:
    """Validate both ledgers before allowing either transaction to write."""
    task_ledger = load_task_operations(root)
    run_ledger = load_run_operations(root)
    for operation_id, record in task_ledger.get("operations", {}).items():
        _validated_task_operation_record(operation_id, record)
    for operation_id, record in run_ledger.get("operations", {}).items():
        _validated_run_operation_record(operation_id, record)
    task_pending = [
        operation_id
        for operation_id, record in task_ledger.get("operations", {}).items()
        if isinstance(record, dict) and record.get("status") == "pending"
    ]
    run_pending = [
        operation_id
        for operation_id, record in run_ledger.get("operations", {}).items()
        if isinstance(record, dict) and record.get("status") == "pending"
    ]
    if len(task_pending) + len(run_pending) > 1:
        raise ValueError("multiple_pending_operations")
    if task_pending:
        _apply_pending_task_operation(task_ledger, task_pending[0], root)
    elif run_pending:
        _apply_pending_run_operation(run_ledger, run_pending[0], root)


def sync_progress_state(root: Path | None = None) -> dict[str, Any]:
    with progress_write_lock(root):
        recover_pending_operations(root)
        data = load_progress(root)
        sync_progress_data_js(data, root)
        return data


def mark_task(
    task_id: str,
    undo: bool = False,
    root: Path | None = None,
    note: str = "",
    evidence_path: str = "",
    operation_id: str = "",
) -> dict[str, Any]:
    if operation_id and not OPERATION_ID_RE.fullmatch(operation_id):
        raise ValueError("invalid_operation_id")
    request = task_operation_request(task_id, undo, note, evidence_path)
    request_fingerprint = task_operation_fingerprint(request)
    with task_mutation_lock(task_id, root), progress_write_lock(root):
        recover_pending_operations(root)
        data = load_progress(root)
        tasks = data["tasks"]
        if task_id not in tasks:
            raise KeyError(task_id)

        ledger = load_task_operations(root)
        for ledger_operation_id, ledger_record in ledger.get("operations", {}).items():
            _validated_task_operation_record(ledger_operation_id, ledger_record)

        if operation_id:
            existing_record = ledger["operations"].get(operation_id)
            if existing_record:
                _validated_task_operation_record(operation_id, existing_record)
            if existing_record and existing_record.get("request_fingerprint") != request_fingerprint:
                raise ValueError("operation_id_conflict")
            existing = existing_record.get("event") if isinstance(existing_record, dict) else None
            if not existing:
                # Compatibility with events produced before the independent operation ledger.
                existing = next(
                    (
                        event for event in reversed(load_action_events(root))
                        if event.get("operation_id") == operation_id
                    ),
                    None,
                )
            if existing:
                _validated_task_action_event(existing, request, operation_id)
                if (
                    existing.get("task_id") != task_id
                    or existing.get("action_type") != ("undo_done" if undo else "mark_done")
                    or (not existing_record and task_operation_fingerprint(task_operation_request(
                        task_id,
                        undo,
                        str(existing.get("note") or ""),
                        str(existing.get("evidence_path") or ""),
                    )) != request_fingerprint)
                ):
                    raise ValueError("operation_id_conflict")
                if existing_record:
                    current_matches = [
                        event for event in load_action_events(root)
                        if event.get("action_id") == existing.get("action_id")
                    ]
                    if len(current_matches) != 1 or current_matches[0] != existing:
                        raise ValueError("operation_event_not_in_current_history")
                task = tasks[task_id]
                total = len(tasks)
                feedback_payload = read_feedback_payload(root)
                return {
                    "ok": True,
                    "task_id": task_id,
                    "done": bool(task.get("done")),
                    "done_at": task.get("done_at"),
                    "lane": task.get("lane", ACTIVE_COURSE_ID),
                    "result": "replayed_operation",
                    "message": f"replayed:{task_id}",
                    "action_id": existing.get("action_id"),
                    "event": dict(existing),
                    "operation_id": operation_id,
                    "revision": max(0, int(data.get("revision") or 0)),
                    "total": total,
                    "done_count": sum(1 for item in tasks.values() if item.get("done")),
                    "tasks": tasks,
                    "lanes": data.get("lanes", {}),
                    "feedback": feedback_payload.get("feedback", {}),
                }

        task = tasks[task_id]
        if "lane" not in task:
            task["lane"] = ACTIVE_COURSE_ID
        base_task_state = dict(task)

        action_type = "undo_done" if undo else "mark_done"
        result = "ok"

        if undo and not task.get("done"):
            result = "noop_already_undone"
            message = f"already_undone:{task_id}"
        elif undo:
            task["done"] = False
            task["done_at"] = None
            message = f"undone:{task_id}"
        elif task.get("done"):
            result = "noop_already_done"
            message = f"already_done:{task_id}"
        else:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            task["done"] = True
            task["done_at"] = now
            message = f"done:{task_id}:{now}"

        data["revision"] = max(0, int(data.get("revision") or 0)) + 1
        event = build_action_event(
            task_id,
            task.get("lane", ACTIVE_COURSE_ID),
            action_type,
            result,
            root=root,
            note=note,
            evidence_path=evidence_path,
            operation_id=operation_id,
        )
        operation_key = operation_id or f"legacy:{event['action_id']}"
        ledger["operations"][operation_key] = {
            "status": "pending",
            "request": request,
            "request_fingerprint": request_fingerprint,
            "base_revision": data["revision"] - 1,
            "target_revision": data["revision"],
            "base_task_state": base_task_state,
            "task_state": dict(task),
            "event": event,
            "prepared_at": datetime.datetime.now().isoformat(timespec="seconds"),
        }
        preimages = _capture_file_preimages(task_transaction_paths(root))
        try:
            save_task_operations(ledger, root)
            data, feedback = _apply_pending_task_operation(ledger, operation_key, root)
        except Exception:
            _restore_file_preimages(preimages)
            raise
        tasks = data["tasks"]
        task = tasks[task_id]

        total = len(tasks)
        done_count = sum(1 for item in tasks.values() if item.get("done"))
        return {
            "ok": True,
            "task_id": task_id,
            "done": bool(task.get("done")),
            "done_at": task.get("done_at"),
            "lane": task.get("lane", ACTIVE_COURSE_ID),
            "result": result,
            "message": message,
            "action_id": event["action_id"],
            "event": dict(event),
            "operation_id": operation_id,
            "revision": data["revision"],
            "total": total,
            "done_count": done_count,
            "tasks": tasks,
            "lanes": data.get("lanes", {}),
            "feedback": feedback.get("feedback", {}),
        }


def list_status(root: Path | None = None) -> dict[str, Any]:
    data = load_progress(root)
    tasks = data["tasks"]
    done_count = sum(1 for item in tasks.values() if item.get("done"))
    return {
        "version": data.get("version", 2),
        "revision": max(0, int(data.get("revision") or 0)),
        "lanes": data.get("lanes", {}),
        "tasks": tasks,
        "total": len(tasks),
        "done_count": done_count,
    }
