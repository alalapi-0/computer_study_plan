#!/usr/bin/env python3
"""Round 16 · Week 2 exercises: 列表/详情接口草图."""

import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


def main() -> None:
    base = Path.home() / "cli-lab" / "round16" / "week2"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "api_data_layer_week2.txt"
    marker.write_text("列表/详情接口草图\n", encoding="utf-8")
    print("已写入:", marker)

    mark("r16-w2-ex2")
    input("请手动完成第2周自测后按回车继续...")
    mark("r16-w2-self")


if __name__ == "__main__":
    main()
