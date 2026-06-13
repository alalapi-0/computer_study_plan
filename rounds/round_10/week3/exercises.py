import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


#!/usr/bin/env python3
"""Round 10 · Week 3 exercises: controlled errors and self checks."""


class PrepToolError(Exception):
    """Domain error for sandbox exercises."""


def normalize_records(records: list[str]) -> list[str]:
    if not records:
        raise PrepToolError("records must not be empty")
    return [item.strip() for item in records if item.strip()]


def run_self_checks() -> None:
    assert normalize_records([" a ", "b "]) == ["a", "b"]
    try:
        normalize_records([])
    except PrepToolError:
        pass
    else:
        raise AssertionError("expected PrepToolError")


def main() -> None:
    run_self_checks()
    print("自检通过：normalize_records 与 PrepToolError 行为符合预期。")

    mark("r10-w3-ex3")
    input("请手动完成第3周自测后按回车继续...")
    mark("r10-w3-self")


if __name__ == "__main__":
    main()
