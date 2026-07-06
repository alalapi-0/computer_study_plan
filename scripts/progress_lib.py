#!/usr/bin/env python3
"""Shared progress read/write helpers for mark_done.sh and progress_server.py."""

from __future__ import annotations

import datetime
import json
import os
import re
import shlex
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any

DEFAULT_LANES: dict[str, dict[str, str]] = {
    "engineering": {
        "title": "工程实操线",
        "description": "Linux/Shell/Git/Python/工程化/服务化/AI 工程/VPS",
    },
    "soft_exam": {
        "title": "软考中级线",
        "description": "默认软件设计师，高分/满分导向",
    },
    "math2": {
        "title": "数学二线",
        "description": "高等数学 + 线性代数（长期低强度）",
    },
    "cs408": {
        "title": "408/0854 线",
        "description": "数据结构 + 计组 + 操作系统 + 计算机网络",
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


def load_progress(root: Path | None = None) -> dict[str, Any]:
    path = progress_json_path(root)
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return normalize_progress(data)


def normalize_progress(data: dict[str, Any]) -> dict[str, Any]:
    data["version"] = 2
    lanes = data.setdefault("lanes", {})
    for key, meta in DEFAULT_LANES.items():
        lanes.setdefault(key, dict(meta))
    tasks = data.setdefault("tasks", {})
    for info in tasks.values():
        if isinstance(info, dict) and "lane" not in info:
            info["lane"] = "engineering"
    return data


def save_progress(data: dict[str, Any], root: Path | None = None) -> None:
    path = progress_json_path(root)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


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
        "lanes": data.get("lanes", {}),
        "tasks": data.get("tasks", {}),
    }
    body = json.dumps(payload, ensure_ascii=False, indent=2)
    content = (
        "// Auto-generated — DO NOT edit manually\n"
        "// Source of truth: progress.json\n"
        f"window.PROGRESS_DATA = {body};\n"
    )
    js_path.write_text(content, encoding="utf-8")


def resolve_round_id(task_id: str) -> str:
    if task_id.startswith(("w1-", "w2-", "w3-", "fin-")):
        return "round_00"
    if task_id.startswith("r") and len(task_id) >= 4 and task_id[1:3].isdigit():
        return f"round_{int(task_id[1:3]):02d}"
    if task_id.startswith("soft_exam-"):
        return "soft_exam"
    if task_id.startswith("math2-"):
        return "math2"
    if task_id.startswith("cs408-"):
        return "cs408"
    return "unknown"


def append_action_event(
    task_id: str,
    lane: str,
    action_type: str,
    result: str,
    root: Path | None = None,
    note: str = "",
    evidence_path: str = "",
    details: dict[str, Any] | None = None,
) -> str:
    log_file = action_log_path(root)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    action_id = str(uuid.uuid4())
    event = {
        "action_id": action_id,
        "task_id": task_id,
        "round_id": resolve_round_id(task_id),
        "lane": lane,
        "action_type": action_type,
        "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
        "result": result,
        "note": note,
        "evidence_path": evidence_path,
    }
    if details:
        event["details"] = details
    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    return action_id


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


def run_task_script(task_id: str, root: Path | None = None) -> dict[str, Any]:
    root = root or repo_root()
    data = load_progress(root)
    tasks = data["tasks"]
    if task_id not in tasks:
        raise KeyError(task_id)

    plan = runnable_task_execution_plan(task_id, root)
    plan["sandbox"].mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env.update(
        {
            "PROGRESS_UI_RUN": "1",
            "COMPUTER_STUDY_PLAN_ROOT": str(root),
            "PYTHONUNBUFFERED": "1",
        }
    )

    started = time.monotonic()
    timed_out = False
    returncode: int | None = None
    stdout = ""
    stderr = ""
    try:
        proc = subprocess.run(
            plan["command"],
            cwd=plan["sandbox"],
            env=env,
            input="",
            capture_output=True,
            text=True,
            timeout=RUN_TIMEOUT_SECONDS,
            check=False,
        )
        returncode = proc.returncode
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
        result = "ok" if proc.returncode == 0 else "failed"
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        stdout = output_excerpt(exc.stdout)
        stderr = output_excerpt(exc.stderr)
        result = "timeout"

    duration_ms = int((time.monotonic() - started) * 1000)

    latest = load_progress(root)
    task = latest["tasks"].get(task_id, tasks[task_id])
    note = f"Web UI 执行练习脚本：{plan['file']}；结果：{result}"
    action_id = append_action_event(
        task_id,
        task.get("lane", "engineering"),
        "run_exercise",
        result,
        root=root,
        note=note,
        evidence_path=str(plan["sandbox"]),
        details={
            "script_path": plan["file"],
            "sandbox_path": str(plan["sandbox"]),
            "returncode": returncode,
            "timed_out": timed_out,
            "duration_ms": duration_ms,
            "stdout_excerpt": output_excerpt(stdout),
            "stderr_excerpt": output_excerpt(stderr),
        },
    )
    feedback = write_feedback_payload(latest, root)

    total = len(latest["tasks"])
    done_count = sum(1 for item in latest["tasks"].values() if item.get("done"))
    return {
        "ok": True,
        "execution_ok": result == "ok",
        "task_id": task_id,
        "action_id": action_id,
        "result": result,
        "returncode": returncode,
        "timed_out": timed_out,
        "duration_ms": duration_ms,
        "script_path": plan["file"],
        "sandbox_path": str(plan["sandbox"]),
        "stdout": output_excerpt(stdout),
        "stderr": output_excerpt(stderr),
        "tasks": latest.get("tasks", {}),
        "lanes": latest.get("lanes", {}),
        "feedback": feedback.get("feedback", {}),
        "total": total,
        "done_count": done_count,
    }


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
    log_file = terminal_log_path(root)
    log_file.parent.mkdir(parents=True, exist_ok=True)
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
    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
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
    path.write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in commands),
        encoding="utf-8",
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

    feedback_items: dict[str, dict[str, Any]] = {}
    for task_id, info in tasks.items():
        task_events = grouped.get(task_id, [])
        action_count = len(task_events)
        last_event = task_events[-1] if task_events else {}
        done = bool(info.get("done"))
        lane = info.get("lane", "engineering")

        if done:
            feedback_type = "completed"
            message = "已完成，建议进入复盘或继续下一个任务。"
            next_suggestion = "继续同主线下一个任务，或安排 10 分钟复盘。"
        elif action_count == 0:
            feedback_type = "not_started"
            message = "尚未开始，建议先做一个 15 分钟启动动作。"
            next_suggestion = "先阅读资料，或完成一条最小练习。"
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


