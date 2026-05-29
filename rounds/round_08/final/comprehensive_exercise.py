#!/usr/bin/env python3
"""Round 08 · Final: consolidation checklist runner."""

from pathlib import Path


CHECKLIST = {
    "project_layout": ["README.md", "tests/test_basic.py"],
    "sqlite": ["week2/runs.db"],
    "api_rehearsal": ["week3/exercises.py"],
}


def scan(base: Path) -> dict[str, bool]:
    result: dict[str, bool] = {}
    for key, rel_files in CHECKLIST.items():
        result[key] = all((base / rel_file).exists() for rel_file in rel_files)
    return result


def main() -> None:
    base = Path.home() / "cli-lab" / "round8"
    base.mkdir(parents=True, exist_ok=True)

    summary = scan(base)
    print("Round 08 收口检查")
    for key, ok in summary.items():
        print(f"- {key}: {'OK' if ok else 'MISSING'}")


if __name__ == "__main__":
    main()
