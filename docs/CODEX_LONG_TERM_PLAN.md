# Codex / Cursor 续作入口

> 2026-10-13 · TASK-PROBLEM-WORKBENCH-20261013

先读AGENTS要求的八份权威文档与PROJECT_STATE。当前产品是问题驱动的实操工作台；旧课程/XP/Figma全屏对齐队列已被本次用户请求替代，不执行历史Prompt中的自动推进指令。

唯一源码仓库 `/home/alalapi/Projects/computer-study-plan`。Root持有共享状态、控制面、Git和外部效果；Repair只写显式分配的内容，Reviewer只读。先确认当轮任务文件所有权，不把空锁/共享cwd/idle当另一任务已结束。无需改全局Agent或兄弟PCH项目。

平台保留原生HTML/CSS/JS、Python本地服务、JSON历史；xterm是固定本地资产。不要因偏好换框架、数据库或构建完整调度平台。先隔离再开放Shell；未就绪拒绝，不回退宿主。系统真实问题只在适用VM/原生OS中验证。

每个题包版本改变后重新走初始故障、全提示、正面/负面、重置/再解和适用替代解法。可信维护者本地导入是当前能力；不将可执行题包上传直接运行。真实事故必须保留可获得证据，缺失原因标未知，教学改编显式说明。

复用既有质量门和固定UI运行时。测试仅临时环境/内存夹具；不向正式Attempt注入Agent演示，不改原学习记录。新Attempt不随旧存档读档回滚。真实浏览器与截图分别记录功能、视觉、console/network；Linux代验不等于用户独立解题或其他OS接受。

恢复/备份：停止服务后同时保存 `.lab-runtime/attempts.json` 与旧progress/records；恢复Attempt历史不会复活PTY进程，active标lost。可丢弃workspace无需备份；准确行为见ARCHITECTURE。回滚代码仅本任务精确差异和基线，保留新历史；不重置用户后续改动。

当前续作唯一队列见NEXT_ACTIONS，R00–R02无需无变化重跑。任何发布/提交/推送/合并、VPS、密码、sudo与宿主网络操作需对应授权；本次只本地未暂存候选。
