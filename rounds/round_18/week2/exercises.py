#!/usr/bin/env python3
"""Round 18 · Week 2 exercises: pandas 读取 CSV."""

import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


def main() -> None:
    base = Path.home() / "cli-lab" / "round18" / "week2"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "numerics_analytics_week2.txt"
    marker.write_text("pandas 读取 CSV\n", encoding="utf-8")
    print("已写入:", marker)

    mark("r18-w2-ex2")
    input("请手动完成第2周自测后按回车继续...")
    mark("r18-w2-self")


if __name__ == "__main__":
    main()
