# Round 09 · 仓库规范化与测试入门

这个目录是 Round 09（仓库结构整理、分支工作流、测试入门）的 Web UI 可练习版本。

> **仓库根**：`~/PycharmProjects/computer_study_plan`  
> **练习沙盒**：`~/cli-lab/round9`  
> 路径说明见 [`docs/WORKSPACE.md`](../../docs/WORKSPACE.md)。

## 目录结构

```
round_09/
├─ README.md
├─ week1/
│  ├─ notes.md
│  └─ exercises.py
├─ week2/
│  ├─ notes.md
│  └─ exercises.py
├─ week3/
│  ├─ notes.md
│  └─ exercises.py
└─ final/
   ├─ comprehensive_exercise.py
   └─ repo_testing_cheatsheet.md
```

## 使用方式

### 推荐：只通过 Web UI 完成

1. 在仓库根启动本地服务：

   ```bash
   python3 scripts/progress_server.py
   ```

2. 浏览器打开 `http://127.0.0.1:8765/progress.html?round=round_09`。
3. 在 Round 09 任务列表里按顺序完成：
   - 阅读任务：点“打开”，直接在页面中读 `notes.md`、脚本和 `round_09.md`。
   - 自动练习：点“运行”，脚本会在 `~/cli-lab/round9/*_auto` 生成规范化项目、沙盒 Git 仓库、测试文件和收口报告，并自动记录对应练习完成。
   - 自测任务：点“终端”，在浏览器映射终端中自己创建文件、运行本地 Git / Python 命令；确认理解后再手动点“记录 / 完成”。
   - 小抄与验收：读 `final/repo_testing_cheatsheet.md`，能解释后再手动完成记录。

### 命令行备用

仍可在仓库根直接运行：

```bash
python3 rounds/round_09/week1/exercises.py
python3 rounds/round_09/week2/exercises.py
python3 rounds/round_09/week3/exercises.py
python3 rounds/round_09/final/comprehensive_exercise.py
```

## 完成边界

- 自动脚本只标记 `r09-w1-ex1`、`r09-w2-ex2`、`r09-w3-ex3`、`r09-fin-comp`。
- `r09-w*-self`、`r09-fin-sheet`、`r09-fin-acc1` 必须由用户通过 Web UI 阅读、手写、自测和手动记录。
- 本轮不在仓库中安装 pytest，不做 GitHub 远程操作；Git 分支与合并只在 `~/cli-lab/round9` 沙盒本地仓库里演练。
