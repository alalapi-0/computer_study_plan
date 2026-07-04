# Round 19 · 机器学习最小闭环

Round 19 的目标是把机器学习最小流程说清楚、跑出可检查产物，并建立“不偷看测试集”的基本直觉。

> **仓库根**：`~/PycharmProjects/computer_study_plan`  
> **练习沙盒**：`~/cli-lab/round19`  
> 路径说明见 [`docs/WORKSPACE.md`](../../docs/WORKSPACE.md)。

## Web UI 完成方式

1. 打开 `progress.html?round=round_19`。
2. 依次展开 Week 1 / Week 2 / Week 3 的阅读任务，直接在页面阅读 notes。
3. 点击每周“练习”任务的“运行”，系统会在 `~/cli-lab/round19` 下生成代码、样例数据和静态检查报告，并自动记录该练习任务完成。
4. 点击每周“自测”任务的“终端”，在浏览器映射终端中手写一个小脚本，确认自己能解释核心概念；自测完成后手动记录。
5. 最终运行 `r19-fin-comp`，再阅读并手动记录小抄和验收任务。

## 本轮边界

- Web UI 自动练习**不执行** `pip install scikit-learn numpy pandas`。
- 自动练习会生成真实 scikit-learn 风格代码，但用 Python 标准库和 AST 做静态检查，保证用户能在没有第三方依赖时完成页面闭环。
- 所有练习产物只写入 `~/cli-lab/round19`，不写入仓库。

## 目录结构

```
round_19/
├─ README.md
├─ week1/notes.md + exercises.py
├─ week2/notes.md + exercises.py
├─ week3/notes.md + exercises.py
└─ final/comprehensive_exercise.py + ml_minimal_loop_cheatsheet.md
```

## 完成标准

- 能解释 `X`、`y`、训练集、测试集、`random_state`。
- 能描述 `fit` / `predict` / `score` 的顺序。
- 能区别 accuracy、precision、recall、F1。
- 能解释训练分数高、测试分数低为什么是过拟合信号。
- 能说明预处理为什么只能在训练集上 `fit`，以及 Pipeline 为什么能减少数据泄漏。
