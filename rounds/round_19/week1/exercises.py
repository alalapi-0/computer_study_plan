#!/usr/bin/env python3
"""Round 19 · Week 1 exercises: 训练/验证划分."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round19" / "week1"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "ml_minimal_loop_week1.txt"
    marker.write_text("训练/验证划分\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
