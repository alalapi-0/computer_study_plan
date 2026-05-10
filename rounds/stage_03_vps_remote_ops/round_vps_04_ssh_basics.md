# Round VPS-04 · SSH 与远程 Linux 基础任务文档

## 概览

| 项目 | 内容 |
|---|---|
| 主题 | SSH 登录 + 远程 Linux 基础命令的"可执行任务文档" |
| 操作权限等级 | 文档设计：**Level 1**；实际执行：**Level 2 / Level 3** |
| 是否需要用户授权 | 文档阶段否；执行阶段需要 |
| 前置 | [VPS-03](round_vps_03_permission_levels.md) |
| 下一轮 | [VPS-05](round_vps_05_first_readonly_check.md) |

## 目标

- 设计 SSH 登录学习任务（含密钥 vs 密码登录区别）。
- 设计 Linux 基础命令练习（在远程环境中复习 Round 00–02 的命令）。
- 设计 VPS 基础检查记录模板（供 VPS-05 首次执行时使用）。

## 背景

很多新手"以为自己在远程其实在本地"。本轮先把"SSH 是什么、密钥是什么、`whoami` / `hostname` 为何重要"讲清楚，避免后续真实操作时困惑。

## 涉及文件

- 新增 / 维护 `rounds/stage_03_vps_remote_ops/notes/ssh_basics.md`（可选）
- 新增 / 维护 `rounds/stage_03_vps_remote_ops/outputs/server_check_record_template.md`
- 不修改任何已有文件

## 操作权限等级

- 等级：**Level 1**（仅文档设计）。
- 该轮**不**执行 SSH，仅准备好"被 VPS-05 使用的文档"。

## 学习内容（在文档中讲清）

- IP / 用户名 / 端口
- SSH key 与密码登录区别
- `~/.ssh/config` 别名机制
- 本地终端 vs 远程终端
- Linux 目录结构（`/`、`/home/`、`/etc/`、`/var/`）
- 文件权限基础（`r/w/x`、`chmod` 数字与符号写法）
- 常用命令：`pwd`、`ls`、`cd`、`mkdir`、`touch`、`cat`、`whoami`、`hostname`、`uname -a`、`df -h`、`free -h`

## 任务示例（**示例命令仅供后续 Round 执行**）

```bash
ssh your_user@your_server_alias
pwd
ls
whoami
uname -a
mkdir -p ~/study
cd ~/study
touch hello_vps.txt
echo "hello vps" > hello_vps.txt
cat hello_vps.txt
```

## 服务器只读检查记录模板（建议字段）

```markdown
# Server Check Record · YYYY-MM-DD

- 服务器别名：your_server_alias
- 登录用户：your_user
- 登录方式：SSH key
- whoami: ______
- hostname: ______
- pwd（登录初始路径）: ______
- uname -a: ______
- df -h（关键挂载点）: ______
- free -h: ______
- 已安装工具：git ___ / python3 ___ / node ___ / tmux ___
- 缺失工具：______
- 备注：______
```

## 验收标准

- [ ] SSH 登录、密钥登录、本地 vs 远程的区别在文档中说清楚。
- [ ] Linux 基础命令在远程环境下的用法被标注。
- [ ] 服务器只读检查记录模板已写好，可被 VPS-05 直接复用。
- [ ] 所有示例使用占位符。
- [ ] 本轮没有执行任何 `ssh` 命令。

## 风险与禁止事项

- 不写真实 IP / 用户名 / 端口。
- 不在文档中粘贴任何私钥内容。
- 不连接远程服务器。

## 输出物

- 学习任务文档（可放 `rounds/stage_03_vps_remote_ops/notes/ssh_basics.md`，或集中写在本 Round 文档内）。
- 服务器只读检查记录模板（`outputs/server_check_record_template.md`）。

## 下一轮接口

VPS-05 将使用本轮模板，**首次**真实进行 Level 2 远程只读检查。
