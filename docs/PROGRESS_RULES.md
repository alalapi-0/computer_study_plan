# Progress Rules · 进度规则（v2.0）

> 更新日期：2026-08-14
> 单课程阶段：只有 `linux-foundations` 一条正式进度 lane。

## 1. 唯一正式课程 / lane

| lane / course_id | 中文名 | 主要内容 |
|---|---|---|
| `linux-foundations` | Linux 基础与工程实践 | 终端、文件系统、Shell、自动化、远程实操 |

进度完成状态由 `progress.json` 持有；Web UI / `mark_done.sh` 写入；`progress_data.js` 是前端镜像；`rounds_data.js` 提供任务展示元数据。

每个任务的完成事实必须成对一致：`done: true` 时 `done_at` 是非空字符串；`done: false` 时 `done_at` 必须为 `null`。正式读取、恢复和前端响应提交都在写入或呈现前核对这一不变量。

## 2. 完成与撤销

- Web UI：「记录并完成」必须填写本次记录后保存
- CLI：`bash mark_done.sh <task-id>` / `--undo`
- 完成与撤销都会更新进度、镜像、动作日志和任务反馈
- Web 写入带唯一 `operation_id`；同一任务、动作、备注和证据在超时后重试只提交一次。不同输入不得复用同一 ID
- 备注与证据路径分别最多 500 个 Unicode 字符；Web、API 与核心写入库使用同一精确字符串语义，超长输入明确拒绝，不静默截断、规整路径或改写 Unicode
- 进度写入使用单调 `revision` 与本地操作账本；进程中断后由下一次服务或 CLI 访问恢复，读档不会回退 revision，也不会删除幂等账本
- 操作账本只保留请求身份，不替代当前动作历史；读档移除某个 event 后，旧 `operation_id` 的重放必须明确拒绝，不能返回或复活不在当前 `events.jsonl` 中的动作
- 前端只为超时、网络中断、服务端错误或已提交但响应校验失败等结果不确定情形保留同一 ID；明确的 4xx 拒绝会释放本地重试 ID，使相同输入可用新 ID 再提交
- 恢复 pending 操作前必须完整核对账本 key、输入指纹、基准/目标任务状态、revision 与动作事件；损坏记录不得触发任何状态写入
- Web 成功响应必须携带与本次操作一致的持久化 event；客户端在任务快照、反馈、消息和 event 全部匹配前不得显示成功或提交本地状态

## 3. 动作日志与反馈

- 动作日志：`records/action_logs/events.jsonl`
- 任务反馈：`records/feedback/task_feedback.json`（生成器维护，不手工编辑）
- 当前反馈仍是最小实现，不是完整规则引擎

## 4. 生成关系

| 命令 | 输出 |
|---|---|
| `npm run build:rounds` | `rounds_data.js` + 合并/裁剪 `progress.json` + 同步镜像 |
| `npm run sync:progress` | `progress_data.js`（含与 `progress.json` 一致的 `revision`） |
| `python3 scripts/generate_task_feedback.py` | `task_feedback.json` |

## 5. 禁止事项

- 不手工编辑 `progress_data.js` / `rounds_data.js` / `task_feedback.json`
- 不重新引入 soft_exam / math2 / cs408 作为正式 lane
- 不把“打开页面”当成任务完成
