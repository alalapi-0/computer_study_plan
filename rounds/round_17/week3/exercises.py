#!/usr/bin/env python3
"""Round 17 · Week 3 exercises: 部署前检查表."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round17" / "week3"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "service_wrapup_week3.txt"
    marker.write_text("部署前检查表\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
