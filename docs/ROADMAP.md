# Roadmap · Linux 单课程垂直验证

> 更新日期：2026-07-18
> 原则：先把一门 Linux 课做成可验证产品，再谈多课程。

## Phase 0：单课程化内容清理与项目重新定位

目标：

- 删除非 Linux 正式课程内容
- 固定产品愿景
- 固定 Linux 单课程范围
- 重写路线和架构

完成标准：

- 仓库中没有正式的非 Linux 课程内容
- README、ROADMAP、PROJECT_STATE 与真实仓库一致
- Linux 成为唯一 active course（`linux-foundations`）

本轮状态：**进行中 / 本轮目标**

## Phase 1：Linux 通用课程内容模型

目标：

- 建立 Course / Module / Lesson / Task 数据结构
- 当前只注册 `linux-foundations`
- 将现有 Round 00 Linux 内容迁入统一模型

完成标准：

- Linux 课程可以被统一任务系统识别
- 不依赖根目录散落的 round 文件作为唯一来源
- Round 00 现有执行能力保持兼容

## Phase 2：用户 Attempt 与 Action Event

目标：

- 记录用户每一次具体学习动作
- 不只记录 completed

完成标准：

- 每个任务可以查看操作历史
- 记录尝试次数、结果、时间和备注

## Phase 3：规则驱动反馈机制

目标：

- 根据正确、错误、重试、提示等动作返回反馈

完成标准：

- 每个有效动作都有明确反馈
- 错误反馈具有建设性
- 系统能给出下一步建议

## Phase 4：XP、Mastery、关卡和通关机制

目标：

- 建立最小成长系统

完成标准：

- 用户能够获得 XP
- 每个技能有 Mastery
- Linux Module 可以通关
- 奖励与真实学习证据绑定

## Phase 5：Linux Round 00 网页交互垂直切片

目标：

- 用户能通过网页完成 Round 00 的完整学习闭环

完成标准：

- 网页能展示任务
- 用户能提交动作
- 系统能记录
- 系统能反馈
- 系统能更新进度和 XP
- 用户能完成最终挑战并通关

## Phase 6：UI/UX 系统重新设计

目标：

- 重新定义产品视觉、交互、信息架构和游戏化反馈表现

说明：

- **下一轮再展开**
- 本轮只保留占位，不实施视觉重构

## Phase 7：Linux 课程逐模块完善

目标：

- 逐步完善文件系统、权限、Shell、进程、日志、SSH、网络和自动化模块

完成标准：

- 每个模块都有任务、验证、反馈和通关挑战

## Phase 8：工程质量与测试

目标：

- 增加数据校验、自动测试和迁移验证

## Phase 9：可选服务化

目标：

- 静态文件方案无法满足交互需求时，才引入后端和数据库

## Phase 10：多课程评估

目标：

- Linux 产品验证成功之后，再评估第二门课程

非目标：

- 当前不建设第二门课程

## 相关文档

- 愿景：`docs/PRODUCT_VISION.md`
- 架构：`docs/ARCHITECTURE.md`
- Codex 协作：`docs/CODEX_LONG_TERM_PLAN.md`
- 当前状态：`docs/PROJECT_STATE.md`
