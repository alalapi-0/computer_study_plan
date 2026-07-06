# Project User Review · Round 5 · 2026-07-06

## Review Scope

- README and current browser/UI workflow docs after the Round 4 fixes.
- Default Web UI desktop and 390px mobile behavior at `progress.html`.
- Current task, record/complete flow, terminal panel behavior, and side navigation.
- Tooling state: `npm run check:mcp` passed. `npm run check:cursor-mcp` still reports Cursor-side servers as `needs approval` in the CLI layer while listing some tools. Live UI inspection used the available local browser path.

## Findings

1. **Some UI workflow docs still point to the static server**  
   `docs/cursor_browser_ui_runbook.md`, `docs/prompts/CURSOR_UI_IMPLEMENTATION_PROMPT.md`, and `docs/WORKSPACE.md` still mention `python3 -m http.server` as a normal UI start path. That path disables the local API and does not match the real record, terminal, save, and exercise workflow.

2. **Default-page copy still treats terminal work as the normal path**  
   The default current task is a soft-exam reading task with no terminal button, but the side rail still says “左侧读教程，右侧敲命令”, and the workspace subtitle still says the browser terminal is placed in the same screen. This makes the page feel internally inconsistent.

3. **The idle terminal panel still takes too much space**  
   For the default non-engineering task, the terminal panel is only an informational idle state, but it still takes about 445px height on desktop and 249px on a 390px mobile viewport. On mobile, the management section starts around 2257px, so the no-op terminal still delays useful controls.

4. **The record flow makes evidence optional while the task flow asks for a record**  
   The current task says “写记录并完成”, but the record modal labels both note and evidence as optional, and the direct `完成` button can mark the task done with no note. This weakens the learning loop and makes accidental empty completion too easy.

5. **The side navigation item `进度设置` does not open settings**  
   Clicking the side rail `进度设置` link scrolls to the collapsed `进度、配置、存档与复盘信息` summary, but the `<details>` stays closed. Users have to click again to reveal the controls, so the navigation item does not do what it says.

## Fix Direction

- Replace remaining static-server workflow examples with `python3 scripts/progress_server.py` and mention static mode only as read-only fallback.
- Make default-page copy say “按任务做练习 / 工程任务再用终端”.
- Hide or strongly collapse the terminal panel when the current task does not use terminal.
- Route completion through a record-first flow or require a note before marking done from the record modal.
- Make the side navigation open the management `<details>` before scrolling to it.
