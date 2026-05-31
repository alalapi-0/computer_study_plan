#!/usr/bin/env python3
"""Round 16 · Week 1 exercises: 路由调用 db 模块."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round16" / "week1"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "api_data_layer_week1.txt"
    marker.write_text("路由调用 db 模块\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
