# Round 02 · Week 3 笔记

## 本周目标

- 跑通 Git 最小闭环：`init → status → add → commit → log`。
- 能看懂工作区与暂存区的基础状态变化。

## 最小闭环命令

| 步骤 | 命令 | 作用 |
|---|---|---|
| 初始化仓库 | `git init` | 创建 `.git` 历史目录 |
| 查看状态 | `git status` | 看文件处于未跟踪/已暂存/待提交 |
| 暂存改动 | `git add <file>` | 把改动放入暂存区 |
| 创建提交 | `git commit -m "msg"` | 生成历史快照 |
| 查看历史 | `git log --oneline` | 快速浏览提交记录 |

## 常见观察点

- `untracked`：Git 还没接管该文件。
- `changes to be committed`：已暂存，下一次 commit 会带上。
- `changes not staged`：改过但还没 add。

## 本周完成后你应该能回答

- [ ] 为什么提交前要 `git status`？
- [ ] `git add` 与 `git commit` 的边界是什么？
- [ ] 看到 `git log --oneline` 的多条记录后，如何描述你的变更历史？
