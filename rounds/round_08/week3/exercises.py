import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


#!/usr/bin/env python3
"""Round 08 · Week 3 exercises: API shape rehearsal."""


def build_health() -> dict[str, str]:
    return {"status": "ok"}


def build_run_response(input_file: str, dedup: bool) -> dict[str, object]:
    return {
        "status": "accepted",
        "input_file": input_file,
        "dedup": dedup,
    }


def main() -> None:
    print("health:", build_health())
    print("run:", build_run_response("input/demo.txt", True))

    mark("r08-w3-ex3")
    input("请手动完成第3周自测后按回车继续...")
    mark("r08-w3-self")


if __name__ == "__main__":
    main()
