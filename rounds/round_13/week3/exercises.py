#!/usr/bin/env python3
"""Round 13 · Week 3 exercises: 发布前自检清单."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round13" / "week3"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "env_repro_week3.txt"
    marker.write_text("发布前自检清单\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
