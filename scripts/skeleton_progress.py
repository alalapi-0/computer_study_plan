#!/usr/bin/env python3
"""Build minimal progress tasks + progress_rounds weeks for scaffold rounds."""

from __future__ import annotations

import re
from pathlib import Path

from round_status import extract_md_lanes, extract_md_title, extract_md_difficulty

REPO = Path(__file__).resolve().parent.parent


def notes_week_title(notes_path: Path) -> str:
    if not notes_path.is_file():
        return ""
    for line in notes_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def exercise_extension(round_dir: Path) -> str:
    if (round_dir / "week1" / "exercises.py").is_file():
        return "py"
    return "sh"


def build_round_package(repo: Path, round_num: int) -> tuple[dict[str, dict], list[dict], dict]:
    round_id = f"round_{round_num:02d}"
    round_dir = repo / "rounds" / round_id
    md_path = repo / f"round_{round_num:02d}.md"
    prefix = f"r{round_num:02d}"
    ext = exercise_extension(round_dir)
    ex_file = f"exercises.{ext}"

    lanes = extract_md_lanes(md_path) if md_path.is_file() else ["engineering"]
    lane = lanes[0]

    final_dir = round_dir / "final"
    comp_candidates = list(final_dir.glob("comprehensive_exercise.*"))
    comp_file = (
        f"rounds/{round_id}/final/{comp_candidates[0].name}"
        if comp_candidates
        else f"rounds/{round_id}/final/comprehensive_exercise.{ext}"
    )
    cheat_candidates = list(final_dir.glob("*cheatsheet*.md"))
    sheet_file = (
        f"rounds/{round_id}/final/{cheat_candidates[0].name}"
        if cheat_candidates
        else f"rounds/{round_id}/final/cheatsheet.md"
    )

    tasks: dict[str, dict] = {}
    weeks: list[dict] = []

    for w in (1, 2, 3):
        wk = f"week{w}"
        notes_rel = f"rounds/{round_id}/{wk}/notes.md"
        ex_rel = f"rounds/{round_id}/{wk}/{ex_file}"
        ex_suffix = w if w > 1 else 1
        week_title = notes_week_title(round_dir / wk / "notes.md") or f"第 {w} 周"

        week_tasks = [
            {
                "id": f"{prefix}-w{w}-read",
                "type": "reading",
                "title": f"阅读 {wk}/notes.md",
                "cmd": f"bash mark_done.sh {prefix}-w{w}-read",
                "file": notes_rel,
            },
            {
                "id": f"{prefix}-w{w}-ex{ex_suffix}",
                "type": "exercise",
                "title": f"练习：执行 {wk} 脚本",
                "cmd": "自动",
                "file": ex_rel,
            },
            {
                "id": f"{prefix}-w{w}-self",
                "type": "test",
                "title": f"第{w}周自测",
                "cmd": "自动",
                "file": ex_rel,
            },
        ]
        for t in week_tasks:
            tasks[t["id"]] = {"done": False, "done_at": None, "lane": lane}
        weeks.append(
            {
                "id": f"round{round_num:02d}-week{w}",
                "title": week_title,
                "tasks": week_tasks,
            }
        )

    final_tasks = [
        {
            "id": f"{prefix}-fin-comp",
            "type": "exercise",
            "title": "综合练习",
            "cmd": "自动",
            "file": comp_file,
        },
        {
            "id": f"{prefix}-fin-sheet",
            "type": "output",
            "title": "完成本轮小抄",
            "cmd": "自动",
            "file": sheet_file,
        },
        {
            "id": f"{prefix}-fin-acc1",
            "type": "test",
            "title": f"验收：对照 round_{round_num:02d}.md",
            "cmd": "自动",
            "file": f"round_{round_num:02d}.md",
        },
    ]
    for t in final_tasks:
        tasks[t["id"]] = {"done": False, "done_at": None, "lane": lane}
    weeks.append(
        {
            "id": f"round{round_num:02d}-final",
            "title": "最终验收",
            "tasks": final_tasks,
        }
    )

    title = extract_md_title(md_path) if md_path.is_file() else round_id
    difficulty = extract_md_difficulty(md_path) if md_path.is_file() else "—"

    ui_meta = {
        "id": round_id,
        "title": title,
        "lane": lane,
        "lanes": lanes,
        "difficulty": difficulty or "—",
        "duration": "3 周",
        "weeks": weeks,
        "progress_linked": True,
        "scaffold_only": False,
        "readme": f"rounds/{round_id}/README.md",
    }
    return tasks, weeks, ui_meta


def register_rounds(
    repo: Path,
    start: int = 5,
    end: int = 21,
    only_missing: bool = True,
) -> dict[str, int]:
    from progress_store import load_progress, save_progress

    data = load_progress(repo)
    added = 0
    for n in range(start, end + 1):
        round_dir = repo / "rounds" / f"round_{n:02d}"
        if not round_dir.is_dir():
            continue
        new_tasks, _, _ = build_round_package(repo, n)
        for tid, info in new_tasks.items():
            if only_missing and tid in data["tasks"]:
                continue
            if tid not in data["tasks"]:
                data["tasks"][tid] = info
                added += 1
    if added:
        save_progress(data, repo)
    return {"tasks_added": added, "total_tasks": len(data["tasks"])}
