#!/usr/bin/env python3
"""Generate minimal task feedback from progress and action logs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def build_feedback(progress: dict, events: list[dict]) -> dict:
    tasks = progress.get("tasks", {})
    event_count_by_task: dict[str, int] = {}
    last_event_by_task: dict[str, dict] = {}
    for event in events:
        tid = event.get("task_id")
        if not tid:
            continue
        event_count_by_task[tid] = event_count_by_task.get(tid, 0) + 1
        last_event_by_task[tid] = event

    feedback_items: dict[str, dict] = {}
    for task_id, info in tasks.items():
        done = bool(info.get("done"))
        lane = info.get("lane", "engineering")
        action_count = event_count_by_task.get(task_id, 0)
        last_event = last_event_by_task.get(task_id, {})

        if done:
            message = "已完成，建议进入错题回看或下一小节。"
            next_suggestion = "继续同 lane 下一个任务，或安排 10 分钟复盘。"
            feedback_type = "completed"
        elif action_count == 0:
            message = "尚未开始，建议先做一个 15 分钟启动动作。"
            next_suggestion = "先读 1 小节笔记或完成 1 道基础题。"
            feedback_type = "not_started"
        else:
            message = "已产生学习动作但尚未完成，建议收敛到最小闭环。"
            next_suggestion = "先把当前任务推进到 done，再切换任务。"
            feedback_type = "in_progress"

        feedback_items[task_id] = {
            "task_id": task_id,
            "lane": lane,
            "done": done,
            "action_count": action_count,
            "last_action_type": last_event.get("action_type"),
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root path (default: current directory)",
    )
    parser.add_argument(
        "--output",
        default="records/feedback/task_feedback.json",
        help="Output JSON file path relative to repo root",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    progress_path = repo_root / "progress.json"
    action_log_path = repo_root / "records/action_logs/events.jsonl"
    output_path = repo_root / args.output

    progress = load_json(progress_path)
    events = load_jsonl(action_log_path)
    payload = build_feedback(progress, events)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Generated feedback: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
