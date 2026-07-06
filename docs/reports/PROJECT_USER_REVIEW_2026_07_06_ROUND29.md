# Project User Review · Round 29

> 日期：2026-07-06
> 视角：普通学习者 + 后续自动推进 Agent
> 范围：转换协议版本与进度系统范围、Round 状态表、工作区只读说明、Round 03 自动记录边界、README 当前下一步

## 本轮发现的 5 个问题

1. `CONVERSION_PROTOCOL.md` 标题和版本表仍停在 v2.0，但变更记录已存在 v2.1，后续 Agent 会误判协议状态。
2. 转换协议开头仍把进度系统缩成 `progress.json / progress_data.js / mark_done.sh / progress.html`，遗漏 `rounds_data.js`、`progress_ui.js`、本地 API、动作日志和任务反馈。
3. 转换协议的 Round 00 状态表备注写“已完成最小闭环”，容易把材料展开误读成用户已经学完。
4. `docs/WORKSPACE.md` 顶部只读说明仍比脚本表更含糊，只说“只读检查”，没有说明静态打开缺少写 API、练习脚本、动作日志和浏览器终端。
5. 当前学习指引仍有局部歧义：Round 03 的自动记录说明没有明确只限 `exercise` 任务，README 当前下一步也过于单点地强调首屏信息密度。

## 修复摘要

- 将转换协议标题和当前版本更新到 v2.1。
- 将转换协议开头的进度系统范围扩展为当前 Web UI、本地 API、生成数据、动作日志和任务反馈组合。
- 将 Round 00 状态表备注改为“已展开并接入 Web UI；真实学习完成状态以 `progress.json` 为准”。
- 将 WORKSPACE 顶部静态打开说明补全为只读布局 / 进度检查，并列出缺失能力。
- 将 Round 03 自动记录边界改为只自动记录对应练习任务；README 下一步改为继续做 Web UI / 文档用户视角评测。

## 验证结果

- 文本扫描确认本轮目标旧说法不再残留。
- `python3 scripts/agent_gate.py --verify` 通过。
- 浏览器回检默认 Web UI、桌面 Round 02 与移动端 Round 02：页面标题和左侧品牌均为“学习工作区”，`读教程`、`记录并完成`、Round 02 `终端练习` 与 `~/cli-lab/round2` 绑定均正常，无横向溢出。
