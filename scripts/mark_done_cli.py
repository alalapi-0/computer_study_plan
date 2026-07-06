#!/usr/bin/env python3
"""CLI for marking tasks done — used by mark_done.sh."""

from __future__ import annotations

import collections
import sys

from progress_lib import list_status, mark_task, repo_root, task_metadata_map

DEFAULT_STATUS_LIMIT = 8


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


def print_usage() -> None:
    print("用法：")
    print("  bash mark_done.sh                         # 简洁查看：每条主线前 8 个未完成任务")
    print("  bash mark_done.sh --lane soft_exam        # 只看某条主线")
    print("  bash mark_done.sh --limit 20              # 调整每条主线显示数量")
    print("  bash mark_done.sh --all                   # 查看全部任务")
    print("  bash mark_done.sh <task-id>               # 记录完成")
    print("  bash mark_done.sh <task-id> --undo        # 取消完成")


def parse_status_args(args: list[str]) -> tuple[bool, str | None, int] | None:
    show_all = False
    lane_filter: str | None = None
    limit = DEFAULT_STATUS_LIMIT
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--all":
            show_all = True
        elif arg == "--lane":
            if i + 1 >= len(args):
                print("❌ --lane 需要提供 lane code，例如 soft_exam")
                return None
            lane_filter = args[i + 1]
            i += 1
        elif arg.startswith("--lane="):
            lane_filter = arg.split("=", 1)[1]
        elif arg == "--limit":
            if i + 1 >= len(args):
                print("❌ --limit 需要提供数字")
                return None
            try:
                limit = max(1, int(args[i + 1]))
            except ValueError:
                print("❌ --limit 必须是数字")
                return None
            i += 1
        elif arg.startswith("--limit="):
            try:
                limit = max(1, int(arg.split("=", 1)[1]))
            except ValueError:
                print("❌ --limit 必须是数字")
                return None
        elif arg in {"-h", "--help"}:
            print_usage()
            return None
        else:
            print(f"❌ 未知参数：{arg}")
            print_usage()
            return None
        i += 1
    return show_all, lane_filter, limit


def print_status(show_all: bool = False, lane_filter: str | None = None, limit: int = DEFAULT_STATUS_LIMIT) -> int:
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
    if lane_filter and lane_filter not in ordered:
        print(f"❌ 未知 lane：{lane_filter}")
        print("   已知 lane：" + ", ".join(ordered))
        return 1
    if not show_all:
        print(f"默认只显示每条主线前 {limit} 个未完成任务；查看全部用：bash mark_done.sh --all\n")
    for lane_key in ordered:
        if lane_filter and lane_key != lane_filter:
            continue
        items = by_lane.get(lane_key, [])
        if not items:
            continue
        title = lanes.get(lane_key, {}).get("title", lane_key)
        done = [x for x in items if x[1].get("done")]
        open_items = [x for x in items if not x[1].get("done")]
        visible = items if show_all else open_items[:limit]
        mode = "全部任务" if show_all else f"未完成前 {min(limit, len(open_items))} 项"
        print(f"─── {title}（{lane_key}）  {len(done)}/{len(items)} · {mode} ───")
        if not visible:
            print("  ✅ 当前没有未完成任务")
        for tid, info in visible:
            label = task_label(tid, meta_by_task)
            if info.get("done"):
                print(f"  ✅ {label}  ({info.get('done_at')})")
            else:
                print(f"  ⬜ {label}")
        if not show_all and len(open_items) > limit:
            print(f"  … 其余 {len(open_items) - limit} 个未完成任务：bash mark_done.sh --lane {lane_key} --all")
        print()
    return 0


def main(argv: list[str]) -> int:
    if len(argv) <= 1:
        print_usage()
        print()
        return print_status()

    if argv[1].startswith("-"):
        parsed = parse_status_args(argv[1:])
        if parsed is None:
            return 0 if argv[1] in {"-h", "--help"} else 1
        show_all, lane_filter, limit = parsed
        return print_status(show_all=show_all, lane_filter=lane_filter, limit=limit)

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
            print(f"   ... 其余 {len(known) - 20} 个任务可运行 bash mark_done.sh --all 查看")
        return 1

    meta = task_metadata_map(repo_root()).get(task_id) or {}
    label = task_label(task_id, {task_id: meta})
    if undo:
        print(f"↩️  已取消完成：{label}")
    elif result["result"] == "noop_already_done":
        print(f"✅ 已是完成状态（{result['done_at']}），无需重复标记")
    else:
        print(f"✅ 已记录完成：{label}  ({result['done_at']})")

    print(f"📊 总进度：{result['done_count']}/{result['total']}")
    print(f"📝 已记录事件：{result['action_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
