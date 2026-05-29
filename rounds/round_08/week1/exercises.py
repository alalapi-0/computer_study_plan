#!/usr/bin/env python3
"""Round 08 · Week 1 exercises: project cleanup and test stubs."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round8" / "week1" / "ai_prep_tool"
    (base / "tests").mkdir(parents=True, exist_ok=True)

    readme = base / "README.md"
    readme.write_text("# ai_prep_tool\n\nRound 08 weekly sandbox\n", encoding="utf-8")

    test_file = base / "tests" / "test_basic.py"
    test_file.write_text(
        "def test_smoke():\n"
        "    assert 1 + 1 == 2\n",
        encoding="utf-8",
    )

    print("已生成最小项目骨架:", base)
    print("下一步可在本地安装 pytest 后运行 tests。")


if __name__ == "__main__":
    main()
