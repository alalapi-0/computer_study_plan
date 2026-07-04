# Web UI 完成审计报告（2026-07-05）

## 目标

验证用户能否主要通过 `progress.html` 完成学习推进：

- 在页面内选择 Round / 计划入口。
- 在页面内阅读本地学习文档和练习脚本。
- 通过外部链接跳转到官方或参考资料。
- 运行工程练习脚本，使用浏览器映射终端完成手敲练习。
- 写入学习记录、完成 / 撤销任务。
- 创建存档并读档恢复。

## 本轮补齐

| 缺口 | 处理结果 |
|---|---|
| `plans/README.md`、软考 README、数学二 README 未作为任务入口出现 | 新增 `plan_overview`，并补齐软考 / 数学二主线总览阅读任务 |
| `plans/linux/README.md` 未接入 Web UI | 新增 `plan_linux`，归入 `engineering` lane |
| `rounds/stage_03_vps_remote_ops/` 现有 VPS 文档只能在文件树中读 | 新增 `plan_vps`，注册 VPS 总纲 + VPS-00 至 VPS-12 共 14 个阅读任务 |
| 浏览器默认请求 `/favicon.ico` 产生无意义 404 控制台错误 | `progress.html` 添加内联 favicon |

当前 `rounds_data.js` 覆盖 28 个 Web UI 分组、304 个任务，其中 101 个是可运行 `exercise` 任务。新增的 18 个任务均为阅读 / 记录型任务，不会自动执行真实远程操作。

## 数据覆盖

| 验证项 | 结果 |
|---|---|
| `rounds_data.js` 分组数 | 28 |
| Web UI 总任务数 | 304 |
| 可运行 exercise 任务数 | 101 |
| 任务文件引用 | 全部存在 |
| 新增计划入口 | `plan_overview`、`plan_linux`、`plan_vps`，并扩展 `plan_soft_exam` / `plan_math2` |
| 新增任务 lane | Linux / VPS 均归 `engineering`；软考 / 数学二维持各自 lane |

## 功能审计

| 用户能力 | 证据 | 结论 |
|---|---|---|
| 只通过 Web UI 选择学习模块 | Chrome 打开 `plan_overview`、`plan_soft_exam`、`plan_math2`、`plan_cs408`、`plan_linux`、`plan_vps`、`round_00`、`round_21` 均能选中正确面板 | 通过 |
| 文档在页面内阅读 | `plan_vps` 点击“打开”后弹窗显示 `Stage 03 · VPS 远程操作`，正文包含“用户授权”安全提示 | 通过 |
| 外部链接直接跳转 | `round_05.md` 阅读弹窗渲染 5 个 `https://` 链接，均为 `target="_blank"` 且 `rel="noreferrer noopener"` | 通过 |
| 练习脚本可运行 | 101 个 `exercise` 任务通过 `/api/tasks/<id>/run` 全量 API 验证，无失败 | 通过 |
| 浏览器映射终端入口存在 | Round 00 显示 18 个“终端”按钮，Round 21 显示 9 个“终端”按钮；终端卡片在页面可见 | 通过 |
| 记录与完成入口存在 | 抽检所有计划入口与 Round 00 / Round 21 均显示“记录”和“完成 / 撤销”按钮 | 通过 |
| 存档读档 | `POST /api/saves`、临时完成任务、`POST /api/saves/<id>/load`、`GET /api/saves` 验证通过；读档前自动恢复点存在 | 通过 |
| 桌面布局 | 1280px 下抽检页面 `scrollWidth == clientWidth`，无整页横向溢出 | 通过 |
| 移动端布局 | 390px 下 `plan_vps` 14 个任务可见，按钮换行，`scrollWidth == clientWidth` | 通过 |
| 控制台错误 | 添加 favicon 后 Chrome 回归 `consoleErrors: []` | 通过 |

## 截图

- `/tmp/web_ui_completion_round05_links.png`：Round 05 阅读弹窗外链渲染。
- `/tmp/web_ui_completion_plan_vps_mobile.png`：390px 移动端 VPS 支线任务列表。
- `/tmp/web_ui_completion_round21_reader.png`：Round 21 阅读弹窗抽检截图。

## 工具与记录保护

- Codex 应用内浏览器成功发起页面请求，但在 DOM 状态读取阶段连续超时；最终使用系统 Chrome + Playwright 做同等真实浏览器回归，未向项目添加依赖。
- API 全量练习与存档读档测试前后均备份并恢复真实记录文件。
- 本轮保留的 `progress.json` / `progress_data.js` / `records/feedback/task_feedback.json` 变化来自新增 18 个正式阅读任务，不是测试污染。
- 测试产生的临时终端历史、临时存档和动作日志变动已清理或恢复。

## 边界

- 软考、数学二、408 的具体题目、考点条目、院校招生数据和考试大纲不得凭经验写入仓库，后续必须以最新官方来源为准。
- VPS Level 2 及以上真实远程操作仍需用户授权；Web UI 当前提供阅读、记录与准备入口，不默认连接服务器。
