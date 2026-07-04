#!/usr/bin/env python3
"""Round 09 · Week 2: local Git branch workflow rehearsal."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round9" / "week2_auto" / "workflow_demo"


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], check=True)


def git(args: list[str], cwd: Path) -> str:
    proc = subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)
    return (proc.stdout + proc.stderr).strip()


def main() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    LAB.mkdir(parents=True)

    transcript: list[str] = []

    def run(args: list[str]) -> None:
        transcript.append("$ git " + " ".join(args))
        output = git(args, LAB)
        if output:
            transcript.append(output)

    run(["init"])
    run(["checkout", "-b", "main"])
    run(["config", "user.email", "learner@example.local"])
    run(["config", "user.name", "Learner"])

    (LAB / "README.md").write_text("# Workflow Demo\n\nRound 09 local Git sandbox.\n", encoding="utf-8")
    run(["add", "README.md"])
    run(["commit", "-m", "init"])

    run(["checkout", "-b", "feature/improve-readme"])
    (LAB / "README.md").write_text("# Workflow Demo\n\nFeature branch note.\n", encoding="utf-8")
    run(["add", "README.md"])
    run(["commit", "-m", "feature-readme-note"])
    run(["checkout", "main"])
    run(["merge", "feature/improve-readme"])
    run(["branch", "-d", "feature/improve-readme"])

    run(["checkout", "-b", "hotfix/empty-input"])
    (LAB / "empty_input.txt").write_text("handle empty input gracefully\n", encoding="utf-8")
    run(["add", "empty_input.txt"])
    run(["commit", "-m", "fix-empty-input-note"])
    run(["checkout", "main"])
    run(["merge", "hotfix/empty-input"])
    run(["branch", "-d", "hotfix/empty-input"])

    log = git(["log", "--oneline"], LAB)
    transcript.append("$ git log --oneline")
    transcript.append(log)
    (LAB / "git_log.txt").write_text(log + "\n", encoding="utf-8")
    (LAB / "workflow_transcript.txt").write_text("\n".join(transcript) + "\n", encoding="utf-8")
    (LAB / "next_steps.txt").write_text(
        "Week 2 自动练习已在本地沙盒仓库完成 feature 与 hotfix 分支合并。\n"
        "自测请在 Web UI 点击 r09-w2-self 的“终端”，自己走一遍 git init / branch / commit / merge。\n"
        "只在 ~/cli-lab/round9 内练习，不做 push/pull/remote。\n",
        encoding="utf-8",
    )

    print("repo:", LAB)
    print("commits:", len(log.splitlines()))
    print("branches:", git(["branch"], LAB).replace("\n", " | "))
    print("log-file:", LAB / "git_log.txt")

    mark("r09-w2-ex2")
    print("Week 2 自动练习完成。请继续手动完成 r09-w2-self。")


if __name__ == "__main__":
    main()
