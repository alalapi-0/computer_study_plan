#!/usr/bin/env python3
"""Round 10 · Week 2: config.ini and logging setup."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round10" / "week2_auto" / "ai_prep_tool"


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], check=True)


CONFIG_TEMPLATE = """[defaults]
output_dir = output
log_dir = logs
min_length = 3

[filter]
dedup = true
"""

CONFIG_PY = '''"""Configuration helpers for ai_prep_tool sandbox."""

import configparser
from pathlib import Path


def load_config(config_path: str = "config.ini") -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    if Path(config_path).exists():
        config.read(config_path)
    return config


def get_output_dir(config: configparser.ConfigParser) -> str:
    return config.get("defaults", "output_dir", fallback="output")


def get_log_dir(config: configparser.ConfigParser) -> str:
    return config.get("defaults", "log_dir", fallback="logs")


def get_min_length(config: configparser.ConfigParser) -> int:
    return config.getint("defaults", "min_length", fallback=1)


def get_dedup(config: configparser.ConfigParser) -> bool:
    return config.getboolean("filter", "dedup", fallback=False)
'''

LOG_UTILS_TEMPLATE = '''"""Logging helpers for ai_prep_tool sandbox."""

import logging
from pathlib import Path


def setup_logging(log_dir: str = "logs", level: int = logging.INFO) -> None:
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(Path(log_dir) / "app.log", encoding="utf-8"),
        ],
        force=True,
    )
'''

CORE_TEMPLATE = '''"""Core processing with logging."""

import logging

logger = logging.getLogger(__name__)


def filter_records(records: list[str], min_length: int) -> list[str]:
    result = [item.strip() for item in records if len(item.strip()) >= min_length]
    logger.info("filter_records: %s -> %s", len(records), len(result))
    return result


def dedup_records(records: list[str]) -> list[str]:
    result = list(dict.fromkeys(records))
    logger.info("dedup_records: %s -> %s", len(records), len(result))
    return result
'''

APP_TEMPLATE = '''"""Small app wiring config, logging, and core helpers."""

from pathlib import Path

from config import get_dedup, get_log_dir, get_min_length, get_output_dir, load_config
from core import dedup_records, filter_records
from log_utils import setup_logging


def main() -> None:
    config = load_config("config.ini")
    setup_logging(get_log_dir(config))
    records = [line.strip() for line in Path("input/sample.txt").read_text(encoding="utf-8").splitlines() if line.strip()]
    records = filter_records(records, get_min_length(config))
    if get_dedup(config):
        records = dedup_records(records)
    output = Path(get_output_dir(config)) / "result.txt"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\\n".join(records) + "\\n", encoding="utf-8")
    print(f"written: {output}")


if __name__ == "__main__":
    main()
'''


def main() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    (LAB / "input").mkdir(parents=True)
    (LAB / "output").mkdir()
    (LAB / "logs").mkdir()

    (LAB / "config.ini").write_text(CONFIG_TEMPLATE, encoding="utf-8")
    (LAB / "config.py").write_text(CONFIG_PY, encoding="utf-8")
    (LAB / "log_utils.py").write_text(LOG_UTILS_TEMPLATE, encoding="utf-8")
    (LAB / "core.py").write_text(CORE_TEMPLATE, encoding="utf-8")
    (LAB / "app.py").write_text(APP_TEMPLATE, encoding="utf-8")
    (LAB / "input" / "sample.txt").write_text("ai\nprep\nprep\ntool\n", encoding="utf-8")

    result = subprocess.run(["python3", "app.py"], cwd=LAB, check=True, capture_output=True, text=True)
    output = (LAB / "output" / "result.txt").read_text(encoding="utf-8").splitlines()
    log_text = (LAB / "logs" / "app.log").read_text(encoding="utf-8")
    assert output == ["prep", "tool"], output
    assert "filter_records" in log_text and "dedup_records" in log_text, log_text
    (LAB / "week2_report.txt").write_text(result.stdout + "\n" + log_text, encoding="utf-8")
    (LAB / "next_steps.txt").write_text(
        "Week 2 自动练习已生成 config.ini、config.py、log_utils.py，并写出 output/result.txt 与 logs/app.log。\n"
        "自测请在 Web UI 点击 r10-w2-self 的“终端练习”，自己读取 config.ini 并初始化 logging。\n"
        "能解释 fallback、日志级别和日志文件位置后，再点击“记录并完成”。\n",
        encoding="utf-8",
    )

    print("project:", LAB)
    print("config_min_length: 3")
    print(result.stdout.strip())
    print("log:", LAB / "logs" / "app.log")

    mark("r10-w2-ex2")
    print("Week 2 自动练习完成。请继续在 Web UI 点击“记录并完成”保存 r10-w2-self。")


if __name__ == "__main__":
    main()
