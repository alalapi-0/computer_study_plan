#!/usr/bin/env python3
"""Round 09 · Week 1 exercises: repo layout and baseline docs."""

import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


def main() -> None:
    base = Path.home() / "cli-lab" / "round9" / "week1" / "ai_prep_tool"
    (base / "tests").mkdir(parents=True, exist_ok=True)
    (base / "input").mkdir(parents=True, exist_ok=True)
    (base / "output").mkdir(parents=True, exist_ok=True)

    readme = base / "README.md"
    readme.write_text(
        "# AI Prep Tool\n\n最小项目说明：用于练习仓库规范化与测试入门。\n",
        encoding="utf-8",
    )

    gitignore = base / ".gitignore"
    gitignore.write_text(
        "__pycache__/\n*.pyc\n.venv/\nvenv/\noutput/\n*.log\n",
        encoding="utf-8",
    )

    print("已生成 Round 09 Week 1 沙盒目录:", base)
    print("请手动检查 README 与 .gitignore 是否符合预期。")

    mark("r09-w1-ex1")
    input("请手动完成第1周自测后按回车继续...")
    mark("r09-w1-self")


if __name__ == "__main__":
    main()
