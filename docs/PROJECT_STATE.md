# Project State

> 更新日期：2026-10-01
> 本文件只记录当前事实。

## 1. 当前定位

`computer_study_plan` 处于 **Linux 单课程验证阶段**：

- 唯一正式课程：`linux-foundations`（Linux 基础与工程实践）
- 长期方向：网页交互式、游戏化、强正反馈学习体验
- 当前不建设第二门课程

唯一工作副本：

- `~/Projects/computer-study-plan`
- `/home/alalapi/Projects/computer-study-plan`

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
- Web UI 已重构为“今日、学习、路线、复习、手册、成长”六个核心视图，并包含独立模块检查点页；Desktop / Mobile 共用同一原生 HTML/JavaScript 实现。
- Figma 文件 `WtmY7TC867Wdp0qXY2b5uz` 当前有 5 页：校准页、10 个 Desktop 产品屏、10 个 Mobile/Mini Program 屏、3 组核心组件，以及 6 个 Motion/Codex Handoff 页面。Motion 页以可读取的参数、状态机、转场和降级规范表达；`get_motion_context` 当前没有返回编码动画轨道。
- 2026-08-13 首个完整设计切片已落到首页：Desktop/Mobile 共享真实当前任务与进度，移动端改为 5 个非沉浸导航入口，学习工作区隐藏移动底栏；方块具备桌面 6px 阈值/±28px 和触控 220ms 长按/±18px/最多 4 个对象的边界与回弹，按钮按压保留可见侧壁，减少动效模式保留 160ms 状态淡入淡出。
- 同日第二个设计切片已落到学习工作区：阅读任务使用双栏、终端任务使用三栏聚焦布局；移动端改为可用方向键操作且不重建内容的“任务 / 讲解 / 练习”面板。课程资料具备真实 loading/error/retry 与页内阅读位置恢复，终端明确是本地允许命令约束而非 OS 级隔离。
- “脚本正常结束”“终端命令返回 0”“任务已完成”现在是三个不同事实：脚本成功/失败使用真实返回码与 stdout/stderr 反馈；手动完成后显示服务器已保存的备注、证据、时间与课程任务数，并停留到用户明确继续，不展示 Figma 示例中的 XP、Mastery、尝试次数或复习日期。
- 同日第三个设计切片已落到成长记录与模块检查点：学习者视图按当前六个真实任务组展示完成标记和 action log，不再混入项目治理 Stage；检查点范围显式写入历史状态，脚本确实使任务组由未完成转为完成时，用户查看执行回执后可进入对应检查点。课程总数只按 80 个已注册任务核对；空、缺失、多余或条目异常的进度响应不会被解释成 0% / 100%，仓库镜像只能作为带来源提示的只读快照。
- 同日第四个设计切片已落到 D02–D03/M02–M03 路线地图与模块总览：地图按 5 个真实模块和 1 个课程导览汇总 80 个注册任务，模块页只展示真实周/任务摘要、完成标记检查点和显式学习入口，不再复制完整任务执行工作台。浏览学习组、历史返回和旧 `round`/`activeRound` 深链不会隐式改变当前学习任务；进度不可核对时显示未知态，仓库镜像只读且不能触发检查点结论。
- 同日第五个设计切片已落到 D07/M07 复习：真实 0 动作状态收敛为一个可直接进入当前任务的主引导；只有已注册课程任务确有 action event 时，才展示最近动作、记录队列、任务级当前建议和时间线。运行失败、超时、状态未变与成功记录均显示真实结果；未知或已退出课程范围的历史事件不计入当前课程指标。该视图不把任意动作、静态 `not_started` 反馈或 Figma 示例解释成到期复习、弱项、Mastery 或 Attempt。
- 同日第六个设计切片已落到 D08/M08 命令手册：界面只从 5 份登记 Markdown 课程真源构建“来源 → 章节/搜索结果 → 正文”关系，搜索索引仅存在于运行内存；稳定文档 ID 与章节深链不接受原始路径。读取具备 loading、empty、error、timeout、retry 与竞态裁决，专注阅读与 Back/Forward 保持上下文和焦点，Desktop/Mobile 共用只读数据，不因阅读、搜索或导航写进度，也不展示虚构的解锁、收藏、Mastery 或 Attempt。
- 2026-08-14 跨屏任务上下文已收敛：首页的当前任务只取已核对进度推导的全局下一项；Route、Review 与检查点显式进入的注册任务由 Learn URL 和历史条目持有。刷新、Back / Forward、直接链接及旧 Learn 锚点可恢复精确任务，已完成任务仍可复查、查看记录和撤销；无效或重复任务参数会被清除，不能进入文件、终端或 API 请求。任务切换或离开 Learn 会废弃旧 reader / terminal 请求，包括没有任务 ID 的旧终端入口；该边界不改变进度、动作或本地 API 协议。
- 同日完成首个 Components / Motion 横切检查点：空间块在拖拽时暂停视差，桌面与触控净位移分别受 ±28px / ±18px 约束，释放或取消回到基准位置；运行中切换减少动效会取消手势并清除装饰位移，降级为不超过 160ms 的必要状态反馈。视图语义、隐藏状态与焦点现在原子切换，通用全屏反馈闪烁已移除；终端输入恢复可见键盘焦点，延迟执行期间输入与按钮具备单请求忙碌态。该检查点不改变任务或本地 API 协议。
- 同日完成 H04 Home → Learn 与移动触控检查点：首页卡片和主按钮只在冻结出同一个已注册任务后才进入 Learn；支持 View Transition API 且未请求减少动效时，当前任务卡以 520ms 共享材料关系进入聚焦任务面板，URL、render、可见性和标题焦点仍在同一次导航事务中提交。不支持 API、减少动效、重入、窗口变化或历史导航时安全回到原子切换；`popstate` / `hashchange` 不再重复处理同一次遍历，首次进度尚未核对时也不能进入无任务 Learn。390 / 430 / 720 / 920px 已统一首屏行动、44px 触控与单面板 Learn；安全区 CSS 约定已核对，非零设备 inset 仍待真机回归。
- 仓库已有可重复 UI 回归入口：`tests/ui/` 默认使用只读内存 API、随机端口和 Playwright Chromium 验证 Home → Learn、快速重入、Back / Forward、loading 门禁、reduced-motion 以及 390 / 430 / 720 / 920px 触控；只有显式 opt-in 的隔离内存模式才开放完成/撤销，覆盖单次提交、pending、成功回执、HTTP 错误、超时、输入指纹重试、晚响应/重开、严格响应校验和 390px 触控。fixture 不导入生产进度或终端库，也不写正式数据。
- 同日完成 D05/D06/M05/M06 与 `Depth Button` 的写入事务检查点：记录 modal 以局部材料层级呈现 pending、成功与可聚焦错误，关闭窗口不取消服务器事务也不会被晚响应重新打开；同任务完成/撤销/运行互斥，重复激活只发一个请求。Web 完成/撤销使用精确输入指纹绑定的 `operation_id`；备注与证据各限 500 个 Unicode 字符，超长请求明确拒绝而不截断。服务端使用单调 revision、跨进程本地锁和独立操作账本，生成镜像携带相同 revision；任务完成事实、完整课程快照与对应持久化 event 全部校验后，前端才一次提交并显示成功。可捕获失败回滚精确写前状态；进程中断恢复前会完整核对 WAL 的 request、fingerprint、基准/目标状态、revision 与 event，损坏记录零写入拒绝，合法记录才前滚；读档不回退 revision 或幂等键，且旧 ID 对应 event 已被恢复历史移除时明确拒绝重放，不产生幽灵记录。前端仅为结果不确定失败保留旧 ID，确定性拒绝后相同输入会生成新 ID，避免重试死循环。临时仓库中的并发、重放、故障注入和恢复测试不触碰正式 0/80 数据。
- 新 UI 保留既有任务、教程、受限终端、脚本运行、记录、反馈、存档与深链契约；阅读型任务不再无条件显示终端入口，工程练习仍可绑定 `~/cli-lab` 沙盒。
- Round 00 闭环可运行（教程加载 + 终端绑定 `~/cli-lab/round0` 已验证）。
- 仍使用 JSON / JSONL，无数据库、账号系统或云同步。
- XP / Mastery / 成就 / 完整反馈引擎：**未实现**。
- 自然语言学习编排与第二门课程：**未实现**；长期通用学习平台方向已写入 `PRODUCT_VISION` 与 `ROADMAP`，当前仍坚持 Linux 单课程验证。
- UI/UX 系统重设计：**in progress**。2026-08-11 版本是校准基线；当前首页、D02–D03/M02–M03 路线与模块、D04–D06/M04–M06 学习与反馈、D07/M07 复习、D08/M08 命令手册，以及 D09/D10/M09/M10 成长记录与模块检查点已形成六个可运行切片，跨屏显式任务状态、首个 Components / Motion 横切检查点、H04 Home → Learn 连续关系与移动触控检查点也已收敛，但这些不等于整体验收。现有屏幕切片已在真实浏览器覆盖 Desktop/Mobile、关键宽度、键盘与历史导航、console/network；共享转场的原生与原子降级分支另由只读 Playwright Chromium 回归覆盖。完成/异常数据矩阵使用浏览器隔离响应或临时副本验证，正式数据仍为 0/80、0 条动作记录。
- 本地目标日期仍保留历史 `softExamDate/math2Date/cs408Date` 内部 ID 与 `csp_exam_dates_v1` 存储键，用于兼容已有 localStorage / 存档；可见语义已是 Linux Module 02 / 03 / VPS。

