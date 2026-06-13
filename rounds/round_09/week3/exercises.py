import subprocess
from pathlib import Path

def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)


#!/usr/bin/env python3
"""Round 09 · Week 3 exercises: pure function and checks."""


def dedup_records(records: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in records:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def run_self_checks() -> None:
    assert dedup_records(["a", "b", "a"]) == ["a", "b"]
    assert dedup_records([]) == []
    assert dedup_records(["x", "x", "x"]) == ["x"]


def main() -> None:
    run_self_checks()
    print("自检通过：dedup_records 满足最小测试样例。")

    mark("r09-w3-ex3")
    input("请手动完成第3周自测后按回车继续...")
    mark("r09-w3-self")


if __name__ == "__main__":
    main()
