#!/usr/bin/env python3
"""Round 08 · Week 1: project cleanup and no-dependency test runner."""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round8" / "week1_auto" / "ai_prep_tool"


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], check=True)


def write_project(base: Path) -> None:
    (base / "tests").mkdir(parents=True)
    (base / "input").mkdir()
    (base / "output").mkdir()
    (base / "logs").mkdir()
    (base / "README.md").write_text(
        "# ai_prep_tool\n\n"
        "Round 08 project cleanup sandbox.\n\n"
        "Run checks with:\n\n"
        "```bash\npython3 run_tests.py\n```\n",
        encoding="utf-8",
    )
    (base / ".gitignore").write_text(
        "__pycache__/\n*.py[cod]\n*.log\n*.db\noutput/\nlogs/\n.env\nvenv/\n",
        encoding="utf-8",
    )
    (base / "ai_prep_tool.py").write_text(
        "def dedup_records(items):\n"
        "    seen = set()\n"
        "    result = []\n"
        "    for item in items:\n"
        "        if item not in seen:\n"
        "            seen.add(item)\n"
        "            result.append(item)\n"
        "    return result\n\n"
        "def build_summary(original, processed):\n"
        "    return {\n"
        "        'original_count': len(original),\n"
        "        'processed_count': len(processed),\n"
        "        'removed_count': len(original) - len(processed),\n"
        "    }\n",
        encoding="utf-8",
    )
    (base / "tests" / "test_basic.py").write_text(
        "from ai_prep_tool import build_summary, dedup_records\n\n"
        "def test_dedup_removes_duplicates():\n"
        "    assert dedup_records(['a', 'b', 'a', 'c']) == ['a', 'b', 'c']\n\n"
        "def test_summary_counts():\n"
        "    summary = build_summary(['a', 'b', 'a'], ['a', 'b'])\n"
        "    assert summary['original_count'] == 3\n"
        "    assert summary['processed_count'] == 2\n"
        "    assert summary['removed_count'] == 1\n",
        encoding="utf-8",
    )
    (base / "run_tests.py").write_text(
        "import importlib.util\n"
        "from pathlib import Path\n\n"
        "test_path = Path('tests/test_basic.py')\n"
        "spec = importlib.util.spec_from_file_location('test_basic', test_path)\n"
        "module = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(module)\n"
        "for name in sorted(n for n in dir(module) if n.startswith('test_')):\n"
        "    getattr(module, name)()\n"
        "print('tests: ok')\n",
        encoding="utf-8",
    )
    (base / "next_steps.txt").write_text(
        "Week 1 自动练习已生成 ai_prep_tool 项目骨架和无依赖测试入口。\n"
        "自测请在 Web UI 点击 r08-w1-self 的“终端练习”，自己写 tests/test_basic.py 并运行。\n"
        "能解释 README、.gitignore、tests 和 run_tests.py 后，再点击“记录并完成”。\n",
        encoding="utf-8",
    )


def run_tests(base: Path) -> str:
    sys.path.insert(0, str(base))
    spec = importlib.util.spec_from_file_location("test_basic", base / "tests" / "test_basic.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot_load_test_basic")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    names = sorted(name for name in dir(module) if name.startswith("test_"))
    for name in names:
        getattr(module, name)()
    sys.path.pop(0)
    report = f"tests: ok ({len(names)} passed)\n"
    (base / "test_report.txt").write_text(report, encoding="utf-8")
    return report.strip()


def main() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    write_project(LAB)
    report = run_tests(LAB)

    print("project:", LAB)
    print(report)
    print("files:", "README.md, .gitignore, ai_prep_tool.py, tests/test_basic.py, run_tests.py")

    mark("r08-w1-ex1")
    print("Week 1 自动练习完成。请继续在 Web UI 点击“记录并完成”保存 r08-w1-self。")


if __name__ == "__main__":
    main()
