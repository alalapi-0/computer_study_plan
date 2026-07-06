#!/usr/bin/env python3
"""Round 12 · Week 3: log rotation and scheduled-entry rehearsal."""

from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round12" / "week3_auto" / "scheduled_pipeline"


LOG_UTILS = '''"""Logging helpers for Round 12 scheduled pipeline rehearsal."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(log_path: Path, max_bytes: int = 400, backup_count: int = 2) -> logging.Logger:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("round12_pipeline")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    handler = RotatingFileHandler(
        log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    return logger
'''

RUN_BATCH_SH = """#!/usr/bin/env bash
# Round 12 scheduled-entry rehearsal. Review paths before using with cron.
set -euo pipefail
BASE="${HOME}/cli-lab/round12/week3_auto/scheduled_pipeline"
mkdir -p "${BASE}/logs"
printf '[%s] batch entry reached\\n' "$(date)" >> "${BASE}/logs/batch_entry.log"
"""

CRON_EXAMPLE = """# Example only. Do not install automatically.
# */30 * * * * ${HOME}/cli-lab/round12/week3_auto/scheduled_pipeline/scripts/run_batch.sh
"""

NOHUP_TMUX_NOTES = """nohup example:
  nohup bash scripts/run_batch.sh >> logs/nohup.log 2>&1 &

tmux example:
  tmux new -s round12-batch
  bash scripts/run_batch.sh

These are notes only. This exercise does not start background jobs.
"""


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> tuple[Path, Path]:
    package_dir = LAB / "ai_prep_tool"
    scripts_dir = LAB / "scripts"
    logs_dir = LAB / "logs"
    for directory in (package_dir, scripts_dir, logs_dir):
        directory.mkdir(parents=True, exist_ok=True)
        for path in directory.glob("*"):
            if path.is_file():
                path.unlink()
    return package_dir, scripts_dir


def write_files(package_dir: Path, scripts_dir: Path) -> Path:
    log_utils = package_dir / "log_utils.py"
    log_utils.write_text(LOG_UTILS, encoding="utf-8")
    run_sh = scripts_dir / "run_batch.sh"
    run_sh.write_text(RUN_BATCH_SH, encoding="utf-8")
    run_sh.chmod(0o755)
    (LAB / "cron_example.txt").write_text(CRON_EXAMPLE, encoding="utf-8")
    (LAB / "nohup_tmux_notes.txt").write_text(NOHUP_TMUX_NOTES, encoding="utf-8")
    (LAB / "next_steps.txt").write_text(
        "自己在浏览器终端写 log_demo.py，再点击“记录并完成”保存记录 r12-w3-self。\n",
        encoding="utf-8",
    )
    return log_utils


def exercise_rotation(log_utils: Path) -> list[Path]:
    spec = importlib.util.spec_from_file_location("round12_log_utils", log_utils)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load log_utils.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    logger = module.setup_logger(LAB / "logs" / "app.log", max_bytes=300, backup_count=2)
    for index in range(50):
        logger.info("batch item %s %s", index, "x" * 30)
    return sorted((LAB / "logs").glob("app.log*"))


def main() -> None:
    package_dir, scripts_dir = reset_lab()
    log_utils = write_files(package_dir, scripts_dir)
    log_files = exercise_rotation(log_utils)
    if not log_files:
        raise RuntimeError("log rotation did not create log files")
    print("Round 12 Week 3 日志轮转与定时入口排练")
    print("sandbox:", LAB)
    print("log_utils:", log_utils)
    print("run_batch:", scripts_dir / "run_batch.sh")
    print("cron_example:", LAB / "cron_example.txt")
    print("nohup_tmux_notes:", LAB / "nohup_tmux_notes.txt")
    print("log_files:", ", ".join(path.name for path in log_files))
    mark("r12-w3-ex3")


if __name__ == "__main__":
    main()
