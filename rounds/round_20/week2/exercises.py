#!/usr/bin/env python3
"""Round 20 · Week 2 exercises: 最小训练循环."""

import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


def main() -> None:
    base = Path.home() / "cli-lab" / "round20" / "week2"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "pytorch_intro_week2.txt"
    marker.write_text("最小训练循环\n", encoding="utf-8")
    print("已写入:", marker)

    mark("r20-w2-ex2")
    input("请手动完成第2周自测后按回车继续...")
    mark("r20-w2-self")


if __name__ == "__main__":
    main()
