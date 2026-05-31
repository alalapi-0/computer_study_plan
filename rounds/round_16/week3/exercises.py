#!/usr/bin/env python3
"""Round 16 · Week 3 exercises: 错误响应约定."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round16" / "week3"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "api_data_layer_week3.txt"
    marker.write_text("错误响应约定\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
