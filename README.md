# Computer Study Plan · 真实问题练习工作台

在一次性 Linux 环境中亲自观察、调查、修改和验证实际问题。首批题目是明确标注的教学改编，固定提示、解答与判定均可离线运行。

```bash
cd ~/Projects/computer-study-plan
python3 scripts/progress_server.py
# 浏览器打开 http://127.0.0.1:8777/
```

选择问题 → 建立实验 → 在真实终端调查/修复 → 检查目标与保护约束 → 重置复练。提示只有「常开 / 常关」，跨刷新、跨题保持；完整解答单独打开。网页不会替你执行提示命令。

当前使用已有 Bubblewrap、Bash、Python、Git 等宿主工具的隔离用户态，显示实际工具版本与架构；没有公网、宿主用户目录、凭据、系统socket或仓库挂载。自由 Shell 只存在于实验边界中。环境不可用时拒绝启动，不回退宿主。此版本面向本机所有者，不是公网、多用户或恶意代码服务。

## 题目与记录

首批8题覆盖路径、权限、脚本输出、Git保留工作、重启持久化、重复重试、API字段/错误处理的离线程序子集、WAV产物质量。每个包位于 `content/scenarios/<id>/`，包含版本化题面、完整提示、解答、初始化与独立检查器。公开题包修改后必须重新运行发布门禁；维护者使用 `python3 scripts/validate_scenarios.py --runtime --publish` 生成匹配题包与工具的准入记录，复验前不能启动。

新Attempt独立存放在Git忽略的 `.lab-runtime/`：题目版本/内容摘要、环境和工具、开始/结束、提示/解答阅读、检查和证据。旧完成标记不会迁成独立解决。停止/重置丢弃一次性工作副本，保留历史；刷新仅重连仍活着的同一会话，服务重启显示失效。

历史Linux课程仍在 [progress.html](progress.html)，80任务、Round00、教程、原受限终端、CLI、进度事务与存档保留。原 `progress.json` 仍是旧课程进度唯一真源；`mark_done.sh` 不给新问题判定通关。旧受限终端不是OS隔离。

## 验证

```bash
python3 scripts/agent_gate.py --verify
python3 -m unittest tests.test_progress_transactions tests.test_run_transactions tests.test_workbench_http tests.test_lab_runtime tests.test_scenarios
python3 scripts/validate_scenarios.py --runtime
scripts/external-ui-python --check
scripts/external-ui-python --self-test
npm run test:ui
# 额外真实PTY/浏览器联调（fixedUI外层禁止nested userns）
PLAYWRIGHT_BROWSERS_PATH=/home/alalapi/Runtimes/computer-study-plan/browsers /home/alalapi/Runtimes/computer-study-plan/ui-venv/bin/python -B -m unittest tests.test_lab_browser_integration
```

现有固定Python3.12/Playwright1.60/Chromium1223回归环境继续复用；已安装时无需bootstrap。只在首次安装运行 `scripts/external-ui-python --bootstrap`，守卫不允许覆盖已有运行时。浏览器测试使用内存夹具或独立临时Attempt，不写正式学习数据。截图在 `/home/alalapi/Artifacts/computer-study-plan/linux-ui`（已核实指向DATA项目输出）。

完整系统/systemd、双节点网络、真实浏览器API场景、后台任务、AI模型、原生Windows/macOS仍见 [当前状态](docs/PROJECT_STATE.md) 与 [路线](docs/ROADMAP.md)。Linux技术回归不替代用户亲自练习或其他系统验收。

## 维护入口

[工作区](docs/WORKSPACE.md) · [产品愿景](docs/PRODUCT_VISION.md) · [架构/数据边界](docs/ARCHITECTURE.md) · [阶段与轮次](docs/ROADMAP.md) · [下一步](docs/NEXT_ACTIONS.md)

服务绑定127.0.0.1；只开放批准的网页/课程材料，实验工作副本、检查器、状态、Git和服务代码不经静态HTTP提供。xterm6.0.0固定资产及MIT许可证位于 `vendor/xterm/`，来源和完整性记录在 `provenance.json`，不依赖CDN。
