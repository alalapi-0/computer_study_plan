# Round VPS-05 · 首次远程服务器只读检查

## 概览

| 项目 | 内容 |
|---|---|
| 主题 | 第一次连接 VPS 并做完整只读检查 |
| 操作权限等级 | **Level 2** |
| 是否需要用户授权 | **是**（必须） |
| 前置 | [VPS-04](round_vps_04_ssh_basics.md) |
| 下一轮 | [VPS-06](round_vps_06_remote_dirs.md) |

## 目标

- 通过 SSH 安全连接到 VPS。
- 仅执行只读命令，记录服务器基础信息。
- 形成第一份"服务器只读检查记录"。
- **不修改任何远程文件 / 不安装任何软件**。

## 用户授权请求范例（必须先发给用户）

```
本轮将进行 Level 2 远程服务器只读检查。
只会执行 whoami、pwd、ls、uname、df、free、which 等只读命令。
不会安装软件，不会删除文件，不会修改配置。
请确认是否执行。
```

## 涉及文件

- 输入：`rounds/stage_03_vps_remote_ops/outputs/server_check_record_template.md`（VPS-04 已建立）
- 产出：`rounds/stage_03_vps_remote_ops/outputs/server_check_record_YYYYMMDD.md`（执行后由用户填写）

## 操作权限等级

- 等级：**Level 2**
- 仅允许执行只读命令（参见 `docs/governance/remote_operation_permissions.md` Level 2 段）。

## 具体任务

1. 用户使用 `docs/templates/remote_operation_confirmation.md` 走完确认。
2. 编程 AI / 用户自行通过本地终端 `ssh your_user@your_server_alias` 登录。
3. 登录后立即确认身份与位置：`whoami`、`hostname`、`pwd`。
4. 顺序执行只读命令清单（见下）。
5. 把输出写入 `outputs/server_check_record_YYYYMMDD.md`，**对真实 IP / 用户名做脱敏**。
6. 退出会话：`exit`。

## 命令示例（只读）

```bash
ssh your_user@your_server_alias

whoami
hostname
pwd
ls -la
uname -a
df -h
free -h
ps aux | head -n 20
ss -tulpn 2>/dev/null | head -n 20

which git
which python3
which node
which tmux

cat /etc/os-release
uptime

exit
```

## 验收标准

- [ ] 已成功 SSH 登录。
- [ ] 仅执行了只读命令，未发生任何写入。
- [ ] 已填写 `server_check_record_YYYYMMDD.md`，关键字段齐全。
- [ ] 缺失工具清单已被列出（用于后续 Round 决定是否安装）。
- [ ] 记录文件中**没有**真实 IP / 真实用户名 / 真实主机名（已脱敏或使用占位符）。
- [ ] `docs/checklists/vps_safety_checklist.md` 与 `docs/checklists/remote_operation_checklist.md` 已逐项打勾。

## 风险与禁止事项

- 不安装软件。
- 不删除文件。
- 不修改任何配置。
- 不读取 `.env`、`id_rsa` 等敏感文件内容。
- 不输出真实凭证到仓库文件。

## 输出物

- 一份**已脱敏**的服务器只读检查记录。
- 缺失工具清单（决定 VPS-06 / VPS-07 / VPS-08 是否需要补装）。

## 下一轮接口

VPS-06 将基于本轮发现，进入 Level 3 写入操作（创建学习目录与测试文件）。