## 存储运行边界（2026-09-03）

原 Mac UI 回归入口保留在 `scripts/external-ui-python-macos`。Linux 使用统一入口 `scripts/external-ui-python`：独立Python3.12/Playwright1.60及Chromium1223位于 `/home/alalapi/Runtimes/computer-study-plan`；缓存和临时目录在对应 `Caches`/`Temp` 根。固定UUID、路径、安装来源及完整树守卫先行；UI测试自动隔离网络、系统IPC与正式数据。现有只读/显式内存夹具保留，报告与截图在 `/home/alalapi/Artifacts/computer-study-plan/linux-ui`。真实学习数据、Linux单课程范围、Phase6状态和下列业务队列不因技术迁移改变；完整产品和真机安全区仍未验收。

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
- Phase 6：继续对齐完整 Figma。跨屏任务身份、直接操控、H04 Home → Learn 连续关系、移动触控和完成/撤销事务已收敛；下一高价值检查点是 revisioned run operation，解决脚本事件与反馈共用 revision、并发/中断恢复和错误自动验收边界。之后仍须基于新状态继续审计 Components、跨屏关系、窄屏密度与遗留实现；六个屏幕切片和现有流程/动效检查点不得视为整体完成
- `progress` / `events` / `feedback` 已有最小 loading、ready-empty、error、stale/read-only 状态和请求竞态保护；终端、存档及其他资源尚未统一到同一状态约定，后续只在相关切片确有价值时收敛
- `progress.html` 仍保留较大的历史内联样式与脚本，新界面由 `progress_ui.css` / `progress_ui.js` 叠加收敛；这是可维护性债务，后续应在可重复回归证据保护下逐步移除重复真源，而不是为清理而重写闭环
- Phase 8+：已建立只读 Home → Learn 与隔离内存完成/撤销自动化，并有生产 `progress_lib` 临时仓库事务测试；后续按实际切片扩展视觉差异、脚本/终端竞态、错误资源和更多屏幕，不一次性搭建与当前风险无关的完整套件
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
