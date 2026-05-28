# Progress Rules · 进度规则（v1.0）

> 本文档规定本仓库进度系统在**四条主线（lanes）下的统一操作规则**。
> 进度数据由 `progress.json` 单一事实源持有，`mark_done.sh` 写入，`progress_data.js` 镜像，`progress.html` 展示。
> 详细数据结构与脚本规范见 `CONVERSION_PROTOCOL.md` Section 8。

---

## 1. 四条主线（lanes）

| lane code | 中文名 | 主要内容 |
|---|---|---|
| `engineering` | 工程实操线 | Linux / Shell / Git / Python / 工程化 / 服务化 / AI 工程 / VPS |
| `soft_exam` | 软考中级线 | 软件设计师（默认）+ 备选方向 |
| `math2` | 数学二线 | 高等数学 + 线性代数 |
| `cs408` | 408/0854 线 | 数据结构 + 计组 + 操作系统 + 网络 |

每条 lane 在 `progress.json` 顶层的 `lanes` 对象中有一个条目，每个任务通过 `tasks.<id>.lane` 字段归属。

---

## 2. 状态模型

### 2.1 当前阶段使用的最小状态集

| 字段 | 含义 | 取值 |
|---|---|---|
| `done` | 是否完成 | `true` / `false` |
| `done_at` | 完成时间戳 | `YYYY-MM-DD HH:MM` 或 `null` |
| `lane` | 所属主线 | `engineering` / `soft_exam` / `math2` / `cs408` |

### 2.2 v2 暂未启用的扩展字段（保留命名空间，**不在本轮实现**）

> 这些字段在未来增强时启用；当前 `mark_done.sh` 不写入也不读取。

| 字段 | 含义 |
|---|---|
| `status` | `not_started` / `in_progress` / `done` / `review` / `weak` |
| `review_required` | 是否需要复习 |
| `attempts` | 累计尝试次数 |
| `last_action_at` | 最近一次动作时间 |
| `notes` | 备注 |

### 2.3 标记规则（当前阶段）

| 行为 | 表现 |
|---|---|
| **完成** | `bash mark_done.sh <task-id>` → `done=true`、`done_at=now`，写回 `progress.json` 与 `progress_data.js` |
| **撤销** | `bash mark_done.sh <task-id> --undo` → `done=false`、`done_at=null` |
| **复习中** | （当前阶段）暂无字段；用 `records/weekly_reviews/` 与 `records/error_notes/` 表达 |
| **薄弱项** | （当前阶段）暂无字段；写在周复盘的"高频错题模块"段 |

---

## 3. 任务 ID 命名

| 用途 | 规则 | 例子 |
|---|---|---|
| Round 00 旧任务 | 保留简写（不改） | `w1-read`、`w1-ex1`、`fin-comp` |
| Round 01+ 新任务 | `rXX-wN-taskShort` | `r01-w1-read` |
| 阶段性支线 | `<scope>-XX-taskShort` | `vps-05-readonly`、`soft-os-ch01` |
| 软考章节自定任务 | `soft-<module>-<short>` | `soft-os-pv-1` |
| 数学二章节自定任务 | `math2-<module>-<short>` | `math2-calc-limit-1` |
| 408 章节自定任务 | `cs408-<module>-<short>` | `cs408-ds-tree-1` |

任务 ID **全局唯一**。所有任务必须有 `lane` 字段。

---

## 4. 错题与复习的进度表达（当前阶段非状态字段）

由于 v2 不引入 `status` 字段，错题与复盘的进度通过文件位置和命名表达：

| 行为 | 沉淀位置 |
|---|---|
| 记录错题 | `records/error_notes/<lane>/<module>/YYYY-MM-DD-shortid.md` |
| 周复盘 | `records/weekly_reviews/YYYY-WW.md` |
| 完成的练习快照 | `records/completed_tasks/<lane>/...`（可选） |
| 高频错题导致计划调整 | 写入对应 `plans/<lane>/...` 中的"调整记录"段 |

