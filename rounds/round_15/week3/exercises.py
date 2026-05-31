#!/usr/bin/env python3
"""Round 15 · Week 3 exercises: Pydantic 模型骨架."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round15" / "week3"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "fastapi_basics_week3.txt"
    marker.write_text("Pydantic 模型骨架\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
