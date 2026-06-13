#!/usr/bin/env python3
"""Round 17 · Week 3 exercises: 部署前检查表."""

import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


def main() -> None:
    base = Path.home() / "cli-lab" / "round17" / "week3"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "service_wrapup_week3.txt"
    marker.write_text("部署前检查表\n", encoding="utf-8")
    print("已写入:", marker)

    mark("r17-w3-ex3")
    input("请手动完成第3周自测后按回车继续...")
    mark("r17-w3-self")


if __name__ == "__main__":
    main()
