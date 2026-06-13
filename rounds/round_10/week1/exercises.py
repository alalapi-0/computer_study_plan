#!/usr/bin/env python3
"""Round 10 · Week 1 exercises: split cli/core/io modules."""

import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


CLI_TEMPLATE = '''"""CLI entry for ai_prep_tool sandbox."""

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI prep tool sandbox")
    parser.add_argument("--input", default="input/sample.txt")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    print("CLI ready, input =", args.input)

    mark("r10-w1-ex1")
    input("请手动完成第1周自测后按回车继续...")
    mark("r10-w1-self")


if __name__ == "__main__":
    main()
'''

CORE_TEMPLATE = '''"""Core processing for ai_prep_tool sandbox."""


def run_pipeline(text: str) -> str:
    return text.strip().upper()


def main() -> None:
    print(run_pipeline("hello round10"))

    mark("r10-w1-ex1")
    input("请手动完成第1周自测后按回车继续...")
    mark("r10-w1-self")


if __name__ == "__main__":
    main()
'''

IO_TEMPLATE = '''"""IO helpers for ai_prep_tool sandbox."""

from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
'''


def main() -> None:
    base = Path.home() / "cli-lab" / "round10" / "week1" / "ai_prep_tool"
    base.mkdir(parents=True, exist_ok=True)
    (base / "input").mkdir(exist_ok=True)

    (base / "cli.py").write_text(CLI_TEMPLATE, encoding="utf-8")
    (base / "core.py").write_text(CORE_TEMPLATE, encoding="utf-8")
    (base / "io_utils.py").write_text(IO_TEMPLATE, encoding="utf-8")
    (base / "input" / "sample.txt").write_text("hello\n", encoding="utf-8")

    print("已生成 Round 10 Week 1 模块骨架:", base)
    print("建议依次运行: python3 cli.py  与  python3 core.py")

    mark("r10-w1-ex1")
    input("请手动完成第1周自测后按回车继续...")
    mark("r10-w1-self")


if __name__ == "__main__":
    main()
