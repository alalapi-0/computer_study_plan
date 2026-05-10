# Round VPS-08 · tmux 后台任务训练

## 概览

| 项目 | 内容 |
|---|---|
| 主题 | 用 tmux 让远程任务在断开 SSH 后继续运行 |
| 操作权限等级 | **Level 3** |
| 是否需要用户授权 | **是**（必须） |
| 前置 | [VPS-07](round_vps_07_github_sync.md) |
| 下一轮 | [VPS-09](round_vps_09_network_check.md) |

## 目标

- 理解为什么远程任务不能依赖普通 SSH 窗口（断网即死）。
- 掌握 tmux 基础：new / detach / attach / kill。
- 在 tmux 里跑**低风险**测试任务（如 `python3 -m http.server` 仅监听 127.0.0.1，或简单循环）。
- 学会查看 tmux 会话状态。
- **不**在 tmux 中跑公网服务（公网部署在 VPS-11）。

## 用户授权请求范例

```
本轮将进行 Level 3 tmux 训练。
计划在 ~/study/ 下创建一个 tmux 会话 study_test，运行低风险测试命令。
不启动任何对外服务、不安装额外软件（仅当 which tmux 显示为空时，才单独提请安装）。
请确认是否执行。
```

## 涉及文件

- 远程：tmux 会话 `study_test`
- 本地：`rounds/stage_03_vps_remote_ops/outputs/tmux_session_record_template.md`

## 操作权限等级

- 等级：**Level 3**
- 注意：如果 VPS 未安装 tmux，安装动作属于"修改系统"，请单独取得授权（仍可视为 Level 3 边界，但要先发确认）。

## 学习内容

- tmux session、window、pane 的概念
- 为什么需要 tmux：SSH 断开 → 普通进程被 SIGHUP → 任务终止
- tmux 与 nohup 的区别（tmux 还能"重新连进去"）
- 适合放进 tmux 的任务：长时间 ASR / API 批量调用 / 训练 / 抓取 / 学习用临时服务
- detach / attach / list / kill-session 的快捷键和命令

## 命令示例

```bash
ssh your_user@your_server_alias

# 检查 tmux 是否安装
which tmux
tmux -V

# 新建会话
tmux new -s study_test

# 在会话内跑一个低风险任务
echo "hello tmux"
date
# 仅监听本地，不对外
python3 -m http.server 8000 --bind 127.0.0.1

# 离开会话（detach）：按 Ctrl+b 然后 d

# 此时回到普通 shell
tmux ls

# 重新连接
tmux attach -t study_test

# 任务结束后停止会话（注意：此命令会强制终止会话内进程）
tmux kill-session -t study_test

exit
```

## tmux 会话记录模板（建议字段）

```markdown
# Tmux Session Record · YYYY-MM-DD

- 服务器别名：your_server_alias
- 会话名：study_test
- 启动命令：tmux new -s study_test
- 会话内任务：______（如 python3 -m http.server 8000 --bind 127.0.0.1）
- 是否对外开放：[ ] 否（默认必勾）
- detach → attach 是否成功：[ ] 是
- tmux ls 输出：______
- 结束方式：[ ] kill-session / [ ] 自然结束 / [ ] 仍保留运行
- 后续如何停止：tmux kill-session -t study_test
```

## 验收标准

- [ ] 能创建 tmux 会话。
- [ ] 能 detach 后再 attach，不丢失任务。
- [ ] 能用 `tmux ls` 看到会话列表。
- [ ] 能解释为什么 AI 脚本 / 长任务 / 批量 API 调用适合放进 tmux。
- [ ] 测试服务仅监听 127.0.0.1，未对公网开放。
- [ ] 安全 / 远程操作两份 checklist 已逐项打勾。

## 风险与禁止事项

- 不在 tmux 中启动公网监听的服务（这是 VPS-11 的范畴）。
- 不让 tmux 会话中跑未审阅的脚本。
- 不让 tmux 会话长期持有真实 API Key（必须放在 `.env`，不在命令行中明文）。

## 输出物

- 一份脱敏后的 tmux 会话记录。

## 下一轮接口

VPS-09 将进入网络与端口检查，理解"为什么访问不通"的常见排查路径。
