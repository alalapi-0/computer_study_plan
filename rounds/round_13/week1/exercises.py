#!/usr/bin/env python3
"""Round 13 · Week 1 exercises: 虚拟环境与依赖锁定."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round13" / "week1"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "env_repro_week1.txt"
    marker.write_text("虚拟环境与依赖锁定\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
