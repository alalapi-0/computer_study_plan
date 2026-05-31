#!/usr/bin/env python3
"""Round 15 · Final checklist."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round15"
    base.mkdir(parents=True, exist_ok=True)
    markers = [base / f"week{n}" / "fastapi_basics_week{n}.txt" for n in (1, 2, 3)]
    print("Round 15 收口检查")
    for path in markers:
        print(f"- {path.name}: {'OK' if path.exists() else 'MISSING'}")


if __name__ == "__main__":
    main()
