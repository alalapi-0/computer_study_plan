#!/usr/bin/env python3
"""Round 20 · Week 3 exercises: checkpoint 路径约定."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round20" / "week3"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "pytorch_intro_week3.txt"
    marker.write_text("checkpoint 路径约定\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
