#!/usr/bin/env python3
"""CLI for marking tasks done — used by mark_done.sh."""

from __future__ import annotations

import collections
import sys

from progress_lib import list_status, mark_task, repo_root


def print_status() -> int:
    data = list_status()
    lanes = data["lanes"]
    tasks = data["tasks"]
    by_lane: dict[str, list[tuple[str, dict]]] = collections.defaultdict(list)
    for tid, info in tasks.items():
        by_lane[info.get("lane", "engineering")].append((tid, info))

    print(f"📊 总进度：{data['done_count']}/{data['total']}\n")
    ordered = list(lanes.keys()) + [k for k in by_lane if k not in lanes]
    for lane_key in ordered:
        items = by_lane.get(lane_key, [])
        if not items:
            continue
        title = lanes.get(lane_key, {}).get("title", lane_key)
        done = [x for x in items if x[1].get("done")]
        print(f"─── {title}（{lane_key}）  {len(done)}/{len(items)} ───")
        for tid, info in items:
            if info.get("done"):
                print(f"  ✅ {tid}  ({info.get('done_at')})")
            else:
                print(f"  ⬜ {tid}")
        print()
    return 0


def main(argv: list[str]) -> int:
    if len(argv) <= 1:
        print("用法：bash mark_done.sh <task-id> [--undo]")
        print()
        return print_status()

    task_id = argv[1]
    undo = len(argv) > 2 and argv[2] == "--undo"
    try:
        result = mark_task(task_id, undo=undo, root=repo_root())
    except KeyError:
        data = list_status()
        print(f"❌ 未知任务 ID：{task_id}")
        print("   已知 ID：" + ", ".join(data["tasks"].keys()))
        return 1

    if undo:
        print(f"↩️  已取消完成：{task_id}")
    elif result["result"] == "noop_already_done":
        print(f"✅ 已是完成状态（{result['done_at']}），无需重复标记")
    else:
        print(f"✅ 已标记完成：{task_id}  ({result['done_at']})")

    print(f"📊 总进度：{result['done_count']}/{result['total']}")
    print(f"📝 已记录事件：{result['action_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
