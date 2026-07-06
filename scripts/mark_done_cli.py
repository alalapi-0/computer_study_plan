#!/usr/bin/env python3
"""CLI for marking tasks done — used by mark_done.sh."""

from __future__ import annotations

import collections
import sys

from progress_lib import list_status, mark_task, repo_root, task_metadata_map


def task_label(task_id: str, meta_by_task: dict[str, dict]) -> str:
    meta = meta_by_task.get(task_id) or {}
    task = meta.get("task") or {}
    week = meta.get("week") or {}
    title = task.get("title")
    if not title:
        return task_id
    week_title = week.get("title")
    suffix = f" / {week_title}" if week_title else ""
    return f"{task_id} — {title}{suffix}"


def print_status() -> int:
    root = repo_root()
    data = list_status()
    lanes = data["lanes"]
    tasks = data["tasks"]
    meta_by_task = task_metadata_map(root)
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
            label = task_label(tid, meta_by_task)
            if info.get("done"):
                print(f"  ✅ {label}  ({info.get('done_at')})")
            else:
                print(f"  ⬜ {label}")
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
        meta_by_task = task_metadata_map(repo_root())
        print(f"❌ 未知任务 ID：{task_id}")
        known = list(data["tasks"].keys())
        preview = [task_label(tid, meta_by_task) for tid in known[:20]]
        print("   前 20 个已知任务：")
        for item in preview:
            print(f"   - {item}")
        if len(known) > 20:
            print(f"   ... 其余 {len(known) - 20} 个任务可运行 bash mark_done.sh 查看")
        return 1

    meta = task_metadata_map(repo_root()).get(task_id) or {}
    label = task_label(task_id, {task_id: meta})
    if undo:
        print(f"↩️  已取消完成：{label}")
    elif result["result"] == "noop_already_done":
        print(f"✅ 已是完成状态（{result['done_at']}），无需重复标记")
    else:
        print(f"✅ 已标记完成：{label}  ({result['done_at']})")

    print(f"📊 总进度：{result['done_count']}/{result['total']}")
    print(f"📝 已记录事件：{result['action_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
