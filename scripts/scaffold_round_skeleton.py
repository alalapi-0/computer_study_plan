#!/usr/bin/env python3
"""Generate minimal round_NN skeleton (week1-3 + final). Internal automation helper."""

from __future__ import annotations

import argparse
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

ROUNDS: dict[int, tuple[str, str, str, str, str, str]] = {
    13: (
        "环境复现与发布",
        "env_repro",
        "虚拟环境与依赖锁定",
        "`.env.example` 与配置分层",
        "发布前自检清单",
        "env_repro_cheatsheet.md",
    ),
    14: (
        "HTTP 与 API 设计",
        "http_api",
        "HTTP 动词与状态码",
        "请求/响应 JSON 约定",
        "最小 REST 路由草图",
        "http_api_cheatsheet.md",
    ),
    15: (
        "FastAPI 基础",
        "fastapi_basics",
        "FastAPI 应用入口",
        "路径参数与查询参数",
        "Pydantic 模型骨架",
        "fastapi_basics_cheatsheet.md",
    ),
    16: (
        "API 与数据层结合",
        "api_data_layer",
        "路由调用 db 模块",
        "列表/详情接口草图",
        "错误响应约定",
        "api_data_layer_cheatsheet.md",
    ),
    17: (
        "服务化收口",
        "service_wrapup",
        "启动脚本与健康检查",
        "日志与配置收口",
        "部署前检查表",
        "service_wrapup_cheatsheet.md",
    ),
    18: (
        "数值计算与数据分析",
        "numerics_analytics",
        "numpy 数组入门",
        "pandas 读取 CSV",
        "简单聚合统计",
        "numerics_analytics_cheatsheet.md",
    ),
    19: (
        "机器学习最小闭环",
        "ml_minimal_loop",
        "训练/验证划分",
        "基线模型拟合",
        "指标记录骨架",
        "ml_minimal_loop_cheatsheet.md",
    ),
    20: (
        "PyTorch 入门",
        "pytorch_intro",
        "Tensor 与 Dataset",
        "最小训练循环",
        "checkpoint 路径约定",
        "pytorch_intro_cheatsheet.md",
    ),
    21: (
        "NLP 前置基础",
        "nlp_prereq",
        "分词与词表",
        "文本张量批处理",
        "推理脚本入口骨架",
        "nlp_prereq_cheatsheet.md",
    ),
}


def write_round(num: int) -> None:
    title, slug, w1, w2, w3, cheatsheet = ROUNDS[num]
    root = REPO / f"rounds/round_{num:02d}"
    if root.exists():
        print(f"skip round_{num:02d}: already exists")
        return
    root.mkdir(parents=True)

    readme = f"""# Round {num:02d} · {title}

这个目录是 Round {num:02d}（{title}）的最小实操骨架。

> **仓库根**：`~/PycharmProjects/computer_study_plan`  
> **练习沙盒**：`~/cli-lab/round{num:02d}`  
> 路径说明见 [`docs/WORKSPACE.md`](../../docs/WORKSPACE.md)。

## 目录结构

```
round_{num:02d}/
├─ README.md
├─ week1/ … week3/
└─ final/
```

## 使用方式

1. 每周先阅读 `weekN/notes.md`，再执行 `python3 weekN/exercises.py`。
2. 全部练习在 `~/cli-lab/round{num:02d}` 沙盒执行。
3. 本轮先落最小骨架，后续按需要接入进度任务。
"""
    (root / "README.md").write_text(readme, encoding="utf-8")

    week_topics = [w1, w2, w3]
    for wn, topic in enumerate(week_topics, start=1):
        wdir = root / f"week{wn}"
        wdir.mkdir(parents=True)
        (wdir / "notes.md").write_text(
            f"# Round {num:02d} · Week {wn} 笔记（{topic}）\n\n"
            f"## 本周目标\n\n- 在沙盒完成「{topic}」最小练习。\n\n"
            f"## 本周自查\n\n- [ ] 能用自己的话说明本周产出路径\n",
            encoding="utf-8",
        )
        (wdir / "exercises.py").write_text(
            f'''#!/usr/bin/env python3
"""Round {num:02d} · Week {wn} exercises: {topic}."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round{num:02d}" / "week{wn}"
    base.mkdir(parents=True, exist_ok=True)
    marker = base / "{slug}_week{wn}.txt"
    marker.write_text("{topic}\\n", encoding="utf-8")
    print("已写入:", marker)


if __name__ == "__main__":
    main()
''',
            encoding="utf-8",
        )

    fdir = root / "final"
    fdir.mkdir(parents=True)
    (fdir / "comprehensive_exercise.py").write_text(
        f'''#!/usr/bin/env python3
"""Round {num:02d} · Final checklist."""

from pathlib import Path


def main() -> None:
    base = Path.home() / "cli-lab" / "round{num:02d}"
    base.mkdir(parents=True, exist_ok=True)
    markers = [base / f"week{{n}}" / "{slug}_week{{n}}.txt" for n in (1, 2, 3)]
    print("Round {num:02d} 收口检查")
    for path in markers:
        print(f"- {{path.name}}: {{'OK' if path.exists() else 'MISSING'}}")


if __name__ == "__main__":
    main()
''',
        encoding="utf-8",
    )
    (fdir / cheatsheet).write_text(
        f"# Round {num:02d} · {title}速查\n\n"
        f"## 建议顺序\n\n1. {w1}\n2. {w2}\n3. {w3}\n\n"
        f"## 最小通过标准\n\n- 沙盒三周 marker 文件均可生成。\n"
        f"- 能对照 `round_{num:02d}.md` 说明本轮与前后轮关系。\n",
        encoding="utf-8",
    )
    print(f"created round_{num:02d}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("rounds", nargs="+", type=int, help="Round numbers e.g. 13 14 15")
    args = parser.parse_args()
    for num in args.rounds:
        if num not in ROUNDS:
            raise SystemExit(f"round {num} not in scaffold map")
        write_round(num)


if __name__ == "__main__":
    main()
