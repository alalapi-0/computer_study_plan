# Round 13 · 环境复现与发布基础

Round 13 的目标是把前面几轮做出的 Python 小工具，整理成“换一台机器也能读懂、重建、交付”的最小发布包。用户应当可以只通过 Web UI 完成阅读、运行练习脚本、浏览器终端自测、点击“记录并完成”保存小抄和最终验收。

> **仓库根**：`~/PycharmProjects/computer_study_plan`  
> **练习沙盒**：`~/cli-lab/round13`  
> 路径说明见 [`docs/WORKSPACE.md`](../../docs/WORKSPACE.md)。

## Web UI 完成路径

1. 启动本地服务：`python3 scripts/progress_server.py`。
2. 打开 `http://127.0.0.1:8777/progress.html?round=round_13`。
3. 逐周点击“读教程”打开 notes，点击“运行脚本”生成标准沙盒产物。
4. 对自测任务点击“终端练习”，在浏览器终端中手敲最小命令。
5. 最后运行综合练习，阅读并点击“记录并完成”保存 `env_repro_cheatsheet.md` 与验收解释。

## 本轮安全边界

- 所有自动脚本只写入 `~/cli-lab/round13`，不会改仓库外的系统配置。
- Week 1 会用标准库生成一个无 pip 的演示虚拟环境，用于理解 venv 结构；不会联网安装依赖。
- Week 3 与 final 会生成 Dockerfile、`.dockerignore` 和发布检查脚本；不会自动执行 `docker build` 或 `docker run`。
- 浏览器终端仍会拦截 `pip install`、`docker`、网络下载、远程 Git、SSH 等高风险或非沙盒命令。

## 产物地图

| 阶段 | 自动脚本产物 | 用户自测产物 |
|---|---|---|
| Week 1 | `week1_auto/env_report.json`、`requirements.txt`、`.venv_demo/` | 自己创建 `.venv_self` 并解释 `pyvenv.cfg` |
| Week 2 | `week2_auto/pyproject.toml`、`.env.example`、配置读取脚本 | 自己写 `read_env.py` 或检查 `tomllib` |
| Week 3 | `week3_auto/Dockerfile`、`.dockerignore`、`release_check.py` | 自己写最小 Dockerfile 并说明暂不 build |
| Final | `final_auto/ai_prep_tool_release/` 与 zip 交付包 | 完成环境复现小抄和验收解释 |
