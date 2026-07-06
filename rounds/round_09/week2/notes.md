# Round 09 · Week 2 笔记（Git 分支工作流）

## 本周目标

- 练习“新功能新分支”的基础流程。
- 熟悉 feature/hotfix 分支的最小协作语义。

## Web UI 学习路径

1. 先点击本文件“读教程”，理解 feature / hotfix 都是在本地沙盒仓库中排练。
2. 点击 `r09-w2-ex2` 的“运行脚本”。脚本会在 `~/cli-lab/round9/week2_auto/workflow_demo` 自动完成：
   - `git init`
   - 配置本地 user name / email
   - `main` 初始提交
   - `feature/improve-readme` 分支提交并合并
   - `hotfix/empty-input` 分支提交并合并
   - 输出 `git_log.txt`
3. 点击 `r09-w2-self` 的“终端练习”，自己在 `~/cli-lab/round9` 里建一个小仓库，完整走一次分支流程。

## 安全边界

- 只在 `~/cli-lab/round9` 里练本地 Git。
- 不做 `git push`、`git pull`、`git fetch`、`git remote`，这些在浏览器终端里会被拦截。
- 如果 Git 要求身份信息，只配置当前沙盒仓库的本地身份，不改全局配置。

## 浏览器终端自测命令

在 `r09-w2-self` 的终端里逐条运行：

```bash
mkdir week2_self
cd week2_self
git init
git checkout -b main
git config user.email learner@example.local
git config user.name Learner
printf '# Workflow Demo\n' > README.md
git add README.md
git commit -m init
git checkout -b feature/readme-note
printf 'feature note\n' >> README.md
git add README.md
git commit -m feature-readme-note
git checkout main
git merge feature/readme-note
git branch -d feature/readme-note
git log --oneline
```

能解释为什么先开分支再合并后，回到任务行点击“记录并完成”。

## 本周自查

- [ ] 能在本地完成新分支创建、提交、切回主分支
- [ ] 能解释为什么不建议直接在 main 上开发
- [ ] 能说明 feature 与 hotfix 的语义区别