def write_feedback_payload(progress: dict[str, Any], root: Path | None = None) -> dict[str, Any]:
    events = load_action_events(root)
    payload = build_feedback_payload(progress, events)
    path = feedback_json_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
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


def create_progress_save(
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
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "save_id": save_id,
        "label": payload["label"],
        "reason": reason,
        "created_at": created_at,
        "path": str(path.relative_to(root)),
        "summary": payload["summary"],
    }


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
    path = progress_save_path(save_id, root)
    if not path.exists():
        raise FileNotFoundError(save_id)
    payload = json.loads(path.read_text(encoding="utf-8"))
    progress = payload.get("progress")
    if not isinstance(progress, dict) or not isinstance(progress.get("tasks"), dict):
        raise ValueError("invalid_save_payload")

    backup = create_progress_save(
        root=root,
        label=f"读档前恢复点 · {save_id}",
        personal=personal,
        reason="auto-before-load",
    )

    restored = normalize_progress(progress)
    save_progress(restored, root)
    sync_progress_data_js(restored, root)

    events = payload.get("events") if isinstance(payload.get("events"), list) else []
    log_file = action_log_path(root)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text(
        "".join(json.dumps(event, ensure_ascii=False) + "\n" for event in events),
        encoding="utf-8",
    )
    if "terminal_commands" in payload:
        terminal_commands = payload.get("terminal_commands") if isinstance(payload.get("terminal_commands"), list) else []
        write_terminal_commands(terminal_commands, root)
    feedback = write_feedback_payload(restored, root)
    return {
        "save_id": save_id,
        "label": str(payload.get("label") or save_id),
        "created_at": str(payload.get("created_at") or ""),
        "backup": backup,
        "summary": summarize_save_payload(payload),
        "personal": payload.get("personal") or {},
        "tasks": restored.get("tasks", {}),
        "lanes": restored.get("lanes", {}),
        "feedback": feedback.get("feedback", {}),
    }


def mark_task(
    task_id: str,
    undo: bool = False,
    root: Path | None = None,
    note: str = "",
    evidence_path: str = "",
) -> dict[str, Any]:
    data = load_progress(root)
    tasks = data["tasks"]
    if task_id not in tasks:
        raise KeyError(task_id)

    task = tasks[task_id]
    if "lane" not in task:
        task["lane"] = "engineering"

    action_type = "undo_done" if undo else "mark_done"
    result = "ok"

    if undo:
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

    save_progress(data, root)
    sync_progress_data_js(data, root)
    action_id = append_action_event(
        task_id,
        task.get("lane", "engineering"),
        action_type,
        result,
        root=root,
        note=note,
        evidence_path=evidence_path,
    )
    feedback = write_feedback_payload(data, root)

    total = len(tasks)
    done_count = sum(1 for item in tasks.values() if item.get("done"))
    return {
        "ok": True,
        "task_id": task_id,
        "done": task.get("done", False),
        "done_at": task.get("done_at"),
        "lane": task.get("lane", "engineering"),
        "result": result,
        "message": message,
        "action_id": action_id,
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
        "lanes": data.get("lanes", {}),
        "tasks": tasks,
        "total": len(tasks),
        "done_count": done_count,
    }
