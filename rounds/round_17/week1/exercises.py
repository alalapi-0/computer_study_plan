#!/usr/bin/env python3
"""Round 17 · Week 1 exercises: 启动脚本与健康检查."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round17" / "week1"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "service_wrapup_week1.txt"
    marker.write_text("启动脚本与健康检查\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
