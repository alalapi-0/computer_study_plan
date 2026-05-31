#!/usr/bin/env python3
"""Round 11 · Final: persistence checklist."""

from pathlib import Path


CHECKLIST = {
    "week1_db": ["week1/ai_prep_tool.db"],
    "week3_db_module": ["week3/ai_prep_tool/db.py"],
}


def scan(base: Path) -> dict[str, bool]:
    result: dict[str, bool] = {}
    for key, rel_paths in CHECKLIST.items():
        result[key] = all((base / rel_path).exists() for rel_path in rel_paths)
    return result


def main() -> None:
    base = Path.home() / "cli-lab" / "round11"
    base.mkdir(parents=True, exist_ok=True)

    summary = scan(base)
    print("Round 11 收口检查")
    for key, ok in summary.items():
        print(f"- {key}: {'OK' if ok else 'MISSING'}")


if __name__ == "__main__":
    main()
