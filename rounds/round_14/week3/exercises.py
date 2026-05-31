#!/usr/bin/env python3
"""Round 14 · Week 3 exercises: 最小 REST 路由草图."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round14" / "week3"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "http_api_week3.txt"
    marker.write_text("最小 REST 路由草图\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
