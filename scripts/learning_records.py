#!/usr/bin/env python3
"""Read/write learning records for learn_server (PW-5)."""

from __future__ import annotations

import datetime
import json
import re
from pathlib import Path

ALLOWED_LANES = frozenset({"engineering", "soft_exam", "math2", "cs408"})
MODULE_RE = re.compile(r"^[a-z0-9_/-]+$")


def read_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def get_task_events(repo_root: Path, task_id: str, limit: int = 30) -> list[dict]:
    path = repo_root / "records" / "action_logs" / "events.jsonl"
    events = [e for e in read_jsonl(path) if e.get("task_id") == task_id]
    return events[-limit:]


def get_task_feedback(repo_root: Path, task_id: str) -> dict | None:
    path = repo_root / "records" / "feedback" / "task_feedback.json"
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("feedback", {}).get(task_id)


def save_error_note(
    repo_root: Path,
    lane: str,
    module: str,
    title: str,
    wrong_answer: str,
    correct_answer: str,
    note: str = "",
) -> dict:
    if lane not in ALLOWED_LANES:
        raise ValueError(f"invalid lane: {lane}")
    module = module.strip().lower().replace(" ", "_")
    if not module or not MODULE_RE.match(module):
        raise ValueError("invalid module name")
    if not title.strip():
        raise ValueError("title required")

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    shortid = re.sub(r"[^a-z0-9]+", "-", title.strip().lower())[:24].strip("-") or "note"
    filename = f"{date}-{shortid}.md"
    target_dir = repo_root / "records" / "error_notes" / lane / module
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / filename
    if target.exists():
        suffix = now.strftime("%H%M%S")
        filename = f"{date}-{shortid}-{suffix}.md"
        target = target_dir / filename

    body = (
        f"# 错题 · {title.strip()}\n\n"
        f"> lane: `{lane}` · module: `{module}` · 记录时间: {now.isoformat(timespec='seconds')}\n\n"
        "## 题面 / 知识点摘要\n\n"
        f"{title.strip()}\n\n"
        "## 我的错误思路或答案\n\n"
        f"{wrong_answer.strip() or '（未填写）'}\n\n"
        "## 正确思路或答案\n\n"
        f"{correct_answer.strip() or '（未填写）'}\n\n"
        "## 复盘备注\n\n"
        f"{note.strip() or '（未填写）'}\n"
    )
    target.write_text(body, encoding="utf-8")
    return {
        "ok": True,
        "path": str(target.relative_to(repo_root)),
        "lane": lane,
        "module": module,
    }
