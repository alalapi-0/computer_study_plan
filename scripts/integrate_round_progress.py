#!/usr/bin/env python3
"""Integrate Round 05–21 into progress.json, progress.html, and exercise scripts."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROGRESS_JSON = REPO / "progress.json"
PROGRESS_HTML = REPO / "progress.html"
PROGRESS_JS = REPO / "progress_data.js"

FIRST_ROUND = 5
LAST_ROUND = 21

DIFFICULTY = {
    5: "⭐⭐⭐☆☆",
    6: "⭐⭐⭐☆☆",
    7: "⭐⭐⭐☆☆",
    8: "⭐⭐⭐☆☆",
    9: "⭐⭐⭐☆☆",
    10: "⭐⭐⭐⭐☆",
    11: "⭐⭐⭐⭐☆",
    12: "⭐⭐⭐⭐☆",
    13: "⭐⭐⭐⭐☆",
    14: "⭐⭐⭐⭐☆",
    15: "⭐⭐⭐⭐☆",
    16: "⭐⭐⭐⭐☆",
    17: "⭐⭐⭐⭐☆",
    18: "⭐⭐⭐⭐⭐",
    19: "⭐⭐⭐⭐⭐",
    20: "⭐⭐⭐⭐⭐",
    21: "⭐⭐⭐⭐⭐",
}

WEEK_TASKS = [
    ("week1", "w1-read", "reading", "阅读 week1/notes.md", "week1"),
    ("week1", "w1-ex1", "exercise", "练习1", "week1"),
    ("week1", "w1-self", "test", "第1周自测", "week1"),
    ("week2", "w2-read", "reading", "阅读 week2/notes.md", "week2"),
    ("week2", "w2-ex2", "exercise", "练习2", "week2"),
    ("week2", "w2-self", "test", "第2周自测", "week2"),
    ("week3", "w3-read", "reading", "阅读 week3/notes.md", "week3"),
    ("week3", "w3-ex3", "exercise", "练习3", "week3"),
    ("week3", "w3-self", "test", "第3周自测", "week3"),
]

FINAL_TASKS = [
    ("final", "fin-comp", "exercise", "综合练习", "final"),
    ("final", "fin-sheet", "output", "完成 Round 小抄", "final"),
    ("final", "fin-acc1", "test", "验收", "final"),
]


def round_prefix(num: int) -> str:
    return f"r{num:02d}"


def task_id(num: int, suffix: str) -> str:
    return f"{round_prefix(num)}-{suffix}"


def read_round_title(num: int) -> str:
    readme = REPO / f"rounds/round_{num:02d}/README.md"
    line = readme.read_text(encoding="utf-8").splitlines()[0]
    m = re.match(r"# Round \d+ · (.+)", line)
    return m.group(1).strip() if m else f"Round {num:02d}"


def read_week_title(num: int, week: int) -> str:
    notes = REPO / f"rounds/round_{num:02d}/week{week}/notes.md"
    line = notes.read_text(encoding="utf-8").splitlines()[0]
    m = re.search(r"笔记[（(](.+?)[）)]", line)
    if m:
        return f"第 {week} 周：{m.group(1)}"
    return f"第 {week} 周"


def exercise_ext(num: int) -> str:
    return "sh" if num <= 6 else "py"


def comprehensive_name(num: int) -> str:
    ext = exercise_ext(num)
    return f"comprehensive_exercise.{ext}"


def find_cheatsheet(num: int) -> str:
    final_dir = REPO / f"rounds/round_{num:02d}/final"
    for path in sorted(final_dir.glob("*cheatsheet*.md")):
        return path.name
    for path in sorted(final_dir.glob("*.md")):
        return path.name
    return "cheatsheet.md"


def add_progress_tasks(data: dict) -> int:
    tasks = data.setdefault("tasks", {})
    added = 0
    for num in range(FIRST_ROUND, LAST_ROUND + 1):
        for _, suffix, _, _, _ in WEEK_TASKS + FINAL_TASKS:
            tid = task_id(num, suffix)
            if tid in tasks:
                continue
            tasks[tid] = {"done": False, "done_at": None, "lane": "engineering"}
            added += 1
    return added


def js_str(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def build_round_js(num: int) -> str:
    prefix = round_prefix(num)
    title = read_round_title(num)
    ext = exercise_ext(num)
    comp = comprehensive_name(num)
    cheatsheet = find_cheatsheet(num)
    diff = DIFFICULTY.get(num, "⭐⭐⭐☆☆")

    weeks_js: list[str] = []
    week_groups: dict[str, list[tuple]] = {}
    for week_key, suffix, typ, label, path_week in WEEK_TASKS:
        week_groups.setdefault(week_key, []).append((suffix, typ, label, path_week))

    for week_key in ("week1", "week2", "week3"):
        wnum = week_key[-1]
        wtitle = read_week_title(num, int(wnum))
        task_lines = []
        for suffix, typ, label, path_week in week_groups[week_key]:
            tid = task_id(num, suffix)
            ex_file = f"rounds/round_{num:02d}/{path_week}/exercises.{ext}"
            notes_file = f"rounds/round_{num:02d}/{path_week}/notes.md"
            if typ == "reading":
                cmd = f"bash mark_done.sh {tid}"
                file_ref = notes_file
            else:
                cmd = "自动"
                file_ref = ex_file
            task_lines.append(
                f'        {{ id:{js_str(tid)}, type:{js_str(typ)}, title:{js_str(label)}, '
                f'cmd:{js_str(cmd)}, file:{js_str(file_ref)} }}'
            )
        weeks_js.append(
            f'      {{ id: {js_str(f"round{num:02d}-{week_key}")}, title: {js_str(wtitle)}, tasks: [\n'
            + ",\n".join(task_lines)
            + "\n      ]}"
        )

    final_tasks = []
    for _, suffix, typ, label, _ in FINAL_TASKS:
        tid = task_id(num, suffix)
        if suffix == "fin-comp":
            file_ref = f"rounds/round_{num:02d}/final/{comp}"
        elif suffix == "fin-sheet":
            file_ref = f"rounds/round_{num:02d}/final/{cheatsheet}"
        else:
            file_ref = f"round_{num:02d}.md"
        cmd = f"bash mark_done.sh {tid}" if typ == "reading" else "自动"
        final_tasks.append(
            f'        {{ id:{js_str(tid)}, type:{js_str(typ)}, title:{js_str(label)}, '
            f'cmd:{js_str(cmd)}, file:{js_str(file_ref)} }}'
        )

    weeks_js.append(
        f'      {{ id: {js_str(f"round{num:02d}-final")}, title: "最终验收", tasks: [\n'
        + ",\n".join(final_tasks)
        + "\n      ]}"
    )

    return (
        f"  {{\n"
        f'    id: "round_{num:02d}",\n'
        f'    title: "Round {num:02d} · {title}",\n'
        f'    lane: "engineering",\n'
        f'    difficulty: "{diff}",\n'
        f'    duration: "3 周",\n'
        f"    weeks: [\n"
        + ",\n".join(weeks_js)
        + "\n    ]\n"
        f"  }}"
    )


def patch_progress_html() -> None:
    html = PROGRESS_HTML.read_text(encoding="utf-8")
    marker = "  // 后续 Round 在落地为实操目录时按本结构追加"
    if marker not in html:
        raise SystemExit("progress.html marker not found")

    rounds_js = ",\n".join(build_round_js(n) for n in range(FIRST_ROUND, LAST_ROUND + 1))
    replacement = (
        f",\n{rounds_js}\n"
        f"  // Round 00–21 均已注册进度任务（Round 05–21 由 scripts/integrate_round_progress.py 接入）。"
    )
    html = html.replace(
        "  }\n  // 后续 Round 在落地为实操目录时按本结构追加；当前已展开 Round 00、Round 01、Round 02、Round 03、Round 04。\n];",
        "  }" + replacement + "\n];",
    )
    PROGRESS_HTML.write_text(html, encoding="utf-8")


def shell_header() -> str:
    return (
        'REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"\n\n'
        "mark() {\n"
        '  bash "$REPO_ROOT/mark_done.sh" "$1"\n'
        "}\n"
    )


def patch_shell_week(num: int, week: int) -> None:
    path = REPO / f"rounds/round_{num:02d}/week{week}/exercises.sh"
    text = path.read_text(encoding="utf-8")
    tid_ex = task_id(num, f"w{week}-ex{week if week > 1 else 1}")
    tid_self = task_id(num, f"w{week}-self")
    if f"mark {tid_ex}" in text:
        return
    if "REPO_ROOT=" not in text:
        text = text.replace("set -e\n\n", "set -e\n\n" + shell_header() + "\n", 1)
    text = text.rstrip() + (
        f"\n\nmark {tid_ex}\n\n"
        f'echo "请手动完成第{week}周自测后按回车继续..."\n'
        "read\n"
        f"mark {tid_self}\n"
    )
    path.write_text(text, encoding="utf-8")


def patch_shell_final(num: int) -> None:
    path = REPO / f"rounds/round_{num:02d}/final/comprehensive_exercise.sh"
    text = path.read_text(encoding="utf-8")
    if f"mark {task_id(num, 'fin-comp')}" in text:
        return
    if "REPO_ROOT=" not in text:
        text = text.replace("set -e\n\n", "set -e\n\n" + shell_header() + "\n", 1)
    cheatsheet = find_cheatsheet(num)
    text = text.rstrip() + (
        f"\n\nmark {task_id(num, 'fin-comp')}\n\n"
        f'echo "请检查 rounds/round_{num:02d}/final/{cheatsheet} 后按回车..."\n'
        "read\n"
        f"mark {task_id(num, 'fin-sheet')}\n\n"
        f'echo "请确认你能解释 Round {num:02d} 核心概念后按回车..."\n'
        "read\n"
        f"mark {task_id(num, 'fin-acc1')}\n\n"
        'echo "Final 完成。"\n'
    )
    path.write_text(text, encoding="utf-8")


PYTHON_MARK_BLOCK = '''
def _repo_root() -> "Path":
    return Path(__file__).resolve().parents[3]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(_repo_root() / "mark_done.sh"), task_id], check=False)
'''


def ensure_python_imports(text: str) -> str:
    if "import subprocess" not in text:
        text = text.replace("from pathlib import Path\n", "import subprocess\nfrom pathlib import Path\n", 1)
    if "def mark(task_id" not in text:
        anchor = "from pathlib import Path\n\n\n"
        if anchor in text:
            text = text.replace(anchor, "from pathlib import Path\n" + PYTHON_MARK_BLOCK + "\n\n", 1)
        else:
            text = "import subprocess\nfrom pathlib import Path\n" + PYTHON_MARK_BLOCK + "\n\n" + text
    return text


def patch_python_week(num: int, week: int) -> None:
    path = REPO / f"rounds/round_{num:02d}/week{week}/exercises.py"
    text = path.read_text(encoding="utf-8")
    tid_ex = task_id(num, f"w{week}-ex{week if week > 1 else 1}")
    tid_self = task_id(num, f"w{week}-self")
    if f'mark("{tid_ex}")' in text:
        return
    text = ensure_python_imports(text)
    insert = (
        f'\n    mark("{tid_ex}")\n'
        f'    input("请手动完成第{week}周自测后按回车继续...")\n'
        f'    mark("{tid_self}")\n'
    )
    text = text.replace("\n\nif __name__ == \"__main__\":\n    main()\n", insert + '\n\nif __name__ == "__main__":\n    main()\n')
    path.write_text(text, encoding="utf-8")


def patch_python_final(num: int) -> None:
    path = REPO / f"rounds/round_{num:02d}/final/comprehensive_exercise.py"
    text = path.read_text(encoding="utf-8")
    if f'mark("{task_id(num, "fin-comp")}")' in text:
        return
    text = ensure_python_imports(text)
    cheatsheet = find_cheatsheet(num)
    insert = (
        f'\n    mark("{task_id(num, "fin-comp")}")\n'
        f'    input("请检查 rounds/round_{num:02d}/final/{cheatsheet} 后按回车...")\n'
        f'    mark("{task_id(num, "fin-sheet")}")\n'
        f'    input("请确认你能解释 Round {num:02d} 核心概念后按回车...")\n'
        f'    mark("{task_id(num, "fin-acc1")}")\n'
    )
    text = text.replace("\n\nif __name__ == \"__main__\":\n    main()\n", insert + '\n\nif __name__ == "__main__":\n    main()\n')
    path.write_text(text, encoding="utf-8")


def patch_exercises() -> None:
    for num in range(FIRST_ROUND, LAST_ROUND + 1):
        if num <= 6:
            for week in (1, 2, 3):
                patch_shell_week(num, week)
            patch_shell_final(num)
        else:
            for week in (1, 2, 3):
                patch_python_week(num, week)
            patch_python_final(num)


def sync_progress_data_js(data: dict) -> None:
    js_payload = {
        "version": data.get("version", 2),
        "lanes": data.get("lanes", {}),
        "tasks": data.get("tasks", {}),
    }
    js_body = json.dumps(js_payload, ensure_ascii=False, indent=2)
    PROGRESS_JS.write_text(
        "// Auto-generated by integrate_round_progress.py — DO NOT edit manually\n"
        "// Source of truth: progress.json\n"
        f"window.PROGRESS_DATA = {js_body};\n",
        encoding="utf-8",
    )


def patch_mark_done_round_resolver() -> None:
    path = REPO / "mark_done.sh"
    text = path.read_text(encoding="utf-8")
    old = '''def resolve_round_id(tid: str) -> str:
    if tid.startswith("r02-"):
        return "round_02"
    if tid.startswith(("w1-", "w2-", "w3-", "fin-")):
        return "round_00"
    return "unknown"'''
    new = '''def resolve_round_id(tid: str) -> str:
    import re
    m = re.match(r"^r(\\d{2})-", tid)
    if m:
        return f"round_{m.group(1)}"
    if tid.startswith(("w1-", "w2-", "w3-", "fin-")):
        return "round_00"
    return "unknown"'''
    if old in text:
        path.write_text(text.replace(old, new), encoding="utf-8")


def main() -> None:
    data = json.loads(PROGRESS_JSON.read_text(encoding="utf-8"))
    added = add_progress_tasks(data)
    PROGRESS_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    patch_progress_html()
    patch_exercises()
    patch_mark_done_round_resolver()
    sync_progress_data_js(data)
    print(f"Added {added} tasks to progress.json")
    print(f"Total tasks: {len(data['tasks'])}")


if __name__ == "__main__":
    main()
