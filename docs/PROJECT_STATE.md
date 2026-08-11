# Project State

> 更新日期：2026-08-11
> 本文件只记录当前事实。

## 1. 当前定位

`computer_study_plan` 处于 **Linux 单课程验证阶段**：

- 唯一正式课程：`linux-foundations`（Linux 基础与工程实践）
- 长期方向：网页交互式、游戏化、强正反馈学习体验
- 当前不建设第二门课程

唯一工作副本：

- `~/PycharmProjects/computer_study_plan`
- `/Users/alalapi/PycharmProjects/computer_study_plan`

练习沙盒默认在 `~/cli-lab/roundN`，不进入 Git。

## 2. 当前可运行入口

- Web UI：`progress.html`
- 本地服务：`python3 scripts/progress_server.py`
- 默认地址：`http://127.0.0.1:8777/progress.html`
- CLI：`bash mark_done.sh`
- 数据源：`progress.json`
- 前端镜像：`progress_data.js`、`rounds_data.js`
- 课程注册：`content/courses/linux-foundations/course.json`

## 3. 当前实现事实

- 工作树已删除软考 / 数学二 / 408 计划目录，以及 Round 03–05、07–21 非 Linux 课程内容（备份标签可恢复）。
- 保留 Linux 课程材料：Round 00 / 01 / 02 / 06、VPS 支线、`plans/linux/`。
- 已建立 `content/courses/linux-foundations/` 课程与模块索引（canonical 注册；Round 真源仍兼容保留在 `rounds/`）。
- 进度系统收敛为单一 lane / course：`linux-foundations`（80 任务）。
- Web UI 仍支持：当前任务、内联教程、浏览器终端、练习脚本、记录完成/撤销、动作日志、反馈、存档读档。
- Web UI 已重构为“今日、学习、路线、复习、手册、成长”六个核心视图，并包含独立阶段结算页；Desktop / Mobile 共用同一原生 HTML/JavaScript 实现。
- 首页视觉依据为 Figma 文件 `WtmY7TC867Wdp0qXY2b5uz` 中当前唯一可访问的 `00｜Reference & Calibration` 页面：暖铜/冷紫光场、半透明暗部卡片、实体按钮与有限空间交互。该文件当前没有可读取的 Desktop / Mini Program / Components / Motion 页面或 Motion 数据。
- 新 UI 保留既有任务、教程、受限终端、脚本运行、记录、反馈、存档与深链契约；阅读型任务不再无条件显示终端入口，工程练习仍可绑定 `~/cli-lab` 沙盒。
- Round 00 闭环可运行（教程加载 + 终端绑定 `~/cli-lab/round0` 已验证）。
- 仍使用 JSON / JSONL，无数据库、账号系统或云同步。
- XP / Mastery / 成就 / 完整反馈引擎：**未实现**。
- 自然语言学习编排与第二门课程：**未实现**；长期通用学习平台方向已写入 `PRODUCT_VISION` 与 `ROADMAP`，当前仍坚持 Linux 单课程验证。
- UI/UX 系统重设计：**已完成本地实现、项目质量门与真实浏览器回归；精确候选仍由当前任务的独立 Judge 结论约束**。
- 本地目标日期仍保留历史 `softExamDate/math2Date/cs408Date` 内部 ID 与 `csp_exam_dates_v1` 存储键，用于兼容已有 localStorage / 存档；可见语义已是 Linux Module 02 / 03 / VPS。

## 4. 保护边界

默认保护：

- `progress.json` / `progress_data.js` / `rounds_data.js`
- `progress.html` / `progress_ui.js` / `scripts/progress_server.py`
- `mark_done.sh`
- `records/action_logs/` / `records/feedback/`
- `rounds/round_00/`
- Linux 课程兼容文档：`round_00.md`、`round_01.md`、`round_02.md`、`round_06.md`

## 5. 当前问题 / 后续

- Phase 1：把 Round 内容进一步迁入统一 Course/Module/Task 模型
- Phase 2+：Attempt、规则反馈、XP/通关
- Phase 6：2026-08-11 UI/UX 重设计已完成本地实现与浏览器回归；若 Figma 后续补齐产品屏或 Motion 数据，再做逐屏对齐审计
- Phase 8+：补充可重复的自动化 UI / E2E 测试入口，降低仅靠人工浏览器回归的成本
- 历史多课程文档若仍出现在 git history 或旧报告中，不代表当前正式范围

## 6. 本轮重构元数据（治理状态）

- 契约：`TASK-LINUX-ONLY-BASELINE-20260718` / revision `r2`
- 备份标签：`pre-linux-only-refactor-20260718-1029` → `d244177`
- 交付提交：`41daa9c`（已 fast-forward 并推送到 `origin/main`）
- 审计：`docs/CONTENT_AUDIT.md`
- 删除清单：`docs/REMOVAL_MANIFEST.md`
- 治理阶段：**DELIVERED**（Judge PASS → Governor APPROVE → 本地提交 → 用户授权后合入并推送 `main`）
- 浏览器冒烟：已完成（Round 00 教程 + 终端 `pwd`；无 JS error）
- 状态同步：本文件与 `NEXT_ACTIONS` 于 2026-07-23 按交付结果修正
