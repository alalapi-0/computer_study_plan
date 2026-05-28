# plans/ · 学习计划专题目录

> 本目录承载**按 lane 组织的具体学习计划与章节笔记骨架**。
> 与 `rounds/round_XX/`（可执行练习目录）和 `records/`（真实学习记录）分工明确：
>
> - `rounds/round_XX/` → 可执行练习目录，每个 Round 一份
> - `plans/<lane>/` → 章节学习计划与笔记骨架，每个 lane 一份
> - `records/` → 用户真实学习记录（错题、周复盘等）

---

## 目录结构

```
plans/
├─ linux/        ← 工程实操线（engineering）下的 Linux 专项
├─ soft_exam/    ← 软考中级线（默认软件设计师）
├─ math2/        ← 数学二线
└─ 408/          ← 408 / 0854 线
```

> 任何 lane 的章节笔记 / 学习节奏 / 资料索引都按 lane 各自的子目录组织。
> 章节命名遵循 `docs/governance/file_naming_rules.md`。

---

## 文档读取顺序

1. `docs/MASTER_STUDY_ROADMAP.md`（总目标）
2. `docs/STAGE_PLAN.md`（阶段计划）
3. `docs/KNOWLEDGE_MAPPING.md`（知识点映射）
4. 本目录下对应 lane 的 README
5. 该 lane 内具体模块的 md

---

## 维护规则

- 新增 lane 之前先在 `docs/MASTER_STUDY_ROADMAP.md` 与 `progress.json` 的 `lanes` 中注册。
- 同一知识模块若被多条 lane 共用（如"数据结构"在软考 + 408 共用），各自 lane 下都建一份对应章节笔记，**不要在 plans 之间软链接**。
- plans 下的笔记**不写错题**；错题归 `records/error_notes/`。
- plans 下的笔记可以引用 `rounds/round_XX/` 下的练习作为辅助素材。
