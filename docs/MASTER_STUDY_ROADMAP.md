# Master Study Roadmap · Linux 单课程总路线

> 更新日期：2026-07-18
> 本文档是仓库总目标路线图。多课程/考研/软考旧路线已退出正式范围，需要追溯时查看 git history。

## 1. 总目标

用一门正式课程 **Linux 基础与工程实践**（`linux-foundations`）验证：

- 用户是否愿意持续学习
- 任务是否可记录
- 动作是否有反馈
- 是否形成掌握度、关卡和通关感
- 网页交互是否有趣、美观、有效
- 是否真正帮助用户学会并坚持 Linux

详细愿景见 `docs/PRODUCT_VISION.md`。分阶段计划见 `docs/ROADMAP.md`。

## 2. 当前唯一正式课程

| 字段 | 值 |
|---|---|
| course_id | `linux-foundations` |
| 标题 | Linux 基础与工程实践 |
| 内容入口 | `content/courses/linux-foundations/` |
| 兼容练习真源 | `rounds/round_00`、`01`、`02`、`06`、`stage_03_vps_remote_ops` |
| 进度 lane | `linux-foundations` |

## 3. 模块主线

1. Terminal 初见（Round 00）
2. 文件系统与基础命令（Round 01）
3. Shell、管道与 Git 最小工作流（Round 02）
4. Linux 进阶与自动化（Round 06）
5. VPS 远程实操，只读优先（stage_03）

## 4. 非目标

在 Linux 单课程闭环验证成功前：

- 不新增第二门正式课程
- 不恢复软考 / 数学二 / 408 / 考研正式路线
- 不把 Python / 算法 / FastAPI / ML / NLP 独立课程重新纳入正式范围

## 5. 平台能力与课程内容的边界

- Python / JavaScript / Shell 作为**平台实现代码**可以存在
- 被删除的是**非 Linux 课程教学内容**
- Git、SSH、基础服务排练若服务于 Linux 工程实践，可作为邻接模块保留
