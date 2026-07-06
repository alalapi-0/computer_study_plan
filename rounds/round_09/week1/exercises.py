#!/usr/bin/env python3
"""Round 09 · Week 1: repo layout and baseline docs."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round9" / "week1_auto" / "ai_prep_tool"


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], check=True)


def write_project(base: Path) -> dict[str, bool]:
    (base / "tests").mkdir(parents=True)
    (base / "input").mkdir()
    (base / "output").mkdir()
    (base / "logs").mkdir()

    readme = base / "README.md"
    readme.write_text(
        "# AI Prep Tool\n\n"
        "一个命令行数据预处理练习项目，支持读取、去重和统计的最小演示。\n\n"
        "## 运行\n\n"
        "```bash\npython3 ai_prep_tool.py\n```\n\n"
        "## 测试\n\n"
        "```bash\npython3 run_tests.py\n```\n",
        encoding="utf-8",
    )
    gitignore = base / ".gitignore"
    gitignore.write_text(
        "__pycache__/\n*.py[cod]\n.venv/\nvenv/\noutput/\nlogs/\n*.log\n*.db\n.DS_Store\n",
        encoding="utf-8",
    )
    (base / "ai_prep_tool.py").write_text(
        "def dedup_records(items):\n"
        "    return list(dict.fromkeys(items))\n\n"
        "if __name__ == '__main__':\n"
        "    print(dedup_records(['ok', 'blur', 'ok']))\n",
        encoding="utf-8",
    )
    (base / "tests" / "test_dedup.py").write_text(
        "from ai_prep_tool import dedup_records\n\n"
        "def test_dedup_basic():\n"
        "    assert dedup_records(['a', 'b', 'a']) == ['a', 'b']\n",
        encoding="utf-8",
    )
    (base / "run_tests.py").write_text(
        "import importlib.util\n"
        "from pathlib import Path\n\n"
        "spec = importlib.util.spec_from_file_location('test_dedup', Path('tests/test_dedup.py'))\n"
        "module = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(module)\n"
        "module.test_dedup_basic()\n"
        "print('tests: ok')\n",
        encoding="utf-8",
    )

    readme_text = readme.read_text(encoding="utf-8")
    gitignore_text = gitignore.read_text(encoding="utf-8")
    checks = {
        "readme_has_purpose": "数据预处理" in readme_text,
        "readme_has_run": "python3 ai_prep_tool.py" in readme_text,
        "gitignore_has_cache": "__pycache__/" in gitignore_text and "*.py[cod]" in gitignore_text,
        "gitignore_has_venv": ".venv/" in gitignore_text and "venv/" in gitignore_text,
        "gitignore_has_outputs": "output/" in gitignore_text and "logs/" in gitignore_text,
    }
    report = "\n".join(f"{key}: {'OK' if ok else 'MISSING'}" for key, ok in checks.items()) + "\n"
    (base / "layout_report.txt").write_text(report, encoding="utf-8")
    (base / "next_steps.txt").write_text(
        "Week 1 自动练习已生成 README、.gitignore、ai_prep_tool.py、tests/test_dedup.py 和 run_tests.py。\n"
        "自测请在 Web UI 点击 r09-w1-self 的“终端练习”，自己写 README / .gitignore / ai_prep_tool.py。\n"
        "能解释 README 和 .gitignore 的作用后，再点击“记录并完成”。\n",
        encoding="utf-8",
    )
    return checks


def main() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    checks = write_project(LAB)

    subprocess.run(["python3", "run_tests.py"], cwd=LAB, check=True)
    print("project:", LAB)
    for key, ok in checks.items():
        print(f"{key}:", "OK" if ok else "MISSING")

    mark("r09-w1-ex1")
    print("Week 1 自动练习完成。请继续在 Web UI 点击“记录并完成”保存 r09-w1-self。")


if __name__ == "__main__":
    main()
