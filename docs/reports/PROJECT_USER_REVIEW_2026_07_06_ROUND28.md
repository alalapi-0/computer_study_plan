# Project User Review · Round 28

> 日期：2026-07-06
> 视角：普通学习者 + 后续自动推进 Agent
> 范围：README 只读入口说明、WORKSPACE 路径约定、转换协议 CLI 语义、Round 03 说明、Round 00 综合验收脚本提示

## 本轮发现的 5 个问题

1. README 的只读打开方式只写“无写 API”，没有明确说明练习脚本、动作日志和浏览器终端也不可用，容易让用户继续用静态页面学习。
2. `docs/WORKSPACE.md` 只说直接打开 `progress.html` 用于只读检查，没有明确列出缺失能力，和 README 的当前 Web UI 工作流不够一致。
3. README 与 `CONVERSION_PROTOCOL.md` 仍把 CLI 用途写成“补标记 / 标记完成”，弱化了当前“记录并完成 / 补录完成”的语义。
4. `rounds/round_03/README.md` 仍说脚本“不会替你打卡”，与当前 Web UI 的“记录并完成”说法不一致。
5. Round 00 综合验收脚本结束时输出“Round 00 全部完成”，但该脚本只完成综合验收相关任务，容易让用户误以为所有周任务都已完成。

## 修复摘要

- README 与 WORKSPACE 的只读打开方式已明确为布局 / 只读进度检查，不具备写 API、练习脚本运行、动作日志和浏览器终端能力。
- README 与转换协议里的 CLI 用途改为“补录完成”，命令注释改为“记录完成（CLI 补录）”。
- Round 03 终端边界说明改为脚本不会替用户“记录完成”。
- Round 00 综合验收脚本结束提示改为“综合验收脚本已完成”。

## 验证结果

- 文本扫描确认本轮目标旧说法不再残留。
- `bash -n rounds/round_00/final/comprehensive_exercise.sh` 通过。
- 浏览器回检默认 Web UI、桌面 Round 02 与移动端 Round 02：页面正常加载，`学习工作区`、`读教程`、`记录并完成`、Round 02 `终端练习` 与 `~/cli-lab/round2` 绑定均正常，无横向溢出。
- `python3 scripts/agent_gate.py --verify` 通过。
