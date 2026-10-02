# UI 回归

这组测试用仓库静态文件和隔离 fixture 验证 Home → Learn、history、reduced-motion、移动触控，以及任务完成/撤销事务的浏览器契约。

- `FixtureServer()` 默认严格只读，所有写请求返回 `405`；既有 5 项测试保持零写入。
- 只有显式 `FixtureServer(task_actions=True)` 才开放纯内存的 task done/undo/run API。done/undo 按 canonical ASCII task ID、原始字符串 `operation_id` 与完整 task/action/note/evidence payload 执行 500 Unicode code point 校验和幂等冲突判定；run 只接受精确的 `operation_id` payload，以独立内存账本提交单一 revision/event/feedback/snapshot 事务。同 ID 重试只重放 canonical execution，不重复模拟执行、追加事件或提升 revision；失败、超时及未到登记验证点均不会伪造完成，读档移除旧 event 后也拒绝账本幽灵重放。两者都返回完整 80-task 状态、canonical UUID events 与 feedback，并可用 `action_plan` / `run_plan` 安排成功、HTTP 错误或畸形响应。
- fixture 不导入生产 `progress_lib`，也不会写 `progress.json`、`progress_data.js`、`records/`、终端状态、存档或 `~/cli-lab`。
- delayed run 还覆盖展示上下文隔离：响应前离开 Learn 或切换任务时，内存事务仍提交，但旧任务的执行结果不会强开 modal 覆盖当前界面。

计划响应示例：

```python
FixtureServer(task_actions=True, action_plan=[
    {"kind": "success", "delay": 0.4},
    {"kind": "http_error", "status": 503, "error": "planned"},
    {"kind": "timeout", "delay": 0.35},
])
```

```bash
npm run test:ui
```

## Linux工作站

固定入口仍为 `scripts/external-ui-python` 与 `npm run test:ui`，只接受原有四个动作。`--bootstrap` 显式安装锁定的Playwright1.60依赖与其官方Chromium1223；已有目标拒绝覆盖。`--check`、`--self-test` 和测试不下载依赖，也不回退其他Python、浏览器或仓内环境。

运行环境/浏览器在 `/home/alalapi/Runtimes/computer-study-plan`；缓存与临时目录在对应 `/home/alalapi/Caches`、`/home/alalapi/Temp` 根。入口先核对ext4 UUID `9d258b70-f313-4a5d-9cf6-c715c5edca3d`、规范路径、所有者及依赖/浏览器完整树。Linux UI测试通过既有bubblewrap隔离网络、系统IPC和Home，源码/正式数据/运行时只读；只有项目缓存与临时根可写。所有完成/撤销/run仍只在现有显式内存夹具执行。

报告和截图位于 `/home/alalapi/Artifacts/computer-study-plan/linux-ui`。实际浏览器回归与技术截图不代表Phase6整体验收、用户真实学习或真机安全区通过。

## 历史Mac环境（保留）

首次建立项目自有外置 UI Python 运行时：

```bash
scripts/external-ui-python --bootstrap
npm run test:ui
```

固定入口会先验证外盘 volume/container UUID 和治理映射，再使用项目专属的 `/Volumes/AI_WORK_SSD/Runtimes/computer-study-plan/browsers/chromium_headless_shell-1223`。该副本来自既有本地浏览器的离线复制；入口不自动下载浏览器，也不回退到内盘共享缓存。UI venv、浏览器和测试临时目录都在外盘；外盘不可用时明确退出，不在仓库内重建 `.venv-ui`。

浏览器夹具中的视口无法模拟非零 `env(safe-area-inset-bottom)`；自动化只验证对应 CSS 约定，真实设备安全区仍属于后续人工/真机回归范围。

`npm run test:ui` 会发现并运行 `tests/ui/test_*.py`。测试不会接入 `agent_gate.py`：浏览器依赖单独安装，但每次 UI 检查点验收都应运行它。

生产 `progress_lib` 的并发、幂等、故障回滚、中断恢复、读档 revision 和 API 输入边界使用临时仓库测试：

```bash
npm run test:progress
```

该测试只复制必要状态到系统临时目录；不会调用正式仓库的完成 API。
覆盖包含 500/501 Unicode code point（含 astral 字符）、missing/empty 重放、同 operation 不同 payload 冲突、canonical task URL、读档后的旧 event 重放拒绝，以及 `progress.json` / `progress_data.js` revision 一致性。
