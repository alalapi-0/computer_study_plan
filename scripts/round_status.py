#!/usr/bin/env python3
"""Scan round overview docs, scaffold dirs, progress.json, and UI metadata.

Single source for agents/users: run `python3 scripts/round_status.py --json`
or `python3 scripts/round_status.py --markdown` instead of hardcoding round lists.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parent.parent
ROUND_MD_RE = re.compile(r"^round_(\d{2})\.md$")
TASK_ROUND_RE = re.compile(r"^r(\d+)-")
OVERVIEW_LANE_RE = re.compile(r"\*\*所属主线\*\*\s*\|\s*([^|]+)")


@dataclass
class RoundStatus:
    round_id: str
    number: int
    title: str
    overview_md: bool
    scaffold_dir: bool
    scaffold_complete: bool
    mark_done_in_exercises: bool
    progress_task_count: int
    progress_linked: bool
    ui_linked: bool
    lanes: list[str]
    difficulty: str | None
    notes: list[str]


def task_id_to_round_id(task_id: str) -> str | None:
    if task_id.startswith(("w1-", "w2-", "w3-", "fin-")):
        return "round_00"
    match = TASK_ROUND_RE.match(task_id)
    if match:
        return f"round_{int(match.group(1)):02d}"
    return None


def extract_md_title(md_path: Path) -> str:
    first = md_path.read_text(encoding="utf-8").splitlines()[0].strip()
    if first.startswith("# "):
        return first[2:].strip()
    return md_path.stem


def extract_md_lanes(md_path: Path) -> list[str]:
    text = md_path.read_text(encoding="utf-8")
    match = OVERVIEW_LANE_RE.search(text)
    if not match:
        return ["engineering"]
    raw = match.group(1).strip()
    parts = re.split(r"\s*\+\s*", raw)
    lanes: list[str] = []
    for part in parts:
        key = part.strip().split()[0]
        if key in {"engineering", "soft_exam", "math2", "cs408"}:
            lanes.append(key)
    return lanes or ["engineering"]


def extract_md_difficulty(md_path: Path) -> str | None:
    text = md_path.read_text(encoding="utf-8")
    match = re.search(r"\*\*难度\*\*\s*\|\s*([^|]+)", text)
    return match.group(1).strip() if match else None


def scaffold_complete(round_dir: Path) -> bool:
    if not round_dir.is_dir():
        return False
    for week in ("week1", "week2", "week3"):
        w = round_dir / week
        if not (w / "notes.md").is_file():
            return False
        if not any((w / name).is_file() for name in ("exercises.sh", "exercises.py")):
            return False
    final = round_dir / "final"
    if not final.is_dir():
        return False
    if not any(final.glob("comprehensive_exercise.*")):
        return False
    cheatsheets = list(final.glob("*cheatsheet*.md")) + list(final.glob("*_cheatsheet.md"))
    if not cheatsheets:
        return False
    return True


def exercises_use_mark_done(round_dir: Path) -> bool:
    if not round_dir.is_dir():
        return False
    for path in round_dir.rglob("exercises.*"):
        if path.suffix not in {".sh", ".py"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "mark_done.sh" in text:
            return True
    final = list(round_dir.glob("final/comprehensive_exercise.*"))
    for path in final:
        text = path.read_text(encoding="utf-8", errors="replace")
        if "mark_done.sh" in text:
            return True
    return False


def load_progress_tasks(repo: Path) -> dict[str, dict[str, Any]]:
    path = repo / "progress.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("tasks", {})


def load_ui_round_ids(repo: Path) -> set[str]:
    path = repo / "progress_rounds.json"
    if not path.is_file():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    rounds = data.get("rounds", [])
    return {r["id"] for r in rounds if isinstance(r, dict) and r.get("id")}


def scan_rounds(repo: Path = REPO) -> list[RoundStatus]:
    tasks = load_progress_tasks(repo)
    tasks_by_round: dict[str, int] = {}
    for tid in tasks:
        rid = task_id_to_round_id(tid)
        if rid:
            tasks_by_round[rid] = tasks_by_round.get(rid, 0) + 1

    ui_ids = load_ui_round_ids(repo)
    statuses: list[RoundStatus] = []

    for n in range(22):
        rid = f"round_{n:02d}"
        md_path = repo / f"round_{n:02d}.md"
        round_dir = repo / "rounds" / rid
        notes: list[str] = []

        overview = md_path.is_file()
        scaffold = round_dir.is_dir()
        scaffold_ok = scaffold_complete(round_dir) if scaffold else False
        mark_done = exercises_use_mark_done(round_dir) if scaffold else False
        task_count = tasks_by_round.get(rid, 0)
        progress_linked = task_count > 0
        ui_linked = rid in ui_ids

        if scaffold and not progress_linked:
            notes.append("实操骨架已存在，进度任务未接入 progress.json")
        if progress_linked and not mark_done:
            notes.append("progress.json 有任务，练习脚本尚未调用 mark_done.sh")
        if progress_linked and not ui_linked:
            notes.append("进度已接入，但 progress_rounds.json 未注册 UI 元数据")
        if ui_linked and not progress_linked:
            notes.append("看板有元数据，但 progress.json 无对应任务")

        title = extract_md_title(md_path) if overview else rid
        lanes = extract_md_lanes(md_path) if overview else ["engineering"]
        difficulty = extract_md_difficulty(md_path) if overview else None

        statuses.append(
            RoundStatus(
                round_id=rid,
                number=n,
                title=title,
                overview_md=overview,
                scaffold_dir=scaffold,
                scaffold_complete=scaffold_ok,
                mark_done_in_exercises=mark_done,
                progress_task_count=task_count,
                progress_linked=progress_linked,
                ui_linked=ui_linked,
                lanes=lanes,
                difficulty=difficulty,
                notes=notes,
            )
        )
    return statuses


def tier_label(st: RoundStatus) -> str:
    if st.progress_linked and st.mark_done_in_exercises and st.ui_linked:
        return "进度闭环"
    if st.progress_linked:
        return "进度已接入"
    if st.scaffold_complete:
        return "最小骨架"
    if st.scaffold_dir:
        return "目录不完整"
    if st.overview_md:
        return "仅概览文档"
    return "缺失"


def to_markdown_table(statuses: list[RoundStatus]) -> str:
    lines = [
        "| 轮次 | 主题 | 层级 | 概览 md | 实操目录 | 进度任务数 | 看板 UI | 备注 |",
        "|------|------|------|---------|----------|------------|---------|------|",
    ]
    for st in statuses:
        note = "; ".join(st.notes) if st.notes else "—"
        lines.append(
            f"| {st.round_id} | {st.title.split('·', 1)[-1].strip() if '·' in st.title else st.title} "
            f"| {tier_label(st)} | {'✅' if st.overview_md else '❌'} "
            f"| {'✅' if st.scaffold_complete else ('⚠️' if st.scaffold_dir else '❌')} "
            f"| {st.progress_task_count} | {'✅' if st.ui_linked else '❌'} | {note} |"
        )
    return "\n".join(lines)


def summary(statuses: list[RoundStatus]) -> dict[str, Any]:
    return {
        "overview_md_count": sum(1 for s in statuses if s.overview_md),
        "scaffold_complete_count": sum(1 for s in statuses if s.scaffold_complete),
        "progress_linked_rounds": [s.round_id for s in statuses if s.progress_linked],
        "ui_linked_rounds": [s.round_id for s in statuses if s.ui_linked],
        "full_loop_rounds": [
            s.round_id
            for s in statuses
            if s.progress_linked and s.mark_done_in_exercises and s.ui_linked
        ],
        "scaffold_only_rounds": [
            s.round_id
            for s in statuses
            if s.scaffold_complete and not s.progress_linked
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan round status across the repository.")
    parser.add_argument("--json", action="store_true", help="Print JSON")
    parser.add_argument("--markdown", action="store_true", help="Print markdown table")
    parser.add_argument("--summary", action="store_true", help="Print summary only")
    args = parser.parse_args()

    statuses = scan_rounds()
    if args.json:
        payload = {"summary": summary(statuses), "rounds": [asdict(s) for s in statuses]}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    elif args.markdown:
        print(to_markdown_table(statuses))
    elif args.summary:
        print(json.dumps(summary(statuses), ensure_ascii=False, indent=2))
    else:
        print(to_markdown_table(statuses))
        print()
        print(json.dumps(summary(statuses), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
