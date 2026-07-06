# Round 02 · Week 3 笔记（Git 最小工作流）

## 本周目标

- 跑通 Git 最小闭环：`init → status → add → commit → log`。
- 能看懂工作区与暂存区的基础状态变化。
- 只在 `~/cli-lab/round2` 沙盒中练本地 Git，不做远程推送。

## 在 Web UI 里怎么学

1. 阅读本文件后，点击 Week 3 的三个“运行脚本”按钮。
2. 脚本会在 `~/cli-lab/round2/week3/git_lab_auto` 中创建一个可重复生成的本地 Git 仓库。
3. 自测时打开“终端练习”，在 `~/cli-lab/round2/week3/git_lab_manual` 中手敲最小 Git 闭环。
4. 能解释 `git status` 和 `git log --oneline` 后，再点击“记录并完成”保存自测记录。

## 最小闭环命令

| 步骤 | 命令 | 作用 |
|---|---|---|
| 初始化仓库 | `git init` | 创建 `.git` 历史目录 |
| 查看状态 | `git status` | 看文件处于未跟踪/已暂存/待提交 |
| 暂存改动 | `git add <file>` | 把改动放入暂存区 |
| 创建提交 | `git commit -m "msg"` | 生成历史快照 |
| 查看历史 | `git log --oneline` | 快速浏览提交记录 |
| 查看差异 | `git diff` | 查看未暂存改动 |

## 常见观察点

- `untracked`：Git 还没接管该文件。
- `changes to be committed`：已暂存，下一次 commit 会带上。
- `changes not staged`：改过但还没 add。

## 推荐手敲流程

```bash
cd ~/cli-lab/round2/week3
mkdir git_lab_manual
cd git_lab_manual
git init
git config user.name "Round 02 Learner"
git config user.email "round02@example.local"
git config commit.gpgsign false
echo "# manual git lab" > README.md
git status
git add README.md
git commit -m "init manual lab"
echo "second line" >> README.md
git diff
git add README.md
git commit -m "update readme"
git log --oneline
```

如果 `git commit` 提示缺少用户名、邮箱或签名配置，就在这个练习仓库里重新执行 `git config user.name ...`、`git config user.email ...` 和 `git config commit.gpgsign false`。

## 本周完成后你应该能回答

- [ ] 为什么提交前要 `git status`？
- [ ] `git add` 与 `git commit` 的边界是什么？
- [ ] 看到 `git log --oneline` 的多条记录后，如何描述你的变更历史？

## 本周自测

不看上面的命令，独立完成：

1. 创建一个新的本地 Git 仓库
2. 做第一次提交
3. 修改 `README.md` 并做第二次提交
4. 用 `git status` 确认工作区状态
5. 用 `git log --oneline` 解释两次提交的历史

完成后点击“记录并完成”，保存 `自测：解释 status 与 log` 的本次记录。
