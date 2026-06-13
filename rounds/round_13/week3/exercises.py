#!/usr/bin/env python3
"""Round 13 · Week 3 exercises: 发布前自检清单."""

import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


def main() -> None:
    base = Path.home() / "cli-lab" / "round13" / "week3"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "env_repro_week3.txt"
    marker.write_text("发布前自检清单\n", encoding="utf-8")
    print("已写入:", marker)

    mark("r13-w3-ex3")
    input("请手动完成第3周自测后按回车继续...")
    mark("r13-w3-self")


if __name__ == "__main__":
    main()
