# Cursor Current Thread Tool Registry Check

> CLI 层 MCP 检查脚本见 `scripts/check_cursor_mcp_status.sh`；本文说明**当前 Agent 对话线程**的工具暴露问题。

---

## 核心事实（6 点）

1. **终端里的 MCP ready 只能说明 server 可用**  
   `cursor-agent mcp list` 或 Settings 绿点，只表示 MCP server 进程/配置层面就绪，**不等于**当前 Agent 对话已注册这些工具。

2. **当前 Agent 对话必须实际暴露工具**  
   Agent 能否调用 `browser_navigate`、`playwright_*`、`stitch_*` 等，取决于**当前对话线程**的工具注册表，必须在该对话中实际可见。

3. **Multitask 子 Agent 可能没有继承 Workspace MCP**  
   后台子 Agent / Multitask 模式下的子任务，经常**无法访问** Workspace 级 MCP 工具（含 chrome-devtools、playwright、stitch 等）。

4. **旧对话可能仍停留在批准前的工具注册表**  
   在 Settings 批准 MCP **之前**已打开的对话，可能永久缺少新工具，直到重启 Cursor 并新建对话。

5. **正确处理方式：完全重启 Cursor + 新开普通 Agent 对话**  
   批准 MCP 或修改 `.cursor/mcp.json` 后：Quit Cursor → 重开仓库 → Settings 确认 ready → **新建普通前台 Agent**（禁用 Multitask）。

6. **连字符 server 名称可能导致路由问题**  
   若 `wechat-chrome-session` 等带连字符的名称无法路由，可在 `.cursor/mcp.json` 增加 underscore alias（如 `wechat_chrome_session`），并在文档中说明两者等价。**本仓库非微信项目，通常不需要此 alias。**

---

## 排查表

| 现象 | 可能原因 | 解决方法 |
|---|---|---|
| `cursor-agent mcp list` 显示 ready，但对话中 server does not exist | 当前线程未继承工具注册表 | 重启 Cursor，新建普通 Agent |
| Multitask 中缺少 MCP 工具 | 子 Agent 未继承 Workspace MCP | 禁用 Multitask |
| wechat-chrome-session ready 但无法调用 | 工具未暴露给当前线程或名称路由问题 | 新建前台 Agent，必要时增加 `wechat_chrome_session` alias |
| playwright 打开的是未登录页面 | Playwright 新开隔离浏览器 | 微信任务改用 wechat-chrome-session |
| chrome-devtools 不能接管现有页面 | Chrome 未开启 remote debugging 或线程没有工具 | 启动 remote debugging 并重启 Cursor |

---

## Agent 缺工具时的标准输出

```
BLOCKED: MISSING_FROM_THREAD_TOOL_REGISTRY

当前对话线程未暴露所需 MCP 工具：<tool-name>

请执行：
1. 完全退出 Cursor（Quit）
2. 重新打开本仓库
3. Settings → Tools & MCP 确认 server ready
4. 新建普通前台 Agent 对话（禁用 Multitask）
5. 重新发送任务
```

---

## 与本仓库的检查命令

```bash
# CLI 层配置与 server 列表（≠ 当前线程工具暴露）
bash scripts/check_cursor_mcp_status.sh
npm run check:cursor-mcp

# 静态 mcp.json 校验
npm run check:mcp
```

**重要：** 以上命令通过，仍可能在当前 Agent 对话中缺工具。最终以**当前对话实际可见的工具列表**为准。
