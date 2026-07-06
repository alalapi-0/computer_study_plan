# Cursor UI 实现 Prompt 模板

> 复制下方整段到 **新的普通前台 Agent 对话**（禁用 Multitask）中使用。

---

## 可复制 Prompt

```
请在本仓库执行一轮 UI 优化，严格遵守以下约束：

【环境与模式】
- 必须使用普通前台 Agent
- 禁止 Multitask / 后台子 Agent
- 开始前检查当前对话线程是否暴露以下 MCP 工具：stitch、chrome-devtools、playwright、filesystem、context7、github
- 若任一必需工具未暴露，输出 BLOCKED: MISSING_FROM_THREAD_TOOL_REGISTRY 并停止，不要假装执行浏览器操作

【阅读上下文】
- README.md
- AGENTS.md
- docs/MASTER_STUDY_ROADMAP.md
- docs/cursor_browser_ui_runbook.md
- docs/design/（若存在）

【本轮范围】
- 只选择一个 UI 改造切片（例如 progress.html 的某一区块）
- 不改变业务逻辑（progress.json、mark_done.sh 闭环必须保持可用）
- 不大范围重构无关文件

【标准流程】
1. 启动本地服务（`python3 scripts/progress_server.py`）并打开 `http://127.0.0.1:8777/progress.html`
2. before：截图 + 检查 console + 检查 network
3. 参考 Stitch 设计输入（若 STITCH_API_KEY 可用）或现有设计文档
4. 修改 UI 代码
5. 重新打开页面
6. after：截图 + 检查 console + 检查 network + 检查响应式
7. 运行 npm run check:mcp 与 npm run check:cursor-mcp（及项目既有低成本校验）
8. 更新必要文档
9. 默认在 `main` commit；remote 存在时直接 push `main`

【微信页面】
- 本仓库为普通本地 Web 项目，不使用 wechat-chrome-session
- 若误涉及微信已登录页面，停止并说明需切换工具

请开始：先报告当前线程可用 MCP 工具，再执行 before 检查。
```

---

## 使用前 checklist

- [ ] 已在 Settings → Tools & MCP 批准所需 server
- [ ] 已完全退出并重开 Cursor
- [ ] 新建普通前台 Agent 对话（非 Multitask）
- [ ] 本地已配置 `GITHUB_PERSONAL_ACCESS_TOKEN` / `STITCH_API_KEY`（见 `.env.example`）
