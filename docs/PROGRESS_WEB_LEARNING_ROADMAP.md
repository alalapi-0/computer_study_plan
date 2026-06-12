# Progress 网页学习闭环路线图（v1.0）

> **目标**：用户在 `http://localhost:8000/progress.html` 完成**全部**学习与练习相关操作——读材料、做练习、打卡、看反馈、写错题与周复盘——**不必切换终端执行 `mark_done.sh` 或手动找目录**。
>
> **现状（2026-06）**：`progress.html` 是**只读看板** + localStorage 个人配置；任务状态靠 `bash mark_done.sh`；练习脚本在 `rounds/round_XX/` 与 `~/cli-lab` 沙盒；Round 00–04 进度闭环，05–21 为骨架。详见 `python3 scripts/round_status.py --summary`。
>
> **原则**：本地优先、单用户、`progress.json` 仍为状态单一事实源；先扩能力再换框架；不破坏 Round 00 现有 CLI 闭环。

---

## 1. 目标体验（用户视角）

打开 `http://localhost:8000/progress.html` 后应能：

| 能力 | 当前 | 目标 |
|------|------|------|
| 看总进度 / 四主线 / Stage | ✅ | ✅ |
| 按 Round 浏览任务清单 | ✅（00–04 有任务；05–21 骨架提示） | ✅ 全路线有任务或明确「仅阅读模式」 |
| 阅读当周 `notes.md` | ❌ 需自己开文件 | ✅ 页面内 Markdown 阅读 |
| 启动当周练习 | ❌ 终端 `bash/python3 exercises.*` | ✅ 页面「开始练习」+ 步骤引导 |
| 标记完成 / 撤销 | ❌ 终端 `mark_done.sh` | ✅ 页面按钮，等价 CLI |
| 查看动作历史 / 反馈 | ❌ 需读 JSONL / JSON | ✅ 任务详情侧栏 |
| 录入错题 | ❌ 手写 `records/error_notes/` | ✅ 表单写入仓库（遵守 lane 目录） |
| 写周复盘 | ❌ 手写 `records/weekly_reviews/` | ✅ 模板表单 + 归档 |
| 软考 / 数学二 lane 学习入口 | ⚠️ 仅 plans 文档链接 | ✅ 模块笔记 + 保底节奏打卡 |

**非目标（本路线图 v1 不做）**：多人账号、云同步、公网部署、在线判题、视频托管、替代官方考纲内容。

---

## 2. 架构方向（实现约束）

```
浏览器  progress.html（原生 JS，渐进增强）
    │  fetch /api/*
    ▼
本地学习服务  scripts/learn_server.py（推荐，单进程）
    │  读写 progress.json、records/、events.jsonl
    │  可选：子进程运行 rounds/**/exercises.*（沙盒路径固定为 ~/cli-lab）
    ▼
仓库文件  progress.json · progress_rounds.json · rounds/ · records/
```

| 决策 | 选择 | 说明 |
|------|------|------|
| 服务形态 | 本地 HTTP + 少量 API | 替代「仅静态 `http.server`」；默认只监听 `127.0.0.1` |
| 状态存储 | 继续 JSON / JSONL | 与 ADR-0001、ADR-0005 一致；超限时再评估 SQLite |
| 前端 | 保留静态 HTML + JS | 与 ADR-0002 一致；组件化仍用原生模块即可 |
| CLI 兼容 | `mark_done.sh` 保留 | API 与脚本共用同一 Python 写入层，避免双事实源 |
| 练习执行 | 沙盒 + 引导式步骤 | Shell 轮次以「步骤清单 + 验收命令」为主；Python 轮次可服务端 `py_compile` / 受限 `subprocess` |
| 安全 | 仅 localhost | 禁止默认绑定 `0.0.0.0`；无认证（单用户本机） |

启动方式（目标态，写入 README 时使用）：

```bash
cd <仓库根>
python3 scripts/learn_server.py          # 默认 http://127.0.0.1:8000/progress.html
# 或
npm run learn:server
```

---

## 3. 分阶段实现路径（PW-0 → PW-6）

每阶段：**可独立验收**、**可回滚**、**不一次性引入 React/数据库**。

### PW-0：本地学习服务基座

