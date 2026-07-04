# Web UI 用户视角测试报告（2026-07-04）

## 目标

验证学习系统是否能让用户只通过 Web UI 完成以下闭环：

1. 找到下一条该学的任务。
2. 在页面内阅读学习资料或练习脚本。
3. 在页面内写入学习记录、备注和证据路径。
4. 在页面内完成 / 撤销任务，并同步 `progress.json`、`records/action_logs/events.jsonl`、`records/feedback/task_feedback.json`。
5. 桌面与移动端布局可理解、可使用、无横向溢出。

## Before 测试发现

| 问题 | 用户影响 | 处理 |
|---|---|---|
| 首屏是统计看板，用户不知道下一步该学什么 | 打开页面后仍要自己判断路线 | 新增“继续学习”卡片，优先推荐当前最高优先级未完成任务 |
| Markdown 阅读器只做简单正则替换，表格、引用、代码块、编号列表显示混乱 | 资料能打开但不适合学习 | 重写轻量 Markdown 渲染，支持标题、引用、无序 / 有序列表、表格、代码块、链接 |
| `.sh` / `.py` 练习脚本不能在页面内阅读 | 用户看不到练习步骤，仍依赖终端 / 编辑器 | 允许脚本文件在阅读弹窗中以代码块打开 |
| 页面能写 action log，但 UI 看不到历史记录 | “完成记录”不可验证，用户不清楚是否写入成功 | 新增 `/api/events` 与每个任务的“记录”入口 |
| 完成 / 撤销后 feedback 文件不会自动更新 | 页面建议可能与真实动作不一致 | `mark_task()` 写入动作后自动重建 task feedback |
| 旧按钮绑定逻辑会把“阅读”按钮也当作打卡按钮处理 | 可能发出 `/api/tasks/null/done` 之类错误请求 | 只给带 `data-action` 的按钮绑定完成 / 撤销逻辑 |
| `progress.json` 中有 2 条 Round 02 冗余任务不在 UI 元数据中 | 用户无法通过 UI 覆盖所有任务 | 补齐 Round 02 完整任务元数据，并删除无脚本、无事件的旧冗余任务 |
| 移动端任务行横向溢出 | 手机上出现横向滚动条，按钮挤出卡片 | 增加移动端网格布局与输入区收缩规则 |
| 浏览器缓存旧 `progress_ui.js` | 更新后页面可能继续运行旧逻辑 | 给关键脚本加版本查询串 |

## After 验证结果

| 验证项 | 结果 |
|---|---|
| Web UI 首页出现“继续学习”卡片 | 通过 |
| 软考数据结构资料可在弹窗中阅读 | 通过 |
| Round 00 `.sh` 练习脚本可在弹窗中阅读 | 通过 |
| “记录”弹窗可写备注和证据路径并标记完成 | 通过 |
| 页面撤销后任务恢复未完成，feedback 回到未完成建议 | 通过 |
| 本轮 UI 测试产生的临时事件已清理 | 通过 |
| `progress.json` 与 `rounds_data.js` 任务集合完全对齐 | 通过，均为 286 条 |
| 桌面端无横向溢出 | 通过 |
| 390px 移动端无横向溢出，按钮无截断 | 通过 |

## Figma 视觉重设计补测

- Figma 文件：<https://www.figma.com/design/SYls2yaG0D7EEAJGvrcZUd>
- 设计稿内容：桌面工作台、移动端工作台、实现说明。
- before 视觉问题：首屏由说明文字和同质卡片堆叠，下一步任务不够突出；顶部技术说明占用高度；任务状态依赖 emoji；按钮和类型标签噪声偏大；浅灰背景 + 大量白卡缺少层级。
- 实现调整：新增左侧学习导航轨；首屏改为“今日学习”工作区；“继续学习”卡片升级为下一步任务主行动；主线指标、阶段、薄弱项降级为扫描信息；任务状态改为 CSS 状态圆点；移动端只保留局部导航横向滚动，不允许整页横向滚动。
- after 回测：桌面端 1280px 无横向溢出；移动端 390px 无横向溢出；“阅读资料”和“记录”弹窗可正常打开；当前 URL 无 console error；未点击完成按钮，未写入真实学习记录。

## 存档与读档补测

- 新增能力：Web UI 可创建本地学习进度快照，快照保存 `progress.json`、动作日志、任务反馈、浏览器终端命令历史、本周任务与考试倒计时。
- 安全策略：读档前自动创建“读档前恢复点”，避免误读档后无法恢复。
- API 验证：`GET /api/saves`、`POST /api/saves`、`POST /api/saves/<save_id>/load` 均通过；测试快照含 286 个任务、7 条动作记录。
- UI 验证：用户可在“存档与读档”卡片输入备注、点击“创建存档”、在列表点击“读档”、确认后完成恢复；读档后自动恢复点出现在列表。
- 布局验证：桌面端 1280px 无横向溢出；390px 移动端无整页横向溢出；当前 URL 无 console error。
- 清理：本轮 API/UI 测试产生的 `codex-*test-save` 临时快照已删除，未保留为真实用户存档。

## 练习脚本运行补测

- 新增能力：Web UI 在练习任务旁显示“运行”按钮，可从浏览器触发本地白名单脚本；自测 / 验收任务保留手动终端与记录入口。
- 安全策略：服务端不接收任意命令，只按 `rounds_data.js` 中的任务 ID 反查脚本；脚本路径必须匹配 `rounds/round_XX/weekN|final/(exercises|comprehensive_exercise).sh|py`；工作目录固定为 `~/cli-lab/roundN`；运行超时为 20 秒。
- 记录策略：运行成功、失败或超时都会追加 `run_exercise` 动作事件，记录脚本路径、沙盒路径、返回码、耗时与输出摘要。
- 用户理解：点击运行前有浏览器确认框，说明脚本路径、沙盒目录和可能写入动作记录；运行后弹出输出面板。
- API 验证：`r07-w1-ex1` 对应 `rounds/round_07/week1/exercises.py` 可运行成功，输出包含 `工作目录` 与 `TXT 行数`；测试事件已恢复清理。

## 浏览器练习终端补测

- 新增能力：Web UI 新增“练习终端”卡片，用户可在浏览器内输入命令并看到输出，工作目录映射到本机 `~/cli-lab` 沙盒。
- 安全策略：`cd` 由后端解析并限制在 `~/cli-lab` 内；普通命令使用白名单；危险命令、远程命令、网络命令、仓库外绝对路径、`..` 路径和输入重定向会被拦截；命令超时为 10 秒。
- 记录策略：命令历史写入 `records/terminal/commands.jsonl`，不混入任务完成事件；任务是否完成仍由“完成 / 记录”决定。
- 用户理解：页面说明终端只映射沙盒，不是无限制系统终端；提供“回到 ~/cli-lab”和“清屏”按钮。
- API 验证：`pwd` 返回 `/Users/alalapi/cli-lab`；`cd codex-ui-cd-test` 后 `pwd` 返回沙盒子目录；`cat /etc/passwd` 返回 400 并显示 `terminal_command_blocked`。
- UI 验证：桌面端真实页面存在“练习终端”卡片和输入框；输入 `pwd` 后输出 `/Users/alalapi/cli-lab`；输入 `cat /etc/passwd` 后输出区显示 `terminal_command_blocked`；页面无整页横向溢出。
- 存档验证：临时终端命令后创建测试存档，摘要包含 `terminal_command_count: 1`；测试存档和测试终端历史已清理。
- 工具备注：浏览器控制插件在接受运行确认框后出现控制会话超时，但服务端日志显示 `/api/tasks/r07-w1-ex1/run` 已 200 返回；后续用 API 与页面状态检查完成验证。

## Round 01 内容填充与终端映射补测

