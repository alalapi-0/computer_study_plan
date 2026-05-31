#!/usr/bin/env python3
"""Round 13 · Week 2 exercises: `.env.example` 与配置分层."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round13" / "week2"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "env_repro_week2.txt"
    marker.write_text("`.env.example` 与配置分层\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
