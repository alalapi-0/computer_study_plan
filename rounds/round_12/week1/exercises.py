#!/usr/bin/env python3
"""Round 12 · Week 1: batch scanning, output names, and failure records."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round12" / "week1_auto" / "batch_pipeline"


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> tuple[Path, Path]:
    input_dir = LAB / "input"
    output_dir = LAB / "output"
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    for directory in (input_dir, output_dir):
        for path in directory.glob("*"):
            if path.is_file():
                path.unlink()
    (LAB / "failures.log").unlink(missing_ok=True)
    (LAB / "batch_report.json").unlink(missing_ok=True)
    (LAB / "next_steps.txt").unlink(missing_ok=True)
    return input_dir, output_dir


def seed_inputs(input_dir: Path) -> None:
    samples = {
        "alpha.txt": "apple\nbanana\n",
        "beta.txt": "carrot\nbanana\n",
        "broken.txt": "BROKEN\nthis file simulates a parse failure\n",
    }
    for name, text in samples.items():
        (input_dir / name).write_text(text, encoding="utf-8")


def scan_inputs(input_dir: Path) -> list[Path]:
    return sorted(input_dir.glob("*.txt"))


def make_output_path(input_file: Path, output_dir: Path, index: int) -> Path:
    return output_dir / f"{index:02d}_{input_file.stem}_clean.txt"


def process_file(input_file: Path, output_file: Path) -> int:
    lines = [line.strip() for line in input_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    if any(line == "BROKEN" for line in lines):
        raise ValueError("simulated parse failure")
    cleaned = sorted(set(lines))
    output_file.write_text("\n".join(cleaned) + "\n", encoding="utf-8")
    return len(cleaned)


def run_batch(input_dir: Path, output_dir: Path) -> dict:
    successes: list[dict] = []
    failures: list[dict] = []
    for index, input_file in enumerate(scan_inputs(input_dir), start=1):
        output_file = make_output_path(input_file, output_dir, index)
        try:
            processed_count = process_file(input_file, output_file)
        except Exception as exc:  # noqa: BLE001 - this exercise records per-file failures.
            failures.append({"file": input_file.name, "error": str(exc)})
        else:
            successes.append(
                {
                    "input": input_file.name,
                    "output": output_file.name,
                    "processed_count": processed_count,
                }
            )
    report = {
        "input_count": len(successes) + len(failures),
        "success_count": len(successes),
        "failure_count": len(failures),
        "successes": successes,
        "failures": failures,
    }
    (LAB / "batch_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if failures:
        (LAB / "failures.log").write_text(
            "\n".join(f"{item['file']}: {item['error']}" for item in failures) + "\n",
            encoding="utf-8",
        )
    (LAB / "next_steps.txt").write_text(
        "自己在浏览器终端写一个 scan_demo.py，再手动记录 r12-w1-self。\n",
        encoding="utf-8",
    )
    return report


def main() -> None:
    input_dir, output_dir = reset_lab()
    seed_inputs(input_dir)
    report = run_batch(input_dir, output_dir)
    if report["success_count"] != 2 or report["failure_count"] != 1:
        raise RuntimeError(f"unexpected batch report: {report}")
    print("Round 12 Week 1 批处理扫描")
    print("sandbox:", LAB)
    print("input_count:", report["input_count"])
    print("success_count:", report["success_count"])
    print("failure_count:", report["failure_count"])
    print("report:", LAB / "batch_report.json")
    print("failure_log:", LAB / "failures.log")
    mark("r12-w1-ex1")


if __name__ == "__main__":
    main()
