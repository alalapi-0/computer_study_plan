# Project State

> 更新日期：2026-07-06
> 本文件只记录当前事实。2026-04/05 的旧状态日志已从正文移除，必要时从 git history 追溯。

## 1. 当前定位

`computer_study_plan` 是本地优先的长期学习总控仓库，服务于：

- 软考中级软件设计师高分 / 满分导向。
- 数学二、408 兼容基础、0854 跨专业考研准备。
- Linux / Shell / Git / Python / Web/API / 数据与 AI 工程实操。

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

推荐启动：

```bash
cd ~/PycharmProjects/computer_study_plan
python3 scripts/progress_server.py
open http://127.0.0.1:8777/progress.html
```

## 3. 当前实现事实

- `rounds/round_00` 至 `rounds/round_21` 均已展开为可读 notes、可运行练习脚本和最终验收材料。
- `rounds_data.js` 提供 28 个 Round / 计划分组；`progress.json` 跟踪 304 个任务，其中 101 个 exercise 任务可通过本地 API 运行。
- 计划入口已接入 Web UI：学习计划总览、软考、数学二、408、Linux、VPS 支线。
- Web UI 已支持：
  - 当前任务聚焦。
  - 内联教程阅读。
  - 浏览器映射终端。
  - 白名单练习脚本运行。
  - 记录并完成 / 已完成记录回看 / 撤销。
  - 动作日志与任务反馈。
  - 存档与读档。
- 当前仍使用 JSON / JSONL 文件，不使用数据库、账号系统或云同步。

## 4. 保护边界

默认保护：

- `progress.json`
- `progress_data.js`
- `rounds_data.js`
- `progress.html`
- `progress_ui.js`
- `mark_done.sh`
- `rounds/round_00/`
- `round_00.md` 至 `round_21.md`

当前用户已说明 `records/` 下不存在需要保护的真实学习记录；后续若出现真实记录，需要重新标注保护范围。

## 5. 当前问题

- Web UI 仍需要持续以用户视角检查信息密度、教程/终端联动和移动端可用性。
- 软考 / 数学二 / 408 仍主要是计划入口，不含具体题库或官方考纲缓存。
- VPS 支线只提供阅读与授权前准备，不默认执行真实远程操作。
- Cursor MCP CLI 层可能显示 `needs approval`；当前 Codex 线程可用工具和 Cursor 工具注册状态不完全一致。

## 6. 当前协作规则

- 默认直接在 `main` 上完成、验证、commit、push。
- 独立分支和 PR 仅在用户要求审查、实验性大改或 main 推送失败时使用。
- 每轮仍必须运行验证并更新 `docs/PROJECT_STATE.md` 与 `docs/NEXT_ACTIONS.md`。
- 不缓存具体考题、考点条目、院校招生数据；涉及考试信息必须使用最新官方源。

## 7. 2026-07-06 TASK-RR-56 治理规则与旧路线压缩

状态：done

本轮完成：

- 将仓库规则从“禁止直接 push main / 默认独立分支”改为“默认直接 push main”。
- 删除正文中的早期 Phase 0-7 和 TASK-002 至 TASK-012 长篇旧路线，保留当前路线入口。
- 压缩 `PROJECT_STATE` 和 `NEXT_ACTIONS`，避免新 Agent 被历史日志误导。
- 修正 `agent_gate` 输出，使后续自动推进提示 `branch_hint: "main"`，并正确显示任务标题。

风险边界：

- 不删除 Round 00-21 学习内容。
- 不删除进度系统核心文件。
- 不写入未经官方核验的考试或院校信息。

## 8. 2026-07-06 TASK-RR-57 第三轮项目用户视角评测与入口清理

状态：done

本轮评测报告：

- `docs/reports/PROJECT_USER_REVIEW_2026_07_06_ROUND3.md`

本轮发现并修复：

- README 把 MCP / Cursor 工具配置放在学习入口之前，已新增“快速开始”，并把工具配置标注为普通学习可跳过。
- README 对仓库定位、当前目标版本、Round 12–21 展开状态和 Round 数量的描述过期，已同步为当前 Web UI 学习系统事实。
- `docs/STAGE_PLAN.md` Stage 0 / Stage 1 仍像仓库建设未完成，已改为区分“仓库材料已展开”和“用户学习完成状态”。
- Web UI 当前阅读任务缺少“终端练习”入口，已允许 engineering reading 任务绑定浏览器终端。
- 390px 移动端顶部 chrome 推迟学习工作区，已隐藏移动端 `今日学习` 顶栏并压缩侧栏 / 工作区标题区域。

验证摘要：

- 桌面 `progress.html?round=round_02` 当前任务显示 `读教程 / 终端练习 / 记录并完成`。
- 点击当前阅读任务的 `终端练习` 后，终端工作目录绑定为 `~/cli-lab/round2`，内联教程仍为 `rounds/round_02/week1/notes.md`。
- 390px 移动端无横向溢出，学习工作区从约 474px 提前到约 265px 开始，内联教程进入首屏。

## 9. 2026-07-06 TASK-RR-58 第四轮项目用户视角评测与默认入口一致性修复

状态：done

本轮评测报告：

- `docs/reports/PROJECT_USER_REVIEW_2026_07_06_ROUND4.md`

本轮发现并修复：

