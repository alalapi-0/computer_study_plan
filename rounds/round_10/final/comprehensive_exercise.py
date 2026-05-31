#!/usr/bin/env python3
"""Round 10 · Final: engineering layout checklist."""

from pathlib import Path


CHECKLIST = {
    "week1_modules": [
        "week1/ai_prep_tool/cli.py",
        "week1/ai_prep_tool/core.py",
        "week1/ai_prep_tool/io_utils.py",
    ],
    "week2_config": ["week2/ai_prep_tool/config.ini", "week2/ai_prep_tool/log_utils.py"],
    "week3_logic": ["week3/exercises.py"],
}


def scan(base: Path) -> dict[str, bool]:
    result: dict[str, bool] = {}
    for key, rel_paths in CHECKLIST.items():
        result[key] = all((base / rel_path).exists() for rel_path in rel_paths)
    return result


def main() -> None:
    base = Path.home() / "cli-lab" / "round10"
    base.mkdir(parents=True, exist_ok=True)

    summary = scan(base)
    print("Round 10 收口检查")
    for key, ok in summary.items():
        print(f"- {key}: {'OK' if ok else 'MISSING'}")


if __name__ == "__main__":
    main()
