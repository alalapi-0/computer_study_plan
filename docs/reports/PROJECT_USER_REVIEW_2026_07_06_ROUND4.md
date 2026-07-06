# Project User Review · Round 4 · 2026-07-06

## Review Scope

- README first-run and UI development instructions.
- Default Web UI desktop and 390px mobile behavior at `progress.html`.
- Current plan entries opened by the default learning task.
- Error review and records documentation consistency.
- Tooling state: `npm run check:mcp` passed. `npm run check:cursor-mcp` still reports Cursor-side servers as needing approval in the CLI layer, while several tool lists are visible through the same script. This review used the available local browser inspection path and records that mismatch as tooling state.

## Findings

1. **README still suggests the wrong server for UI development**  
   The Cursor Browser UI workflow says to start the project with `python3 -m http.server 8000`. That opens a static page without the local API, so completion, records, terminal, saves, and exercise runs do not match the real learning workflow.

2. **The default soft-exam task shows terminal guidance that cannot be followed**  
   The default current task is `阅读软考中级主线总览`. Its buttons are `读教程 / 记录 / 完成`, but the card still says “需要命令时点终端练习” and the right-side terminal says to click `终端练习`. There is no terminal button for this task because it is not an engineering task.

3. **Round browsing is not aligned with the current task**  
   On the same default page, the current task is in the `soft_exam` lane, but the “按主线查看 Round” section defaults to `engineering` and `Round 00`. The user sees two competing starts: study soft exam now, or browse engineering Round 00.

4. **The soft-exam plan entry is stale about its own module files**  
   `plans/soft_exam/README.md` says all 12 module files are not pre-created, but `os.md`, `ds.md`, and `db.md` already exist. Since the default task opens this plan, the stale wording makes the plan look less ready than it is.

5. **The error-review docs contradict the no-question-cache rule**  
   `docs/ERROR_REVIEW_SYSTEM.md` requires a full “题面” field and says to copy the question text. `records/README.md` also says the error notebook can write the question text and solution process. This conflicts with the repository rule that it must not cache concrete exam questions or question items.

## Fix Direction

- Replace the static-server UI development example with `python3 scripts/progress_server.py` and the real 8777 URL.
- Make terminal guidance conditional: non-engineering tasks should say the terminal is not needed, and the terminal panel should not ask for a missing button.
- Align the active lane / Round browser with the default current task when no route parameter was provided.
- Update `plans/soft_exam/README.md` to mark existing starter modules and name the next files that still need creation.
- Rewrite error-review templates to use a short self-written prompt summary plus source locator, not copied full question text.
