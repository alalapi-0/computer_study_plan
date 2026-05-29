#!/usr/bin/env python3
"""Round 07 · Week 1 exercises: pathlib and file formats."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round7" / "week1"
    base.mkdir(parents=True, exist_ok=True)

    txt_file = base / "labels.txt"
    txt_file.write_text("ok\nblur\nok\n", encoding="utf-8")

    lines = [line.strip() for line in txt_file.read_text(encoding="utf-8").splitlines() if line.strip()]

    print("工作目录:", base)
    print("TXT 行数:", len(lines))
    print("建议补充: 在此目录手动创建 csv/json/jsonl 文件并扩展读取脚本。")


if __name__ == "__main__":
    main()
