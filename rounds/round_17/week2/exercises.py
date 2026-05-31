#!/usr/bin/env python3
"""Round 17 · Week 2 exercises: 日志与配置收口."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round17" / "week2"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "service_wrapup_week2.txt"
    marker.write_text("日志与配置收口\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
