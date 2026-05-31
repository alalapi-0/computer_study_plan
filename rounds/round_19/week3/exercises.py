#!/usr/bin/env python3
"""Round 19 · Week 3 exercises: 指标记录骨架."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round19" / "week3"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "ml_minimal_loop_week3.txt"
    marker.write_text("指标记录骨架\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
