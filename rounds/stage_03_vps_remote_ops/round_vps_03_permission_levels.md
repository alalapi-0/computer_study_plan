# Round VPS-03 · 建立远程操作权限等级与安全规则

## 概览

| 项目 | 内容 |
|---|---|
| 主题 | 远程操作权限等级 + 安全 checklist + 确认模板 |
| 操作权限等级 | **Level 1** |
| 是否需要用户授权 | 否 |
| 前置 | [VPS-02](round_vps_02_module_anchor.md) |
| 下一轮 | [VPS-04](round_vps_04_ssh_basics.md) |

## 目标

在仓库中正式建立可被后续 Round 引用的：

- 远程操作权限等级文档
- 高风险操作定义
- 执行前确认模板
- 操作日志格式（基础版）

## 背景

如果不先把权限等级和确认机制确定下来，后续 Round（VPS-04 起）会无法判断"什么操作必须先问用户"。
本轮文档化、不执行任何远程命令。

## 涉及文件

- `docs/governance/remote_operation_permissions.md`
- `docs/checklists/vps_safety_checklist.md`
- `docs/checklists/remote_operation_checklist.md`
- `docs/templates/remote_operation_confirmation.md`
- `docs/templates/repository_cleanup_confirmation.md`

## 操作权限等级

- 等级：**Level 1**

## 具体任务

1. 维护 `docs/governance/remote_operation_permissions.md`：
   - 定义 Level 0 ~ Level 5 的允许 / 禁止动作。
   - 给出每个等级的命令示例（占位符）。
   - 给出权限等级速查表。
2. 维护 `docs/checklists/vps_safety_checklist.md`：
   - 凭证 / SSH / 命令 / 端口 / 服务 / 备份 / 记录 / Level 5 八个分组。
3. 维护 `docs/checklists/remote_operation_checklist.md`：
   - 执行前 / 连接 / 命令 / 服务运行 / 退出 / 操作记录 / 后续 七阶段。
4. 维护两份确认模板：
   - 远程操作确认（含目标服务器占位、命令预览、风险、回滚、用户确认记录、执行结果）。
   - 仓库治理确认。
5. 在 `docs/governance/codex_workflow.md` 中说明"Codex 在做远程操作前必须先走确认模板"。

## 命令示例

```bash
git checkout -b codex/vps-03-permission-levels
# 修改文档
git add docs/governance/ docs/checklists/ docs/templates/
git status
bash mark_done.sh
git commit -m "VPS-03: establish remote operation permission levels"
git push -u origin codex/vps-03-permission-levels
```

## 验收标准

- [ ] Level 0 ~ Level 5 在 `remote_operation_permissions.md` 中定义清晰。
- [ ] 每级有"允许 / 禁止"列表与命令示例（占位符）。
- [ ] 高风险操作清单完整覆盖：`rm -rf` / 防火墙 / sshd / systemd / 一键脚本 / 重启等。
- [ ] 安全 checklist 与远程操作 checklist 完整。
- [ ] 两份确认模板可直接被后续 Round 引用。
- [ ] 文档全部使用占位符。

## 风险与禁止事项

- 不连接远程服务器。
- 不执行任何 `ssh` 命令。
- 不在文档中写真实 IP / Key / 用户名。

## 输出物

- 完整的 governance + checklists + templates 三个目录。
- 在 `docs/PROJECT_STATE.md` 中标记"远程操作权限体系已建立"。

## 下一轮接口

VPS-04 将基于这套权限体系，**设计**SSH 与远程 Linux 基础任务（仍为 Level 1，文档准备）。
