# Round 11 · SQLite 持久化速查

## Web UI 完成路径

1. 打开 `progress.html?round=round_11`。
2. 依次阅读 Week 1–3 notes。
3. 点击三个练习任务的“运行脚本”，生成 SQLite 自动练习产物。
4. 点击三个自测任务的“终端练习”，自己写 sqlite3 建表、插入和查询脚本。
5. 点击 `r11-fin-comp` 的“运行脚本”，生成 `~/cli-lab/round11/final_auto/ai_prep_tool/round11_summary.json`。
6. 能解释本小抄里的问题后，再点击“记录并完成”保存 `r11-fin-sheet` 与 `r11-fin-acc1`。

## runs 表字段速查

| 字段 | 含义 |
|---|---|
| `id` | 自增主键，每条运行记录一个编号 |
| `input_file` | 本次运行使用的输入文件 |
| `output_file` | 本次运行写出的输出文件 |
| `format` | 输入格式，例如 `txt` / `csv` / `jsonl` |
| `original_count` | 处理前记录数 |
| `processed_count` | 处理后记录数 |
| `dedup` | 是否去重，通常用 0 / 1 |
| `run_time` | 运行时间 |

## 参数化 SQL 口诀

- 插入：`VALUES (?, ?, ?)` + 参数 tuple。
- 查询：`WHERE format = ?` + `(fmt,)`。
- 不拼接用户输入：不要写 `f"WHERE format = '{fmt}'"`。
- 写入后记得 `conn.commit()`。

## db.py 最小函数

- `init_db()`：创建 `runs` 表。
- `insert_run()`：写入一条运行记录。
- `get_all_runs()`：查询全部历史。
- `get_runs_by_format(fmt)`：按格式查询历史。

## .db 文件边界

- `runs.db` 是运行产物，应该生成在 `~/cli-lab/round11` 沙盒。
- `.gitignore` 应包含 `*.db`。
- 本轮不引入 ORM、不做 migration、不做多表关系。

## 最小通过标准

- 沙盒中存在可打开的 SQLite 文件。
- 插入与查询均使用参数化 SQL。
- 能说明 `runs` 表字段含义与一次运行如何落库。
- 每次运行 `ai_prep_tool.py` 后，`runs.db` 至少新增一条摘要记录。
- 能解释为什么只记录运行摘要，不把原始数据全文塞进数据库。

## 最终验收自问

- [ ] 我能写出 `CREATE TABLE IF NOT EXISTS runs (...)` 的基本结构。
- [ ] 我能解释 `?` 占位符为什么比字符串拼接安全。
- [ ] 我能说清 `conn.commit()` 的作用。
- [ ] 我能用 `get_all_runs()` 和 `get_runs_by_format("txt")` 查历史。
- [ ] 我能说明为什么 `*.db` 不应该提交进 Git。
