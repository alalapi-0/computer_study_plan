#!/usr/bin/env python3
"""Preflight gate and next-task selector for automated Codex rounds.

Exit codes:
  0  — task selected (stdout: JSON brief)
  1  — generic failure
  10 — git working tree not clean
  11 — only human-required tasks remain
  12 — no automatable task found
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
NEXT_ACTIONS = REPO_ROOT / "docs" / "NEXT_ACTIONS.md"
CONVERSION_PROTOCOL = REPO_ROOT / "CONVERSION_PROTOCOL.md"

TASK_HEADER_RE = re.compile(r"^## (TASK-[A-Z0-9-]+)：", re.MULTILINE)
STATUS_RE = re.compile(r"- 状态：\*\*(.+?)\*\*")
USER_NEEDED_RE = re.compile(r"- 是否需要用户介入：\*\*(.+?)\*\*")
OPTIONAL_ROUND_RE = re.compile(r"Round (\d{2}) 最小骨架")


@dataclass
class GateTask:
    task_id: str
    title: str
    status: str
    needs_user: bool
    source: str  # "queue" | "optional_round"


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def git_is_clean() -> bool:
    proc = run_git(["status", "--porcelain"])
    if proc.returncode != 0:
        return False
    return proc.stdout.strip() == ""


def parse_task_blocks(text: str) -> list[GateTask]:
    headers = list(TASK_HEADER_RE.finditer(text))
    tasks: list[GateTask] = []
    for idx, match in enumerate(headers):
        start = match.start()
        end = headers[idx + 1].start() if idx + 1 < len(headers) else len(text)
        block = text[start:end]
        task_id = match.group(1)
        title = match.group(0).split("：", 1)[-1].strip().rstrip("#").strip()
        status_m = STATUS_RE.search(block)
        user_m = USER_NEEDED_RE.search(block)
        status = status_m.group(1) if status_m else "unknown"
        needs_raw = user_m.group(1) if user_m else ""
        needs_user = needs_raw.strip() in {"是", "yes", "Yes", "YES"}
        tasks.append(
            GateTask(
                task_id=task_id,
                title=title,
                status=status,
                needs_user=needs_user,
                source="queue",
            )
        )
    return tasks


def pick_queue_task(tasks: list[GateTask]) -> GateTask | None:
    automatable_status = {"pending", "in_progress"}
    for task in tasks:
        if task.needs_user:
            continue
        if not any(task.status.startswith(s) for s in automatable_status):
            continue
        if task.status.startswith("done"):
            continue
        if task.status.startswith("deferred"):
            continue
        if task.status.startswith("superseded"):
            continue
        return task
    return None


def expanded_round_numbers() -> list[int]:
    nums: list[int] = []
    rounds_dir = REPO_ROOT / "rounds"
    if rounds_dir.is_dir():
        for path in rounds_dir.iterdir():
            m = re.fullmatch(r"round_(\d{2})", path.name)
            if m and path.is_dir():
                nums.append(int(m.group(1)))
    return sorted(nums)


def next_optional_round() -> int | None:
    """Suggest Round N+1 skeleton when overview md exists but rounds dir missing."""
    expanded = expanded_round_numbers()
    next_num = (max(expanded) + 1) if expanded else 0
    for n in range(next_num, 22):
        if not (REPO_ROOT / f"round_{n:02d}.md").exists():
            continue
        if (REPO_ROOT / f"rounds/round_{n:02d}").exists():
            continue
        return n
    return None


def pick_optional_round_task() -> GateTask | None:
    if NEXT_ACTIONS.exists():
        text = NEXT_ACTIONS.read_text(encoding="utf-8")
        for match in OPTIONAL_ROUND_RE.finditer(text):
            num = int(match.group(1))
            if not (REPO_ROOT / f"rounds/round_{num:02d}").exists():
                return GateTask(
                    task_id=f"TASK-RR-{num:02d}-round{num:02d}-skeleton",
                    title=f"Stage 1 可选推进 · Round {num:02d} 最小骨架",
                    status="pending",
                    needs_user=False,
                    source="optional_round",
                )
    num = next_optional_round()
    if num is None:
        return None
    return GateTask(
        task_id=f"TASK-RR-{num:02d}-round{num:02d}-skeleton",
        title=f"Stage 1 可选推进 · Round {num:02d} 最小骨架",
        status="pending",
        needs_user=False,
        source="optional_round",
    )


def run_verify() -> int:
    commands = [
        [sys.executable, "scripts/check_protocol_sync.py"],
        [sys.executable, "scripts/validate_learning_data.py"],
        ["python3", "-m", "json.tool", "progress.json"],
    ]
    for cmd in commands:
        print("$", " ".join(cmd))
        proc = subprocess.run(cmd, cwd=REPO_ROOT)
        if proc.returncode != 0:
            return proc.returncode
    return 0


def select_task() -> GateTask | None:
    if not NEXT_ACTIONS.exists():
        return None
    text = NEXT_ACTIONS.read_text(encoding="utf-8")
    queue = parse_task_blocks(text)
    queued = pick_queue_task(queue)
    if queued:
        return queued
    return pick_optional_round_task()


def main() -> int:
    parser = argparse.ArgumentParser(description="Agent gate for automated study-plan rounds")
    parser.add_argument("--verify", action="store_true", help="Run standard validation commands")
    parser.add_argument("--json", action="store_true", help="Emit selected task as JSON")
    parser.add_argument(
        "--require-clean",
        action="store_true",
        default=True,
        help="Fail when git working tree is dirty (default: true)",
    )
    parser.add_argument(
        "--no-require-clean",
        action="store_false",
        dest="require_clean",
        help="Allow dirty working tree (debug only)",
    )
    args = parser.parse_args()

    if args.verify:
        return run_verify()

    if args.require_clean and not git_is_clean():
        print("agent_gate: git working tree is not clean", file=sys.stderr)
        proc = run_git(["status", "--short"])
        if proc.stdout:
            print(proc.stdout, file=sys.stderr)
        return 10

    task = select_task()
    if task is None:
        if NEXT_ACTIONS.exists():
            all_tasks = parse_task_blocks(NEXT_ACTIONS.read_text(encoding="utf-8"))
            pending_human = [
                t
                for t in all_tasks
                if t.needs_user
                and not t.status.startswith("done")
                and not t.status.startswith("deferred")
            ]
            if pending_human:
                print(
                    "agent_gate: only human-required tasks remain",
                    file=sys.stderr,
                )
                for t in pending_human[:5]:
                    print(f"  - {t.task_id}: {t.status}", file=sys.stderr)
                return 11
        print("agent_gate: no automatable task found", file=sys.stderr)
        return 12

    payload = {
        "repo_root": str(REPO_ROOT),
        "task_id": task.task_id,
        "title": task.title,
        "status": task.status,
        "needs_user": task.needs_user,
        "source": task.source,
        "branch_hint": f"codex/{task.task_id.lower()}",
        "commit_to_main": True,
        "verify_commands": [
            "python3 scripts/check_protocol_sync.py",
            "python3 scripts/validate_learning_data.py",
        ],
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"SELECTED_TASK={task.task_id}")
        print(f"TITLE={task.title}")
        print(f"SOURCE={task.source}")
        print(f"BRANCH_HINT={payload['branch_hint']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
