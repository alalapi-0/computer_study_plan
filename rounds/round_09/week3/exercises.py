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


if __name__ == "__main__":
    main()
