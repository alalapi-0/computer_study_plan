# Project User Review · Round 26

> 日期：2026-07-06
> 视角：普通学习者 + 后续自动推进 Agent
> 范围：README 日常入口、工作区路径说明、长期协作验证基线、Web UI 标题与提示

## 本轮发现的 5 个问题

1. README 的日常入口章节仍叫“看进度”，会把 Web UI 误导成被动看板，而不是用于阅读、练习、记录和终端联动的学习工作区。
2. README 仍使用“看板首屏 / 看板包含 / 进度看板任务集合”等旧说法，削弱了“先在学习工作区完成一个小动作”的主流程。
3. `docs/WORKSPACE.md` 的路径规范仍写“开看板”，与当前 Web UI 学习工作区定位不一致。
4. `docs/CODEX_LONG_TERM_PLAN.md` 的产品边界未列动作日志和任务反馈，验证基线也没有跟 `agent_gate.py --verify` 的当前低成本检查保持一致。
5. `progress.html` 的浏览器标题和记录提示仍使用“学习进度看板 / 下次打开看板”，用户可见层面仍把页面说成旧看板。

## 修复摘要

- 将 README 日常入口改为“打开 Web UI 学习工作区”，并把剩余看板措辞改为 Web UI / 学习工作区。
- 更新 WORKSPACE 路径表，避免继续把日常入口称作“开看板”。
- 将长期协作计划的产品边界补入动作日志与任务反馈，并将默认验证入口改为 `python3 scripts/agent_gate.py --verify`。
- 将 Web UI 浏览器标题改为“学习工作区 · 四主线”，记录提示改为“下次打开 Web UI 会自动加载”。

## 验证结果

- `python3 scripts/agent_gate.py --verify` 通过。
- `npm run build:rounds` 与 `npm run sync:progress` 通过，生成数据保持一致。
- 文本扫描确认 README、WORKSPACE、CODEX_LONG_TERM_PLAN 和 Web UI 标题 / 提示不再残留本轮目标旧说法。
- 浏览器回检默认 Web UI、桌面 Round 02 与移动端 Round 02：标题为“学习工作区 · 四主线”，教程入口、`记录并完成`、工程任务终端、`~/cli-lab/round2` 绑定和横向溢出检查均通过。