**目标**：在 8000 端口提供静态资源 + 健康检查 API，为网页写操作铺路。

**产出**：

- `scripts/learn_server.py`（`threading` + `http.server` 或极简 FastAPI，二选一以「零/少新依赖」为先）
- `GET /api/health`、`GET /api/progress`（只读 `progress.json`）
- `package.json`：`learn:server` 脚本
- README §6.3 更新：推荐 `learn_server` 而非裸 `http.server`

**验收**：

- `curl http://127.0.0.1:8000/api/health` 返回 OK
- 浏览器打开 `/progress.html` 与现网一致
- `python3 scripts/check_user_journey.py` 仍通过

**风险**：与现有 `python3 -m http.server 8000` 文档冲突 → 在 README 标明「交互功能需 learn_server」。

---

### PW-1：网页内任务打卡（替代终端 mark_done）

**目标**：在任务行上点击「完成 / 撤销」，效果等同 `bash mark_done.sh <id>`。

**产出**：

- `POST /api/tasks/<task_id>/done`、`POST /api/tasks/<task_id>/undo`
- 共用写入模块（建议 `scripts/progress_store.py`）：更新 `progress.json`、`progress_data.js`、追加 `events.jsonl`
- `progress.html`：任务项操作按钮；`file://` 模式下降级提示「请用 learn_server」
- `mark_done.sh` 改为调用 `progress_store`（或内嵌相同逻辑），消除双实现

**验收**：

- 页面点击后 `progress.json` 更新且 `validate_learning_data.py` 通过
- CLI `mark_done.sh` 与 API 结果一致
- Round 00 旧 task ID 行为不变

---

### PW-2：学习内容内嵌（notes 阅读器）

**目标**：在 Round / 周次面板内直接阅读 `rounds/round_XX/weekN/notes.md`。

**产出**：

- `GET /api/content?path=rounds/round_XX/weekN/notes.md`（路径白名单，禁止任意文件读取）
- 页面 Markdown 渲染（轻量库或服务端转 HTML，优先无构建）
- 阅读类任务 `reading` 一键标记完成

**验收**：

- Round 00 week1 notes 可在页面完整阅读
- 恶意路径 `../../../etc/passwd` 被拒绝

---

### PW-3：练习工作区（Shell + Python 引导）

**目标**：用户从页面进入练习，而不必记忆 `exercises.sh` 路径。

**产出**：

- 练习面板：步骤列表（从 `progress_rounds.json` 或解析练习脚本注释生成）
- Shell 轮次：展示要在 `~/cli-lab/roundN` 执行的命令序列 + 「我已完成」确认 → 调 PW-1 打卡
- Python 轮次：`POST /api/exercise/run` 在沙盒目录执行 `python3 exercises.py`（超时、stdout 回传）；**不**自动 mark 全部练习项，保留自测确认
- 文档：`docs/WORKSPACE.md` 补充沙盒与网页练习关系

**验收**：

- Round 00 week1：页面引导完成一次练习流程并打卡
- Round 07 week1：页面触发 `exercises.py` 并看到输出

**非目标**：浏览器内嵌完整终端（xterm.js）——v1 用步骤清单即可，终端模拟放 PW-3b 可选。

---

### PW-4：全路线进度接入 + 看板元数据同步

**目标**：Round 05–21 接入 `progress.json` 与看板 weeks 元数据，与 PW-1–3 能力对齐。

**产出**：

- 批量任务注册脚本（基于 `round_status` + 模板），或逐轮 Agent 任务队列 `TASK-WEB-04-*`
- `generate_progress_rounds.py` 为每轮生成 weeks/tasks
- 骨架轮次若暂无可执行练习，UI 显示「阅读 + 自测清单」模式

**验收**：

- `progress.json` 任务数覆盖 22 轮（或文档声明的 engineering 全线）
- 看板每轮非空面板；`check_user_journey.py` 扩展用例

**依赖**：可与 PW-1–3 并行，但**网页打卡**依赖 PW-1。

---

### PW-5：反馈、历史与错题入口

**目标**：任务详情可看动作历史与 `task_feedback`；错题可从页面写入 `records/error_notes/`。

**产出**：