- README 的 UI 开发流程仍建议 `python3 -m http.server 8000`，已改为使用 `python3 scripts/progress_server.py` 和真实 8777 URL。
- 默认软考阅读任务没有终端按钮，但任务卡和终端面板仍提示点击“终端练习”，已改为非工程任务显示“不需要终端”，并压缩终端面板。
- 默认当前任务在 `soft_exam`，但 Round 浏览停在 `engineering / Round 00`，已让默认 Round 浏览跟随当前任务所在 lane。
- `plans/soft_exam/README.md` 说所有模块文件都未创建，但 `os.md`、`ds.md`、`db.md` 已存在，已改为显示已有启动骨架和待建模块。
- 错题系统要求抄写完整题面，和“不缓存具体考题”规则冲突，已改为自写题意摘要、来源定位、错误原因和订正思路。

验证摘要：

- 默认 `progress.html` 当前任务仍为软考阅读任务，但任务卡不再提示缺失的终端入口。
- 默认 Round 浏览切到软考主线，而不是工程 Round 00。
- 非工程默认任务下终端面板进入压缩提示状态；工程任务仍保留终端绑定能力。

## 10. 2026-07-06 TASK-RR-59 第五轮项目用户视角评测与记录优先流程修复

状态：done

本轮评测报告：

- `docs/reports/PROJECT_USER_REVIEW_2026_07_06_ROUND5.md`

本轮发现并修复：

- `docs/cursor_browser_ui_runbook.md`、`docs/prompts/CURSOR_UI_IMPLEMENTATION_PROMPT.md`、`docs/WORKSPACE.md` 仍把静态服务器写成常规 UI 启动方式，已改为默认使用 `python3 scripts/progress_server.py`。
- 默认软考阅读任务下，侧栏和工作区标题仍强调“右侧敲命令 / 浏览器终端”，已改为按任务做练习或写要点，工程任务再启用终端。
- 默认非工程任务下的空闲终端面板仍占用桌面和移动端空间，已在非终端任务中隐藏终端面板。
- 任务流要求“写记录并完成”，但记录备注可空且可直接完成，已改为“记录并完成”，未完成任务必须填写本次记录。
- 侧栏 `进度设置` 只滚到折叠标题但不展开，已改为点击后自动展开管理区并滚动定位。

验证摘要：

- 默认 `progress.html` 软考任务下不显示终端面板。
- `记录并完成` 打开记录弹窗，未填写本次记录时不会标记完成。
- 点击侧栏 `进度设置` 会打开 `进度、配置、存档与复盘信息` 管理区。
- `round=round_02` 工程任务仍显示 `终端练习`，终端绑定能力保留。

## 11. 2026-07-06 TASK-RR-60 第六轮项目用户视角评测与任务清单/记录入口修复

状态：done

本轮评测报告：

- `docs/reports/PROJECT_USER_REVIEW_2026_07_06_ROUND6.md`

本轮发现并修复：

- Web UI 把跨主线任务区继续叫 `Round 清单 / 按主线查看 Round`，但默认入口已是软考计划任务，已改为 `任务清单 / 按主线查看任务`。
- 未完成任务同时显示 `记录` 和 `记录并完成`，而 `记录` 入口实际也会进入完成流程，已改为未完成任务只显示 `记录并完成`。
- 练习运行结果提示仍引导点击旧的 `完成` 或 `记录`，已改为统一提示使用 `记录并完成`。
- `PROJECT_STATE.md` 把 `rounds_data.js` 的显示分组和 `progress.json` 的任务跟踪混写为“28 个分组、304 个任务”，已拆开说明真实数据来源。
- 软考模块 README 的已有骨架文件只是代码文本，且内联阅读器不支持相对 Markdown 链接，已把 `os.md`、`ds.md`、`db.md` 改为链接并支持页内打开。

验证摘要：

- 默认 `progress.html` 软考任务下只显示 `读教程 / 记录并完成`，不再显示重复的 `记录` 入口。
- 软考总览内的 `os.md`、`ds.md`、`db.md` 链接可在页内继续打开。
- 任务清单区域标题和侧栏导航已切到任务视角。
- `round=round_02` 工程任务仍显示 `读教程 / 终端练习 / 记录并完成`。

## 12. 2026-07-06 TASK-RR-61 第七轮项目用户视角评测与记录/启动产物修复

状态：done

本轮评测报告：

- `docs/reports/PROJECT_USER_REVIEW_2026_07_06_ROUND7.md`

本轮发现并修复：

- README 和任务流文案仍像是先写记录再点按钮，已改为点击 `记录并完成` 后在弹窗中填写记录并保存。
- 记录弹窗的备注和证据示例固定为软考 / Round 00 场景，已改为按 engineering / soft_exam / math2 / cs408 生成示例。
- 终端绑定后显示 `~/roundN`，与文档中的 `~/cli-lab/roundN` 不一致，已统一显示完整沙盒路径，并修正 Round 21 残留命令。
- `docs/STAGE_PLAN.md` Stage 2 仍说软考 README 是 Stage 0 空表，已改为当前已有启动骨架与最小产物清单的事实。
- 软考、数学二、408 启动页面缺少“做到什么算完成”的标准，已补最小产物清单，避免只读完就打卡。

验证摘要：

- 默认软考任务的流程提示改为先点 `记录并完成`，再在弹窗写记录。
- 记录弹窗在软考任务下显示 `plans/soft_exam/README.md` 这类证据示例，在工程任务下显示 `~/cli-lab/roundN` 示例。
- `round=round_02` 终端绑定后工作目录显示 `~/cli-lab/round2`。
