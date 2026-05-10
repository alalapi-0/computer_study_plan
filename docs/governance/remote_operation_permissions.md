# Remote Operation Permission Levels（远程操作权限等级）

> 本文件定义编程 AI（Codex / Cursor / 本地编程 AI / 未来 VULTRagent）在本仓库语境下可以做哪些操作、不可以做哪些操作。
> 任何 Level 2 及以上的真实远程操作，都必须经过用户明确授权（参见 `docs/templates/remote_operation_confirmation.md`）。

## 0. 总原则

1. 默认按**最低权限**操作。
2. 升级权限必须**逐级**进行，不允许从 Level 0 直接跳到 Level 4。
3. 任何破坏性操作必须先讲清**目的、命令、风险、回滚**。
4. 任何远程操作必须留下**可追溯记录**。
5. 真实 IP / Key / 凭证**永不写入仓库文档**。

## Level 0 · 只读学习与文档整理

**默认开启。**

允许：

- 阅读仓库文件
- 分析文档结构
- 修改学习文档（不涉及进度系统硬数据）
- 整理路线图、模块总纲、Round 概览
- 设计任务、生成命令示例（必须用占位符）

禁止：

- 不连接远程服务器
- 不执行 SSH
- 不读取真实密钥
- 不修改任何服务器
- 不删除仓库文件（除非任务明确允许，且经 Level 1 授权）

## Level 1 · 本地仓库治理

**需要任务边界明确，但不需要用户额外授权。**

允许：

- 修改本地仓库文档（含 README、roadmap、progress、checklist、Round 文档）
- 合并已确认重复的文档
- 删除已确认无用的文件（须在 commit / 报告中列出）
- 重命名文档
- 创建目录与索引
- 更新 `docs/PROJECT_STATE.md`、`docs/NEXT_ACTIONS.md`

禁止：

- 不连接远程服务器
- 不执行远程命令
- 不修改系统配置
- 不处理真实密钥
- 不删除 Round 00 相关文件、`progress.json`、`mark_done.sh`、主线 Round 概览（除非走 `repository_cleanup_confirmation.md` 流程）

## Level 2 · 远程服务器只读检查

**必须先取得用户明确授权。**

允许（仅只读命令）：

- SSH 登录服务器
- 查看系统信息：`uname -a`、`whoami`、`hostname`
- 查看路径与目录：`pwd`、`ls`
- 查看磁盘 / 内存：`df -h`、`free -h`
- 查看进程 / 监听：`ps aux`、`ss -tulpn`
- 查看日志（只读）
- 检查工具是否安装：`which git`、`which python3`、`which node`、`which tmux`

示例命令清单（复制安全）：

```bash
pwd
ls
whoami
uname -a
df -h
free -h
ps aux
ss -tulpn
which git
which python3
which node
which tmux
```

禁止：

- 不安装软件
- 不删除文件
- 不修改任何配置
- 不开放端口
- 不启动长期服务
- 不写入敏感文件
- 不读取 `.env`、`id_rsa` 等敏感文件内容

## Level 3 · 远程服务器低风险写入操作

**必须先取得用户明确授权，并指定目录与目标。**

允许：

- 创建学习目录（如 `~/study/`、`~/study/logs/`）
- 创建测试文件（如 `hello_vps.txt`）
- `git clone` **公开**仓库（先确认 URL）
- `git pull` 已 clone 的公开仓库
- 创建 `.env.example`
- 创建普通学习脚本
- 启动**短时间**测试命令
- 使用 tmux 运行**低风险**测试任务（如打印日志、定时心跳）

示例命令清单：

```bash
mkdir -p ~/study
mkdir -p ~/study/logs
git clone your_repo_url
touch test.txt
echo "hello vps" > test.txt
tmux new -s study_test
```

禁止：

- 不删除系统目录
- 不修改 `sshd_config`、`/etc/ssh/`
- 不关闭防火墙、不修改 `ufw` 规则
- 不开放危险端口（如 22 之外的 0.0.0.0 监听）
- 不安装不明来源脚本
- 不写入真实 API Key
- 不部署对公网开放的真实服务（应进入 Level 4）

## Level 4 · 远程服务部署与运行

**必须先取得用户明确授权，并完成部署预检。**

允许：

- 安装必要依赖（须列出依赖清单）
- 运行 Python / Node.js 项目
- 启动本地端口服务（**优先 `127.0.0.1` 监听**）
- 用 tmux 或 systemd 管理测试服务（systemd 仅在 Level 5 已授权时使用）
- 用 curl 自我测试服务
- 配置简单文件日志
- 在明确端口范围内开放**测试**端口
- 部署最小 API 服务、最小静态网页

部署预检（必须事先确认）：

- 使用哪个仓库
- 部署到哪个目录
- 监听哪个端口、是否绑定到 `127.0.0.1`
- 是否需要公网访问
- 日志路径
- 启动命令、停止命令、回滚命令
- 失败回滚方案

禁止：

- 不默认配置生产环境
- 不默认绑定真实域名
- 不默认配置 HTTPS
- 不默认安装 Nginx
- 不默认改系统级防火墙
- 不默认设置开机自启
- 不默认暴露敏感接口
- 不默认在 0.0.0.0 上开新端口

## Level 5 · 高风险系统级操作

**默认禁止。** 仅在用户**逐项确认**后允许执行。

包含但不限于：

- 删除服务器上的已有项目 / 大目录
- 修改 `sshd_config`、root 登录策略
- 修改防火墙策略 / `iptables` / `ufw`
- 修改 / 安装 systemd 服务
- 设置开机自启
- 安装 Docker、Nginx、数据库等系统级服务
- 配置 HTTPS / 申请 / 部署证书
- 绑定真实域名
- 修改用户 / 权限 / `sudoers`
- 执行一键安装脚本（`curl ... | bash`）
- 执行 `rm -rf`
- 清空日志
- 重启 / 重装服务器

执行前必须：

1. 说明目的；
2. 列出完整命令；
3. 说明风险与影响范围；
4. 给出回滚方案；
5. 等用户**逐项**明确确认；
6. 执行后写入操作日志。

## 权限等级速查表

| 等级 | 范围 | 是否需用户授权 | 默认 |
|---|---|---|---|
| 0 | 仅文档与示例 | 否 | 开启 |
| 1 | 本地仓库治理 | 否（任务边界明确即可） | 开启 |
| 2 | 远程只读检查 | **是** | 关闭 |
| 3 | 远程低风险写入 | **是** | 关闭 |
| 4 | 远程服务部署与运行 | **是** | 关闭 |
| 5 | 远程高风险系统级 | **是（逐项）** | 关闭 |

## 与确认模板的关系

- Level 2 / 3 / 4 / 5 必须使用 `docs/templates/remote_operation_confirmation.md`。
- 所有 Level 5 操作还必须配合 `docs/checklists/vps_safety_checklist.md` 完整勾选。
- 仓库治理类删除 / 重命名必须使用 `docs/templates/repository_cleanup_confirmation.md`。
