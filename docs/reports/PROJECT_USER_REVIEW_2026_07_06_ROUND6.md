# Project User Review · Round 6 · 2026-07-06

## Review Scope

- Default Web UI desktop and 390px mobile behavior at `progress.html`.
- Current task actions, record/complete flow, task-list naming, and engineering-task fallback.
- README, `PROJECT_STATE.md`, and soft-exam startup material after the Round 5 fixes.
- Tooling state: `npm run check:mcp` passed. `npm run check:cursor-mcp` still reports Cursor-side servers as `needs approval` in the CLI layer while listing some tools. Live UI inspection used the available local browser path.

## Findings

1. **The cross-lane task area is still named as a Round list**  
   The side rail says `Round 清单`, and the section says `按主线查看 Round`. This is accurate for the engineering lane, but the default current lane is `soft_exam` and its entries are plan tasks, not Rounds. The label makes the page feel like it is still organized around the old engineering-only route.

2. **Unfinished tasks expose two record-looking entry points**  
   The current task shows both `记录` and `记录并完成`. For an unfinished task, opening `记录` still leads to the same record-and-complete flow, so the two buttons are not meaningfully different.

3. **Exercise output still mentions the old completion path**  
   The run result hint says to click `完成` or open `记录`, but Round 5 changed completion to the record-first `记录并完成` flow. The hint is now stale and can make users search for a button that no longer exists.

4. **`PROJECT_STATE.md` mixes display grouping with tracked task data**  
   The state doc says the Web UI has "28 个分组、304 个任务", while `progress.json` tracks 304 tasks and has no `groups` field. The 28 display groups come from `rounds_data.js`, so the source of truth needs to be named explicitly.

5. **The soft-exam startup table is not actionable inside the reader**  
   `plans/soft_exam/README.md` lists existing `os.md`, `ds.md`, and `db.md` files as inline code text, and the lightweight Markdown renderer does not support relative document links. In the Web UI reader this forces users to leave the page or manually locate files instead of jumping to the available note skeletons.

## Fix Direction

- Rename user-facing Round-list labels to task-list labels while keeping the existing DOM ids and data model stable.
- Hide the standalone record button until a task is already done; unfinished tasks should have one clear `记录并完成` path.
- Update stale run-result hints to the current record-first completion action.
- Split current-state wording between `rounds_data.js` display groups and `progress.json` task tracking.
- Link existing soft-exam module skeletons from the startup README and teach the reader to open relative Markdown links in-page.
