#!/usr/bin/env python3
"""Round 20 · Week 1 exercises: Tensor 与 Dataset."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round20" / "week1"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "pytorch_intro_week1.txt"
    marker.write_text("Tensor 与 Dataset\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
