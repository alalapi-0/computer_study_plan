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
```

## 当前结论

核心 Web UI 闭环已成立：用户可以从 Web UI 找到下一条任务，打开资料或脚本，运行受控练习脚本，写入学习记录，完成或撤销任务，并看到记录历史与反馈建议。

仍建议后续继续增强：继续逐轮补齐计划内容质量，并把更多考试主线任务从“阅读骨架”升级为可检查产物。
