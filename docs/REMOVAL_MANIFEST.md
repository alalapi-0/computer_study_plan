# Removal Manifest

> 日期：2026-07-18
> 备份标签：`pre-linux-only-refactor-20260718-1029`
> 工作分支：`codex/linux-single-course-refactor`

## 删除原则

1. 本轮只删除工作树中的**非 Linux 正式课程内容**；Git 历史仍完整保留。
2. 只删除 `CONTENT_AUDIT.md` 中分类为 `REMOVE_NON_LINUX` 的路径。
3. 平台代码、Round 00–02 / Round 06、VPS 支线、`plans/linux/` 不删除。
4. 恢复时优先使用备份标签，不要猜测路径。

通用恢复命令：

```bash
git checkout pre-linux-only-refactor-20260718-1029 -- <path>
# 或
git restore --source=pre-linux-only-refactor-20260718-1029 <path>
```

## 删除项目

### Round 03–05（Python / 数据结构 / 算法独立课程）

- 路径：`round_03.md`、`round_04.md`、`round_05.md`；`rounds/round_03/`、`rounds/round_04/`、`rounds/round_05/`
- 内容说明：Python 基础、核心数据结构、高频算法模式
- 删除原因：不属于 `linux-foundations` 正式课程
- 关联旧文档：`docs/MASTER_STUDY_ROADMAP.md`、`docs/STAGE_PLAN.md`、`docs/PROJECT_STATE.md`
- 恢复方式：`git restore --source=pre-linux-only-refactor-20260718-1029 round_03.md round_04.md round_05.md rounds/round_03 rounds/round_04 rounds/round_05`

### Round 07–21（Python 工程 / API / ML / NLP 等）

- 路径：`round_07.md`–`round_21.md`；`rounds/round_07/`–`rounds/round_21/`
- 内容说明：AI 工具、工程化、SQLite、流水线、Docker/发布、HTTP/FastAPI、数值计算、机器学习、PyTorch、NLP 前置
- 删除原因：独立非 Linux 课程路线
- 关联旧文档：`README.md`、`CONVERSION_PROTOCOL.md`、`docs/CODEX_LONG_TERM_PLAN.md`
- 恢复方式：`git restore --source=pre-linux-only-refactor-20260718-1029 round_0{7,8,9}.md round_1{0,1,2,3,4,5,6,7,8,9}.md round_2{0,1}.md rounds/round_0{7,8,9} rounds/round_1{0,1,2,3,4,5,6,7,8,9} rounds/round_2{0,1}`

### 软考 / 数学二 / 408 计划目录

- 路径：`plans/soft_exam/`、`plans/math2/`、`plans/408/`
- 内容说明：考试与考研计划骨架
- 删除原因：非 Linux 正式课程
- 关联旧文档：`plans/README.md`、`docs/PROGRESS_RULES.md`、`progress.json` lane 任务
- 恢复方式：`git restore --source=pre-linux-only-refactor-20260718-1029 plans/soft_exam plans/math2 plans/408`

### 考研与多目标作品集文档

- 路径：`docs/GRADUATE_SCHOOL_TRACKER.md`、`docs/PROJECT_PORTFOLIO_TRACK.md`
- 内容说明：院校跟踪模板；跨考试/求职作品集追踪
- 删除原因：服务考研与多目标作品集，不是 Linux 单课程验证范围
- 关联旧文档：`docs/MASTER_STUDY_ROADMAP.md`、`docs/STAGE_PLAN.md`
- 恢复方式：`git restore --source=pre-linux-only-refactor-20260718-1029 docs/GRADUATE_SCHOOL_TRACKER.md docs/PROJECT_PORTFOLIO_TRACK.md`

### 进度数据中的非 Linux 任务与 lane（重建清除）

- 路径：`progress.json`、`progress_data.js`、`rounds_data.js`、`records/feedback/task_feedback.json`
- 内容说明：soft_exam / math2 / cs408 lane 与 Round 03–05、07–21 任务
- 删除原因：与已删除课程内容同步；通过生成器重建，不手工编辑镜像
- 关联旧文档：`docs/PROGRESS_RULES.md`、`scripts/build_rounds_data.py`
- 恢复方式：`git restore --source=pre-linux-only-refactor-20260718-1029 progress.json progress_data.js rounds_data.js records/feedback/task_feedback.json`

## 未删除的不确定项

无。所有原 `REVIEW_REQUIRED` 候选已在 `CONTENT_AUDIT.md` §6 裁定为保留或重写，不进入删除清单。
