# Project User Review · Round 3 · 2026-07-06

## Review Scope

- README first-run clarity and daily-use guidance.
- Current planning/state docs after the governance cleanup.
- Web UI desktop and 390px mobile behavior at `progress.html?round=round_02`.
- Tooling state: `npm run check:mcp` passed; `npm run check:cursor-mcp` still reported Cursor MCP servers as `needs approval`, so live UI inspection used the available in-app browser.

## Findings

1. **README front-loads tooling instead of learning**  
   A new learner reaches MCP server setup and Cursor browser workflow before the daily Web UI start path. This makes the project feel like an agent/tooling repo before it explains how to study today.

2. **README positioning and status wording are stale**  
   The README says the repository is not a tool repo and does not contain business code, while the current project includes a local Web UI, API service, scripts, and browser terminal workflow. It also says “当前总目标（v2026-05）”, describes `round_12` to `round_21` as only “已展开最小骨架”, and says not to confuse “21 份 Round 概览” with completion. Current state is 22 Round overview files, all `rounds/round_00` to `rounds/round_21` expanded and registered in the Web UI.

3. **`STAGE_PLAN.md` still reads like Stage 0 setup is not complete**  
   Stage 0 exit criteria are unchecked even though the current state says Stage 0 scaffolding is complete. Stage 1 still says to expand Round 01 / Round 02 / Round 06 “按需做完”, which conflicts with the current expanded Round 00–21 directory set.

4. **Web UI current reading task does not bind the terminal**  
   Desktop browser evidence: `round_02` route correctly focuses “阅读：重定向、追加、管道” and loads the inline tutorial, but the terminal remains “未绑定任务” and the current task card has no “终端练习” button. The UI copy says to click “终端练习” when commands are needed, but the focused reading task does not provide that action.

5. **Mobile first screen still delays the learning workspace**  
   At 390px width, the side rail, `今日学习` card, and API banner consume the first ~460px before the workspace begins. The inline reader starts below the first viewport and the terminal starts much farther down, so the mobile experience still feels stacked and indirect.

## Fix Direction

- Move the README quick start / daily learning path before MCP/Cursor tooling details.
- Reword repository positioning around “local learning system, not production/business app.”
- Update stale README and Stage Plan status wording to match current Round/Web UI state.
- Let engineering reading tasks bind the browser terminal, so the current task can keep tutorial and terminal connected.
- Compress mobile chrome around the Web UI so the learning workspace reaches the first screen sooner.
