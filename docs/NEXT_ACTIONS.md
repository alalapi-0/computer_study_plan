# Next Actions

> 更新日期：2026-07-23
> 只保留当前可执行任务队列。

## 当前推进规则

- 唯一正式课程：`linux-foundations`
- 用户当轮直接指定任务时，以用户指令优先
- 不新增第二门课程
- 涉及真实 VPS 写操作时，必须先取得明确授权
- 大范围重构在独立分支完成；不直接假设可推 main

## TASK-LINUX-ONLY-BASELINE-20260718：Linux 单课程化基线重构

- 状态：**候选待验收**（revision `r2`；非 done / 非 DELIVERED）
- 分支：`codex/linux-single-course-refactor`
- 备份标签：`pre-linux-only-refactor-20260718-1029`
- 下一步治理路径：**Root VERIFY → 独立 Judge → Governor APPROVE → DELIVER**
- 浏览器冒烟：`UI_SMOKE_DEFERRED_FOR_ROOT`
- 当前候选摘要（待独立核验，非最终结论）：
  - `CONTENT_AUDIT` / `REMOVAL_MANIFEST` 齐全且删除分类一致
  - 非 Linux 正式课程目录已从工作树移除；进度收敛为 `linux-foundations`
  - `content/courses/linux-foundations/` 已注册（course.json + 5 模块 overview + README）
  - 本轮不做 UI 视觉重设计 / XP / 后端；不推 main

## 下一轮候选（仅在本任务 DELIVER 之后）

1. Phase 1：Course/Module/Lesson/Task 数据模型与 Round 物理迁移
2. Phase 6 准备：UI/UX 重设计研究（需真实浏览器 before/after）
3. Phase 2：Attempt / Action Event 细化

## 已退出正式队列

- 软考 / 数学二 / 408 / 考研相关推进任务
- Round 07–21 独立课程填充任务
- 多主线并行铺开任务
