#!/usr/bin/env python3
"""Round 14 · Week 2 exercises: 请求/响应 JSON 约定."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round14" / "week2"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "http_api_week2.txt"
    marker.write_text("请求/响应 JSON 约定\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
