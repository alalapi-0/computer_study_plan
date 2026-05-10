# 仓库治理 Checklist

> 本清单适用于"删除文件 / 重命名文件 / 合并文档 / 重组目录"这一类**Level 1 仓库治理**操作。
> 与 `docs/templates/repository_cleanup_confirmation.md` 配合使用。

## A. 扫描与判断

- [ ] 已完整列出仓库当前结构（`ls -la` / `tree`）。
- [ ] 已识别**疑似重复文档**及其证据（重复段落、相同主题等）。
- [ ] 已识别**疑似过期文档**（与当前路线无关 / 已被新文档取代）。
- [ ] 已识别**命名混乱文件**（不符合 `docs/governance/file_naming_rules.md`）。
- [ ] 已识别**临时残留文件**（`tmp.*`、`untitled.*`、`.DS_Store` 等）。
- [ ] 已确认**未触碰**以下高保护对象：
  - [ ] `progress.json`
  - [ ] `progress_data.js`
  - [ ] `progress.html`
  - [ ] `mark_done.sh`
  - [ ] `rounds/round_00/`
  - [ ] 任意 `round_XX.md` / `plan_round_XX.txt`（未经用户授权）

## B. 提案

- [ ] 已写出"拟合并文件清单"。
- [ ] 已写出"拟删除文件清单"。
- [ ] 已写出"拟重命名文件清单"。
- [ ] 每条改动都附**理由**与**风险评估**。
- [ ] 已说明信息是否已迁移到新位置；未迁移的内容**不允许删除**。
- [ ] 已说明回滚方式（git 回退即可）。

## C. 用户确认

- [ ] 已使用 `docs/templates/repository_cleanup_confirmation.md` 提交确认。
- [ ] 已取得用户**明确**授权。
- [ ] 用户对**每个高风险条目**逐项确认（如删除 Round 文档、删除进度数据相关文件）。

## D. 执行

- [ ] 在独立分支 `codex/<task-id>-short-title` 上执行。
- [ ] 删除 / 重命名通过 `git mv` 或 `git rm` 完成（保留可追溯性）。
- [ ] 合并文档时保留信息来源记录。
- [ ] 必要时在原文件位置留下跳转说明（"本文件内容已迁移至 X"）。

## E. 验证

- [ ] `git status` 状态清晰，未触碰本轮无关文件。
- [ ] `git diff --check` 无白空格 / 行尾问题。
- [ ] Round 00 最小闭环验证：`bash mark_done.sh` 仍可运行。
- [ ] 涉及 JSON 时：`python3 -m json.tool progress.json` 通过。

## F. 报告

- [ ] commit message 含完整变更摘要。
- [ ] 变更报告（PR 描述或回复正文）包含：
  - [ ] 新增文件清单
  - [ ] 修改文件清单
  - [ ] 删除文件清单
  - [ ] 合并说明
  - [ ] 风险与已规避项
  - [ ] 验证结果

## G. 同步

- [ ] `docs/PROJECT_STATE.md` 已更新。
- [ ] `docs/NEXT_ACTIONS.md` 已更新。
- [ ] 必要时 `README.md` 的"项目结构"已同步。
- [ ] push 到 origin 独立分支；不直接 push `main`。
