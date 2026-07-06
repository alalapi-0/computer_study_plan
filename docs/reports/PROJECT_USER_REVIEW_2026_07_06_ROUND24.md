# Project User Review · Round 24

> 日期：2026-07-06
> 视角：普通学习者 + 后续自动推进 Agent
> 范围：`docs/STAGE_PLAN.md`、`README.md` 的阶段计划、项目结构与维护规则

## 本轮发现的 5 个问题

1. `docs/STAGE_PLAN.md` Stage 0 产物仍把进度系统描述成旧四件套 `progress.json / progress_data.js / mark_done.sh / progress.html`，漏掉当前 Web UI、生成 Round 数据、本地 API、动作日志和任务反馈。
2. Stage 0 退出标准仍只说 `progress.html` 能看到四主线总进度，没有体现当前学习工作区已经支持内联教程、终端、记录、存档和反馈。
3. Stage 7 推荐项目仍把“Linux 学习进度可视化页面”说成“已部分存在”，容易诱导后续重复建设只读看板，而不是在现有 Web UI 上做复盘报表或作品集增量。
4. Stage 资产对照表仍把 `progress.html` 标为“四主线进度”，没有把 `progress_ui.js` 和 `scripts/progress_server.py` 纳入全 Stage 学习工作区入口。
5. README 的项目结构和维护规则仍使用旧进度系统保护口径：缺少 `progress_ui.js`、`rounds_data.js`、`scripts/progress_server.py`、动作日志和反馈目录，并把 `progress_data.js` 写成只由 `mark_done.sh` 生成。

## 修复摘要

- 将 Stage 0 产物和退出标准改为当前 Web UI 学习工作区事实。
- 将 Stage 7 项目方向改为“学习工作区增强”，避免重复建设只读进度页。
- 将 Stage 资产表补充为 `progress.html` / `progress_ui.js` / `scripts/progress_server.py` 组合入口。
- 在 Stage 决策原则中说明当前没有用户标注真实学习记录，动作日志和反馈属于进度系统产物。
- 更新 README 项目结构和维护规则，补齐当前进度系统文件、生成脚本关系和保护边界。

## 验证结果

- 文本扫描确认目标旧说法不再残留。
- `git diff --check` 通过。
- `node --check progress_ui.js` 通过。
- `python3 scripts/check_protocol_sync.py` 通过。
- `python3 scripts/validate_learning_data.py` 通过。
- `python3 -m json.tool progress.json` 通过。
- `npm run build:rounds` 与 `npm run sync:progress` 通过。
- `bash mark_done.sh --limit 5` 可正常输出四主线任务摘要。
- 浏览器回检通过：默认页显示学习工作区、`读教程`、`记录并完成`；`progress.html?round=round_02` 显示 `终端练习` 并绑定 `~/cli-lab/round2`；390px 移动端无横向溢出。
