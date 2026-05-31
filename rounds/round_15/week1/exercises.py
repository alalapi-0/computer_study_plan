#!/usr/bin/env python3
"""Round 15 · Week 1 exercises: FastAPI 应用入口."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round15" / "week1"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "fastapi_basics_week1.txt"
    marker.write_text("FastAPI 应用入口\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
