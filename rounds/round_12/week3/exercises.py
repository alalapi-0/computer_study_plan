#!/usr/bin/env python3
"""Round 12 · Week 3 exercises: logging rotation and cron entry stub."""

import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


LOG_UTILS = '''"""Logging helpers for ai_prep_tool sandbox (Round 12)."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(log_path: Path, max_bytes: int = 64_000, backup_count: int = 3) -> logging.Logger:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("ai_prep_tool")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = RotatingFileHandler(
            log_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(handler)
    return logger
'''

RUN_BATCH_SH = """#!/usr/bin/env bash
# Round 12 cron entry stub — edit paths before enabling crontab.
set -euo pipefail
BASE="${HOME}/cli-lab/round12"
REPO="${HOME}/PycharmProjects/computer_study_plan"
mkdir -p "${BASE}/logs"
python3 "${REPO}/rounds/round_12/week1/exercises.py" >> "${BASE}/logs/batch.log" 2>&1
"""


def main() -> None:
    base = Path.home() / "cli-lab" / "round12" / "week3" / "ai_prep_tool"
    scripts = Path.home() / "cli-lab" / "round12" / "scripts"
    base.mkdir(parents=True, exist_ok=True)
    scripts.mkdir(parents=True, exist_ok=True)

    (base / "log_utils.py").write_text(LOG_UTILS, encoding="utf-8")
    run_sh = scripts / "run_batch.sh"
    run_sh.write_text(RUN_BATCH_SH, encoding="utf-8")
    run_sh.chmod(0o755)

    print("已生成:", base / "log_utils.py")
    print("已生成:", run_sh)

    mark("r12-w3-ex3")
    input("请手动完成第3周自测后按回车继续...")
    mark("r12-w3-self")


if __name__ == "__main__":
    main()
