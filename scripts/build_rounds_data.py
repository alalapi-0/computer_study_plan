#!/usr/bin/env python3
"""Build rounds_data.js and merge linux-foundations tasks into progress.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from progress_lib import (
    ACTIVE_COURSE_ID,
    load_progress,
    repo_root,
    save_progress,
    sync_progress_data_js,
)

LINUX_LANE = ACTIVE_COURSE_ID

DIFFICULTY_BY_ROUND = {
    0: "⭐☆☆☆☆",
    1: "⭐☆☆☆☆",
    2: "⭐⭐☆☆☆",
    6: "⭐⭐⭐☆☆",
}


def round_title(root: Path, num: int) -> str:
    md = root / f"round_{num:02d}.md"
    if md.exists():
        first = md.read_text(encoding="utf-8").splitlines()[0].strip()
        if first.startswith("# "):
            return first[2:].strip()
    return f"Round {num:02d}"


def exercise_ext(round_dir: Path, week: int) -> str:
    for name in (f"week{week}/exercises.sh", f"week{week}/exercises.py"):
        if (round_dir / name).exists():
            return name.split(".")[-1]
    return "sh"


def final_cheatsheet(round_dir: Path) -> str:
    final_dir = round_dir / "final"
    if not final_dir.exists():
        return ""
    for path in sorted(final_dir.glob("*.md")):
        if path.name != "README.md":
            return str(path.relative_to(repo_root())).replace("\\", "/")
    return ""


def final_comprehensive(round_dir: Path) -> str:
    final_dir = round_dir / "final"
    for name in ("comprehensive_exercise.sh", "comprehensive_exercise.py"):
        path = final_dir / name
        if path.exists():
            return str(path.relative_to(repo_root())).replace("\\", "/")
    return ""



def build_round_00(root: Path) -> dict:
    return {
        "id": "round_00",
        "title": round_title(root, 0),
        "lane": LINUX_LANE,
        "difficulty": "⭐☆☆☆☆",
        "duration": "3 周",
        "weeks": [
            {
                "id": "week1",
                "title": "第 1 周：建立感觉（pwd / ls / cd）",
                "tasks": [
                    {"id": "w1-read", "type": "reading", "title": "阅读 week1/notes.md", "file": "rounds/round_00/week1/notes.md"},
                    {"id": "w1-ex1", "type": "exercise", "title": "练习1：认识当前位置", "file": "rounds/round_00/week1/exercises.sh"},
                    {"id": "w1-ex2", "type": "exercise", "title": "练习2：创建子目录并切换", "file": "rounds/round_00/week1/exercises.sh"},
                    {"id": "w1-ex3", "type": "exercise", "title": "练习3：绝对路径 vs 相对路径", "file": "rounds/round_00/week1/exercises.sh"},
                    {"id": "w1-self", "type": "test", "title": "第1周自测", "file": "rounds/round_00/week1/exercises.sh"},
                ],
            },
            {
                "id": "week2",
                "title": "第 2 周：创建东西（mkdir / touch / cat）",
                "tasks": [
                    {"id": "w2-read", "type": "reading", "title": "阅读 week2/notes.md", "file": "rounds/round_00/week2/notes.md"},
                    {"id": "w2-ex4", "type": "exercise", "title": "练习4：创建更多子目录", "file": "rounds/round_00/week2/exercises.sh"},
                    {"id": "w2-ex5", "type": "exercise", "title": "练习5：创建空文件", "file": "rounds/round_00/week2/exercises.sh"},
                    {"id": "w2-ex6", "type": "exercise", "title": "练习6：用 cat 查看空文件", "file": "rounds/round_00/week2/exercises.sh"},
                    {"id": "w2-ex7", "type": "exercise", "title": "练习7：echo + cat", "file": "rounds/round_00/week2/exercises.sh"},
                    {"id": "w2-self", "type": "test", "title": "第2周自测", "file": "rounds/round_00/week2/exercises.sh"},
                ],
            },
            {
                "id": "week3",
                "title": "第 3 周：学会自查（man）",
                "tasks": [
                    {"id": "w3-read", "type": "reading", "title": "阅读 week3/notes.md", "file": "rounds/round_00/week3/notes.md"},
                    {"id": "w3-ex8", "type": "exercise", "title": "练习8：man ls", "file": "rounds/round_00/week3/exercises.sh"},
                    {"id": "w3-ex9", "type": "exercise", "title": "练习9：man pwd/mkdir/touch/cat", "file": "rounds/round_00/week3/exercises.sh"},
                    {"id": "w3-ex10", "type": "exercise", "title": "练习10：man man", "file": "rounds/round_00/week3/exercises.sh"},
                    {"id": "w3-self", "type": "test", "title": "第3周自测", "file": "rounds/round_00/week3/exercises.sh"},
                ],
            },
            {
                "id": "final",
                "title": "最终验收",
                "tasks": [
                    {"id": "fin-comp", "type": "exercise", "title": "综合练习", "file": "rounds/round_00/final/comprehensive_exercise.sh"},
                    {"id": "fin-sheet", "type": "output", "title": "完成命令小抄", "file": "rounds/round_00/final/command_cheatsheet.md"},
                    {"id": "fin-acc1", "type": "test", "title": "验收：Terminal 与 Shell 的区别", "file": "round_00.md"},
                    {"id": "fin-acc2", "type": "test", "title": "验收：能用 7 个命令", "file": "round_00.md"},
                    {"id": "fin-acc3", "type": "output", "title": "验收：cli-lab 目录与小抄存在", "file": "round_00.md"},
                ],
            },
        ],
    }



def build_linux_round(root: Path, num: int) -> dict | None:
    round_dir = root / f"rounds/round_{num:02d}"
    if not round_dir.exists():
        return None

    prefix = f"r{num:02d}"
    ext1 = exercise_ext(round_dir, 1)
    ext2 = exercise_ext(round_dir, 2)
    ext3 = exercise_ext(round_dir, 3)
    ex1 = f"rounds/round_{num:02d}/week1/exercises.{ext1}"
    ex2 = f"rounds/round_{num:02d}/week2/exercises.{ext2}"
    ex3 = f"rounds/round_{num:02d}/week3/exercises.{ext3}"
    sheet = final_cheatsheet(round_dir)
    comp = final_comprehensive(round_dir)

    if num == 1:
        w1_theme, w2_theme, w3_theme = "路径感", "文件操作", "查看文本与帮助"
    elif num == 2:
        w1_theme, w2_theme, w3_theme = "重定向与管道", "最小 shell 脚本", "Git 最小工作流"
    else:
        w1_theme, w2_theme, w3_theme = "基础练习", "进阶练习", "综合练习"

    final_tasks = []
    if comp:
        final_tasks.append({"id": f"{prefix}-fin-comp", "type": "exercise", "title": "综合练习", "file": comp})
    if sheet:
        final_tasks.append({"id": f"{prefix}-fin-sheet", "type": "output", "title": "完成本 Round 小抄", "file": sheet})
    final_tasks.append(
        {
            "id": f"{prefix}-fin-acc1",
            "type": "test",
            "title": f"验收：Round {num:02d} 核心目标",
            "file": f"round_{num:02d}.md",
        }
    )
    if num == 2:
        final_tasks.append(
            {
                "id": f"{prefix}-fin-acc2",
                "type": "output",
                "title": "验收：完成 3 次 Git 提交并解释",
                "file": "round_02.md",
            }
        )
        for task in final_tasks:
            if task["id"] == "r02-fin-comp":
                task["title"] = "综合练习：日志统计器 + 本地 Git 仓库"
            elif task["id"] == "r02-fin-sheet":
                task["title"] = "产出：完成 Round 02 命令小抄"
            elif task["id"] == "r02-fin-acc1":
                task["title"] = "验收：解释重定向、管道、脚本参数"
            elif task["id"] == "r02-fin-acc2":
                task["title"] = "验收：解释 3 次本地 Git 提交"

    if num == 1:
        final_tasks = []
        if comp:
            final_tasks.append(
                {
                    "id": "r01-fin-comp",
                    "type": "exercise",
                    "title": "综合练习：迷你文件整理实验室",
                    "file": comp,
                }
            )
        if sheet:
            final_tasks.append(
                {
                    "id": "r01-fin-sheet",
                    "type": "output",
                    "title": "产出：完成 Round 01 命令小抄",
                    "file": sheet,
                }
            )
        final_tasks.append(
            {
                "id": "r01-fin-acc1",
                "type": "test",
                "title": "验收：解释路径与 13 个基础命令",
                "file": "round_01.md",
            }
        )
        return {
            "id": "round_01",
            "title": round_title(root, num),
            "lane": LINUX_LANE,
            "difficulty": DIFFICULTY_BY_ROUND.get(num, "⭐☆☆☆☆"),
            "duration": "3 周",
            "weeks": [
                {
                    "id": "round01-week1",
                    "title": "第 1 周：路径感",
                    "tasks": [
                        {"id": "r01-w1-read", "type": "reading", "title": "阅读：路径、绝对路径、相对路径", "file": "rounds/round_01/week1/notes.md"},
                        {"id": "r01-w1-ex1", "type": "exercise", "title": "练习：路径切换实验", "file": ex1},
                        {"id": "r01-w1-self", "type": "test", "title": "自测：不用提示切换目录", "file": ex1},
                    ],
                },
                {
                    "id": "round01-week2",
                    "title": "第 2 周：文件操作",
                    "tasks": [
                        {"id": "r01-w2-read", "type": "reading", "title": "阅读：创建、复制、移动、删除", "file": "rounds/round_01/week2/notes.md"},
                        {"id": "r01-w2-ex2", "type": "exercise", "title": "练习：创建 / 复制 / 改名 / 删除", "file": ex2},
                        {"id": "r01-w2-self", "type": "test", "title": "自测：独立整理 week2_test", "file": ex2},
                    ],
                },
                {
                    "id": "round01-week3",
                    "title": "第 3 周：查看文本与帮助",
                    "tasks": [
                        {"id": "r01-w3-read", "type": "reading", "title": "阅读：cat / less / head / tail / man", "file": "rounds/round_01/week3/notes.md"},
                        {"id": "r01-w3-ex3", "type": "exercise", "title": "练习：查看文本与查帮助", "file": ex3},
                        {"id": "r01-w3-self", "type": "test", "title": "自测：head / tail / man", "file": ex3},
                    ],
                },
                {"id": "round01-final", "title": "最终验收", "tasks": final_tasks},
            ],
        }

    if num == 2:
        return {
            "id": "round_02",
            "title": round_title(root, num),
            "lane": LINUX_LANE,
            "difficulty": DIFFICULTY_BY_ROUND.get(num, "⭐⭐☆☆☆"),
            "duration": "3 周",
            "weeks": [
                {
                    "id": "round02-week1",
                    "title": "第 1 周：重定向与管道",
                    "tasks": [
                        {"id": "r02-w1-read", "type": "reading", "title": "阅读：重定向、追加、管道", "file": "rounds/round_02/week1/notes.md"},
                        {"id": "r02-w1-ex1", "type": "exercise", "title": "练习：覆盖与追加", "file": ex1},
                        {"id": "r02-w1-ex2", "type": "exercise", "title": "练习：去重统计", "file": ex1},
                        {"id": "r02-w1-ex3", "type": "exercise", "title": "练习：日志过滤流水线", "file": ex1},
                        {"id": "r02-w1-self", "type": "test", "title": "自测：独立写日志统计链", "file": ex1},
                    ],
                },
                {
                    "id": "round02-week2",
                    "title": "第 2 周：最小 shell 脚本",
                    "tasks": [
                        {"id": "r02-w2-read", "type": "reading", "title": "阅读：最小 Shell 脚本与参数", "file": "rounds/round_02/week2/notes.md"},
                        {"id": "r02-w2-ex4", "type": "exercise", "title": "练习：count_errors.sh", "file": ex2},
                        {"id": "r02-w2-ex5", "type": "exercise", "title": "练习：count_labels.sh", "file": ex2},
                        {"id": "r02-w2-ex6", "type": "exercise", "title": "练习：show_args.sh 参数观察", "file": ex2},
                        {"id": "r02-w2-self", "type": "test", "title": "自测：运行并解释参数脚本", "file": ex2},
                    ],
                },
                {
                    "id": "round02-week3",
                    "title": "第 3 周：Git 最小工作流",
                    "tasks": [
                        {"id": "r02-w3-read", "type": "reading", "title": "阅读：Git 工作区、暂存区、提交历史", "file": "rounds/round_02/week3/notes.md"},
                        {"id": "r02-w3-ex7", "type": "exercise", "title": "练习：初始化与首次提交", "file": ex3},
                        {"id": "r02-w3-ex8", "type": "exercise", "title": "练习：修改 README 后第二次提交", "file": ex3},
                        {"id": "r02-w3-ex9", "type": "exercise", "title": "练习：新增 notes.txt 再提交", "file": ex3},
                        {"id": "r02-w3-self", "type": "test", "title": "自测：解释 status 与 log", "file": ex3},
                    ],
                },
                {"id": "round02-final", "title": "最终验收", "tasks": final_tasks},
            ],
        }

    if num == 6:
        final_tasks = []
        if comp:
            final_tasks.append(
                {
                    "id": "r06-fin-comp",
                    "type": "exercise",
                    "title": "综合练习：批量日志处理流水线",
                    "file": comp,
                }
            )
        if sheet:
            final_tasks.append(
                {
                    "id": "r06-fin-sheet",
                    "type": "output",
                    "title": "产出：完成 Round 06 Linux 自动化小抄",
                    "file": sheet,
                }
            )
        final_tasks.append(
            {
                "id": "r06-fin-acc1",
                "type": "test",
                "title": "验收：解释批处理、进程查看和远程排练边界",
                "file": "round_06.md",
            }
        )
        return {
            "id": "round_06",
            "title": round_title(root, num),
            "lane": LINUX_LANE,
            "difficulty": DIFFICULTY_BY_ROUND.get(num, "⭐⭐⭐☆☆"),
            "duration": "3 周",
            "weeks": [
                {
                    "id": "round06-week1",
                    "title": "第 1 周：find / xargs / sed / awk",
                    "tasks": [
                        {
                            "id": "r06-w1-read",
                            "type": "reading",
                            "title": "阅读：find、xargs、sed、awk 批处理",
                            "file": "rounds/round_06/week1/notes.md",
                        },
                        {"id": "r06-w1-ex1", "type": "exercise", "title": "练习：find/xargs/sed/awk 日志清洗", "file": ex1},
                        {"id": "r06-w1-self", "type": "test", "title": "自测：自己写 find_text_report.sh", "file": ex1},
                    ],
                },
                {
                    "id": "round06-week2",
                    "title": "第 2 周：进程查看与长任务",
                    "tasks": [
                        {
                            "id": "r06-w2-read",
                            "type": "reading",
                            "title": "阅读：ps、后台任务、nohup、tmux",
                            "file": "rounds/round_06/week2/notes.md",
                        },
                        {"id": "r06-w2-ex2", "type": "exercise", "title": "练习：进程查看与长任务日志", "file": ex2},
                        {"id": "r06-w2-self", "type": "test", "title": "自测：自己写 worker_monitor.sh", "file": ex2},
                    ],
                },
                {
                    "id": "round06-week3",
                    "title": "第 3 周：SSH / rsync / crontab 排练",
                    "tasks": [
                        {
                            "id": "r06-w3-read",
                            "type": "reading",
                            "title": "阅读：SSH、rsync、crontab 安全边界",
                            "file": "rounds/round_06/week3/notes.md",
                        },
                        {"id": "r06-w3-ex3", "type": "exercise", "title": "练习：远程同步与 cron 命令排练", "file": ex3},
                        {"id": "r06-w3-self", "type": "test", "title": "自测：自己写 remote_ops_plan.md", "file": ex3},
                    ],
                },
                {"id": "round06-final", "title": "最终验收", "tasks": final_tasks},
            ],
        }


    return None


LANE_PLAN_TASKS = [
    ("linux-course-start", "linux", LINUX_LANE, "阅读 Linux 课程总览", "content/courses/linux-foundations/README.md"),
    ("linux-plan-start", "linux", LINUX_LANE, "阅读 Linux 课程学习路径", "plans/linux/README.md"),
    ("vps-stage-start", "vps", LINUX_LANE, "阅读 VPS 支线总纲", "rounds/stage_03_vps_remote_ops/README.md"),
    ("vps-00-repo-scan", "vps", LINUX_LANE, "阅读 VPS-00：扫描仓库与生成治理报告", "rounds/stage_03_vps_remote_ops/round_vps_00_repo_scan.md"),
    ("vps-01-repo-cleanup", "vps", LINUX_LANE, "阅读 VPS-01：执行仓库治理与文档合并", "rounds/stage_03_vps_remote_ops/round_vps_01_repo_cleanup.md"),
    ("vps-02-module-anchor", "vps", LINUX_LANE, "阅读 VPS-02：建立 VPS 模块总纲", "rounds/stage_03_vps_remote_ops/round_vps_02_module_anchor.md"),
    ("vps-03-permission-levels", "vps", LINUX_LANE, "阅读 VPS-03：远程操作权限等级与安全规则", "rounds/stage_03_vps_remote_ops/round_vps_03_permission_levels.md"),
    ("vps-04-ssh-basics", "vps", LINUX_LANE, "阅读 VPS-04：SSH 与远程 Linux 基础", "rounds/stage_03_vps_remote_ops/round_vps_04_ssh_basics.md"),
    ("vps-05-first-readonly-check", "vps", LINUX_LANE, "阅读 VPS-05：首次远程只读检查", "rounds/stage_03_vps_remote_ops/round_vps_05_first_readonly_check.md"),
    ("vps-06-remote-dirs", "vps", LINUX_LANE, "阅读 VPS-06：远程学习目录与测试文件", "rounds/stage_03_vps_remote_ops/round_vps_06_remote_dirs.md"),
    ("vps-07-github-sync", "vps", LINUX_LANE, "阅读 VPS-07：GitHub 同步与远程运行", "rounds/stage_03_vps_remote_ops/round_vps_07_github_sync.md"),
    ("vps-08-tmux-training", "vps", LINUX_LANE, "阅读 VPS-08：tmux 后台任务训练", "rounds/stage_03_vps_remote_ops/round_vps_08_tmux_training.md"),
    ("vps-09-network-check", "vps", LINUX_LANE, "阅读 VPS-09：网络连通性与端口检查", "rounds/stage_03_vps_remote_ops/round_vps_09_network_check.md"),
    ("vps-10-remote-api-minimal", "vps", LINUX_LANE, "阅读 VPS-10：远程 API 调用最小实验", "rounds/stage_03_vps_remote_ops/round_vps_10_remote_api_minimal.md"),
    ("vps-11-minimal-service", "vps", LINUX_LANE, "阅读 VPS-11：最小 Web/API 服务部署", "rounds/stage_03_vps_remote_ops/round_vps_11_minimal_service.md"),
    ("vps-12-sop-and-vultragent", "vps", LINUX_LANE, "阅读 VPS-12：SOP 与 VULTRagent 需求草案", "rounds/stage_03_vps_remote_ops/round_vps_12_sop_and_vultragent.md"),
]

LANE_PLAN_ROUNDS = [
    ("linux", "Linux · 课程路径", LINUX_LANE),
    ("vps", "VPS · 远程实操支线", LINUX_LANE),
]


def build_plan_rounds(root: Path) -> list[dict]:
    rounds = []
    for plan_key, title, lane in LANE_PLAN_ROUNDS:
        tasks = []
        for tid, tplan_key, _tlane, ttitle, file in LANE_PLAN_TASKS:
            if tplan_key != plan_key:
                continue
            if not (root / file).exists():
                continue
            tasks.append({"id": tid, "type": "reading", "title": ttitle, "file": file})
        if not tasks:
            continue
        rounds.append(
            {
                "id": f"plan_{plan_key}",
                "title": title,
                "lane": lane,
                "difficulty": "⭐☆☆☆☆",
                "duration": "持续",
                "weeks": [
                    {
                        "id": f"plan_{plan_key}_week",
                        "title": "课程文档阅读",
                        "tasks": tasks,
                    }
                ],
            }
        )
    return rounds


def collect_task_ids(rounds: list[dict]) -> set[str]:
    ids: set[str] = set()
    for rnd in rounds:
        for week in rnd.get("weeks", []):
            for task in week.get("tasks", []):
                ids.add(task["id"])
    for tid, *_rest in LANE_PLAN_TASKS:
        ids.add(tid)
    return ids


def merge_and_prune_tasks(data: dict, rounds: list[dict]) -> tuple[int, int]:
    tasks = data.setdefault("tasks", {})
    keep_ids = collect_task_ids(rounds)
    added = 0
    for rnd in rounds:
        for week in rnd.get("weeks", []):
            for task in week.get("tasks", []):
                tid = task["id"]
                if tid not in tasks:
                    tasks[tid] = {"done": False, "done_at": None, "lane": LINUX_LANE}
                    added += 1
                else:
                    info = tasks[tid]
                    info["lane"] = LINUX_LANE
                    info.setdefault("done", False)
                    info.setdefault("done_at", None)
    removed = 0
    for tid in list(tasks.keys()):
        if tid not in keep_ids:
            del tasks[tid]
            removed += 1
    data["lanes"] = {
        LINUX_LANE: {
            "title": "Linux 基础与工程实践",
            "description": "当前唯一正式课程 linux-foundations：终端、文件系统、Shell、自动化与远程实操",
            "course_id": LINUX_LANE,
        }
    }
    data["active_course_id"] = LINUX_LANE
    return added, removed


def write_rounds_js(root: Path, rounds: list[dict]) -> None:
    body = json.dumps(rounds, ensure_ascii=False, indent=2)
    content = (
        "// Auto-generated by scripts/build_rounds_data.py\n"
        f"window.ROUNDS_DATA = {body};\n"
    )
    (root / "rounds_data.js").write_text(content, encoding="utf-8")


def main() -> int:
    root = repo_root()
    rounds = [build_round_00(root)]
    for num in (1, 2, 6):
        item = build_linux_round(root, num)
        if item:
            rounds.append(item)
    rounds.extend(build_plan_rounds(root))

    write_rounds_js(root, rounds)
    data = load_progress(root)
    added, removed = merge_and_prune_tasks(data, rounds)
    save_progress(data, root)
    sync_progress_data_js(data, root)
    print(f"Built rounds_data.js ({len(rounds)} rounds)")
    print(f"Merged {added} new tasks; pruned {removed} obsolete tasks (total {len(data['tasks'])})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
