#!/usr/bin/env python3
"""Round 07 · Week 1 exercises: pathlib and file formats."""

import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


def main() -> None:
    base = Path.home() / "cli-lab" / "round7" / "week1"
    base.mkdir(parents=True, exist_ok=True)

    txt_file = base / "labels.txt"
    txt_file.write_text("ok\nblur\nok\n", encoding="utf-8")

    lines = [line.strip() for line in txt_file.read_text(encoding="utf-8").splitlines() if line.strip()]

    print("工作目录:", base)
    print("TXT 行数:", len(lines))
    print("建议补充: 在此目录手动创建 csv/json/jsonl 文件并扩展读取脚本。")

    mark("r07-w1-ex1")
    input("请手动完成第1周自测后按回车继续...")
    mark("r07-w1-self")


if __name__ == "__main__":
    main()
