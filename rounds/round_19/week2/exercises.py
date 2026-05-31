#!/usr/bin/env python3
"""Round 19 · Week 2 exercises: 基线模型拟合."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round19" / "week2"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "ml_minimal_loop_week2.txt"
    marker.write_text("基线模型拟合\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
