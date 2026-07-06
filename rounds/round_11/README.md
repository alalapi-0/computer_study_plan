# Round 11 · 本地持久化与数据记录

这个目录是 Round 11（SQLite、参数化查询、运行历史记录）的 Web UI 可练习版本。

> **仓库根**：`~/PycharmProjects/computer_study_plan`  
> **练习沙盒**：`~/cli-lab/round11`  
> 路径说明见 [`docs/WORKSPACE.md`](../../docs/WORKSPACE.md)。

## 目录结构

```
round_11/
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
   └─ sqlite_persistence_cheatsheet.md
```

## 使用方式

### 推荐：只通过 Web UI 完成

1. 在仓库根启动本地服务：

   ```bash
   python3 scripts/progress_server.py
   ```

2. 浏览器打开 `http://127.0.0.1:8777/progress.html?round=round_11`。
3. 在 Round 11 任务列表里按顺序完成：
   - 阅读任务：点“读教程”，直接在页面中读 `notes.md`、脚本和 `round_11.md`。
   - 自动练习：点“运行脚本”，脚本会在 `~/cli-lab/round11/*_auto` 创建 SQLite 数据库、`db.py`、查询脚本和收口摘要，并自动记录对应练习完成。
   - 自测任务：点“终端练习”，在浏览器映射终端中自己写 sqlite3 建表、插入、查询脚本；确认理解后再点击“记录并完成”。
   - 小抄与验收：读 `final/sqlite_persistence_cheatsheet.md`，能解释后再点击“记录并完成”保存记录。

### 命令行备用

仍可在仓库根直接运行：

```bash
python3 rounds/round_11/week1/exercises.py
python3 rounds/round_11/week2/exercises.py
python3 rounds/round_11/week3/exercises.py
python3 rounds/round_11/final/comprehensive_exercise.py
```

## 完成边界

- 自动脚本只标记 `r11-w1-ex1`、`r11-w2-ex2`、`r11-w3-ex3`、`r11-fin-comp`。
- `r11-w*-self`、`r11-fin-sheet`、`r11-fin-acc1` 必须由用户通过 Web UI 阅读、手写、自测和点击“记录并完成”保存记录。
- 本轮只使用 Python 标准库 `sqlite3`；`.db` 文件只生成在 `~/cli-lab/round11` 沙盒，不进入 Git。
