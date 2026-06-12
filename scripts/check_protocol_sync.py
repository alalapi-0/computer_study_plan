#!/usr/bin/env python3
"""Basic protocol consistency checker for this repository."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_PATHS = [
    "AGENTS.md",
    "README.md",
    "CONVERSION_PROTOCOL.md",
    "docs/WORKSPACE.md",
    "docs/MASTER_STUDY_ROADMAP.md",
    "docs/STAGE_PLAN.md",
    "docs/CODEX_LONG_TERM_PLAN.md",
    "docs/PROJECT_STATE.md",
    "docs/NEXT_ACTIONS.md",
    "progress.json",
    "progress_rounds.json",
    "progress_rounds.js",
    "progress.html",
    "mark_done.sh",
    "scripts/round_status.py",
    "scripts/generate_progress_rounds.py",
    "scripts/check_user_journey.py",
    "scripts/progress_store.py",
    "scripts/learn_server.py",
    "scripts/content_paths.py",
    "scripts/exercise_guide.py",
    "rounds/round_00/final/comprehensive_exercise.sh",
]


def check_required_files(repo_root: Path) -> list[str]:
    missing: list[str] = []
    for rel in REQUIRED_PATHS:
        if not (repo_root / rel).exists():
            missing.append(rel)
    return missing


def check_progress_schema(repo_root: Path) -> list[str]:
    errors: list[str] = []
    progress_path = repo_root / "progress.json"
    try:
        data = json.loads(progress_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return ["progress.json not found"]
    except json.JSONDecodeError as exc:
        return [f"progress.json invalid JSON: {exc}"]

    if not isinstance(data, dict):
        return ["progress.json top-level must be an object"]
    tasks = data.get("tasks")
    if not isinstance(tasks, dict):
        errors.append("progress.json must contain an object field: tasks")
    elif not tasks:
        errors.append("progress.json.tasks must not be empty")
    return errors


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    all_errors: list[str] = []

    missing_files = check_required_files(repo_root)
    if missing_files:
        all_errors.extend([f"missing: {path}" for path in missing_files])

    all_errors.extend(check_progress_schema(repo_root))

    if all_errors:
        print("Protocol sync check FAILED")
        for err in all_errors:
            print(f"- {err}")
        return 1

    print("Protocol sync check PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
