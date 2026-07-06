#!/usr/bin/env python3
"""Round 09 · Week 3: pure functions and pytest-style checks."""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round9" / "week3_auto"


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], check=True)


def write_project(base: Path) -> None:
    (base / "tests").mkdir(parents=True)
    (base / "ai_prep_tool.py").write_text(
        "from pathlib import Path\n\n"
        "def dedup_records(records):\n"
        "    seen = set()\n"
        "    result = []\n"
        "    for item in records:\n"
        "        if item not in seen:\n"
        "            seen.add(item)\n"
        "            result.append(item)\n"
        "    return result\n\n"
        "def read_txt(path):\n"
        "    return [line.strip() for line in Path(path).read_text().splitlines() if line.strip()]\n",
        encoding="utf-8",
    )
    (base / "tests" / "test_dedup.py").write_text(
        "from ai_prep_tool import dedup_records, read_txt\n\n"
        "def test_dedup_basic():\n"
        "    assert dedup_records(['a', 'b', 'a']) == ['a', 'b']\n\n"
        "def test_dedup_preserves_order():\n"
        "    assert dedup_records(['b', 'a', 'b', 'c']) == ['b', 'a', 'c']\n\n"
        "def test_dedup_empty():\n"
        "    assert dedup_records([]) == []\n\n"
        "def test_dedup_no_duplicates():\n"
        "    assert dedup_records(['a', 'b', 'c']) == ['a', 'b', 'c']\n\n"
        "def test_dedup_all_same():\n"
        "    assert dedup_records(['x', 'x', 'x']) == ['x']\n\n"
        "def test_read_txt(tmp_file='input.txt'):\n"
        "    from pathlib import Path\n"
        "    test_file = Path(__file__).resolve().parents[1] / tmp_file\n"
        "    test_file.write_text('line1\\nline2\\n')\n"
        "    assert read_txt(test_file) == ['line1', 'line2']\n",
        encoding="utf-8",
    )
    (base / "run_tests.py").write_text(
        "import importlib.util\n"
        "from pathlib import Path\n\n"
        "spec = importlib.util.spec_from_file_location('test_dedup', Path('tests/test_dedup.py'))\n"
        "module = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(module)\n"
        "for name in sorted(n for n in dir(module) if n.startswith('test_')):\n"
        "    getattr(module, name)()\n"
        "print('tests: ok')\n",
        encoding="utf-8",
    )


def run_tests(base: Path) -> str:
    sys.path.insert(0, str(base))
    try:
        spec = importlib.util.spec_from_file_location("test_dedup", base / "tests" / "test_dedup.py")
        if spec is None or spec.loader is None:
            raise RuntimeError("cannot_load_test_dedup")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        names = sorted(name for name in dir(module) if name.startswith("test_"))
        for name in names:
            getattr(module, name)()
    finally:
        sys.path.pop(0)
    report = f"tests: ok ({len(names)} passed)\n"
    (base / "test_report.txt").write_text(report, encoding="utf-8")
    return report.strip()


def main() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    write_project(LAB)
    report = run_tests(LAB)
    (LAB / "next_steps.txt").write_text(
        "Week 3 自动练习已生成 ai_prep_tool.py、tests/test_dedup.py 和 run_tests.py。\n"
        "自测请在 Web UI 点击 r09-w3-self 的“终端练习”，自己写 test_dedup.py 并运行。\n"
        "能解释纯函数、边界样例和 pytest 风格命名后，再点击“记录并完成”。\n",
        encoding="utf-8",
    )

    print("project:", LAB)
    print(report)
    print("test-file:", LAB / "tests" / "test_dedup.py")

    mark("r09-w3-ex3")
    print("Week 3 自动练习完成。请继续在 Web UI 点击“记录并完成”保存 r09-w3-self。")


if __name__ == "__main__":
    main()
