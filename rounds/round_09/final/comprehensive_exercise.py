#!/usr/bin/env python3
"""Round 09 · Final: repo readiness checklist runner."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round9" / "final_auto"


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], check=True)


def git(args: list[str], cwd: Path) -> str:
    proc = subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)
    return (proc.stdout + proc.stderr).strip()


def write_layout(base: Path) -> dict[str, bool]:
    project = base / "ai_prep_tool"
    (project / "tests").mkdir(parents=True)
    (project / "input").mkdir()
    (project / "output").mkdir()
    (project / "logs").mkdir()
    (project / "README.md").write_text(
        "# AI Prep Tool\n\nA small repo normalization and testing demo.\n\nRun: `python3 run_tests.py`.\n",
        encoding="utf-8",
    )
    (project / ".gitignore").write_text("__pycache__/\n*.py[cod]\n.venv/\nvenv/\noutput/\nlogs/\n*.log\n", encoding="utf-8")
    return {
        "readme": (project / "README.md").exists(),
        "gitignore": (project / ".gitignore").exists(),
        "tests_dir": (project / "tests").is_dir(),
    }


def write_git_workflow(base: Path) -> int:
    repo = base / "workflow_demo"
    repo.mkdir()
    git(["init"], repo)
    git(["checkout", "-b", "main"], repo)
    git(["config", "user.email", "learner@example.local"], repo)
    git(["config", "user.name", "Learner"], repo)
    (repo / "README.md").write_text("# Workflow Demo\n", encoding="utf-8")
    git(["add", "README.md"], repo)
    git(["commit", "-m", "init"], repo)
    git(["checkout", "-b", "feature/readme-note"], repo)
    (repo / "README.md").write_text("# Workflow Demo\n\nFeature note.\n", encoding="utf-8")
    git(["add", "README.md"], repo)
    git(["commit", "-m", "feature-readme-note"], repo)
    git(["checkout", "main"], repo)
    git(["merge", "feature/readme-note"], repo)
    git(["branch", "-d", "feature/readme-note"], repo)
    log = git(["log", "--oneline"], repo)
    (repo / "git_log.txt").write_text(log + "\n", encoding="utf-8")
    return len(log.splitlines())


def write_tests(base: Path) -> int:
    project = base / "test_project"
    (project / "tests").mkdir(parents=True)
    (project / "ai_prep_tool.py").write_text(
        "def dedup_records(records):\n"
        "    return list(dict.fromkeys(records))\n",
        encoding="utf-8",
    )
    (project / "tests" / "test_dedup.py").write_text(
        "from ai_prep_tool import dedup_records\n\n"
        "def test_basic():\n"
        "    assert dedup_records(['a', 'b', 'a']) == ['a', 'b']\n\n"
        "def test_empty():\n"
        "    assert dedup_records([]) == []\n\n"
        "def test_all_same():\n"
        "    assert dedup_records(['x', 'x']) == ['x']\n",
        encoding="utf-8",
    )
    sys.path.insert(0, str(project))
    try:
        spec = importlib.util.spec_from_file_location("test_dedup", project / "tests" / "test_dedup.py")
        if spec is None or spec.loader is None:
            raise RuntimeError("cannot_load_final_tests")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        names = sorted(name for name in dir(module) if name.startswith("test_"))
        for name in names:
            getattr(module, name)()
    finally:
        sys.path.pop(0)
    return len(names)


def main() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    LAB.mkdir(parents=True)

    layout = write_layout(LAB)
    commits = write_git_workflow(LAB)
    tests = write_tests(LAB)
    summary = {
        "layout": layout,
        "workflow_commits": commits,
        "tests_passed": tests,
        "sandbox": str(LAB),
    }
    (LAB / "round09_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("Round 09 收口检查")
    print("- layout:", "OK" if all(layout.values()) else "MISSING")
    print("- workflow_commits:", commits)
    print("- tests_passed:", tests)
    print("- summary:", LAB / "round09_summary.json")

    mark("r09-fin-comp")
    print("Round 09 Final 自动练习完成。请继续手动完成 r09-fin-sheet 与 r09-fin-acc1。")


if __name__ == "__main__":
    main()
