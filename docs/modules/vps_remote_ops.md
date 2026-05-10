# 模块 · VPS 远程操作（VPS Remote Operations）

> VPS 是把"我在本地学编程"过渡到"在真实服务器环境中运行项目"的关键训练场。
> 本模块不是一篇教程，而是一条贯穿 Linux、网络、GitHub、API、部署的**长期实操训练支线**。

## 1. 模块定位

`computer_study_plan` 主线（Round 00–21）覆盖：

```
终端基础 → Shell/Git → Python/数据结构/算法 → Linux 进阶
       → ai_prep_tool 综合 → 工程化 / 服务化 / AI/ML
```

VPS 模块作为**实操支线**接入这条主线：

```
Round 00–02（终端 / Shell / Git 基础）
        ↓
Round 06（Linux 进阶与自动化）
        ↓
        ├── 主线 Round 14–17（HTTP / FastAPI / 服务化）
        ↓
        └── ★ VPS 支线：rounds/stage_03_vps_remote_ops/
                ↓
        SSH → VPS Linux → 同步 → tmux → 网络 → API → 部署 → SOP
                ↓
        未来：VULTRagent / 个人 Web 产品部署 / AI Agent 远程任务运行
```

VPS 模块连接的学习模块：

| 学习模块 | 接入点 |
|---|---|
| Linux 基础（Round 00–02） | 命令行、文件系统、权限 |
| Linux 进阶（Round 06） | `find` / `xargs` / `sed` / `awk` / SSH / `rsync` / `crontab` / `tmux` |
| 网络基础 | IP / 端口 / DNS / 防火墙 / HTTP 状态码 |
| Git / GitHub | 本地 push、VPS pull 的同步链路 |
| API 学习 | 在远程环境中跑 API 调用，处理 401/403/429/500 |
| 部署（Round 14–17 衔接） | 最小服务部署、tmux/systemd 管理、curl 自测 |
| AI Agent 协作 | 编程 AI 在用户授权下按文档操作远程服务器 |

## 2. 学习目的

学完本模块后，应当能做到：

- 区分本地终端与远程终端，不再"以为自己在远程其实在本地"。
- 通过 SSH 安全连接到 VPS，使用密钥登录而非密码登录。
- 在远程目录下完成**学习目录**结构搭建。
- 通过 GitHub 在本地与 VPS 之间同步代码，理解三角关系（本地 ↔ GitHub ↔ VPS）。
- 使用 `scp` / `rsync` 处理 GitHub 不适合承载的大文件 / 日志同步。
- 使用 tmux 让远程任务在断开连接后继续运行。
- 排查"为什么访问不通"，区分本地、服务器、API 三种失败位置。
- 在 VPS 上跑通最小 API 调用脚本，处理常见错误码。
- 部署一个最小 Web/API 服务（先内网，再决定是否公网）。
- 建立**个人 SOP**，将重复操作整理成可被 AI 复用的清单与脚本。

## 3. 模块的硬约束（与权限等级对齐）

**绝对禁止：**

- 在仓库文档中写入真实服务器 IP、用户名、密码、API Key、私钥。
- 默认启用对公网开放的服务。
- 在未取得用户明确授权的情况下，执行任何 Level 2 及以上的远程操作。
- 执行未知来源的一键安装脚本。
- 在未确认情况下执行 `rm -rf` 或重启服务器。

**所有示例必须使用占位符：**

- `your_server_ip`
- `your_user`
- `your_repo_url`
- `your_api_key_here`
- `example.com`

## 4. 阶段拆分

VPS 模块拆分为 9 个学习阶段（Stage VPS-0 ~ Stage VPS-8）。每个阶段对应若干 Round：

| 阶段 | 主题 | 对应 Round | 默认权限等级 |
|---|---|---|---|
| Stage VPS-0 | 仓库治理与总控接入 | VPS-00、VPS-01、VPS-02、VPS-03 | Level 0 / Level 1 |
| Stage VPS-1 | SSH 与远程 Linux 基础 | VPS-04、VPS-05 | 文档 Level 1，执行 Level 2 |
| Stage VPS-2 | GitHub 与远程仓库同步 | VPS-07 | Level 3 |
| Stage VPS-3 | 文件同步：scp / rsync | VPS-07 衍生 | Level 3 |
| Stage VPS-4 | tmux 与后台任务 | VPS-08 | Level 3 |
| Stage VPS-5 | 网络、端口、防火墙 | VPS-09 | Level 2/3 |
| Stage VPS-6 | 远程 API 调用实验 | VPS-10 | Level 3 |
| Stage VPS-7 | 最小 Web/API 服务部署 | VPS-11 | Level 4 |
| Stage VPS-8 | SOP 与 VULTRagent 接口 | VPS-12 | Level 1 |

> 实际执行顺序参见 `rounds/stage_03_vps_remote_ops/README.md` 中的 Round 索引。

## 5. 模块输出物

完成全部 Round 后应留下：

- VPS 操作 SOP：`docs/checklists/vps_safety_checklist.md` + `docs/checklists/remote_operation_checklist.md`
- 远程部署 checklist：`docs/checklists/project_acceptance_checklist.md` 中的部署部分
- 服务器只读检查记录模板（在 Round VPS-04 / VPS-05 中提供）
- tmux 操作记录模板（在 Round VPS-08 中提供）
- 网络排查记录模板（在 Round VPS-09 中提供）
- 远程 API 调用最小脚本骨架（在 Round VPS-10 中提供）
- 最小服务部署记录模板（在 Round VPS-11 中提供）
- VULTRagent MVP 需求草案（在 Round VPS-12 中提供）

## 6. 与 VULTRagent 的关系

`computer_study_plan` 仍然只承担**学习总控**职责：

- 学习路线
- 阶段规划
- 操作任务
- 验收标准
- 安全规则
- SOP

未来 `VULTRagent` 作为**独立项目仓库**承担**自动化执行**职责：

- 自动检查 VPS 状态
- 自动测试 SSH
- 自动部署仓库
- 自动同步文件
- 自动启动 tmux 任务
- 自动查看日志
- 自动生成服务器报告

接口约定：

- `VULTRagent` 必须遵守本仓库定义的远程操作权限等级。
- `VULTRagent` 必须复用本仓库定义的确认模板与 checklist。
- `VULTRagent` 不在本仓库实现；本模块只为它**写下需求与边界**。

## 7. 验收标准（模块级）

模块整体验收：

- [ ] VPS 模块在 `README.md` 全局路线图中可见。
- [ ] `rounds/stage_03_vps_remote_ops/` 含 13 份 Round 文档（VPS-00 ~ VPS-12）。
- [ ] 文档全部使用占位符，未出现真实 IP / Key / 用户名。
- [ ] 远程操作权限等级被 Round 文档引用。
- [ ] 安全 / 部署 / 远程操作 3 份 checklist 存在。
- [ ] 远程操作确认模板与仓库治理确认模板存在。
- [ ] VULTRagent 需求草案在 Round VPS-12 中留下接口位置。
