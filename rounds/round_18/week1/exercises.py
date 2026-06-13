#!/usr/bin/env python3
"""Round 18 · Week 1 exercises: numpy 数组入门."""

import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


def main() -> None:
    base = Path.home() / "cli-lab" / "round18" / "week1"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "numerics_analytics_week1.txt"
    marker.write_text("numpy 数组入门\n", encoding="utf-8")
    print("已写入:", marker)

    mark("r18-w1-ex1")
    input("请手动完成第1周自测后按回车继续...")
    mark("r18-w1-self")


if __name__ == "__main__":
    main()
