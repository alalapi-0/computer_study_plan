#!/usr/bin/env python3
"""Build rounds_data.js and merge engineering round tasks into progress.json."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from progress_lib import load_progress, repo_root, save_progress, sync_progress_data_js

DIFFICULTY_BY_ROUND = {
    0: "⭐☆☆☆☆",
    1: "⭐☆☆☆☆",
    2: "⭐⭐☆☆☆",
    3: "⭐⭐☆☆☆",
    4: "⭐⭐⭐☆☆",
    5: "⭐⭐⭐☆☆",
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
        "lane": "engineering",
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


def build_standard_round(root: Path, num: int) -> dict | None:
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

    week_titles = {
        1: {1: "路径感", 2: "重定向与管道", 3: "Python 基础语法", 4: "列表与顺序存储"},
    }
    w1_theme = week_titles.get(num, {}).get(1, "基础练习")
    w2_theme = week_titles.get(num, {}).get(2, "进阶练习")
    w3_theme = week_titles.get(num, {}).get(3, "综合练习")

    if num == 1:
        w1_theme, w2_theme, w3_theme = "路径感", "文件操作", "查看文本与帮助"
    elif num == 2:
        w1_theme, w2_theme, w3_theme = "重定向与管道", "最小 shell 脚本", "Git 最小工作流"
    elif num == 3:
        w1_theme, w2_theme, w3_theme = "Python 基础语法", "list/dict 与函数拆分", "复杂度观察"
    elif num == 4:
        w1_theme, w2_theme, w3_theme = "列表与顺序存储", "栈与队列", "哈希与去重"
    elif num == 5:
        w1_theme, w2_theme, w3_theme = "双指针 / 滑动窗口 / 二分", "分治 / DFS / BFS / 回溯", "贪心 / DP 入门"

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
            "lane": "engineering",
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
            "lane": "engineering",
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

    if num == 3:
        final_tasks = []
        if comp:
            final_tasks.append(
                {
                    "id": "r03-fin-comp",
                    "type": "exercise",
                    "title": "综合练习：标签统计器 + 复杂度估算",
                    "file": comp,
                }
            )
        if sheet:
            final_tasks.append(
                {
                    "id": "r03-fin-sheet",
                    "type": "output",
                    "title": "产出：完成 Round 03 Python 与复杂度小抄",
                    "file": sheet,
                }
            )
        final_tasks.append(
            {
                "id": "r03-fin-acc1",
                "type": "test",
                "title": "验收：解释函数、dict 计数与复杂度",
                "file": "round_03.md",
            }
        )
        return {
            "id": "round_03",
            "title": round_title(root, num),
            "lane": "engineering",
            "difficulty": DIFFICULTY_BY_ROUND.get(num, "⭐⭐☆☆☆"),
            "duration": "3 周",
            "weeks": [
                {
                    "id": "round03-week1",
                    "title": "第 1 周：Python 基础语法",
                    "tasks": [
                        {
                            "id": "r03-w1-read",
                            "type": "reading",
                            "title": "阅读：Python 脚本、变量、条件、循环、函数",
                            "file": "rounds/round_03/week1/notes.md",
                        },
                        {"id": "r03-w1-ex1", "type": "exercise", "title": "练习：运行第一个 Python 小程序", "file": ex1},
                        {"id": "r03-w1-self", "type": "test", "title": "自测：自己写 square.py", "file": ex1},
                    ],
                },
                {
                    "id": "round03-week2",
                    "title": "第 2 周：list/dict 与函数拆分",
                    "tasks": [
                        {
                            "id": "r03-w2-read",
                            "type": "reading",
                            "title": "阅读：list/dict 与函数拆分",
                            "file": "rounds/round_03/week2/notes.md",
                        },
                        {"id": "r03-w2-ex2", "type": "exercise", "title": "练习：统计标签出现次数", "file": ex2},
                        {"id": "r03-w2-self", "type": "test", "title": "自测：自己写 count_words.py", "file": ex2},
                    ],
                },
                {
                    "id": "round03-week3",
                    "title": "第 3 周：复杂度观察",
                    "tasks": [
                        {
                            "id": "r03-w3-read",
                            "type": "reading",
                            "title": "阅读：复杂度直觉",
                            "file": "rounds/round_03/week3/notes.md",
                        },
                        {"id": "r03-w3-ex3", "type": "exercise", "title": "练习：观察线性与平方级增长", "file": ex3},
                        {"id": "r03-w3-self", "type": "test", "title": "自测：解释 O(n) 与 O(n^2)", "file": ex3},
                    ],
                },
                {"id": "round03-final", "title": "最终验收", "tasks": final_tasks},
            ],
        }

    if num == 4:
        final_tasks = []
        if comp:
            final_tasks.append(
                {
                    "id": "r04-fin-comp",
                    "type": "exercise",
                    "title": "综合练习：数据结构工具箱",
                    "file": comp,
                }
            )
        if sheet:
            final_tasks.append(
                {
                    "id": "r04-fin-sheet",
                    "type": "output",
                    "title": "产出：完成 Round 04 数据结构小抄",
                    "file": sheet,
                }
            )
        final_tasks.append(
            {
                "id": "r04-fin-acc1",
                "type": "test",
                "title": "验收：解释 list、dict、set、deque 适用场景",
                "file": "round_04.md",
            }
        )
        return {
            "id": "round_04",
            "title": round_title(root, num),
            "lane": "engineering",
            "difficulty": DIFFICULTY_BY_ROUND.get(num, "⭐⭐⭐☆☆"),
            "duration": "3 周",
            "weeks": [
                {
                    "id": "round04-week1",
                    "title": "第 1 周：列表与顺序存储",
                    "tasks": [
                        {
                            "id": "r04-w1-read",
                            "type": "reading",
                            "title": "阅读：list 顺序存储与遍历",
                            "file": "rounds/round_04/week1/notes.md",
                        },
                        {"id": "r04-w1-ex1", "type": "exercise", "title": "练习：list 遍历、过滤与统计", "file": ex1},
                        {"id": "r04-w1-self", "type": "test", "title": "自测：自己写 scores.py", "file": ex1},
                    ],
                },
                {
                    "id": "round04-week2",
                    "title": "第 2 周：栈与队列",
                    "tasks": [
                        {
                            "id": "r04-w2-read",
                            "type": "reading",
                            "title": "阅读：stack 后进先出与 queue 先进先出",
                            "file": "rounds/round_04/week2/notes.md",
                        },
                        {"id": "r04-w2-ex2", "type": "exercise", "title": "练习：stack 与 queue 出入顺序", "file": ex2},
                        {"id": "r04-w2-self", "type": "test", "title": "自测：自己写 browser_history.py", "file": ex2},
                    ],
                },
                {
                    "id": "round04-week3",
                    "title": "第 3 周：哈希与去重",
                    "tasks": [
                        {
                            "id": "r04-w3-read",
                            "type": "reading",
                            "title": "阅读：dict 计数与 set 去重",
                            "file": "rounds/round_04/week3/notes.md",
                        },
                        {"id": "r04-w3-ex3", "type": "exercise", "title": "练习：dict 计数与 set 去重", "file": ex3},
                        {"id": "r04-w3-self", "type": "test", "title": "自测：自己写 tag_report.py", "file": ex3},
                    ],
                },
                {"id": "round04-final", "title": "最终验收", "tasks": final_tasks},
            ],
        }

    if num == 5:
        final_tasks = []
        if comp:
            final_tasks.append(
                {
                    "id": "r05-fin-comp",
                    "type": "exercise",
                    "title": "综合练习：算法模式选择器",
                    "file": comp,
                }
            )
        if sheet:
            final_tasks.append(
                {
                    "id": "r05-fin-sheet",
                    "type": "output",
                    "title": "产出：完成 Round 05 算法模式小抄",
                    "file": sheet,
                }
            )
        final_tasks.append(
            {
                "id": "r05-fin-acc1",
                "type": "test",
                "title": "验收：解释七类算法模式适用场景",
                "file": "round_05.md",
            }
        )
        return {
            "id": "round_05",
            "title": round_title(root, num),
            "lane": "engineering",
            "difficulty": DIFFICULTY_BY_ROUND.get(num, "⭐⭐⭐☆☆"),
            "duration": "3 周",
            "weeks": [
                {
                    "id": "round05-week1",
                    "title": "第 1 周：双指针 / 滑动窗口 / 二分",
                    "tasks": [
                        {
                            "id": "r05-w1-read",
                            "type": "reading",
                            "title": "阅读：双指针、滑动窗口、二分触发条件",
                            "file": "rounds/round_05/week1/notes.md",
                        },
                        {"id": "r05-w1-ex1", "type": "exercise", "title": "练习：二分查找与滑动窗口", "file": ex1},
                        {"id": "r05-w1-self", "type": "test", "title": "自测：自己写 two_sum_sorted.py", "file": ex1},
                    ],
                },
                {
                    "id": "round05-week2",
                    "title": "第 2 周：分治 / DFS / BFS / 回溯",
                    "tasks": [
                        {
                            "id": "r05-w2-read",
                            "type": "reading",
                            "title": "阅读：分治、DFS、BFS、回溯",
                            "file": "rounds/round_05/week2/notes.md",
                        },
                        {"id": "r05-w2-ex2", "type": "exercise", "title": "练习：DFS、BFS 与回溯最小例子", "file": ex2},
                        {"id": "r05-w2-self", "type": "test", "title": "自测：自己写 bfs_levels.py", "file": ex2},
                    ],
                },
                {
                    "id": "round05-week3",
                    "title": "第 3 周：贪心 / DP 入门",
                    "tasks": [
                        {
                            "id": "r05-w3-read",
                            "type": "reading",
                            "title": "阅读：贪心选择与 DP 状态转移",
                            "file": "rounds/round_05/week3/notes.md",
                        },
                        {"id": "r05-w3-ex3", "type": "exercise", "title": "练习：贪心选择与 DP 爬楼梯", "file": ex3},
                        {"id": "r05-w3-self", "type": "test", "title": "自测：自己写 coin_change_dp.py", "file": ex3},
                    ],
                },
                {"id": "round05-final", "title": "最终验收", "tasks": final_tasks},
            ],
        }

    return {
        "id": f"round_{num:02d}",
        "title": round_title(root, num),
        "lane": "engineering",
        "difficulty": DIFFICULTY_BY_ROUND.get(num, "⭐⭐⭐☆☆" if num >= 7 else "⭐⭐☆☆☆"),
        "duration": "3 周",
        "weeks": [
            {
                "id": f"round{num:02d}-week1",
                "title": f"第 1 周：{w1_theme}",
                "tasks": [
                    {"id": f"{prefix}-w1-read", "type": "reading", "title": "阅读 week1/notes.md", "file": f"rounds/round_{num:02d}/week1/notes.md"},
                    {"id": f"{prefix}-w1-ex1", "type": "exercise", "title": "练习1", "file": ex1},
                    {"id": f"{prefix}-w1-self", "type": "test", "title": "第1周自测", "file": ex1},
                ],
            },
            {
                "id": f"round{num:02d}-week2",
                "title": f"第 2 周：{w2_theme}",
                "tasks": [
                    {"id": f"{prefix}-w2-read", "type": "reading", "title": "阅读 week2/notes.md", "file": f"rounds/round_{num:02d}/week2/notes.md"},
                    {"id": f"{prefix}-w2-ex2", "type": "exercise", "title": "练习2", "file": ex2},
                    {"id": f"{prefix}-w2-self", "type": "test", "title": "第2周自测", "file": ex2},
                ],
            },
            {
                "id": f"round{num:02d}-week3",
                "title": f"第 3 周：{w3_theme}",
                "tasks": [
                    {"id": f"{prefix}-w3-read", "type": "reading", "title": "阅读 week3/notes.md", "file": f"rounds/round_{num:02d}/week3/notes.md"},
                    {"id": f"{prefix}-w3-ex3", "type": "exercise", "title": "练习3", "file": ex3},
                    {"id": f"{prefix}-w3-self", "type": "test", "title": "第3周自测", "file": ex3},
                ],
            },
            {"id": f"round{num:02d}-final", "title": "最终验收", "tasks": final_tasks},
        ],
    }


LANE_PLAN_TASKS = [
    ("soft_exam-ds-start", "soft_exam", "阅读软考数据结构骨架", "plans/soft_exam/ds.md"),
    ("soft_exam-os-start", "soft_exam", "阅读软考操作系统骨架", "plans/soft_exam/os.md"),
    ("soft_exam-db-start", "soft_exam", "阅读软考数据库骨架", "plans/soft_exam/db.md"),
    ("math2-limits-start", "math2", "阅读数学二极限启动骨架", "plans/math2/limits.md"),
    ("math2-la-start", "math2", "阅读数学二线性代数启动骨架", "plans/math2/la_matrix.md"),
    ("cs408-ds-start", "cs408", "阅读 408 数据结构计划入口", "plans/408/README.md"),
]

LANE_PLAN_ROUNDS = [
    ("soft_exam", "软考 · 启动模块", "soft_exam"),
    ("math2", "数学二 · 启动模块", "math2"),
    ("cs408", "408 · 启动模块", "cs408"),
]


def build_plan_rounds(root: Path) -> list[dict]:
    rounds = []
    for lane, title, _ in LANE_PLAN_ROUNDS:
        tasks = [
            {"id": tid, "type": "reading", "title": ttitle, "file": file}
            for tid, tlane, ttitle, file in LANE_PLAN_TASKS
            if tlane == lane and (root / file).exists()
        ]
        if not tasks:
            continue
        rounds.append(
            {
                "id": f"plan_{lane}",
                "title": title,
                "lane": lane,
                "difficulty": "⭐☆☆☆☆",
                "duration": "持续",
                "weeks": [
                    {
                        "id": f"plan_{lane}_week",
                        "title": "计划文档阅读",
                        "tasks": tasks,
                    }
                ],
            }
        )
    return rounds


def merge_tasks(data: dict, rounds: list[dict]) -> int:
    tasks = data.setdefault("tasks", {})
    added = 0
    for rnd in rounds:
        for week in rnd.get("weeks", []):
            for task in week.get("tasks", []):
                tid = task["id"]
                if tid in tasks:
                    continue
                tasks[tid] = {"done": False, "done_at": None, "lane": rnd.get("lane", "engineering")}
                added += 1
    for tid, lane, _title, _file in LANE_PLAN_TASKS:
        if tid in tasks:
            continue
        tasks[tid] = {"done": False, "done_at": None, "lane": lane}
        added += 1
    return added


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
    for num in range(1, 22):
        item = build_standard_round(root, num)
        if item:
            rounds.append(item)
    rounds.extend(build_plan_rounds(root))

    write_rounds_js(root, rounds)
    data = load_progress(root)
    added = merge_tasks(data, rounds)
    save_progress(data, root)
    sync_progress_data_js(data, root)
    print(f"Built rounds_data.js ({len(rounds)} rounds)")
    print(f"Merged {added} new tasks into progress.json (total {len(data['tasks'])})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
