#!/usr/bin/env python3
"""Round 07 · Week 3 exercises: minimal integration."""

from collections import Counter


def dedup_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            output.append(item)
    return output


def main() -> None:
    records = ["ok", "blur", "ok", "bad", "bad"]
    deduped = dedup_keep_order(records)
    stats = Counter(deduped)

    print("原始条数:", len(records))
    print("去重后条数:", len(deduped))
    print("统计:", dict(stats))


if __name__ == "__main__":
    main()