- before 问题：Round 01 任务标题仍是“练习1 / 练习2 / 练习3”，用户无法从 UI 判断每个练习要做什么。
- before 问题：Round 01 的 notes 过短，缺少“在 Web UI 中怎么完成”的步骤说明。
- before 问题：Round 01 脚本包含 `read` 等待，会卡住浏览器一键运行；并且会在回车后连带标记自测、小抄和验收，不符合“用户确认后再记录”的原则。
- before 问题：Round 01 需要练习 `rm`，但浏览器终端原先全量拦截 `rm`，导致用户无法只通过 Web UI 完成删除测试文件练习。
- before 问题：Round 01 需要练习 `less` / `man`，但浏览器终端白名单缺少它们，且旧文案把浏览器捕获输出误写成真实分页交互。
- 修复：Round 01 的任务标题已改为“路径切换实验”“创建 / 复制 / 改名 / 删除”“查看文本与查帮助”“迷你文件整理实验室”等动作标题。
- 修复：Week 1–3 notes 已补齐 Web UI 操作路径、手敲命令、自测标准和安全边界。
- 修复：Round 01 脚本已改为非交互运行，只自动记录脚本实际完成的练习任务；自测、小抄和验收仍需用户手动完成。
- 修复：浏览器终端允许沙盒内普通 `rm <file>`，继续拦截 `rm -rf`、`rm *`、`rm ~/x`、命令串联符等危险形式。
- 修复：浏览器终端允许 `less` / `man`，并通过 `PAGER=cat` / `MANPAGER=cat` 在页面中显示捕获输出；Week 3 文案改为说明真实终端中才需要按 `q`。
- UI 验证：真实页面可展开 Round 01，清晰任务标题全部可见；Week 1 notes 可在弹窗中打开，包含 Web UI 步骤、命令块和自测说明；桌面端无横向溢出。
- API / 函数验证：`POST /api/tasks/r01-w2-ex2/run` 返回成功，输出包含“再手动标记 r01-w2-self”；`rm round1_api_rm_test/delete_me.txt` 成功；`less` / `man` 可返回捕获输出；`rm -rf round1_api_rm_test`、`rm *`、`rm ~/x`、`ls; pwd`、`man -P cat ls`、`less +...`、`less -...`、`sh -c`、`bash -c` 均返回 `terminal_command_blocked`。
- 清理：本轮 API/UI 测试产生的进度、动作、反馈和终端历史已从测试前快照恢复。
- 工具备注：应用内浏览器控制在本轮点击运行确认框时再次出现控制会话超时，服务端日志显示该次 UI 点击未完成 POST；因此运行链路使用同一 Web UI 后端 API 补测。

## Round 02 内容填充与任务绑定终端补测

- Figma 文件：<https://www.figma.com/design/gmSFWf3hylozNlXIlHIJAR>
- 设计调整：将“任务列表”和“浏览器映射终端”设计为同一工作台；终端区包含当前任务、工作目录、允许命令、快捷命令和控制台。
- before 问题：Round 02 仍偏骨架，notes 缺少 Web UI 操作路径，用户不知道如何只靠页面完成重定向、管道、脚本参数和本地 Git 练习。
- before 问题：Round 02 脚本包含 `read` 等待，并会连带标记自测、小抄和验收，容易把“用户理解”误写成“系统已完成”。
- before 问题：`.sh` 自测任务会显示“运行”，用户可能误以为点击脚本即可完成自测。
- before 问题：浏览器终端在页面底部，但没有绑定具体任务，也不会把命令历史关联到任务。
- 修复：Round 02 notes 和 final 小抄补齐 Web UI 学习路径、手敲命令、自测标准和本地 Git 边界。
- 修复：Round 02 脚本改为非交互运行，只自动记录脚本实际完成的练习任务；自测、小抄和验收仍由用户手动完成并记录。
- 修复：前端“运行”按钮仅对 `exercise` 类型显示；后端 `/api/tasks/<id>/run` 也拒绝非 `exercise`，返回 `task_not_runnable`。
- 修复：工程实操练习 / 自测 / 产出任务新增“终端”按钮；点击后自动绑定当前任务并切换到对应 `~/cli-lab/roundN`。
- 修复：终端命令历史新增 `task_id` 字段，用于回看命令属于哪个学习任务，但命令执行本身不等同于任务完成。
- API 验证：`/api/terminal?cwd=~/round2` 返回 `~/round2`；执行 `pwd` 成功，日志写入 `task_id=r02-w1-ex1`；`POST /api/tasks/r02-w1-self/run` 返回 `task_not_runnable`。
- UI 验证：真实 Chrome 页面可展开 Round 02；练习任务显示“运行 / 终端 / 记录 / 完成”；点击“终端”后终端当前任务显示“练习：覆盖与追加”，工作目录显示 `~/round2`；UI 输入 `pwd` 输出 `/Users/alalapi/cli-lab/round2`。
- 静态语义验证：脚本型 `exercise` 任务共 101 个，脚本型非 `exercise` 任务共 66 个；运行按钮谓词为 `task.type === "exercise"`。
- 清理：本轮 API/UI 测试产生的进度、动作、反馈和终端历史已从测试前快照恢复。

## Round 03 内容填充与 Python 练习补测

- before 问题：Round 03 仍偏最小骨架，notes 缺少“在 Web UI 中如何创建、运行、解释 Python 脚本”的步骤。
- before 问题：Round 03 任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断每个任务的实际产出。
- before 问题：Round 03 脚本会等待回车，并可能连带标记自测、小抄和验收，不适合浏览器一键运行。
- before 问题：`progress.html?round03=1` 这类直达链接不会选中 Round 03，用户从报告或任务链接进入后仍需要自己找 Round。
- 修复：Round 03 README、Week 1–3 notes、final 小抄已补齐 Python 基础、list/dict、函数拆分、复杂度直觉、自测命令和验收自问。
- 修复：Round 03 脚本改为非交互运行，只自动记录脚本实际完成的练习任务；自测、小抄和验收仍由用户手动完成并记录。
- 修复：Round 03 UI 任务标题改为“运行第一个 Python 小程序”“统计标签出现次数”“观察线性与平方级增长”等动作标题。
- 修复：`progress.html` 支持 `?round=round_03`、`?round03=1` 等直达 Round 参数。
- API 验证：`r03-w1-ex1`、`r03-w2-ex2`、`r03-w3-ex3`、`r03-fin-comp` 均可运行成功；`r03-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`~/round3` 可作为映射目录；终端能在任务 `r03-w1-self` 下写入并运行 Python 文件；`python3 -c` 仍被拦截。
- UI 验证：真实浏览器打开 `progress.html?round=round_03` 后直接选中 Round 03；自测任务不显示“运行”但显示“终端”；点击后当前任务为“自测：自己写 square.py”，工作目录为 `~/round3`；输入 `pwd` 输出 `/Users/alalapi/cli-lab/round3`。
- 移动端验证：390px 宽度无整页横向溢出。
- 清理：本轮 API/UI 测试产生的进度、动作、反馈和终端历史已从测试前快照恢复。
- 工具备注：应用内浏览器插件本轮打开本地页时出现控制超时；已使用本机 Playwright 打开同一 Web UI 完成真实渲染与点击验证。

## Round 04 内容填充与核心数据结构补测

- before 问题：Round 04 仍是最小骨架，notes 只列目标和自查，缺少 Web UI 学习路径和自测命令。
- before 问题：Round 04 任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断要练 list、stack/queue 还是 dict/set。
- before 问题：Round 04 脚本会等待回车，并连带标记自测、小抄和验收，不适合浏览器一键运行。
- 修复：Round 04 README、Week 1–3 notes、final 小抄已补齐 list、stack/queue、dict/set、deque 的场景直觉、自测命令和验收自问。
- 修复：Round 04 脚本改为非交互运行，只自动记录脚本实际完成的练习任务；自测、小抄和验收仍由用户手动完成并记录。
- 修复：Round 04 UI 任务标题改为“list 遍历、过滤与统计”“stack 与 queue 出入顺序”“dict 计数与 set 去重”等动作标题。
- API 验证：`r04-w1-ex1`、`r04-w2-ex2`、`r04-w3-ex3`、`r04-fin-comp` 均可运行成功；`r04-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`~/round4` 可作为映射目录；终端能在任务 `r04-w1-self` 下写入并运行 Python 文件；`python3 -c` 仍被拦截。
- UI 验证：真实浏览器打开 `progress.html?round=round_04` 后直接选中 Round 04；自测任务不显示“运行”但显示“终端”；点击后当前任务为“自测：自己写 scores.py”，工作目录为 `~/round4`；输入 `pwd` 输出 `/Users/alalapi/cli-lab/round4`。
- 移动端验证：390px 宽度无整页横向溢出。
- 清理：本轮 API/UI 测试产生的进度、动作、反馈和终端历史已从测试前快照恢复。
- 工具备注：应用内浏览器插件本轮打开本地页时出现控制超时；已使用本机 Playwright 打开同一 Web UI 完成真实渲染与点击验证。

