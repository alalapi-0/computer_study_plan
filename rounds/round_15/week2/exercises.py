#!/usr/bin/env python3
"""Round 15 · Week 2 exercises: 路径参数与查询参数."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round15" / "week2"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "fastapi_basics_week2.txt"
    marker.write_text("路径参数与查询参数\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
