# Round VPS-07 · GitHub 仓库拉取与远程运行准备

## 概览

| 项目 | 内容 |
|---|---|
| 主题 | 在 VPS 上 clone 公开 GitHub 仓库 + 理解本地 ↔ GitHub ↔ VPS 同步关系 |
| 操作权限等级 | **Level 3** |
| 是否需要用户授权 | **是**（必须） |
| 前置 | [VPS-06](round_vps_06_remote_dirs.md) |
| 下一轮 | [VPS-08](round_vps_08_tmux_training.md) |

## 目标

- 在 `~/study/` 下 clone **公开**仓库（默认即用 `computer_study_plan` 自身或用户指定）。
- 理解 `git status` / `git log` / `git pull` 在远程环境的行为。
- 理解 `.gitignore`、`.env`、`.env.example` 三者关系。
- **不**启动任何对外服务。
- **不**clone 私有仓库（除非用户单独授权并使用安全的 deploy key）。

## 用户授权请求范例

```
本轮将进行 Level 3 远程仓库同步。
计划在 ~/study/ 下 clone 公开仓库 your_repo_url。
仅做 clone / status / log / pull，不启动任何服务，不安装依赖。
请确认是否执行，并指定要 clone 的仓库 URL（必须为公开仓库或已配置 deploy key 的仓库）。
```

## 涉及文件

- 远程：`~/study/<repo_name>/`
- 本地：`rounds/stage_03_vps_remote_ops/outputs/github_sync_record_template.md`

## 操作权限等级

- 等级：**Level 3**

## 学习内容

- `git clone` 与 `git pull` 的区别
- 三角关系：本地 push → GitHub 中转 → VPS pull
- 哪些文件不能进 Git：`.env`、`id_rsa`、真实日志、真实数据库
- 哪些文件可以进 Git：`.env.example`、README、源码
- `git status` 在本地与远程的同等含义
- 公开仓库 vs 私有仓库：本轮**只允许公开仓库**或已正确配置 deploy key 的仓库

## 命令示例

```bash
ssh your_user@your_server_alias

cd ~/study

git clone your_repo_url
cd <repo_name>

git status
git log --oneline -10
git pull

# 在本地（另一个终端）push 一次后，回到 VPS 拉取，体验三角同步
# 本地：在本地仓库 commit & push
# VPS:
git pull

exit
```

## 远程仓库同步记录模板（建议字段）

```markdown
# GitHub Sync Record · YYYY-MM-DD

- 服务器别名：your_server_alias
- 登录用户：your_user
- 仓库 URL（脱敏，仅写仓库名）：computer_study_plan / your_repo_name
- clone 路径：~/study/<repo_name>
- git status 结果：clean / 有未跟踪文件
- git log 最近 3 条：______
- git pull 行为：up to date / 拉取到 N 条新提交
- 是否检测到 .env 错误进入 Git：[ ] 否（默认必勾）
- 备注：______
```

## 验收标准

- [ ] 仓库已成功 clone 到 `~/study/<repo_name>`。
- [ ] `git status` 干净。
- [ ] 用户能解释本地 push 与 VPS pull 的关系。
- [ ] `.env` 未进入 Git；`.env.example` 在仓库中（或在本轮新增）。
- [ ] 没有启动任何服务。
- [ ] 安全 checklist 与远程操作 checklist 已逐项打勾。

## 风险与禁止事项

- 不 clone 私有仓库，除非已配置 deploy key 并经用户单独确认。
- 不安装依赖（依赖安装放到 VPS-10 / VPS-11 中处理）。
- 不启动服务。
- 不在 VPS 上配置 GitHub token（用 deploy key 或公开仓库即可）。

## 输出物

- 一份脱敏后的"远程仓库同步记录"。

## 下一轮接口

VPS-08 将进入 tmux，让远程任务在断开 SSH 后继续运行。
