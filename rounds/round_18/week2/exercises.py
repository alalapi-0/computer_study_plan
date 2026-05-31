#!/usr/bin/env python3
"""Round 18 · Week 2 exercises: pandas 读取 CSV."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round18" / "week2"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "numerics_analytics_week2.txt"
    marker.write_text("pandas 读取 CSV\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
