#!/usr/bin/env python3
"""Generate minimal task feedback from progress and action logs."""

from __future__ import annotations

import argparse
from pathlib import Path

from progress_lib import load_progress, write_feedback_payload


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
    output_path = repo_root / args.output
    feedback_path = repo_root / "records/feedback/task_feedback.json"

    progress = load_progress(repo_root)
    write_feedback_payload(progress, repo_root)
    if output_path != feedback_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(feedback_path.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Generated feedback: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
