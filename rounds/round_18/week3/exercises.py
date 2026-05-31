#!/usr/bin/env python3
"""Round 18 · Week 3 exercises: 简单聚合统计."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round18" / "week3"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "numerics_analytics_week3.txt"
    marker.write_text("简单聚合统计\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
