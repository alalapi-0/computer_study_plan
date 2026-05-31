#!/usr/bin/env python3
"""Round 18 · Week 1 exercises: numpy 数组入门."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round18" / "week1"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "numerics_analytics_week1.txt"
    marker.write_text("numpy 数组入门\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
