# Project User Review · Round 23

> 日期：2026-07-06
> 视角：普通学习者 + 后续自动推进 Agent
> 范围：仓库治理 checklist、确认模板、VPS 支线治理 Round、项目验收 checklist、当前状态文档

## 本轮发现的 5 个问题

1. `docs/checklists/repository_cleanup_checklist.md` 的高保护对象仍只覆盖旧的 `progress.json` / `progress_data.js` / `progress.html` / `mark_done.sh`，漏掉 `rounds_data.js`、`progress_ui.js` 和本地 API。
2. `docs/templates/repository_cleanup_confirmation.md` 的删除确认模板同样使用旧保护范围，执行仓库治理时可能误删当前 Web UI 的生成数据、UI 脚本或服务脚本。
3. `rounds/stage_03_vps_remote_ops/round_vps_01_repo_cleanup.md` 仍沿用旧保护清单，并在命令示例里要求创建独立分支后推分支，和当前默认直接推进 `main` 的规则冲突。
4. `rounds/stage_03_vps_remote_ops/round_vps_02_module_anchor.md` 仍把“不修改进度系统”写成旧四件套；VPS-02 / VPS-03 还保留独立分支推送示例。
5. `docs/checklists/project_acceptance_checklist.md` 和 `docs/governance/repo_rules.md` 的验收 / 删除保护仍只强调 `progress.json`、`progress_data.js` 或 `mark_done.sh`，没有把当前 Web UI、`rounds_data.js`、本地 API、动作日志和反馈纳入风险边界。

## 修复摘要

- 将仓库治理 checklist、确认模板、VPS-01 / VPS-02 / VPS-03 和项目验收 checklist 的保护对象统一到当前进度系统范围。
- 将 `records/action_logs/`、`records/feedback/` 明确归入进度系统产物；用户明确标注的真实学习记录才按真实记录保护，当前仓库未标注则不扩大保护。
- 将 VPS 支线旧的分支 / PR 示例改为当前 `main` 直推流程，并保留验证通过后再推送的约束。
- 补充 `python3 scripts/validate_learning_data.py` / `npm run build:rounds` 等进度系统验证提示。
- 更新 `docs/PROJECT_STATE.md` 的保护边界，补入 `scripts/progress_server.py`、动作日志和反馈目录。

## 验证结果

- 文本扫描确认目标文件不再残留旧四件套保护口径或 VPS 支线独立分支推送示例。
- `git diff --check` 通过。
- `python3 scripts/validate_learning_data.py` 通过。
- `python3 scripts/check_protocol_sync.py` 通过。
- `python3 -m json.tool progress.json` 通过。
- `npm run build:rounds` 与 `npm run sync:progress` 通过。
- `bash mark_done.sh --limit 5` 可正常输出四主线任务摘要。
- 浏览器回检通过：默认页显示当前任务、`读教程`、`记录并完成`；`progress.html?round=round_02` 显示 `终端练习` 并绑定 `~/cli-lab/round2`；390px 移动端无横向溢出。
