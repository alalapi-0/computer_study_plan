# Roadmap · Linux 单课程垂直验证

> 更新日期：2026-08-14
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

状态：**done / DELIVERED**（见 `docs/PROJECT_STATE.md`）

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

当前状态：**in progress**。2026-08-11 已形成可运行的校准版基线；2026-08-13 已重新读取完整 Figma，并开始按实际 Desktop、Mobile、Components、Motion 与 Codex Handoff 逐个高价值切片收敛。首页双端与对应空间交互是首个切片；聚焦学习工作区、真实执行反馈和完成回执是第二个切片；成长记录与模块检查点是第三个切片；路线地图与模块总览是第四个切片；由真实 action event 驱动的复习/记录回看是第五个切片；由 5 份登记 Markdown 真源驱动的只读命令手册是第六个切片。2026-08-14 又完成跨屏显式任务身份、首个 Components / Motion 横切检查点，以及 H04 Home → Learn 连续关系与移动触控检查点：当前任务卡可在支持的浏览器以 520ms 共享材料关系进入 Learn，不支持或 reduced-motion 时保持原子降级；390–920px 的主行动、单面板 Learn 与核心触控约定已统一，安全区 CSS 已核对且非零设备 inset 仍待真机回归，并由首个只读 Playwright 套件保护。六个屏幕切片和现有流程/动效检查点仍不能代表 Phase 6 整体完成。

完成标准：

- 首页、学习、路线、复习、手册、成长与模块检查点形成完整导航关系
- Figma 中 10 个 Desktop 与 10 个 Mobile 核心状态均能映射到真实产品流程；命名和示例内容按项目事实调整
- 核心组件的默认、悬停、按压、禁用、拖拽、回弹和降级状态符合 Components / Motion / Codex Handoff 契约
- Desktop / Mobile 响应式可靠
- 关键 Hover / Press / Drag / Transition / Feedback 状态可用
- 原有教程、终端、记录、反馈、存档和任务闭环不回退
- 真实浏览器、console、布局溢出与项目质量门通过

## Phase 7：Linux 课程逐模块完善

目标：

- 逐步完善文件系统、权限、Shell、进程、日志、SSH、网络和自动化模块

完成标准：

- 每个模块都有任务、验证、反馈和通关挑战

## Phase 8：工程质量与测试

目标：

- 增加数据校验、自动测试和迁移验证

当前状态：**in progress**。已建立 5 项 Home → Learn 只读浏览器回归，并将同一 fixture 以显式 opt-in 的纯内存模式扩展为 5 项 API 契约测试与 18 项浏览器任务动作回归；另有 14 项临时仓库测试覆盖生产后端的并发、幂等、精确输入、镜像 revision、故障回滚、中断恢复、损坏 WAL 零写入拒绝、读档及旧事件重放与 API 边界。正式学习数据不参与夹具写入；尚未覆盖完整视觉快照、脚本/终端全部竞态和全部屏幕。

## Phase 9：可选服务化

目标：

- 静态文件方案无法满足交互需求时，才引入后端和数据库

## Phase 10：通用学习编排与自然语言入口评估

目标：

- 在 Linux 单课程闭环、数据模型和反馈机制稳定后，评估“自然语言目标 → 结构化学习方案 → 用户确认 → 任务执行”的最小垂直切片
- 保持方案生成层与课程事实源、完成证据、奖励结算之间的清晰边界

非目标：

- 当前阶段不实现自然语言编排
- 不允许自然语言输入直接标记完成、授予 XP 或改写进度事实源

## Phase 11：多课程评估

目标：

- Linux 产品验证成功之后，再评估第二门课程
- 长期候选包括编程、计算机科学、AI、英语、日语、其他自然语言与其他学习主题

非目标：

- 当前不建设第二门课程

## 相关文档

- 愿景：`docs/PRODUCT_VISION.md`
- 架构：`docs/ARCHITECTURE.md`
- Codex 协作：`docs/CODEX_LONG_TERM_PLAN.md`
- 当前状态：`docs/PROJECT_STATE.md`
