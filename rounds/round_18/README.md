# Round 18 · 数值计算与数据分析前置

本轮把机器学习前置的数据感觉补起来：数组形状、向量化、CSV、DataFrame、筛选、缺失值、分组统计和最小分析报告。

> **仓库根**：`~/PycharmProjects/computer_study_plan`  
> **练习沙盒**：`~/cli-lab/round18`  
> 路径说明见 [`docs/WORKSPACE.md`](../../docs/WORKSPACE.md)。

## Web UI 完成路径

1. 启动页面服务：`python3 scripts/progress_server.py --host 127.0.0.1 --port 8777`。
2. 打开 `http://127.0.0.1:8777/progress.html?round=round_18`。
3. 在 Round 18 面板中按顺序点击每周的“读教程”阅读 notes。
4. 对“练习”任务点击“运行脚本”，脚本会在 `~/cli-lab/round18` 生成练习产物并写入动作记录。
5. 对“自测”“产出”“验收”任务点击“终端练习”或“记录并完成”，完成后在“记录并完成”弹窗保存备注和证据路径。

## 本轮产物

| 周次 | 自动练习产物 | 用户自测方向 |
|---|---|---|
| Week 1 | `week1_auto/numpy_arrays/` | 手写一个列表/二维表的 shape、axis、广播解释 |
| Week 2 | `week2_auto/pandas_csv/` | 手写一个小 CSV 并统计标签数量 |
| Week 3 | `week3_auto/analysis_pipeline/` | 手写一个“读、清洗、统计、导出”流程说明 |
| Final | `final_auto/numeric_data_lab/` | 完成小抄并解释数据分析主链 |

## 边界

- 自动练习不执行 `pip install numpy pandas`，也不要求 Web UI 终端安装第三方包。
- 自动练习会生成 NumPy/pandas 风格代码和标准库静态检查报告，帮助你先掌握代码形状与数据分析流程。
- 之后如果你在本机环境手动安装 NumPy/pandas，可以到同一沙盒里运行生成的脚本做真实体验。
