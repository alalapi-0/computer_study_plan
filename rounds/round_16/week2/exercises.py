#!/usr/bin/env python3
"""Round 16 · Week 2 exercises: 列表/详情接口草图."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round16" / "week2"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "api_data_layer_week2.txt"
    marker.write_text("列表/详情接口草图\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
