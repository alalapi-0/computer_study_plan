#!/usr/bin/env python3
"""Validate progress, action events, and feedback data consistency."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ALLOWED_ACTION_TYPES = {"mark_done", "undo_done"}
ALLOWED_RESULTS = {"ok", "noop_already_done"}
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
        if not isinstance(info.get("done"), bool):
            errors.append(f"progress.json: task {task_id}.done must be bool")
        done_at = info.get("done_at")
        if done_at is not None and not isinstance(done_at, str):
            errors.append(f"progress.json: task {task_id}.done_at must be null or string")
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


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    errors: list[str] = []

    _, tasks = validate_progress(repo_root, errors)
    task_ids = set(tasks.keys())
    validate_events(repo_root, task_ids, errors)
    validate_feedback(repo_root, task_ids, errors)

    if errors:
        print("Data validation FAILED")
        for err in errors:
            print(f"- {err}")
        return 1
    print("Data validation PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