## Round 05 内容填充与算法模式补测

- before 问题：Round 05 仍是最小骨架，notes 只列目标和自查，缺少 Web UI 学习路径和算法模式触发条件。
- before 问题：Round 05 任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断要练二分、图搜索、回溯、贪心还是 DP。
- before 问题：Round 05 脚本会等待回车，并连带标记自测、小抄和验收，不适合浏览器一键运行。
- 修复：Round 05 README、Week 1–3 notes、final 小抄已补齐二分、滑动窗口、双指针、DFS/BFS、回溯、贪心、DP 的场景直觉、自测命令和验收自问。
- 修复：Round 05 脚本改为非交互运行，只自动记录脚本实际完成的练习任务；自测、小抄和验收仍由用户手动完成并记录。
- 修复：Round 05 UI 任务标题改为“二分查找与滑动窗口”“DFS、BFS 与回溯最小例子”“贪心选择与 DP 爬楼梯”等动作标题。
- API 验证：`r05-w1-ex1`、`r05-w2-ex2`、`r05-w3-ex3`、`r05-fin-comp` 均可运行成功；`r05-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`~/round5` 可作为映射目录；终端能在任务 `r05-w1-self` 下写入并运行 Python 文件；`python3 -c` 仍被拦截。
- UI 验证：真实浏览器打开 `progress.html?round=round_05` 后直接选中 Round 05；自测任务不显示“运行”但显示“终端”；点击后当前任务为“自测：自己写 two_sum_sorted.py”，工作目录为 `~/round5`；输入 `pwd` 输出 `/Users/alalapi/cli-lab/round5`。
- 移动端验证：390px 宽度无整页横向溢出。
- 清理：本轮 API/UI 测试产生的进度、动作、反馈和终端历史已从测试前快照恢复。
- 工具备注：应用内浏览器插件本轮打开本地页时出现控制超时；已使用本机 Playwright 打开同一 Web UI 完成真实渲染与点击验证。

## 文档阅读器外部链接补测

- before 问题：阅读器支持裸 URL / 尖括号 URL，但 `[标题](https://...)` 这种 Markdown 主流外链仍显示为普通文本，用户无法从 Web UI 直接跳转外部资料。
- 修复：`progress_ui.js` 的 `inlineMarkdown()` 支持 `[标题](https://...)`，渲染为新标签页外链，并带 `noreferrer noopener`。
- UI 验证：真实浏览器打开 `progress.html?round=round_05`，在阅读器中打开 `round_05.md`；`Hello Algo` 链接可被定位，文本正确，`target="_blank"`，`rel` 包含 `noreferrer noopener`；页面中共识别到 5 个 `https://` 外部链接。
- 清理：本轮只读取页面和检查链接属性，未写入学习记录。

## Round 06 内容填充与 Linux 自动化补测

- before 问题：Round 06 仍是最小骨架，notes 只列目标和自查，缺少 Web UI 学习路径和安全边界。
- before 问题：Round 06 任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断要练 find/xargs、进程查看还是远程排练。
- before 问题：Round 06 脚本会等待回车，并连带标记自测、小抄和验收，不适合浏览器一键运行。
- before 问题：本轮涉及 `ssh`、`scp`、`rsync`、`crontab` 等真实远程或系统级命令，若不说明边界，用户容易误以为 Web UI 终端应该直接执行。
- 修复：Round 06 README、Week 1–3 notes、final 小抄已补齐 find/xargs/sed/awk、进程查看、长任务保活、远程命令排练、cron 表达式和验收自问。
- 修复：Round 06 脚本改为非交互运行，只自动记录脚本实际完成的练习任务；自测、小抄和验收仍由用户手动完成并记录。
- 修复：Round 06 UI 任务标题改为“find/xargs/sed/awk 日志清洗”“进程查看与长任务日志”“远程同步与 cron 命令排练”等动作标题。
- 修复：浏览器终端允许只读 `ps` 进程查看，继续拦截真实 `ssh`、`scp`、`rsync`、网络命令和高风险操作。
- API 验证：`r06-w1-ex1`、`r06-w2-ex2`、`r06-w3-ex3`、`r06-fin-comp` 均可运行成功；`r06-w2-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`~/round6` 可作为映射目录；终端能在任务 `r06-w2-self` 下执行 `ps aux | grep python | head -1`；`ssh user@host` 返回 `terminal_command_blocked`。
- UI 验证：真实浏览器打开 `progress.html?round=round_06` 后直接选中 Round 06；自测任务不显示“运行”但显示“终端”；点击后当前任务为“自测：自己写 worker_monitor.sh”，工作目录为 `~/round6`。
- 外链验证：在阅读器中打开 `round_06.md`，MIT Missing Semester 外链可被定位，`target="_blank"`，`rel` 包含 `noreferrer noopener`。
- 移动端验证：390px 宽度无整页横向溢出。
- 清理：本轮 API/UI 测试产生的进度、动作、反馈和终端历史已从测试前快照恢复。

## Round 07 内容填充与 AI 数据预处理补测

- before 问题：Round 07 仍是最小骨架，notes 只列目标和自查，缺少 Web UI 学习路径和浏览器终端自测命令。
- before 问题：Week 2 与 Final 脚本默认要求 `--input`，在 Web UI 一键运行时会直接失败。
- before 问题：Round 07 任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断要练多格式读取、参数日志还是整合工具。
- 修复：Round 07 README、Week 1–3 notes、final 小抄已补齐 pathlib、多格式读写、argparse、logging、去重统计、函数拆分、Web UI 完成路径和验收自问。
- 修复：Round 07 Python 脚本改为非交互运行，自动生成演示输入、输出结果、日志和下一步提示，只自动记录脚本实际完成的练习任务；自测、小抄和验收仍由用户手动完成并记录。
- 修复：Round 07 UI 任务标题改为“读取四种小数据格式”“命令行参数与日志输出”“整合 mini ai_prep_tool”等动作标题。
- API 验证：`r07-w1-ex1`、`r07-w2-ex2`、`r07-w3-ex3`、`r07-fin-comp` 均可运行成功；`r07-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`~/round7` 可作为映射目录；终端能在任务 `r07-w1-self` 下写入并运行 `read_formats.py`；`python3 -c` 返回 `terminal_command_blocked`。
- UI 验证：真实 Chrome 打开 `progress.html?round=round_07` 后直接选中 Round 07；`r07-w1-ex1` 显示“运行”，`r07-w1-self` 不显示“运行”但显示“终端”；点击后当前任务为“自测：自己写 read_formats.py”，工作目录为 `~/round7`。
- 外链验证：在阅读器中打开 `round_07.md`，Python argparse 官方链接可被定位，`target="_blank"`，`rel` 包含 `noreferrer noopener`。
- 移动端验证：390px 宽度无整页横向溢出。
- 清理：本轮 API/UI 测试产生的进度、动作、反馈和终端历史已从测试前快照恢复。
- 工具备注：应用内浏览器插件本轮打开本地页时控制超时；已使用本机 Google Chrome + Playwright 打开同一 Web UI 完成真实渲染、点击、终端和截图验证。

## Round 08 内容填充与升级路线补测

- before 问题：Round 08 仍是最小骨架，notes 只列目标和自查，缺少 Web UI 学习路径和浏览器终端自测命令。
- before 问题：Round 08 脚本未接入自动记录，Web UI “运行”后不会推进对应练习状态。
- before 问题：Round 08 任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断要练项目收口、sqlite3 还是服务化接口。
- 修复：Round 08 README、Week 1–3 notes、final 小抄已补齐项目收口、最小测试、sqlite3 运行历史、服务化接口形状、Web UI 完成路径和验收自问。
- 修复：Round 08 Python 脚本改为非交互运行，自动生成项目骨架、测试报告、SQLite 数据库、API 合同和收口摘要，只自动记录脚本实际完成的练习任务；自测、小抄和验收仍由用户手动完成并记录。
- 修复：Round 08 UI 任务标题改为“整理 ai_prep_tool 并运行最小测试”“创建 runs 表并写入运行历史”“设计 health/run/runs 响应”等动作标题。
- API 验证：`r08-w1-ex1`、`r08-w2-ex2`、`r08-w3-ex3`、`r08-fin-comp` 均可运行成功；`r08-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`~/round8` 可作为映射目录；终端能在任务 `r08-w3-self` 下写入并运行 `api_contract.py`；`pip install fastapi` 返回 `terminal_command_not_allowed:pip`。
- UI 验证：真实 Chrome 打开 `progress.html?round=round_08` 后直接选中 Round 08；`r08-w1-ex1` 显示“运行”，`r08-w1-self` 不显示“运行”但显示“终端”；点击后当前任务为“自测：自己写 test_basic.py”，工作目录为 `~/round8`。
- 外链验证：在阅读器中打开 `round_08.md`，pytest 官方链接可被定位，`target="_blank"`，`rel` 包含 `noreferrer noopener`。
- 移动端验证：390px 宽度无整页横向溢出。
- 清理：本轮 API/UI 测试产生的进度、动作、反馈和终端历史已从测试前快照恢复。

## Round 09 内容填充与仓库测试补测

- before 问题：Round 09 仍是最小骨架，notes 只列目标和自查，缺少 Web UI 学习路径和浏览器终端自测命令。
- before 问题：Round 09 脚本只是生成少量文件或打印建议命令，没有形成 Web UI 一键运行后的可检查产物与自动记录。
- before 问题：Round 09 任务标题仍偏泛化，用户无法判断要练 README/.gitignore、本地 Git 分支还是纯函数测试。
- 修复：Round 09 README、Week 1–3 notes、final 小抄已补齐仓库结构、README/.gitignore、本地 Git 分支、纯函数测试、Web UI 完成路径和验收自问。
- 修复：Round 09 Python 脚本改为非交互运行，自动生成规范化项目、本地 Git 工作流沙盒、测试样例和收口摘要，只自动记录脚本实际完成的练习任务；自测、小抄和验收仍由用户手动完成并记录。
- 修复：Round 09 UI 任务标题改为“整理项目结构与基础文档”“本地 Git 分支提交与合并”“拆出纯函数并运行测试”等动作标题。
- 边界：本轮不安装 pytest，不执行 GitHub remote 操作；本地 Git 练习只在 `~/cli-lab/round9` 沙盒完成。
- API 验证：`r09-w1-ex1`、`r09-w2-ex2`、`r09-w3-ex3`、`r09-fin-comp` 均可运行成功；`r09-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`~/round9` 可作为映射目录；终端 API 能在任务 `r09-w2-self` 下完成本地 `git init`、`git commit`、`git log`；`git push origin main` 返回 `terminal_command_blocked`。
- UI 验证：真实 Chrome 打开 `progress.html?round=round_09` 后直接选中 Round 09；`r09-w1-ex1` 显示“运行”，`r09-w1-self` 不显示“运行”但显示“终端”；点击后工作目录为 `~/round9`，输入 `pwd` 输出 `/Users/alalapi/cli-lab/round9`。
- 文档阅读验证：Week 1 notes 可在阅读器中直接阅读，包含 Web UI 学习路径；`round_09.md` 中 pytest 官方链接可被定位，`target="_blank"`，`rel` 包含 `noreferrer noopener`。
- 移动端验证：390px 宽度无整页横向溢出。
- 清理：本轮 API/UI 测试产生的进度、动作、反馈和终端历史已从测试前快照恢复。

## Round 10 内容填充与 Python 工程化补测

- before 问题：Round 10 仍是最小骨架，notes 只列目标和自查，缺少 Web UI 学习路径和浏览器终端自测命令。
- before 问题：Round 10 脚本只是生成骨架或跑内存自检，没有形成 Web UI 一键运行后的可检查产物与自动记录。
- before 问题：Round 10 任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断要练 CLI 拆分、配置日志还是错误处理。
- 修复：Round 10 README、Week 1–3 notes、final 小抄已补齐模块拆分、config.ini、logging、可控错误、入口规范、Web UI 完成路径和验收自问。
- 修复：Round 10 Python 脚本改为非交互运行，自动生成工程化沙盒项目、配置、日志、错误路径报告和收口摘要，只自动记录脚本实际完成的练习任务；自测、小抄和验收仍由用户手动完成并记录。
- 修复：Round 10 UI 任务标题改为“拆出 cli.py / core.py / io_utils.py”“读取配置并写入日志”“处理缺失输入并规范入口”等动作标题。
- 边界：本轮不安装第三方依赖，不切换到 `src/` layout，不做打包发布。
- API 验证：`r10-w1-ex1`、`r10-w2-ex2`、`r10-w3-ex3`、`r10-fin-comp` 均可运行成功；`r10-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`~/round10` 可作为映射目录；终端 API 能在任务 `r10-w3-self` 下写入入口脚本并看到返回码 2；`python3 -c` 返回 `terminal_command_blocked`。
- UI 验证：真实 Chrome 打开 `progress.html?round=round_10` 后直接选中 Round 10；`r10-w1-ex1` 显示“运行”，`r10-w1-self` 不显示“运行”但显示“终端”；点击后工作目录为 `~/round10`，输入 `pwd` 输出 `/Users/alalapi/cli-lab/round10`。
- 文档阅读验证：Week 1 notes 可在阅读器中直接阅读，包含 Web UI 学习路径；`round_10.md` 中 Python argparse 官方链接可被定位，`target="_blank"`，`rel` 包含 `noreferrer noopener`。
- 移动端验证：390px 宽度无整页横向溢出。
- 清理：本轮 API/UI 测试产生的进度、动作、反馈和终端历史已从测试前快照恢复。

## Round 11 内容填充与 SQLite 持久化补测

- before 问题：Round 11 仍是最小骨架，notes 只列目标和自查，缺少 Web UI 学习路径和浏览器终端自测命令。
- before 问题：Round 11 脚本只生成局部文件或依赖前一周产物，没有形成 Web UI 一键运行后的稳定可检查产物与自动记录。
- before 问题：Round 11 任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断要练 `runs` 表、`db.py` 查询封装还是主工具运行历史。
- 修复：Round 11 README、Week 1–3 notes、final 小抄已补齐 SQLite 建表、参数化插入、查询封装、主工具持久化、Web UI 完成路径和验收自问。
- 修复：Round 11 Python 脚本改为非交互运行，自动生成 `runs.db`、`db.py`、`ai_prep_tool.py`、查询报告和收口摘要，只自动记录脚本实际完成的练习任务；自测、小抄和验收仍由用户手动完成并记录。
- 修复：Round 11 UI 任务标题改为“创建 runs.db 与 runs 表”“封装 db.py 并查询历史”“ai_prep_tool 自动写运行历史”等动作标题。
- 边界：本轮只使用 Python 标准库 `sqlite3`，练习数据库只写入 `~/cli-lab/round11` 沙盒，不提交 `.db` 文件。
- API 验证：`r11-w1-ex1`、`r11-w2-ex2`、`r11-w3-ex3`、`r11-fin-comp` 均可运行成功；`r11-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`~/round11` 可作为映射目录；终端 API 能在任务 `r11-w1-self` 下写入并运行 SQLite 脚本；`python3 -c` 返回 `terminal_command_blocked`。
- UI 验证：真实 Chrome 打开 `progress.html?round=round_11` 后直接选中 Round 11；`r11-w1-ex1` 显示“运行”，`r11-w1-self` 不显示“运行”但显示“终端”；点击后工作目录为 `~/round11`，输入 `pwd` 输出 `/Users/alalapi/cli-lab/round11`。
- 文档阅读验证：Week 1 notes 可在阅读器中直接阅读，包含 Web UI 学习路径；`round_11.md` 中 Python sqlite3 官方链接可被定位，`target="_blank"`，`rel` 包含 `noreferrer noopener`。
- 移动端验证：390px 宽度无整页横向溢出。
- 清理：本轮 API/UI 测试产生的进度、动作、反馈和终端历史已从测试前快照恢复。

## Round 16 内容填充与 API 数据层补测

- before 问题：Round 16 仍是最小骨架，notes 只列目标和自查，用户不知道如何只通过 Web UI 完成 API 接真实逻辑、SQLite 记录、上传、错误处理和 API 测试。
- before 问题：Round 16 三周脚本只写 marker 文件，点击“运行”不会生成可检查的 API/Data Layer 产物。
- before 问题：Round 16 UI 任务标题仍是“基础练习 / 练习1 / 练习2 / 练习3”，用户无法判断每个任务实际要做什么。
- 修复：Round 16 README、Week 1–3 notes、final 小抄已补齐 Web UI 学习路径、自动练习产物路径、浏览器终端自测命令、官方外链和验收标准。
- 修复：Round 16 Python 脚本改为非交互运行，自动生成 FastAPI 形状代码、SQLite 数据层、上传入口、错误合同、TestClient 示例、静态检查报告和最终项目包；只自动记录脚本实际完成的练习任务。
- 修复：`scripts/build_rounds_data.py` / `rounds_data.js` 为 Round 16 输出清晰任务标题，并将难度同步为 `⭐⭐⭐⭐☆`。
- 边界：本轮不在 Web UI 中安装 FastAPI / uvicorn，不启动长期服务；自动练习生成真实代码形状，但用 Python 标准库做静态合同验证。
- API 验证：`r16-w1-ex1`、`r16-w2-ex2`、`r16-w3-ex3`、`r16-fin-comp` 均可通过 `/api/tasks/<id>/run` 运行成功；`r16-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`/api/terminal?cwd=~/round16` 返回 `~/round16`；终端 API 可绑定 `r16-w1-self` 并执行 `pwd` / 手写 `smoke.py`；`curl https://example.com` 返回 `terminal_command_blocked`。
- UI 验证：真实 Chrome 打开 `progress.html?round=round_16` 后可选中 Round 16；12 个任务、4 个运行按钮、终端按钮均可见；Week 1 notes 可在阅读器中直接阅读；官方 FastAPI / Python sqlite3 外链可定位并可跳转；点击“运行”有确认框，确认后运行结果弹窗显示“运行成功”和 `static_check_report.json`；终端输入 `pwd` 输出 `/Users/alalapi/cli-lab/round16`。
- 移动端验证：390px 宽度无整页横向溢出。
- 截图：`/tmp/round16_web_ui_current.png`（恢复真实记录后的 Round 16 页面，显示 0/12 完成）；移动端截图为 `/tmp/round16_mobile.png`。
- 清理：本轮 API/UI 测试产生的进度、动作、反馈和终端历史已从测试前快照恢复。
- 工具备注：应用内浏览器可验证资料弹窗和外链跳转，但运行按钮点击在确认框附近出现控制超时；已使用本机 Google Chrome + Playwright 打开同一 Web UI 完成真实渲染、点击、运行、终端和截图验证。

## Round 12 内容填充与自动化流水线补测

- before 问题：Round 12 仍是最小骨架，notes 只列目标和自查，缺少 Web UI 学习路径和浏览器终端自测命令。
- before 问题：Round 12 脚本只生成局部文件或做缺失检查，没有形成 Web UI 一键运行后的稳定可检查产物与自动记录。
- before 问题：Round 12 任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断要练批量扫描、subprocess 归档还是日志轮转。
- before 问题：阅读弹窗不响应 `Escape`，真实浏览器测试中遮住后续“终端”按钮，切换任务不够顺手。
- 修复：Round 12 README、Week 1–3 notes、final 小抄已补齐批处理、失败记录、subprocess、归档、日志轮转、cron/nohup/tmux 排练、Web UI 完成路径和验收自问。
- 修复：Round 12 Python 脚本改为非交互运行，自动生成批处理沙盒、zip 归档、轮转日志、`run_batch.sh`、cron/nohup/tmux 示例和收口摘要，只自动记录脚本实际完成的练习任务；自测、小抄和验收仍由用户手动完成并记录。
- 修复：Round 12 UI 任务标题改为“批量扫描并记录失败项”“运行 worker 并归档输出”“生成 run_batch.sh 与轮转日志”等动作标题。
- 修复：Week 1 自测命令改为 `Path.joinpath()` 写法，避免浏览器终端安全规则拦截复杂斜杠表达式。
- 修复：`progress_ui.js` 支持 `Escape` 关闭阅读弹窗。
- 边界：本轮只生成 cron/nohup/tmux 示例文本，不写系统 crontab，不启动真实后台任务。
- API 验证：`r12-w1-ex1`、`r12-w2-ex2`、`r12-w3-ex3`、`r12-fin-comp` 均可运行成功；`r12-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`~/round12` 可作为映射目录；终端 API 能在任务 `r12-w1-self` 下逐行写入并运行 `scan_demo.py`；`crontab -l` 返回 `terminal_command_not_allowed:crontab`。
- UI 验证：真实 Chrome 打开 `progress.html?round=round_12` 后直接选中 Round 12；`r12-w1-ex1` 显示“运行”，`r12-w1-self` 不显示“运行”但显示“终端”；点击后工作目录为 `~/round12`，输入 `pwd` 输出 `/Users/alalapi/cli-lab/round12`。
- 文档阅读验证：Week 1 notes 可在阅读器中直接阅读，包含 Web UI 学习路径和 `joinpath` 自测写法；阅读弹窗可用 `Escape` 关闭；`round_12.md` 中 Python pathlib 官方链接可被定位，`target="_blank"`，`rel` 包含 `noreferrer noopener`。
- 移动端验证：390px 宽度无整页横向溢出。
- 清理：本轮 API/UI 测试产生的进度、动作、反馈和终端历史已从测试前快照恢复。

## Round 13 内容填充与环境复现发布补测

- before 问题：Round 13 仍是最小骨架，notes 只列目标和自查，缺少 Web UI 学习路径和浏览器终端自测命令。
- before 问题：Round 13 脚本只写 marker 文件，没有形成 venv、requirements、pyproject、Dockerfile、发布检查报告或交付包等可检查产物。
- before 问题：Round 13 任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断要练 venv、项目配置还是 Dockerfile。
- 修复：Round 13 README、Week 1–3 notes、final 小抄已补齐 venv、requirements、pyproject.toml、`.env.example`、Dockerfile、`.dockerignore`、发布前自检、Web UI 完成路径和验收自问。
- 修复：Round 13 Python 脚本改为非交互运行，自动生成演示虚拟环境、依赖清单、项目配置、Dockerfile、发布检查报告、handoff manifest 和 zip 交付包，只自动记录脚本实际完成的练习任务；自测、小抄和验收仍由用户手动完成并记录。
- 修复：Round 13 UI 任务标题改为“生成 venv 结构与 requirements”“生成 pyproject 与配置样例”“生成 Dockerfile 与发布检查”等动作标题。
- 边界：本轮不联网安装依赖，不执行 `docker build` / `docker run`；Dockerfile 只生成和检查。
- API 验证：`r13-w1-ex1`、`r13-w2-ex2`、`r13-w3-ex3`、`r13-fin-comp` 均可运行成功；`r13-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`~/round13` 可作为映射目录；终端 API 能在任务 `r13-w1-self` 下创建无 pip 的 `.venv_self` 并读取 `pyvenv.cfg`；`docker build -t demo .` 返回 `terminal_command_not_allowed:docker`。
- UI 验证：真实 Chrome 打开 `progress.html?round=round_13` 后直接选中 Round 13；`r13-w1-ex1` 显示“运行”，`r13-w1-self` 不显示“运行”但显示“终端”；点击后工作目录为 `~/round13`，输入 `pwd` 输出 `/Users/alalapi/cli-lab/round13`。
- 文档阅读验证：Week 1 notes 可在阅读器中直接阅读，包含 Web UI 学习路径；阅读弹窗和运行结果弹窗均可用 `Escape` 关闭；`round_13.md` 中 Python venv 官方链接可被定位，`target="_blank"`，`rel` 包含 `noreferrer noopener`。
- 移动端验证：390px 宽度无整页横向溢出。
- 清理：本轮 API/UI 测试产生的进度、动作、反馈和终端历史已从测试前快照恢复。
- 工具备注：应用内浏览器插件本轮打开本地页时控制超时；已使用本机 Google Chrome + Playwright 打开同一 Web UI 完成真实渲染、点击、终端和截图验证。

## Round 14 内容填充与 HTTP API 设计补测

- before 问题：Round 14 仍是最小骨架，notes 只列目标和自查，缺少 Web UI 学习路径和浏览器终端自测命令。
- before 问题：Round 14 脚本只写 marker 文件，没有形成方法矩阵、状态码矩阵、JSON 合同、mock API、路由测试或客户端演示等可检查产物。
- before 问题：Round 14 任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断要练 HTTP 方法、JSON 合同还是 REST 路由。
- 修复：Round 14 README、Week 1–3 notes、final 小抄已补齐 HTTP 方法与状态码、JSON 请求/响应、错误形状、REST 路由、Web UI 完成路径和验收自问。
- 修复：Round 14 Python 脚本改为非交互运行，自动生成 `method_matrix.json`、`status_matrix.json`、`api_contract.json`、`mock_api.py`、`route_tests.py`、`client_demo.py` 和预检报告，只自动记录脚本实际完成的练习任务；自测、小抄和验收仍由用户手动完成并记录。
- 修复：Round 14 UI 任务标题改为“生成 HTTP 方法与状态码矩阵”“生成 JSON API 合同”“生成 REST 路由草图与 mock API”等动作标题。
- 边界：本轮不使用 `curl` 访问真实网络，不安装 FastAPI / uvicorn，不启动长期服务；服务端框架留到 Round 15。
- API 验证：`r14-w1-ex1`、`r14-w2-ex2`、`r14-w3-ex3`、`r14-fin-comp` 均可运行成功；`r14-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`~/round14` 可作为映射目录；终端 API 能在任务 `r14-w2-self` 下写入并校验 `request.json`；`curl https://example.com` 返回 `terminal_command_blocked`。
- UI 验证：真实 Chrome 打开 `progress.html?round=round_14` 后直接选中 Round 14；`r14-w2-ex2` 显示“运行”，`r14-w2-self` 不显示“运行”但显示“终端”；点击后工作目录为 `~/round14`，输入 `pwd` 输出 `/Users/alalapi/cli-lab/round14`。
- 文档阅读验证：Week 1 notes 可在阅读器中直接阅读，包含 Web UI 学习路径；阅读弹窗可用 `Escape` 关闭；运行结果弹窗展示 `endpoint_count:` 和 `sample_count:`；`round_14.md` 中 MDN HTTP overview 链接可被定位，`target="_blank"`，`rel` 包含 `noreferrer noopener`。
- 移动端验证：390px 宽度无整页横向溢出。
- 清理：本轮 API/UI 测试产生的进度、动作、反馈和终端历史已从测试前快照恢复。
- 工具备注：应用内浏览器插件本轮 DOM 快照与点击能力出现兼容/超时问题；已使用本机 Google Chrome + Playwright 打开同一 Web UI 完成真实渲染、点击、终端和截图验证。

## Round 15 内容填充与 FastAPI 基础补测

- before 问题：Round 15 仍是最小骨架，notes 只列目标和自查，缺少 Web UI 学习路径和浏览器终端自测命令。
- before 问题：Round 15 脚本只写 marker 文件，没有形成 FastAPI 入口、路径/查询参数、Pydantic 模型、请求/响应示例或 `/docs` 文档示例等可检查产物。
- before 问题：Round 15 任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断要练应用入口、请求体模型还是文档示例。
- 修复：Round 15 README、Week 1–3 notes、final 小抄已补齐 FastAPI 应用入口、路径参数、查询参数、请求体、Pydantic 模型、示例数据、Web UI 完成路径和验收自问。
- 修复：Round 15 Python 脚本改为非交互运行，自动生成 `app/main.py`、`app/routers/*.py`、`app/schemas.py`、`route_table.json`、样例 JSON、OpenAPI 预览和静态检查报告，只自动记录脚本实际完成的练习任务；自测、小抄和验收仍由用户手动完成并记录。
- 修复：Round 15 UI 任务标题改为“生成 FastAPI 读接口骨架”“生成请求体和响应模型骨架”“生成文档示例与 OpenAPI 预览”等动作标题。
- 边界：本轮不在 Web UI 中安装 FastAPI / uvicorn，不启动长期服务；生成真实 FastAPI 代码形状，并通过 Python 标准库做静态合同验证。
- API 验证：`r15-w1-ex1`、`r15-w2-ex2`、`r15-w3-ex3`、`r15-fin-comp` 均可运行成功；`r15-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`~/round15` 可作为映射目录；终端 API 能在任务 `r15-w2-self` 下写入并校验 `request_api.json`；`pip install fastapi` 返回 `terminal_command_not_allowed:pip`；`uvicorn app.main:app` 返回 `terminal_command_not_allowed:uvicorn`。
- UI 验证：真实 Chrome 打开 `progress.html?round=round_15` 后直接选中 Round 15；`r15-w2-ex2` 显示“运行”，`r15-w2-self` 不显示“运行”但显示“终端”；点击后工作目录为 `~/round15`，输入 `pwd` 输出 `/Users/alalapi/cli-lab/round15`。
- 文档阅读验证：Week 1 notes 可在阅读器中直接阅读，包含 Web UI 学习路径；阅读弹窗可用 `Escape` 关闭；运行结果弹窗展示 `model_count:` 和 `model_check_report.json`；`round_15.md` 中 FastAPI Path Parameters 链接可被定位，`target="_blank"`，`rel` 包含 `noreferrer noopener`。
- 移动端验证：390px 宽度无整页横向溢出。
- 清理：本轮 API/UI 测试产生的进度、动作、反馈和终端历史已从测试前快照恢复。

## 验证命令

```bash
npm run check:mcp
npm run check:cursor-mcp
python3 scripts/build_rounds_data.py
python3 scripts/generate_task_feedback.py
python3 scripts/validate_learning_data.py
python3 scripts/check_protocol_sync.py
python3 -m json.tool progress.json
python3 -m json.tool records/feedback/task_feedback.json
node --check progress_ui.js
python3 -m py_compile scripts/progress_lib.py scripts/progress_server.py scripts/generate_task_feedback.py scripts/mark_done_cli.py scripts/sync_progress_data.py scripts/build_rounds_data.py scripts/check_protocol_sync.py scripts/validate_learning_data.py
python3 -m py_compile rounds/round_11/week1/exercises.py rounds/round_11/week2/exercises.py rounds/round_11/week3/exercises.py rounds/round_11/final/comprehensive_exercise.py
python3 -m py_compile rounds/round_12/week1/exercises.py rounds/round_12/week2/exercises.py rounds/round_12/week3/exercises.py rounds/round_12/final/comprehensive_exercise.py
python3 -m py_compile rounds/round_13/week1/exercises.py rounds/round_13/week2/exercises.py rounds/round_13/week3/exercises.py rounds/round_13/final/comprehensive_exercise.py
python3 -m py_compile rounds/round_14/week1/exercises.py rounds/round_14/week2/exercises.py rounds/round_14/week3/exercises.py rounds/round_14/final/comprehensive_exercise.py
python3 -m py_compile rounds/round_15/week1/exercises.py rounds/round_15/week2/exercises.py rounds/round_15/week3/exercises.py rounds/round_15/final/comprehensive_exercise.py
python3 -m py_compile rounds/round_17/week1/exercises.py rounds/round_17/week2/exercises.py rounds/round_17/week3/exercises.py rounds/round_17/final/comprehensive_exercise.py
python3 -m py_compile rounds/round_18/week1/exercises.py rounds/round_18/week2/exercises.py rounds/round_18/week3/exercises.py rounds/round_18/final/comprehensive_exercise.py
python3 -m py_compile rounds/round_19/week1/exercises.py rounds/round_19/week2/exercises.py rounds/round_19/week3/exercises.py rounds/round_19/final/comprehensive_exercise.py
python3 -m py_compile rounds/round_20/week1/exercises.py rounds/round_20/week2/exercises.py rounds/round_20/week3/exercises.py rounds/round_20/final/comprehensive_exercise.py
python3 scripts/agent_gate.py --verify
git diff --check
```

## 当前结论

核心 Web UI 闭环已成立：用户可以从 Web UI 找到下一条任务，打开资料或脚本，运行受控练习脚本，写入学习记录，完成或撤销任务，并看到记录历史与反馈建议。

仍建议后续继续增强：继续逐轮补齐计划内容质量，并把更多考试主线任务从“阅读骨架”升级为可检查产物。

## Round 17 内容填充与服务化收口补测

- before 问题：Round 17 仍是最小骨架，notes 只列目标和自查，缺少 Web UI 学习路径和浏览器终端自测命令。
- before 问题：Round 17 脚本只写 marker 文件，没有形成 APIRouter 拆分、Settings/logging、auth/CORS、Dockerfile、部署检查或服务合同等可检查产物。
- before 问题：Round 17 任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断要练路由拆分、配置日志还是安全部署。
- before 问题：浏览器终端后端不兼容 `~/cli-lab/round17` 这种用户直觉路径，会错误映射到双层 `cli-lab` 目录。
- before 问题：顶部“今日学习”卡片 sticky，在滚动到 Round 清单时遮挡任务区。
- 修复：Round 17 README、Week 1–3 notes、final 小抄已补齐 APIRouter、Settings、metadata、logging、Bearer auth、CORS、Dockerfile、preflight、Web UI 完成路径和验收自问。
- 修复：Round 17 Python 脚本改为非交互运行，自动生成多文件服务结构、配置日志入口、安全部署检查、最终服务化项目包和静态检查报告，只自动记录脚本实际完成的练习任务。
- 修复：Round 17 UI 任务标题改为“生成 APIRouter 多文件服务结构”“生成配置、元数据与日志入口”“生成认证、CORS 与部署检查”等动作标题，并同步四星难度。
- 修复：终端路径解析同时兼容 `~/round17`、`~/cli-lab/round17` 和沙盒内绝对路径；顶部卡片取消 sticky，避免遮挡 Round 清单。
- 边界：本轮不安装 FastAPI / uvicorn，不启动长期服务，不执行 Docker；生成真实代码形状，并用 Python 标准库做静态合同验证。
- API 验证：`r17-w1-ex1`、`r17-w2-ex2`、`r17-w3-ex3`、`r17-fin-comp` 均可运行成功；`r17-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`~/round17` 与 `~/cli-lab/round17` 均映射到 `~/round17`；终端 API 能在任务 `r17-w1-self` 下执行 `pwd` / 手写 `smoke.py` / `cd ~/round17/week1_auto`；`docker build -t demo .` 返回 `terminal_command_not_allowed:docker`。
- UI 验证：Codex 应用内浏览器打开 `progress.html?round=round_17` 后直接选中 Round 17；12 个任务、4 个运行按钮、9 个终端按钮均可见；Week 1 notes 可在阅读器中直接阅读；点击“运行”有确认框，确认后运行结果弹窗显示“运行成功”和 `static_check_report.json`；终端输入 `pwd` 输出 `/Users/alalapi/cli-lab/round17`。
- 文档阅读验证：Week 1 notes 包含 Web UI 学习路径和浏览器终端自测；FastAPI Bigger Applications 与 Metadata 外链渲染为 `_blank` 新标签，`rel` 包含 `noreferrer noopener`。
- 移动端验证：390px 宽度无整页横向溢出；任务按钮换行后不重叠。
- 截图：`/tmp/round17_web_ui_current.png`（恢复真实记录后的 Round 17 页面，显示 0/12 完成）；阅读弹窗 `/tmp/round17_reading_modal.png`；运行结果 `/tmp/round17_run_result.png`；终端 `/tmp/round17_terminal_ui.png`；移动端 `/tmp/round17_mobile_ui.png`。
- 清理：本轮 API/UI 测试产生的进度、动作、反馈和终端历史已从测试前快照恢复。
- 工具备注：应用内浏览器的 DOM snapshot 接口在本页报运行时兼容错误；本轮改用同一应用内浏览器的只读 DOM evaluate、稳定 CSS selector 点击、确认框处理和截图完成真实页面验证。

## Round 18 内容填充与数值数据分析补测

- before 问题：Round 18 仍是最小骨架，notes 只列目标和自查，缺少 Web UI 学习路径和浏览器终端自测命令。
- before 问题：Round 18 脚本只写 marker 文件，没有形成 NumPy 数组、pandas CSV、数据清洗、统计导出或最终项目包等可检查产物。
- before 问题：Round 18 任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断要练数组、CSV 还是完整分析流水线。
- 修复：Round 18 README、Week 1–3 notes、final 小抄已补齐 NumPy、pandas、CSV、DataFrame、清洗、groupby、导出报告、Web UI 完成路径和验收自问。
- 修复：Round 18 Python 脚本改为非交互运行，自动生成数组示例、CSV 样例、分析流水线、标准库预检、静态检查报告和最终项目包，只自动记录脚本实际完成的练习任务。
- 修复：Round 18 UI 任务标题改为“生成 NumPy 数组、axis 与广播示例”“生成 CSV 读取、筛选与 groupby 示例”“生成读、清洗、统计、导出分析流程”等动作标题，并同步三星难度。
- 修复：Week 3 自测命令避免链式比较里的 `<` 被浏览器终端安全规则误拦截，改为 `score >= 0 and not score > 1` 并通过终端 API 验证。
- 边界：本轮不在 Web UI 中执行 `pip install numpy pandas`；自动练习生成真实代码形状，但用 Python 标准库和 AST 做静态合同验证。
- API 验证：`r18-w1-ex1`、`r18-w2-ex2`、`r18-w3-ex3`、`r18-fin-comp` 均可运行成功；`r18-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`~/round18` 与 `~/cli-lab/round18` 均映射到 `~/round18`；终端 API 能分别运行 Week 1 axis、Week 2 CSV 统计、Week 3 清洗过滤三段手写自测；`pip install numpy pandas` 返回 `terminal_command_not_allowed:pip`。
- UI 验证：Codex 应用内浏览器打开 `progress.html?round=round_18` 后直接选中 Round 18；12 个任务、4 个运行按钮、9 个终端按钮均可见；Week 1 notes 可在阅读器中直接阅读；点击“运行”有确认框，确认后运行结果弹窗显示“运行成功”和 `static_check_report.json`；终端输入 `pwd` 输出 `/Users/alalapi/cli-lab/round18`。
- 文档阅读验证：Week 1 notes 包含 Web UI 学习路径和浏览器终端自测；NumPy quickstart 与 absolute beginners 外链渲染为 `_blank` 新标签，`rel` 包含 `noreferrer noopener`。
- 移动端验证：390px 宽度无整页横向溢出；任务按钮换行后不重叠。
- 截图：`/tmp/round18_web_ui_current.png`（恢复真实记录后的 Round 18 页面，显示 0/12 完成）；阅读弹窗 `/tmp/round18_reading_modal.png`；运行结果 `/tmp/round18_run_result.png`；终端 `/tmp/round18_terminal_ui.png`；移动端 `/tmp/round18_mobile_ui.png`。
- 清理：本轮 API/UI 测试产生的进度、动作、反馈和终端历史已从测试前快照恢复。
- 工具备注：应用内浏览器的 DOM snapshot 接口在本页报运行时兼容错误；本轮改用同一应用内浏览器的只读 DOM evaluate、稳定 CSS selector 点击、确认框处理和截图完成真实页面验证。

## Round 19 内容填充与机器学习最小闭环补测

- before 问题：Round 19 仍是最小骨架，notes 只列目标和自查，缺少 Web UI 学习路径、可直接阅读的知识解释和浏览器终端自测命令。
- before 问题：Round 19 脚本只写 marker 文件，没有形成 X/y、train/test split、指标、过拟合、预处理、Pipeline 或最终项目包等可检查产物。
- before 问题：Round 19 任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断要练切分、指标还是 Pipeline 防泄漏。
- 修复：Round 19 README、Week 1-3 notes、final 小抄已补齐 X/y、fit/predict/score、accuracy/precision/recall/F1、过拟合、预处理、Pipeline、防泄漏、Web UI 完成路径和验收自问。
- 修复：Round 19 Python 脚本改为非交互运行，自动生成 scikit-learn 风格代码、标准库可运行 smoke check、静态检查报告和最终机器学习最小闭环项目包，只自动记录脚本实际完成的练习任务。
- 修复：Round 19 UI 任务标题改为“生成 X/y 切分与最小分类闭环”“生成分类指标与过拟合观察示例”“生成预处理、Pipeline 与泄漏检查示例”等动作标题，并同步三星难度。
- 修复：Week 2 / Week 3 自测命令原先用 `/` 做除法，会被浏览器终端安全规则拦截；已改为 `** -1` 乘法倒数写法并通过终端 API 验证。
- 修复：阅读弹窗原先可能命中浏览器缓存，修改 notes 后仍显示旧内容；`progress_ui.js` 已对 markdown fetch 使用 `cache: "no-store"` 和时间戳 cache-bust，`progress.html` 同步版本号。
- 边界：本轮不在 Web UI 中执行 `pip install scikit-learn numpy pandas`；自动练习生成真实代码形状，但用 Python 标准库和静态检查做可运行验证。
- API 验证：`r19-w1-ex1`、`r19-w2-ex2`、`r19-w3-ex3`、`r19-fin-comp` 均可通过 `/api/tasks/<id>/run` 运行成功；`r19-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`~/round19` 与 `~/cli-lab/round19` 均映射到 `~/round19`；终端 API 能分别运行 Week 1 train/test split、Week 2 分类指标、Week 3 scaler 防泄漏三段手写自测；`pip install scikit-learn numpy pandas` 返回 `terminal_command_not_allowed:pip`。
- UI 验证：Codex 应用内浏览器打开 `progress.html?round=round_19` 后直接选中 Round 19；12 个任务、4 个运行按钮、9 个终端按钮均可见；Week 1 notes 可在阅读器中直接阅读；点击“运行”有确认框，确认后运行结果弹窗显示“运行成功”和 `static_check_report.json`；终端输入 `pwd` 输出 `/Users/alalapi/cli-lab/round19`。
- 文档阅读验证：Week 1 notes 包含 Web UI 学习路径和浏览器终端自测；scikit-learn Getting Started 与 train_test_split 官方链接渲染为 `_blank` 新标签，`rel` 包含 `noreferrer noopener`。
- 移动端验证：390px 宽度无整页横向溢出；任务按钮换行后不重叠。
- 截图：`/tmp/round19_web_ui_panel.png`（恢复真实记录后的 Round 19 页面，显示 0/12 完成）；阅读弹窗 `/tmp/round19_reading_modal.png`；运行结果 `/tmp/round19_run_result.png`；终端 `/tmp/round19_terminal_ui.png`；移动端 `/tmp/round19_mobile_ui.png`。
- 清理：本轮 API/UI 测试产生的进度、动作、反馈和终端历史已从测试前快照恢复。
- 工具备注：应用内浏览器的 DOM snapshot 接口在本页报运行时兼容错误；本轮改用同一应用内浏览器的只读 DOM evaluate、稳定 CSS selector 点击、确认框处理和截图完成真实页面验证。
- MCP 备注：`npm run check:mcp` 通过；`npm run check:cursor-mcp` 退出成功，但 CLI 层仍报告 chrome-devtools / playwright / context7 / github / stitch / figma / filesystem 为 `needs approval`，其中 filesystem 工具列表失败。本轮未假定这些 Cursor MCP 已暴露给当前线程，而是使用当前可用的 Codex 应用内浏览器和本地命令完成验证。

## Round 20 内容填充与 PyTorch 入门补测

- before 问题：Round 20 仍是最小骨架，notes 只列目标和自查，缺少 Web UI 学习路径、可直接阅读的知识解释、官方外链和浏览器终端自测命令。
- before 问题：Round 20 脚本只写 marker 文件，没有形成 Tensor、Dataset/DataLoader、nn.Module、训练循环、eval/no_grad、checkpoint 或最终项目包等可检查产物。
- before 问题：Round 20 任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断要练数据层、训练循环还是保存加载。
- 修复：Round 20 README、Week 1-3 notes、final 小抄已补齐 Tensor、Dataset/DataLoader、nn.Module、loss/backward/optimizer、eval/no_grad、state_dict、checkpoint、Web UI 完成路径和验收自问。
- 修复：Round 20 Python 脚本改为非交互运行，自动生成 PyTorch 风格代码、样例 CSV、标准库 smoke check、静态检查报告和最终 PyTorch 入门项目包，只自动记录脚本实际完成的练习任务。
- 修复：Round 20 UI 任务标题改为“生成 tensor、Dataset 与 batch 示例”“生成 nn.Module 与训练循环示例”“生成 eval/no_grad 与 checkpoint 示例”等动作标题，并同步四星难度。
- 修复：初版浏览器终端自测命令使用多行 heredoc，会被终端安全规则拦截；已改为先点“运行”生成 smoke 脚本，再在终端执行短命令 `cd` / `python3` / `cat` 的稳定路径。
- 边界：本轮不在 Web UI 中执行 `pip install torch torchvision`；自动练习生成真实 PyTorch 代码形状，但用 Python 标准库和静态检查做可运行验证。
- API 验证：`r20-w1-ex1`、`r20-w2-ex2`、`r20-w3-ex3`、`r20-fin-comp` 均可通过 `/api/tasks/<id>/run` 运行成功；`r20-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`~/round20` 与 `~/cli-lab/round20` 可进入 Round 20 沙盒；终端 UI 可绑定 `r20-w2-self`，执行 `pwd`、`cd ~/round20/week2_auto/training_loop`、`python3 stdlib_gradient_demo.py`，输出包含 `loss_decreased` 与 `final_loss`；`pip install torch torchvision` 返回 `terminal_command_not_allowed:pip`。
- UI 验证：Codex 应用内浏览器打开 `progress.html?round=round_20` 后直接选中 Round 20；12 个任务、4 个运行按钮、9 个终端按钮均可见；Week 1 notes 可在阅读器中直接阅读；点击“运行”有确认框，确认后运行结果弹窗显示“运行成功”和 `static_check_report.json`；恢复记录后页面显示 0/12 完成。
- 文档阅读验证：Week 1 notes 包含 Web UI 学习路径和浏览器终端自测；PyTorch Learn the Basics、Tensors、Datasets & DataLoaders 外链渲染为 `_blank` 新标签，`rel` 包含 `noreferrer noopener`。
- 移动端验证：390px 宽度无整页横向溢出；任务按钮换行后不重叠。
- 截图：`/tmp/round20_web_ui_panel.png`（恢复真实记录后的 Round 20 页面，显示 0/12 完成）；阅读弹窗 `/tmp/round20_reading_modal.png`；运行结果 `/tmp/round20_run_result.png`；终端 `/tmp/round20_terminal_ui.png`；移动端 `/tmp/round20_mobile_ui.png`。
- 清理：本轮 API/UI 测试产生的进度、动作、反馈和终端历史已从测试前快照恢复。
