#!/usr/bin/env python3
"""Regenerate progress_data.js from progress.json without changing task state."""

from __future__ import annotations

import sys

from progress_lib import load_progress, repo_root, sync_progress_data_js


def main() -> int:
    root = repo_root()
    data = load_progress(root)
    sync_progress_data_js(data, root)
    task_count = len(data.get("tasks", {}))
    print(f"Synced progress_data.js from progress.json ({task_count} tasks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
