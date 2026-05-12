# Round VPS-01 · 执行仓库治理与文档合并

## 概览

| 项目 | 内容 |
|---|---|
| 主题 | 在确认范围内执行仓库治理 |
| 操作权限等级 | **Level 1** |
| 是否需要用户授权 | 默认不需要（任务边界明确即可）；涉及高保护对象时需要 |
| 前置 | [VPS-00](round_vps_00_repo_scan.md) |
| 下一轮 | [VPS-02](round_vps_02_module_anchor.md) |

## 目标

- 在 VPS-00 的扫描报告基础上，实际执行**安全范围内**的仓库治理。
- 合并真正重复的文档，重命名混乱文件，更新入口索引。
- 不破坏 Round 00 闭环；不动主线 Round 概览（除非用户单独授权）。

## 背景

仓库治理是 VPS 模块的"前置工作"：先有清晰的入口与索引，VPS Round 才能有挂靠点。
本轮严格限制在 Level 1，不连接任何远程服务器。

## 涉及文件

> 实际清单由 VPS-00 输出决定。本 Round 文档只列出可能的范围与边界。

允许动的：

- 新增 `docs/governance/`、`docs/modules/`、`docs/checklists/`、`docs/templates/` 子目录及其文档（已在主线本次任务中完成）。
- 新增 `rounds/stage_03_vps_remote_ops/` 阶段目录与 Round 文档。
- 更新 `README.md` 入口引用。
- 更新 `docs/PROJECT_STATE.md`、`docs/NEXT_ACTIONS.md`。

**默认不允许动的**（除非用户单独授权）：

- `progress.json`、`progress_data.js`、`progress.html`、`mark_done.sh`
- `rounds/round_00/` 下任何文件
- `round_XX.md`（任意主线 Round）
- `records/` 下任何已写入的用户真实学习记录
- `AGENTS.md`、`CONVERSION_PROTOCOL.md`、`docs/CODEX_LONG_TERM_PLAN.md`、`docs/AUTO_ADVANCE_PROTOCOL.md`、`docs/DECISIONS.md`、`docs/MASTER_STUDY_ROADMAP.md`、`docs/STAGE_PLAN.md`

## 操作权限等级

- 等级：**Level 1**
- 行为限制：仅本地仓库治理；不连接远程服务器；不修改进度数据。

## 具体任务

1. 复用 `docs/checklists/repository_cleanup_checklist.md` 走完阶段 A（扫描与判断）。
2. 复用 `docs/templates/repository_cleanup_confirmation.md` 写出"拟合并 / 拟删除 / 拟重命名"清单。
3. 如清单中**仅含新增**或**完全在新目录中**的改动，可直接执行；如涉及高保护对象，必须先取得用户授权。
4. 执行变更：
   - 新增文件：`git add` 后 commit。
   - 删除文件：用 `git rm`。
   - 重命名文件：用 `git mv`。
5. 更新 `README.md`、`docs/PROJECT_STATE.md`、`docs/NEXT_ACTIONS.md` 中的相关引用。
6. 验证：
   - `git status`、`git diff --check`
   - `bash mark_done.sh`（确认 Round 00 仍可运行）
   - `python3 -m json.tool progress.json`

## 命令示例

```bash
git checkout -b codex/vps-01-repo-cleanup
git status
git add docs/governance/ docs/modules/ docs/checklists/ docs/templates/ rounds/stage_03_vps_remote_ops/
git status
bash mark_done.sh
python3 -m json.tool progress.json
git commit -m "VPS-01: integrate VPS module documents and governance"
git push -u origin codex/vps-01-repo-cleanup
```

## 验收标准

- [ ] `bash mark_done.sh` 仍可正常运行。
- [ ] `python3 -m json.tool progress.json` 通过。
- [ ] 主线 Round 概览未被破坏。
- [ ] `README.md` 的"项目结构"在涉及新增目录时已同步。
- [ ] commit message 含完整变更摘要。
- [ ] 变更报告（PR 描述或回复正文）含：新增 / 修改 / 删除 / 合并 / 风险 / 验证 五段。

## 风险与禁止事项

- 不删除高保护对象。
- 不在未确认情况下批量删除"看起来重复"的文件。
- 不在 main 分支直接执行。
- 不引入新依赖。

## 输出物

- 一次干净的 commit，对应 PR 描述。
- 更新后的 `docs/PROJECT_STATE.md` 与 `docs/NEXT_ACTIONS.md`。

## 下一轮接口

VPS-02 将基于已治理后的目录，正式建立"VPS 模块总纲"在 README 与路线图中的可见入口。
