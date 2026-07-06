# Project User Review · Round 30

> 日期：2026-07-06
> 视角：普通学习者 + 后续自动推进 Agent
> 范围：转换协议版本表、README 当前下一步、进度规则版本与数据结构说明

## 本轮发现的 5 个问题

1. `CONVERSION_PROTOCOL.md` 已标为 v2.1，但版本表的生效日期仍写 2026-05-12，容易把 v2.1 当成 5 月旧协议。
2. 转换协议的“重大变更”仍只描述 v2.0 移除 txt，没有写 v2.1 对 Web UI、本地 API、生成数据、动作日志和任务反馈的同步。
3. README 当前下一步仍说“把模块骨架变成可检查产物清单”，但软考 12 个模块已经有最小产物清单；下一步应转向概念地图。
4. `docs/PROGRESS_RULES.md` 标题仍是 v1.0，和多轮 Web UI / 本地 API / 动作日志同步后的实际规则版本不一致。
5. 进度规则开头仍把 Web UI 轻描淡写成 `progress.html` 展示，且状态模型没有说明 `progress.json` 顶层 `version / lanes / tasks` 结构。

## 修复摘要

- 将转换协议 v2.1 生效日期改为 2026-07-06，并保留 v2.0 的 2026-05-12 生效信息。
- 将转换协议重大变更补入 v2.1 对当前 Web UI / 本地 API / 生成数据 / 动作日志 / 任务反馈维护边界的同步。
- 将 README 当前下一步改为从软考主线选择 1-2 个模块开始写概念地图。
- 将进度规则版本升为 v1.1。
- 将进度规则开头扩展为 `progress.json`、`progress_data.js`、`rounds_data.js`、`progress.html`、`progress_ui.js`、`scripts/progress_server.py` 的当前分工，并补充 `progress.json` 顶层结构说明。

## 验证结果

- 文本扫描通过：本轮目标旧说法不再残留。
- `python3 scripts/agent_gate.py --verify` 通过。
- 浏览器回检通过：默认 Web UI、Round 02 桌面端、Round 02 移动端均可加载；页面显示“学习工作区 / 读教程 / 记录并完成”；Round 02 显示“终端练习”和 `~/cli-lab/round2`；未出现横向溢出。