> 这种方式不依赖 progress.json 扩展字段，符合 ADR-0001 "继续使用 JSON 简单结构"的约束。

---

## 5. 进度回流机制

进度数据不是"打卡完就忘"。每周复盘后应回流：

1. **打卡完成 ≠ 真懂**：完成 `done=true` 后仍可在错题本里出现该模块的错题。
2. **薄弱项识别**：在周复盘里识别出薄弱模块后，对应 `plans/<lane>/<module>.md` 头部添加"⚠ YYYY-WW 复盘 → 本模块需回炉"标注。
3. **优先级回写**：若 4 周内连续出现高频错题，应在 `docs/KNOWLEDGE_MAPPING.md` 把该模块优先级提升到 P0。

---

## 6. progress.html 展示规则

升级后的 `progress.html` 必须展示：

1. **四主线总进度条**（按 lane 聚合）
2. **每条 lane 内的轮次进度**（继续沿用 ROUNDS 数组）
3. **本周任务占位**（不依赖后端，纯前端从用户输入）
4. **倒计时占位**（软考考试日 + 考研日，可由用户在前端编辑后写入 localStorage，不写入 progress.json）
5. **当前薄弱项板块**（从 progress.json 中"特定 lane 任务完成率 < 30%"自动识别，**非强制**）

> 倒计时与薄弱项**不写入 progress.json**，避免污染状态层。

---

## 7. 进度数据完整性约束

下面这些约束写在脚本/校验工具未来要做的检查中：

- `progress.json` 必须是合法 JSON。
- 每个 `tasks.<id>` 必须包含 `done`（布尔）、`done_at`（字符串或 null）、`lane`（字符串）。
- `lane` 必须是 `lanes` 中已注册的 key。
- 同一 `task_id` 只允许出现一次。
- 不允许手动编辑 `progress_data.js`。

---

## 8. 不破坏 Round 00 的硬约束

- 旧任务 ID（`w1-read`、`w1-ex1`、`fin-comp` 等）必须保留原名。
- 旧任务的 `done` / `done_at` 在升级时如已是 true 必须保留。
- `mark_done.sh` 在升级到 lanes 后仍能无参数运行并按 lane 分组展示。

---

## 9. 周复盘进度行为

每周复盘是进度系统的"事件入口"：

- 写完周复盘 → 必须更新对应 lane 的"本周完成数 / 本周新增错题数"统计（手动写入复盘文件即可）
- 不要求把这些统计写进 progress.json
- 若希望聚合，未来用脚本扫 `records/weekly_reviews/` 生成报表（**未实现**）

---

## 10. 标记示例

```bash
bash mark_done.sh w1-read                       # 标记 Round 00 阅读完成（lane=engineering）
bash mark_done.sh r04-w1-ex1                    # 标记 Round 04 第 1 周练习 1 完成（如已注册）
bash mark_done.sh soft-os-ch01                  # 标记软考 OS 模块章节 1 完成（如已注册）
bash mark_done.sh w1-read --undo                # 撤销
bash mark_done.sh                               # 查看所有任务（按 lane 分组）
```

---

## 11. FAQ

**Q：我做错题应该 mark_done 吗？**
A：不需要。错题用 `records/error_notes/` 文件表达。`progress.json` 只跟踪"任务是否完成"。

**Q：我读完一章不想注册成任务，怎么计入进度？**
A：在 `records/weekly_reviews/` 的周复盘里写一笔即可。`progress.json` 是"显式注册的任务清单"，不是"读书量统计"。

**Q：我可以把 `engineering` 改成 `linux` 之类的吗？**
A：不建议。lane 名是仓库内多份文档共享的硬约定，改名要全仓库同步。

**Q：旧 Round 00 任务 lane 是什么？**
A：`engineering`。升级脚本会自动补 `lane: "engineering"`。
