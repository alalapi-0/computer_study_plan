# computer_study_plan · Linux 单课程学习原型

> **定位**：本地优先的网页交互式学习产品原型。
> **当前唯一正式课程**：Linux 基础与工程实践（`linux-foundations`）。
> **长期方向**：成为可扩展的通用学习平台；当前先用 Linux 验证真实动作、证据、反馈与持续学习闭环。

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
open http://127.0.0.1:8777/progress.html
```

打开后：

1. 在「今日」页确认唯一当前任务
2. 进入「学习」页阅读教程；工程练习会显示受限终端
3. 完成最小验证或运行白名单练习脚本
4. 点击「记录并完成」，填写本次记录后保存；路线、复习、手册和成长页按需打开

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
| **当前** | 用已重构的多视图 Web UI 验证 `linux-foundations` 的持续学习、记录、反馈、通关感与网页体验 |
| **后续** | Course/Module/Task 统一模型、Attempt、规则反馈、XP/Mastery、Round 00 垂直切片 |
| **更后** | Linux 模块完善 → 工程质量 → 可选服务化 → 自然语言学习编排评估 → 再评估第二门课 |

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

- 已交付：Phase 0 单课程化基线重构
- 当前 Web UI：今日、学习、路线、复习、手册、成长六个核心视图，以及独立模块检查点
- 已验证设计切片：首页；路线地图与模块总览；聚焦学习与真实反馈；复习记录；五份课程真源驱动的只读命令手册；成长记录与模块检查点。跨屏显式任务由课程注册 ID、Learn URL 与 history 稳定持有，Home 继续只表示真实全局下一项；H04 Home → Learn 共享任务关系、原子降级和 390–920px 移动触控已有浏览器回归。完成/撤销另有隔离内存浏览器测试与临时仓库事务测试，验证 pending、错误恢复、幂等、revision、并发与中断前滚，不写正式进度。以上不把完成标记或设计示例冒充能力验收
- 工作树已删除：软考、数学二、408 计划，以及 Round 03–05、07–21 非 Linux 课程内容
- 当前仍未实现：完整 Attempt / 规则反馈 / XP / Mastery / 成就引擎、自然语言学习编排、第二门课程
- Figma 设计底板：`WtmY7TC867Wdp0qXY2b5uz` 当前包含校准页、10 个 Desktop 屏、10 个 Mobile/Mini Program 屏、3 组核心组件和 6 个 Motion/Codex Handoff 页面；2026-08-11 的校准版 UI 只是重构基线，不是完整对齐终态

状态见 [`docs/PROJECT_STATE.md`](docs/PROJECT_STATE.md)。

---

## 5. 仓库结构（当前）

```text
computer_study_plan/
├─ content/courses/linux-foundations/  ← 唯一正式课程注册与模块索引
├─ rounds/round_00|01|02|06/           ← Linux 可执行练习（兼容真源）
├─ rounds/stage_03_vps_remote_ops/     ← 远程 Linux 支线
├─ plans/linux/                        ← 课程学习路径
├─ progress.html / progress_ui.js / progress_ui.css  ← Web UI、交互与视觉系统
├─ progress.json / progress_data.js / rounds_data.js
├─ scripts/                            ← 本地服务与生成/校验
├─ tests/ui/ + tests/test_progress_transactions.py  ← 只读/隔离内存浏览器与临时仓库事务回归
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

## 8. 外盘 UI 运行环境

`npm run test:ui` 通过 `scripts/external-ui-python` 使用 `/Volumes/AI_WORK_SSD/Runtimes/computer-study-plan/ui-venv`、同级 `browsers/chromium_headless_shell-1223` 和外盘 `Temp/computer-study-plan`。运行前先用 `scripts/external-ui-python --check`；缺盘、错盘、浏览器路径漂移或临时目录不可用时明确退出，不用内盘缓存回退，不自动下载。

本项目浏览器副本由既有本地缓存离线复制；原 `~/Library/Caches/ms-playwright` 是多消费者共享目录，未被本项目清理。源码、Git、正式学习记录和练习沙盒仍在原位。普通服务器和 CLI 会持久化学习状态，不能当成只读存储验证；隔离 UI 回归不写正式进度。

## 9. 恢复非 Linux 旧内容

本轮删除可通过备份标签恢复，见 [`docs/REMOVAL_MANIFEST.md`](docs/REMOVAL_MANIFEST.md)：

```bash
git restore --source=pre-linux-only-refactor-20260718-1029 <path>
```
