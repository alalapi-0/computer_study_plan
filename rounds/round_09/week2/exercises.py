#!/usr/bin/env python3
"""Round 09 · Week 2 exercises: git workflow rehearsal."""

from pathlib import Path


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


if __name__ == "__main__":
    main()
