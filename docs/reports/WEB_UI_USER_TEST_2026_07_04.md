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

- 新增能力：Web UI 可创建本地学习进度快照，快照保存 `progress.json`、动作日志、任务反馈、本周任务与考试倒计时。
- 安全策略：读档前自动创建“读档前恢复点”，避免误读档后无法恢复。
- API 验证：`GET /api/saves`、`POST /api/saves`、`POST /api/saves/<save_id>/load` 均通过；测试快照含 286 个任务、7 条动作记录。
- UI 验证：用户可在“存档与读档”卡片输入备注、点击“创建存档”、在列表点击“读档”、确认后完成恢复；读档后自动恢复点出现在列表。
- 布局验证：桌面端 1280px 无横向溢出；390px 移动端无整页横向溢出；当前 URL 无 console error。
- 清理：本轮 API/UI 测试产生的 `codex-*test-save` 临时快照已删除，未保留为真实用户存档。

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
python3 -m py_compile scripts/progress_lib.py scripts/progress_server.py scripts/generate_task_feedback.py scripts/mark_done_cli.py scripts/sync_progress_data.py scripts/build_rounds_data.py
```

## 当前结论

核心 Web UI 闭环已成立：用户可以从 Web UI 找到下一条任务，打开资料或脚本，写入学习记录，完成或撤销任务，并看到记录历史与反馈建议。

仍建议后续继续增强：把“脚本练习如何在沙盒中执行”的说明做成更明确的 UI 引导；如果未来要完全不切终端执行练习，需要单独设计安全的本地命令执行权限模型。
