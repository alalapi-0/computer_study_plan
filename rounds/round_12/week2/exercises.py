#!/usr/bin/env python3
"""Round 12 · Week 2: subprocess wrapper and zip archive."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round12" / "week2_auto" / "archive_pipeline"


WORKER = '''#!/usr/bin/env python3
from pathlib import Path

base = Path(__file__).resolve().parent
output = base / "output"
output.mkdir(parents=True, exist_ok=True)
(output / "batch_summary.txt").write_text(
    "processed=3\\nfailed=0\\narchive_ready=yes\\n",
    encoding="utf-8",
)
print("worker_ok processed=3 failed=0")
'''


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> None:
    LAB.mkdir(parents=True, exist_ok=True)
    for rel in ("output", "archive"):
        directory = LAB / rel
        directory.mkdir(parents=True, exist_ok=True)
        for path in directory.glob("*"):
            if path.is_file():
                path.unlink()
    (LAB / "command_report.json").unlink(missing_ok=True)
    (LAB / "next_steps.txt").unlink(missing_ok=True)


def write_worker() -> Path:
    worker = LAB / "batch_worker.py"
    worker.write_text(WORKER, encoding="utf-8")
    worker.chmod(0o755)
    return worker


def run_worker(worker: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(worker)],
        cwd=LAB,
        capture_output=True,
        text=True,
        check=False,
    )


def archive_output() -> Path:
    archive_dir = LAB / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_base = archive_dir / "batch_output"
    zip_path = Path(shutil.make_archive(str(archive_base), "zip", LAB / "output"))
    return zip_path


def main() -> None:
    reset_lab()
    worker = write_worker()
    proc = run_worker(worker)
    zip_path = archive_output()
    report = {
        "worker": str(worker),
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "archive": str(zip_path),
        "archive_exists": zip_path.exists(),
    }
    (LAB / "command_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (LAB / "next_steps.txt").write_text(
        "自己在浏览器终端写 subprocess_demo.py，再点击“记录并完成”保存记录 r12-w2-self。\n",
        encoding="utf-8",
    )
    if proc.returncode != 0 or not zip_path.exists():
        raise RuntimeError(f"subprocess/archive check failed: {report}")
    print("Round 12 Week 2 子进程与归档")
    print("sandbox:", LAB)
    print("returncode:", proc.returncode)
    print("stdout:", proc.stdout.strip())
    print("archive:", zip_path)
    print("report:", LAB / "command_report.json")
    mark("r12-w2-ex2")


if __name__ == "__main__":
    main()
