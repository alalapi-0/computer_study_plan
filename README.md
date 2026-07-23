# computer_study_plan · Linux 单课程学习原型

> **定位**：本地优先的网页交互式学习产品原型。
> **当前唯一正式课程**：Linux 基础与工程实践（`linux-foundations`）。
> **长期方向**：用这一门课验证游戏化、强正反馈、可坚持的学习体验。

---

## 0. 本地路径（唯一工作副本）

| 用途 | 路径 |
|---|---|
| **本仓库 Git 根目录** | `~/PycharmProjects/computer_study_plan` |
| **本机绝对路径** | `/Users/alalapi/PycharmProjects/computer_study_plan` |
| **Round 00 终端练习沙盒（不进 Git）** | `~/cli-lab/round0` |

完整约定见 [`docs/WORKSPACE.md`](docs/WORKSPACE.md)。

---

## 快速开始

```bash
cd ~/PycharmProjects/computer_study_plan
python3 scripts/progress_server.py
open http://127.0.0.1:8777/progress.html?round=round_00
```

打开后：

1. 左侧确认当前 Linux 任务
2. 中间读教程
3. 在右侧终端或练习脚本中完成最小验证
4. 点击「记录并完成」，填写本次记录后保存

---

## Agent / MCP 工具配置（普通学习可跳过）

当前项目需要：

- chrome-devtools
- context7
- filesystem
- github
- playwright
- stitch

检查：

```bash
npm run check:mcp
```

说明见 [`docs/cursor_tool_registry_check.md`](docs/cursor_tool_registry_check.md)。

---

## 1. 仓库定位

本仓库**不是**：

- ❌ 多课程大而全学习平台（当前阶段）
- ❌ 软考 / 考研题库或院校信息库
- ❌ 生产业务系统或公网服务

本仓库**是**：

- ✅ 以 Linux 为唯一正式课程的产品原型
- ✅ 本地 Web UI 学习工作区（阅读 / 练习 / 终端 / 记录 / 反馈 / 存档）
- ✅ 可版本管理的课程内容与平台基础设施
- ✅ 为未来多课程预留 course-agnostic 结构，但本阶段不启用第二门课

愿景：[`docs/PRODUCT_VISION.md`](docs/PRODUCT_VISION.md)
路线：[`docs/ROADMAP.md`](docs/ROADMAP.md)
架构：[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

---

## 2. 当前总目标

| 阶段 | 目标 |
|---|---|
| **当前** | 用 `linux-foundations` 验证持续学习、记录、反馈、通关感与网页体验 |
| **后续** | Attempt、规则反馈、XP/Mastery、Round 00 垂直切片、UI/UX 重设计 |
| **更后** | Linux 模块完善 → 工程质量 → 可选服务化 → 再评估第二门课 |

---

## 3. 唯一正式课程

| course_id | 中文名 | 模块 |
|---|---|---|
| `linux-foundations` | Linux 基础与工程实践 | Terminal → 文件系统 → Shell/Git → 自动化 → VPS |

课程注册：[`content/courses/linux-foundations/`](content/courses/linux-foundations/README.md)

兼容练习真源（保持 Round 00 闭环）：

- `rounds/round_00` / `round_01` / `round_02` / `round_06`
- `rounds/stage_03_vps_remote_ops`

进度 lane 与 course_id 均为 `linux-foundations`。

---

## 4. 当前阶段

- 进行中（候选待验收）：Phase 0 单课程化基线重构；待 VERIFY → Judge → APPROVE → DELIVER
- 工作树已删除：软考、数学二、408 计划，以及 Round 03–05、07–21 非 Linux 课程内容
- 本轮明确未做：完整 XP 引擎、UI 视觉重设计、第二门课程、真实浏览器冒烟（`UI_SMOKE_DEFERRED_FOR_ROOT`）

状态见 [`docs/PROJECT_STATE.md`](docs/PROJECT_STATE.md)。

---

## 5. 仓库结构（当前）

```text
computer_study_plan/
├─ content/courses/linux-foundations/  ← 唯一正式课程注册与模块索引
├─ rounds/round_00|01|02|06/           ← Linux 可执行练习（兼容真源）
├─ rounds/stage_03_vps_remote_ops/     ← 远程 Linux 支线
├─ plans/linux/                        ← 课程学习路径
├─ progress.html / progress_ui.js      ← Web UI
├─ progress.json / progress_data.js / rounds_data.js
├─ scripts/                            ← 本地服务与生成/校验
├─ records/                            ← 动作日志、反馈、存档
├─ docs/PRODUCT_VISION.md
├─ docs/ROADMAP.md
├─ docs/ARCHITECTURE.md
├─ docs/CONTENT_AUDIT.md
├─ docs/REMOVAL_MANIFEST.md
├─ README.md
└─ AGENTS.md
```

---

## 6. CLI

```bash
bash mark_done.sh
bash mark_done.sh --all
bash mark_done.sh --lane linux-foundations
bash mark_done.sh <task-id>
bash mark_done.sh <task-id> --undo
```

---

## 7. 验证

```bash
python3 scripts/agent_gate.py --verify
```

涉及课程数据时：

```bash
npm run build:rounds
npm run sync:progress
python3 scripts/generate_task_feedback.py
```

---

## 8. 恢复非 Linux 旧内容

本轮删除可通过备份标签恢复，见 [`docs/REMOVAL_MANIFEST.md`](docs/REMOVAL_MANIFEST.md)：

```bash
git restore --source=pre-linux-only-refactor-20260718-1029 <path>
```
