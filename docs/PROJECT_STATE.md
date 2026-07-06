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

## 13. 2026-07-06 TASK-RR-62 第八轮项目用户视角评测与状态提示修复

状态：done

本轮评测报告：

- `docs/reports/PROJECT_USER_REVIEW_2026_07_06_ROUND8.md`

本轮发现并修复：

- `bash mark_done.sh` 只显示任务 id，不显示标题，已改为按 lane 输出 `task-id — 任务标题 / 所属分组`。
- Stage 0 在 Web UI 阶段面板显示 `—`，已改为显示治理准备已完成，避免误读为缺失进度。
- 当前薄弱项规则把软考 / 数学二 / 408 这类启动中小主线全部隐藏，已改为“当前关注项”，区分 `启动中` 与 `薄弱项`。
- 工程任务打开后终端面板默认仍显示未绑定任务，已改为当前工程任务自动绑定到对应 `~/cli-lab/roundN` 沙盒。
- README 已说明 CLI 是快速查看 / 补标记 / 撤销工具，正式学习优先用 Web UI。

验证摘要：

- 默认 Web UI 软考任务仍不显示终端面板，关注项会提示软考 / 数学二 / 408 启动状态。
- `round=round_00` 工程任务进入页面后，终端自动绑定到 `~/cli-lab/round0`，教程和终端同屏保留。
- CLI 无参数输出包含任务标题和所属分组，未知任务只预览前 20 个可读任务，避免输出墙。

## 14. 2026-07-06 TASK-RR-63 第九轮项目用户视角评测与 CLI / 阶段参考修复

状态：done

本轮评测报告：

- `docs/reports/PROJECT_USER_REVIEW_2026_07_06_ROUND9.md`

本轮发现并修复：

- `bash mark_done.sh` 默认输出 316 行，已改为每条主线只显示前 8 个未完成任务，并保留 `--all` 查看完整列表。
- CLI 缺少按当前主线收窄的入口，已新增 `--lane <lane>` 和 `--limit N`，并同步 README 示例。
- README 和 Web UI 终端文案仍按手动绑定描述，已改为工程任务自动绑定，`终端练习` 用于切换或重新聚焦。
- 终端快捷命令包含默认沙盒不存在的 `next_steps.txt`，已替换为 `pwd`、`ls`、`ls -la`、`find . -maxdepth 2 -type f`，并在 Round 00 第 1 周追加安全目录切换练习。
- Stage 面板容易被误读为真实验收进度，已改为“阶段参考”，并把 lane 映射百分比标为近似参考。

验证摘要：

- CLI 默认状态输出为紧凑视图，`--all`、`--lane soft_exam`、`--limit 20` 可用。
- 默认 Web UI 的阶段卡片显示“阶段参考”和“近似参考”，不再把 lane 百分比伪装成验收进度。
- `round=round_00` 工程任务仍会自动绑定到 `~/cli-lab/round0`，快捷命令不再包含缺失文件。

## 15. 2026-07-06 TASK-RR-64 第十轮项目用户视角评测与计划/本地记录清理

状态：done

本轮评测报告：

- `docs/reports/PROJECT_USER_REVIEW_2026_07_06_ROUND10.md`

本轮发现并修复：

- `plans/soft_exam/README.md` 出现两个 `## 6` 标题，已把配套文件改为第 7 节。
- `plans/math2/README.md` 说所有笔记都不预先创建，但 `limits.md`、`la_matrix.md` 已存在，已改为链接这两个启动骨架，并只把其他文件标为按需创建。
- `docs/STAGE_PLAN.md` Stage 3 仍指向不存在的 `plans/soft_exam/mock_exams.md`，已改为 `records/weekly_reviews/mock_exams/`。
- Web UI 存档快照 `records/saves/*.json` 会污染 Git 状态，已加入 `.gitignore` 并在目录 README 说明本地快照不提交。
- 浏览器终端历史 `records/terminal/commands.jsonl` 会污染 Git 状态，已加入 `.gitignore` 并在 README 说明长期结论应写入学习记录或周复盘。

验证摘要：

- 默认 Web UI 记录弹窗空记录校验正常，未写入完成状态。
- `lane=math2` 页面显示已有 `limits.md`、`la_matrix.md` 启动骨架，不再与文档事实冲突。
- 生成类存档和终端历史已从 Git 跟踪候选中排除，目录说明仍保留。

## 16. 2026-07-06 TASK-RR-65 第十一轮项目用户视角评测与折叠区/文案修复

状态：done

本轮评测报告：

- `docs/reports/PROJECT_USER_REVIEW_2026_07_06_ROUND11.md`

本轮发现并修复：

- 管理区提示“默认收起”，但 `details.open=false` 时存档、阶段、关注项等内容仍可见，已显式隐藏闭合状态下的 `.secondary-tools-body`。
- 侧栏说明仍写“工程任务再打开终端”，已改为工程任务自动联动终端。
- 内联阅读器空状态仍写工程任务可再绑定终端，已改为自动联动终端。
- 任务清单说明写“点击阅读”，但按钮实际是 `读教程`，已统一为 `读教程`。
- `records/terminal/README.md` 仍写 Web UI 的“完成 / 记录”，已改为当前的“记录并完成 / 记录回看”。

验证摘要：

- 桌面与 390px 移动端浏览器回检确认：`details.open=false` 时 `.secondary-tools-body` 为 `display:none`，存档区没有可见尺寸。
- 页面无横向溢出；任务清单说明已显示 `读教程`。
- 终端自动联动相关文案和终端记录文档已同步当前完成流程。

## 17. 2026-07-06 TASK-RR-66 第十二轮项目用户视角评测与 Round 指引统一

状态：done

本轮评测报告：

- `docs/reports/PROJECT_USER_REVIEW_2026_07_06_ROUND12.md`

本轮发现并修复：

- README 仓库结构把 `rounds/round_00/` 写成“已完成”，已改为“已展开并接入 Web UI”，避免误读为用户已经学完。
- `rounds/round_00/README.md` 和 Round 00 最终脚本仍引导静态 `progress.html` / `python3 -m http.server 8000`，已改为 `scripts/progress_server.py` 与 `http://127.0.0.1:8777/progress.html?round=round_00`。
- 多个 Round README 仍使用 `8765`、`8778`、`8787` 或相对 `progress.html?round=...`，已统一到当前 8777 Web UI 入口。
- Round README、notes、exercise 输出和 final 小抄中的旧按钮名已统一为 `读教程`、`运行脚本`、`终端练习`、`记录并完成`。
- `docs/DECISIONS.md` 和 `docs/AUTO_ADVANCE_PROTOCOL.md` 已同步当前 Web UI / 本地 API / JSONL 记录事实与必读文档清单。

验证摘要：

- 文本回扫确认当前 Round 00–21 入口不再残留旧端口、静态 8000 看板入口或旧按钮组合。
- Shell 脚本语法检查覆盖 Round 00–06 仍涉及的 `.sh` 入口。
- 标准验证与浏览器回检见本轮提交记录。
