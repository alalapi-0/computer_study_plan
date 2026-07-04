# Round 08 · 总复盘与升级路线

这个目录是 Round 08（项目收口、测试入门、sqlite3、服务化接口形状排练）的 Web UI 可练习版本。

> **仓库根**：`~/PycharmProjects/computer_study_plan`  
> **练习沙盒**：`~/cli-lab/round8`  
> 路径说明见 [`docs/WORKSPACE.md`](../../docs/WORKSPACE.md)。

## 目录结构

```
round_08/
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
   └─ upgrade_route_cheatsheet.md
```

## 使用方式

### 推荐：只通过 Web UI 完成

1. 在仓库根启动本地服务：

   ```bash
   python3 scripts/progress_server.py
   ```

2. 浏览器打开 `http://127.0.0.1:8765/progress.html?round=round_08`。
3. 在 Round 08 任务列表里按顺序完成：
   - 阅读任务：点“打开”，直接在页面中读 `notes.md`、脚本和 `round_08.md`。
   - 自动练习：点“运行”，脚本会在 `~/cli-lab/round8/*_auto` 生成项目骨架、测试、数据库或接口排练产物，并自动记录对应练习完成。
   - 自测任务：点“终端”，在浏览器映射终端中自己创建文件、运行脚本；确认理解后再手动点“记录 / 完成”。
   - 小抄与验收：读 `final/upgrade_route_cheatsheet.md`，能解释后再手动完成记录。

### 命令行备用

仍可在仓库根直接运行：

```bash
python3 rounds/round_08/week1/exercises.py
python3 rounds/round_08/week2/exercises.py
python3 rounds/round_08/week3/exercises.py
python3 rounds/round_08/final/comprehensive_exercise.py
```

## 完成边界

- 自动脚本只标记 `r08-w1-ex1`、`r08-w2-ex2`、`r08-w3-ex3`、`r08-fin-comp`。
- `r08-w*-self`、`r08-fin-sheet`、`r08-fin-acc1` 必须由用户通过 Web UI 阅读、手写、自测和手动记录。
- 本轮不在仓库中引入 pytest / FastAPI / uvicorn 等新依赖，也不启动真实后端服务；服务化先做接口形状和升级路线排练。
- 所有临时数据都在 `~/cli-lab/round8`，不写入仓库、也不污染 `records/` 的真实学习记录。
