#!/usr/bin/env python3
"""Round 21 · Week 3 exercises: 推理脚本入口骨架."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round21" / "week3"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "nlp_prereq_week3.txt"
    marker.write_text("推理脚本入口骨架\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
