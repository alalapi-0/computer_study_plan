#!/usr/bin/env python3
"""Round 12 · Week 2 exercises: subprocess wrapper and archive."""

import shutil
import subprocess
import sys
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


def archive_summary(base: Path) -> Path:
    archive_dir = base / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    summary = base / "output" / "batch_summary.txt"
    if not summary.exists():
        summary.write_text("no output yet\n", encoding="utf-8")
    dest = archive_dir / summary.name
    shutil.copy2(summary, dest)
    return dest


def main() -> None:
    base = Path.home() / "cli-lab" / "round12" / "week2"
    base.mkdir(parents=True, exist_ok=True)
    week1_script = Path(__file__).resolve().parents[1] / "week1" / "exercises.py"

    proc = subprocess.run(
        [sys.executable, str(week1_script)],
        cwd=base,
        capture_output=True,
        text=True,
        check=False,
    )
    print("week1 返回码:", proc.returncode)
    if proc.stdout:
        print(proc.stdout.strip())

    archived = archive_summary(base)
    print("已归档摘要:", archived)

    mark("r12-w2-ex2")
    input("请手动完成第2周自测后按回车继续...")
    mark("r12-w2-self")


if __name__ == "__main__":
    main()
