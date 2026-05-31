#!/usr/bin/env python3
"""Round 14 · Week 1 exercises: HTTP 动词与状态码."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round14" / "week1"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "http_api_week1.txt"
    marker.write_text("HTTP 动词与状态码\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
