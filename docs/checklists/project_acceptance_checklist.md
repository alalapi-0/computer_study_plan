# 项目验收 Checklist

> 本清单适用于本仓库范围内的**学习任务验收**与**最小服务部署验收**。
> 它不是企业级生产验收，重点是"对学习者来说，本任务真的完成了吗"。

## A. 学习任务验收（适用于所有 Round）

- [ ] Round 文档中"本轮目标"全部能够说清楚或勾选。
- [ ] Round 文档中"练习清单"已经亲手做过（不只是看过）。
- [ ] Round 文档中"验收标准"全部满足。
- [ ] Round 文档中"本轮不学什么"未被越界。
- [ ] 在不查笔记的情况下，能复述本轮 3 条最重要的命令或概念。

## B. 远程操作类 Round 的额外验收

- [ ] 本轮的"操作权限等级"被明确标注。
- [ ] 本轮的远程操作记录已写入输出物。
- [ ] 本轮没有出现真实 IP / Key / 用户名。
- [ ] `docs/checklists/vps_safety_checklist.md` 已逐项勾选。
- [ ] `docs/checklists/remote_operation_checklist.md` 已逐项勾选。
- [ ] 涉及部署时，可重复"启动 → 自测 → 停止 → 回滚"全流程。

## C. 仓库治理类 Round 的额外验收

- [ ] 本轮新增 / 修改 / 删除文件清单已写入 commit 与变更报告。
- [ ] 删除文件已先经 `docs/templates/repository_cleanup_confirmation.md` 走完确认流程。
- [ ] Linux 正式课程 Round 概览（`round_00.md` / `01` / `02` / `06`）未被破坏。
- [ ] Round 00 最小可运行闭环未被破坏：`bash mark_done.sh --lane linux-foundations` 可正常运行。
- [ ] 未重新引入非 Linux 正式课程目录（如 `plans/soft_exam`、`rounds/round_21`）。
- [ ] 进度系统核心文件未被意外覆盖：`progress.json`、`progress_data.js`、`rounds_data.js`、`progress.html`、`progress_ui.js`、`scripts/progress_server.py`、`mark_done.sh`。
- [ ] 涉及进度系统时，`python3 scripts/validate_learning_data.py` 通过；如修改 Round 元数据，已运行 `npm run build:rounds`。
- [ ] `README.md` 的"项目结构"在必要时已同步。

## D. 最小服务部署验收（适用于 VPS-11 等部署 Round）

- [ ] 服务可以启动。
- [ ] 服务可以通过 `curl http://127.0.0.1:<port>` 自测通过。
- [ ] 服务的端口、日志路径、启动命令、停止命令均已记录。
- [ ] 服务已能稳定停止 / 重启。
- [ ] 服务**未**默认开放公网；如需公网，已经过单独 Level 4 确认。
- [ ] 回滚方案存在且可执行。

## E. 文档与状态同步验收

- [ ] `docs/PROJECT_STATE.md` 已更新。
- [ ] `docs/NEXT_ACTIONS.md` 已更新（本任务标记为 done，必要时追加新任务）。
- [ ] 如有架构决策，`docs/DECISIONS.md` 已新增 ADR。
- [ ] 如涉及面向用户使用方式变化，`README.md` 已同步。

## F. Git 与远程同步验收

- [ ] 本轮在 `main` 上完成；如使用独立分支，已说明原因。
- [ ] 工作区干净（除 IDE / 系统副产物外）。
- [ ] commit message 使用 `TASK-XXX:` 或 `VPS-XX:` 等清晰前缀。
- [ ] 已直接 push 到 origin/main（如 remote 可用）。

> 任何一项未通过，都不算"完成"。可以记录"已部分达成"，但不应直接进入下一轮。
