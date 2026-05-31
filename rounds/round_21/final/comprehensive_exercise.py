#!/usr/bin/env python3
"""Round 21 · Final checklist."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round21"
    base.mkdir(parents=True, exist_ok=True)
    markers = [base / f"week{n}" / "nlp_prereq_week{n}.txt" for n in (1, 2, 3)]
    print("Round 21 收口检查")
    for path in markers:
        print(f"- {path.name}: {'OK' if path.exists() else 'MISSING'}")


if __name__ == "__main__":
    main()
