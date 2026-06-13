#!/usr/bin/env python3
"""Round 09 · Week 2 exercises: git workflow rehearsal."""

import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


def main() -> None:
    base = Path.home() / "cli-lab" / "round9" / "week2" / "workflow_demo"
    base.mkdir(parents=True, exist_ok=True)

    commands = [
        "git init",
        "git checkout -b feature/improve-readme",
        'git commit -m "docs: improve readme"',
        "git checkout main",
        "git merge feature/improve-readme",
        "git branch -d feature/improve-readme",
    ]

    print("建议在以下目录演练 Git 工作流:", base)
    print("参考命令：")
    for command in commands:
        print("-", command)

    mark("r09-w2-ex2")
    input("请手动完成第2周自测后按回车继续...")
    mark("r09-w2-self")


if __name__ == "__main__":
    main()
