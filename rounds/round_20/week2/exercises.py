#!/usr/bin/env python3
"""Round 20 · Week 2 exercises: 最小训练循环."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round20" / "week2"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "pytorch_intro_week2.txt"
    marker.write_text("最小训练循环\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