- `GET /api/tasks/<id>/events`、`GET /api/tasks/<id>/feedback`
- 错题表单：`POST /api/error_notes` → `records/error_notes/<lane>/<module>/`
- 对接 `docs/ERROR_REVIEW_SYSTEM.md` 字段约定

**验收**：

- 完成一任务后，页面展示 `events.jsonl` 最近记录
- 提交一道错题，文件落盘且 `validate_learning_data` 不失败

---

### PW-6：四主线统一学习入口（软考 / 数学二 / 408 阅读态）

**目标**：engineering 以外 lane 在同一 URL 下有可推进入口（不要求全部练习脚本化）。

**产出**：

- `soft_exam`：`plans/soft_exam/*.md` 模块阅读 + 章节勾选（写入 `progress.json` 新任务或独立 `lane_tasks`）
- `math2`：每周一题占位打卡（保底节奏）
- `cs408`：plans 阅读 + 链接 `KNOWLEDGE_MAPPING`
- Stage 卡片与 lane 进度联动真实任务数

**验收**：

- 四主线在页面上均有「本周可执行」入口，而非仅 engineering 有任务

---

## 4. 与现有 Stage / 任务队列的关系

| 仓库阶段 | 与本路线图关系 |
|----------|----------------|
| Stage 0 | PW-0 ~ PW-1 属于「学习系统准备」的延续 |
| Stage 1（engineering） | PW-3、PW-4 直接支撑 Round 实操 |
| Stage 2–5（考试 lane） | PW-6 提供统一入口，不替代 `plans/` 专项深度 |
| `docs/CODEX_LONG_TERM_PLAN.md` Phase 4 | 本文件是 Phase 4「网页交互核心界面」的**可执行拆解** |
| `docs/NEXT_ACTIONS.md` | 见 `TASK-WEB-01` ~ `TASK-WEB-06`（queued，非当前最高优先级） |

**优先级说明**：不挤占软考 Stage 2 内容填充与数学二保底节奏；PW-0 ~ PW-1 可在「工程维护轮」穿插实现；PW-4 全路线接入工作量大，按 Round 分批。

---

## 5. 任务队列编号（供 Agent 选用）

| 任务 ID | 对应阶段 | 是否需要用户介入 |
|---------|----------|------------------|
| TASK-WEB-01 | PW-0 学习服务基座 | 否 |
| TASK-WEB-02 | PW-1 网页打卡 + progress_store | 否 |
| TASK-WEB-03 | PW-2 notes 阅读器 | 否 |
| TASK-WEB-04 | PW-3 练习工作区 | 否 |
| TASK-WEB-05 | PW-4 全路线进度接入 | 否（工作量大，可分 Round 子任务） |
| TASK-WEB-06 | PW-5 反馈与错题 | 部分（真实错题内容仍建议用户填） |
| TASK-WEB-07 | PW-6 四主线入口 | 否 |

推进前运行：`python3 scripts/agent_gate.py --verify`。

---

## 6. 验收总清单（路线图完成定义）

当以下全部成立时，视为本路线图 v1 **完成**：

- [ ] 默认文档入口为 `learn_server`，`progress.html` 在 localhost 可完成：读 notes、做练习引导、打卡、看历史
- [ ] `mark_done.sh` 与网页 API 共用写入层，无状态分叉
- [ ] engineering Round 00–21 均在看板可导航（任务或阅读模式）
- [ ] 四主线均有可执行入口
- [ ] `check_user_journey.py` 含「localhost 学习服务」用例且通过
- [ ] 未引入数据库；未默认公网暴露

---

## 7. 维护规则

- 本文件只描述**产品与阶段路径**；具体 API 字段在实现时写入 `CONVERSION_PROTOCOL.md` 新 § 或 `docs/modules/progress_web_api.md`（PW-0 创建）。
- 每完成一个 PW 阶段：更新 `docs/PROJECT_STATE.md`、`docs/NEXT_ACTIONS.md` 中对应 TASK-WEB 状态。
- 不得将本路线图中的「目标态」写成「已完成」除非 §6 验收项已勾选。

---

## 8. 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-06-12 | 初版：localhost 全学习闭环 PW-0 ~ PW-6 + TASK-WEB 队列 |
