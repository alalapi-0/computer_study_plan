# Round VPS-12 · VPS 操作 SOP 与 VULTRagent 需求草案

## 概览

| 项目 | 内容 |
|---|---|
| 主题 | 把 VPS-00 ~ VPS-11 沉淀成 SOP，并写出 VULTRagent MVP 需求草案 |
| 操作权限等级 | **Level 1** |
| 是否需要用户授权 | 否 |
| 前置 | [VPS-11](round_vps_11_minimal_service.md) |
| 下一轮 | （阶段终点；后续可启动主线 Round 14–17 服务化或独立项目仓库 `VULTRagent`） |

## 目标

- 总结 VPS-00 ~ VPS-11 的全部输出物。
- 形成一份**可直接被编程 AI 使用**的 VPS 操作 SOP。
- 提炼 `VULTRagent`（独立项目）的 MVP 需求草案。
- 明确"哪些操作可以未来自动化、哪些必须人工确认"的边界。

## 涉及文件

- `rounds/stage_03_vps_remote_ops/outputs/vps_sop.md`
- `rounds/stage_03_vps_remote_ops/outputs/vultragent_mvp_requirements.md`
- 更新 `docs/PROJECT_STATE.md`

## 操作权限等级

- 等级：**Level 1**（仅本地文档）。

## 具体任务

1. 汇总以下内容到 `outputs/vps_sop.md`：
   - 远程操作权限等级速查
   - 安全 checklist 速查
   - 远程操作 checklist 速查
   - 各 Round 的关键命令清单（脱敏）
   - 常见错误码清单（401 / 403 / 429 / 5xx）
   - 常用占位符（避免误用真实凭证）
   - 服务启动 / 停止 / 回滚通用流程
2. 写出 `outputs/vultragent_mvp_requirements.md`：
   - 项目定位（独立仓库，与 `computer_study_plan` 协同）
   - 不做的事（不做生产部署、不做多人系统、不接管认证）
   - MVP 功能清单：
     - 自动 SSH 测试（Level 2）
     - 自动只读检查脚本（Level 2）
     - 自动 clone 公开仓库（Level 3）
     - 自动 tmux 管理服务（Level 3 / 4）
     - 自动收集日志（Level 2）
     - 自动生成服务器报告
   - 自动化边界：
     - **永不**自动执行 Level 5 操作
     - Level 4 必须有人工确认
     - 任何凭证必须从用户本地配置读取
   - 复用本仓库定义的：
     - 远程操作权限等级
     - 远程操作确认模板
     - 安全 checklist
3. 在 `docs/PROJECT_STATE.md` 中追加"VPS 模块阶段性收尾"段落，并把后续主推方向写到 `docs/NEXT_ACTIONS.md`。

## SOP 大纲（建议）

```
1. 准备
   - 本地 ~/.ssh/config 别名配置
   - .env 与 .env.example 分离
2. 进入会话
   - ssh 登录
   - 立即 whoami / hostname / pwd
3. 只读检查（Level 2）
   - 系统 / 磁盘 / 内存 / 进程 / 端口
4. 写入操作（Level 3）
   - 学习目录
   - clone 仓库
   - tmux 管理
5. 网络
   - 出站 / 监听 / 防火墙状态
6. API 调用
   - venv / requests / dotenv / 日志
7. 部署
   - 默认 127.0.0.1
   - tmux 管理
   - curl 自测
   - 启停 / 回滚
8. 收尾
   - 日志归档（脱敏）
   - 状态报告
   - exit
```

## VULTRagent MVP 需求草案大纲（建议）

```
- 名称：VULTRagent
- 定位：单人单节点远程运维辅助 Agent
- 上游依赖：
  - 本仓库 docs/governance/remote_operation_permissions.md
  - 本仓库 docs/checklists/*
  - 本仓库 docs/templates/*
- MVP 功能：
  1. ssh_check：测试 SSH 可达
  2. readonly_report：执行 Level 2 只读检查并生成报告
  3. repo_pull：拉取已配置的公开仓库
  4. tmux_run：在 tmux 中启动指定命令
  5. service_curl_check：执行 curl 自测
  6. log_tail：拉取最近日志
  7. status_report：生成"服务器当前状态"报告
- 非 MVP（明确不做）：
  - 系统级安装、Docker、HTTPS 自动化
  - 域名 / DNS 自动化
  - 多人共享 / 团队权限
- 安全约束：
  - 永不自动执行 Level 5
  - Level 4 强制人工确认
  - 凭证仅从本地配置读取，不存仓库
  - 操作记录默认脱敏
- 与本仓库的接口：
  - 操作前读取本仓库的权限等级文档
  - 复用本仓库的确认模板格式
  - 把执行结果按本仓库 outputs/ 模板写入对应 Round
```

## 验收标准

- [ ] `outputs/vps_sop.md` 存在，覆盖 8 大主题。
- [ ] `outputs/vultragent_mvp_requirements.md` 存在，并明确 MVP 范围、非 MVP、安全约束、与本仓库的接口。
- [ ] 至少能向第三方解释"哪些操作可以未来自动化，哪些必须人工确认"。
- [ ] `docs/PROJECT_STATE.md` 已追加阶段性收尾段落。
- [ ] 全部文档使用占位符。

## 风险与禁止事项

- 不在本轮实现 `VULTRagent` 任何代码。
- 不把 SOP 写得过细以致替代用户判断（SOP 是辅助，不是命令本身）。
- 不在草案中承诺会"自动执行 Level 5"。

## 输出物

- 一份完整的 VPS 操作 SOP。
- 一份 VULTRagent MVP 需求草案（可直接作为未来独立仓库的 README 草稿）。

## 阶段终点

VPS 实操支线在此告一段落。下一步可以选：

1. 进入主线 Round 14–17（HTTP / FastAPI / 服务化）。
2. 启动独立 `VULTRagent` 项目仓库，按本草案落地。
3. 进入个人产品部署主线（属未来 stage_04_project_deployment）。

具体路径选择写入 `docs/NEXT_ACTIONS.md`。
