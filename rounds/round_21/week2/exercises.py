#!/usr/bin/env python3
"""Round 21 · Week 2 exercises: 文本张量批处理."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round21" / "week2"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "nlp_prereq_week2.txt"
    marker.write_text("文本张量批处理\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
