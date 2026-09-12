#!/usr/bin/env python3
"""Validate progress, action events, and feedback data consistency."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ALLOWED_ACTION_TYPES = {"mark_done", "undo_done", "run_exercise"}
ALLOWED_RESULTS = {"ok", "noop_already_done", "noop_already_undone", "failed", "timeout"}
ALLOWED_FEEDBACK_TYPES = {"completed", "not_started", "in_progress"}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path):
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def validate_progress(repo_root: Path, errors: list[str]) -> tuple[dict, dict]:
    progress_path = repo_root / "progress.json"
    data = read_json(progress_path)

    lanes = data.get("lanes")
    tasks = data.get("tasks")
    if not isinstance(lanes, dict) or not lanes:
        errors.append("progress.json: lanes must be a non-empty object")
        lanes = {}
    if not isinstance(tasks, dict) or not tasks:
        errors.append("progress.json: tasks must be a non-empty object")
        tasks = {}
        return lanes, tasks

    for task_id, info in tasks.items():
        if not isinstance(info, dict):
            errors.append(f"progress.json: task {task_id} must be object")
            continue
        done = info.get("done")
        if not isinstance(done, bool):
            errors.append(f"progress.json: task {task_id}.done must be bool")
        done_at = info.get("done_at")
        if done is True and (not isinstance(done_at, str) or not done_at):
            errors.append(f"progress.json: completed task {task_id}.done_at must be non-empty string")
        if done is False and done_at is not None:
            errors.append(f"progress.json: incomplete task {task_id}.done_at must be null")
        lane = info.get("lane")
        if lane not in lanes:
            errors.append(f"progress.json: task {task_id}.lane not found in lanes")
    return lanes, tasks


def validate_events(repo_root: Path, task_ids: set[str], errors: list[str]) -> None:
    events_path = repo_root / "records/action_logs/events.jsonl"
    for i, event in enumerate(read_jsonl(events_path), start=1):
        task_id = event.get("task_id")
        if task_id not in task_ids:
            errors.append(f"events.jsonl line {i}: unknown task_id {task_id}")
        if event.get("action_type") not in ALLOWED_ACTION_TYPES:
            errors.append(f"events.jsonl line {i}: invalid action_type")
        if event.get("result") not in ALLOWED_RESULTS:
            errors.append(f"events.jsonl line {i}: invalid result")
        if not isinstance(event.get("timestamp"), str):
            errors.append(f"events.jsonl line {i}: timestamp must be string")
        operation_id = event.get("operation_id")
        if operation_id is not None and (not isinstance(operation_id, str) or not operation_id):
            errors.append(f"events.jsonl line {i}: operation_id must be a non-empty string when present")


def validate_feedback(repo_root: Path, task_ids: set[str], errors: list[str]) -> None:
    feedback_path = repo_root / "records/feedback/task_feedback.json"
    if not feedback_path.exists():
        return
    data = read_json(feedback_path)
    feedback = data.get("feedback", {})
    if not isinstance(feedback, dict):
        errors.append("task_feedback.json: feedback must be object")
        return
    for task_id, item in feedback.items():
        if task_id not in task_ids:
            errors.append(f"task_feedback.json: unknown task_id {task_id}")
            continue
        if item.get("feedback_type") not in ALLOWED_FEEDBACK_TYPES:
            errors.append(f"task_feedback.json: {task_id} invalid feedback_type")
        if not isinstance(item.get("next_suggestion"), str):
            errors.append(f"task_feedback.json: {task_id} next_suggestion must be string")


def validate_runnable_scripts(repo_root: Path, task_ids: set[str], errors: list[str]) -> None:
    rounds_path = repo_root / "rounds_data.js"
    marker = "window.ROUNDS_DATA = "
    text = rounds_path.read_text(encoding="utf-8")
    if marker not in text:
        errors.append("rounds_data.js: missing ROUNDS_DATA assignment")
        return
    rounds = json.loads(text.split(marker, 1)[1].strip().removesuffix(";"))
    metadata: dict[str, dict] = {}
    for round_item in rounds:
        for week in round_item.get("weeks", []):
            for task in week.get("tasks", []):
                task_id = task.get("id")
                if isinstance(task_id, str):
                    metadata[task_id] = task

    runnable_paths: set[str] = set()
    allowed_path = re.compile(
        r"^rounds/round_\d{2}/(?:week[1-3]|final)/(?:exercises|comprehensive_exercise)\.(?:sh|py)$"
    )
    for task_id, task in metadata.items():
        file_path = task.get("file")
        if task.get("type") != "exercise" or not isinstance(file_path, str) or not file_path.endswith((".sh", ".py")):
            continue
        if not allowed_path.fullmatch(file_path):
            errors.append(f"rounds_data.js: runnable task {task_id} has non-whitelisted file {file_path}")
            continue
        if not (repo_root / file_path).is_file():
            errors.append(f"rounds_data.js: runnable task {task_id} file not found: {file_path}")
            continue
        runnable_paths.add(file_path)

    literal_mark = re.compile(r"^\s*mark\s+([A-Za-z0-9._-]+)\s*(?:#.*)?$")
    any_mark = re.compile(r"^\s*mark\s+")
    allowed_mark_delegate = re.compile(
        r'^\s*bash\s+"\$REPO_ROOT/mark_done\.sh"\s+"\$1"\s*$'
    )
    for file_path in sorted(runnable_paths):
        source = (repo_root / file_path).read_text(encoding="utf-8")
        delegate_count = 0
        for line_number, line in enumerate(source.splitlines(), start=1):
            stripped = line.strip()
            if "mark_done.sh" in stripped and not stripped.startswith(("#", "echo ")):
                if allowed_mark_delegate.fullmatch(line):
                    delegate_count += 1
                else:
                    errors.append(
                        f"{file_path}:{line_number}: direct mark_done.sh calls outside the validated mark helper are not allowed"
                    )
            if not any_mark.match(line):
                continue
            match = literal_mark.match(line)
            if not match:
                errors.append(f"{file_path}:{line_number}: dynamic mark target is not allowed")
                continue
            target_id = match.group(1)
            target = metadata.get(target_id)
            if target_id not in task_ids or not target:
                errors.append(f"{file_path}:{line_number}: unknown mark target {target_id}")
            elif target.get("type") != "exercise":
                errors.append(f"{file_path}:{line_number}: non-exercise mark target {target_id}")
            elif target.get("file") != file_path:
                errors.append(f"{file_path}:{line_number}: mark target {target_id} belongs to {target.get('file')}")
        if delegate_count != 1:
            errors.append(f"{file_path}: expected exactly one validated mark helper")


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    errors: list[str] = []

    _, tasks = validate_progress(repo_root, errors)
    task_ids = set(tasks.keys())
    validate_events(repo_root, task_ids, errors)
    validate_feedback(repo_root, task_ids, errors)
    validate_runnable_scripts(repo_root, task_ids, errors)

    if errors:
        print("Data validation FAILED")
        for err in errors:
            print(f"- {err}")
        return 1
    print("Data validation PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
