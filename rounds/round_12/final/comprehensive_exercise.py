#!/usr/bin/env python3
"""Round 12 · Final: complete local pipeline automation rehearsal."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round12" / "final_auto" / "ai_prep_tool"


LOG_UTILS = '''"""Log helpers for the Round 12 final pipeline."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(log_path: Path, max_bytes: int = 500, backup_count: int = 2) -> logging.Logger:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("round12_final")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    handler = RotatingFileHandler(log_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    return logger
'''

PIPELINE = '''"""Tiny batch pipeline for Round 12 final rehearsal."""

import json
from pathlib import Path
from log_utils import setup_logger


def scan(input_dir: Path) -> list[Path]:
    return sorted(input_dir.glob("*.txt"))


def run_pipeline(base: Path) -> dict:
    input_dir = base / "input"
    output_dir = base / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    logger = setup_logger(base / "logs" / "pipeline.log")
    successes = []
    failures = []
    for index, input_file in enumerate(scan(input_dir), start=1):
        output_file = output_dir / f"{index:02d}_{input_file.stem}.out.txt"
        try:
            lines = [line.strip() for line in input_file.read_text(encoding="utf-8").splitlines() if line.strip()]
            if any(line == "BROKEN" for line in lines):
                raise ValueError("simulated parse failure")
            cleaned = sorted(set(lines))
            output_file.write_text("\\n".join(cleaned) + "\\n", encoding="utf-8")
            successes.append({"input": input_file.name, "output": output_file.name, "count": len(cleaned)})
            logger.info("OK %s -> %s", input_file.name, output_file.name)
        except Exception as exc:
            failures.append({"input": input_file.name, "error": str(exc)})
            logger.error("FAILED %s %s", input_file.name, exc)
    summary = {"success_count": len(successes), "failure_count": len(failures), "successes": successes, "failures": failures}
    (base / "batch_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
    if failures:
        (base / "failures.log").write_text("\\n".join(f"{item['input']}: {item['error']}" for item in failures) + "\\n", encoding="utf-8")
    return summary
'''

WORKER = '''#!/usr/bin/env python3
from pathlib import Path
from pipeline import run_pipeline

base = Path(__file__).resolve().parent
summary = run_pipeline(base)
print(f"success={summary['success_count']} failure={summary['failure_count']}")
'''

RUN_BATCH_SH = """#!/usr/bin/env bash
# Round 12 final scheduled-entry rehearsal. Review before using with cron.
set -euo pipefail
BASE="${HOME}/cli-lab/round12/final_auto/ai_prep_tool"
mkdir -p "${BASE}/logs"
python3 "${BASE}/batch_worker.py" >> "${BASE}/logs/batch_entry.log" 2>&1
"""

CRON_EXAMPLE = """# Example only. Do not install automatically.
# */30 * * * * ${HOME}/cli-lab/round12/final_auto/ai_prep_tool/scripts/run_batch.sh
"""

NOHUP_TMUX_NOTES = """nohup:
  nohup bash scripts/run_batch.sh >> logs/nohup.log 2>&1 &

tmux:
  tmux new -s round12-final
  bash scripts/run_batch.sh

These commands are examples only. This final script does not start background jobs.
"""


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> None:
    LAB.mkdir(parents=True, exist_ok=True)
    for child in LAB.iterdir():
        if child.is_file():
            child.unlink()
        elif child.is_dir():
            shutil.rmtree(child)
    for rel in ("input", "output", "archive", "logs", "scripts"):
        (LAB / rel).mkdir(parents=True, exist_ok=True)


def write_project() -> None:
    (LAB / "log_utils.py").write_text(LOG_UTILS, encoding="utf-8")
    (LAB / "pipeline.py").write_text(PIPELINE, encoding="utf-8")
    worker = LAB / "batch_worker.py"
    worker.write_text(WORKER, encoding="utf-8")
    worker.chmod(0o755)
    run_sh = LAB / "scripts" / "run_batch.sh"
    run_sh.write_text(RUN_BATCH_SH, encoding="utf-8")
    run_sh.chmod(0o755)
    (LAB / "cron_example.txt").write_text(CRON_EXAMPLE, encoding="utf-8")
    (LAB / "nohup_tmux_notes.txt").write_text(NOHUP_TMUX_NOTES, encoding="utf-8")
    (LAB / ".gitignore").write_text("archive/*.zip\nlogs/*.log*\noutput/*.txt\n", encoding="utf-8")
    (LAB / "README.md").write_text(
        "# Round 12 final sandbox\n\nLocal batch pipeline rehearsal. Do not install cron automatically.\n",
        encoding="utf-8",
    )


def seed_inputs() -> None:
    samples = {
        "one.txt": "alpha\nbeta\nalpha\n",
        "two.txt": "gamma\ndelta\n",
        "broken.txt": "BROKEN\nneeds retry\n",
    }
    for name, text in samples.items():
        (LAB / "input" / name).write_text(text, encoding="utf-8")


def run_worker() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(LAB / "batch_worker.py")],
        cwd=LAB,
        capture_output=True,
        text=True,
        check=False,
    )


def archive_output() -> Path:
    archive_base = LAB / "archive" / "round12_output"
    return Path(shutil.make_archive(str(archive_base), "zip", LAB / "output"))


def exercise_rotation() -> list[str]:
    spec = importlib.util.spec_from_file_location("round12_final_log_utils", LAB / "log_utils.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load log_utils.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    logger = module.setup_logger(LAB / "logs" / "final_rotation.log", max_bytes=300, backup_count=2)
    for index in range(40):
        logger.info("rotation proof %s %s", index, "x" * 30)
    return sorted(path.name for path in (LAB / "logs").glob("final_rotation.log*"))


def main() -> None:
    reset_lab()
    write_project()
    seed_inputs()
    proc = run_worker()
    archive_path = archive_output()
    rotation_files = exercise_rotation()
    summary = json.loads((LAB / "batch_summary.json").read_text(encoding="utf-8"))
    final_report = {
        "worker_returncode": proc.returncode,
        "worker_stdout": proc.stdout.strip(),
        "success_count": summary["success_count"],
        "failure_count": summary["failure_count"],
        "archive_exists": archive_path.exists(),
        "archive": str(archive_path),
        "rotation_files": rotation_files,
        "required_files": {
            "pipeline.py": (LAB / "pipeline.py").exists(),
            "log_utils.py": (LAB / "log_utils.py").exists(),
            "scripts/run_batch.sh": (LAB / "scripts" / "run_batch.sh").exists(),
            "cron_example.txt": (LAB / "cron_example.txt").exists(),
            "nohup_tmux_notes.txt": (LAB / "nohup_tmux_notes.txt").exists(),
            "failures.log": (LAB / "failures.log").exists(),
        },
    }
    (LAB / "round12_summary.json").write_text(json.dumps(final_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if (
        final_report["worker_returncode"] != 0
        or final_report["success_count"] != 2
        or final_report["failure_count"] != 1
        or not final_report["archive_exists"]
        or not rotation_files
        or not all(final_report["required_files"].values())
    ):
        raise RuntimeError(f"Round 12 final check failed: {final_report}")
    print("Round 12 收口检查")
    print("sandbox:", LAB)
    print("worker_stdout:", final_report["worker_stdout"])
    print("success_count:", final_report["success_count"])
    print("failure_count:", final_report["failure_count"])
    print("archive:", archive_path)
    print("rotation_files:", ", ".join(rotation_files))
    print("summary:", LAB / "round12_summary.json")
    mark("r12-fin-comp")


if __name__ == "__main__":
    main()
