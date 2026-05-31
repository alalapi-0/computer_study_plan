#!/usr/bin/env python3
"""Round 10 · Week 2 exercises: config.ini and logging setup."""

from pathlib import Path


CONFIG_TEMPLATE = """[app]
input_dir = input
output_dir = output
log_level = INFO
"""

LOG_UTILS_TEMPLATE = '''"""Logging helpers for ai_prep_tool sandbox."""

import logging


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(message)s",
    )
'''


def main() -> None:
    base = Path.home() / "cli-lab" / "round10" / "week2" / "ai_prep_tool"
    base.mkdir(parents=True, exist_ok=True)
    (base / "output").mkdir(exist_ok=True)

    (base / "config.ini").write_text(CONFIG_TEMPLATE, encoding="utf-8")
    (base / "log_utils.py").write_text(LOG_UTILS_TEMPLATE, encoding="utf-8")

    print("已生成 Round 10 Week 2 配置与日志骨架:", base)
    print("请在 Python 中 import configparser 读取 config.ini 做一次打印验证。")


if __name__ == "__main__":
    main()
