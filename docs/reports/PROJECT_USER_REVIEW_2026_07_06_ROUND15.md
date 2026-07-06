# Project User Review 2026-07-06 Round 15

## Scope

- Soft exam plan entry in Web UI.
- `plans/soft_exam/`, `docs/STAGE_PLAN.md`, `docs/KNOWLEDGE_MAPPING.md`.
- Generated task data: `rounds_data.js`, `progress.json`, `progress_data.js`, and `records/feedback/task_feedback.json`.

## Findings

1. After Round 14, soft exam had more module skeletons, but the Web UI still registered only four soft exam tasks: overview, data structures, operating systems, and databases.

2. Remaining soft exam modules (`uml`, `oo`, `security`, `c_lang`, `standards`, `english`) were still listed as `待建`, leaving half of the module table as dead ends.

3. `docs/STAGE_PLAN.md` still described Stage 2 output as only `os.md` / `ds.md` / `db.md`, which was stale after the added module skeletons.

4. `docs/KNOWLEDGE_MAPPING.md` still treated UML, C language, information security, and standards/IP as files to create later instead of current startup entries.

5. Generated feedback did not include the new soft exam module tasks until the task data was rebuilt and feedback was regenerated.

## Fixes

- Added startup skeletons for `uml.md`, `oo.md`, `security.md`, `c_lang.md`, `standards.md`, and `english.md`.
- Updated the soft exam README so all 12 modules are links with startup skeleton status.
- Added all 9 newly available module skeletons to `scripts/build_rounds_data.py` as soft exam reading tasks.
- Regenerated `rounds_data.js`, `progress.json`, `progress_data.js`, and task feedback; soft exam now has 13 tasks total.
- Updated Stage Plan and Knowledge Mapping to reflect current skeleton coverage.

## Verification

- Static checks passed: `git diff --check`, Markdown relative link check, `node --check progress_ui.js`, Python compile checks, JSON validation, and `compileall`.
- Project checks passed: `check_protocol_sync.py`, `validate_learning_data.py`, `bash mark_done.sh`, and `npm run check:mcp`.
- `npm run check:cursor-mcp` listed CLI-layer tools; `filesystem` still reports not approved at the Cursor CLI layer, while this thread's filesystem tools worked normally.
- Data checks passed: `progress.json` now has 313 tasks, with 13 in `soft_exam`; the same new soft exam task IDs are present in `progress_data.js`, `rounds_data.js`, and `records/feedback/task_feedback.json`.
- Browser checks passed: `progress.html?lane=soft_exam` shows `0/13 完成`, all 13 soft exam tasks have `读教程` and `记录并完成`, the UML skeleton opens in the inline reader, and desktop/mobile checks showed no horizontal overflow or console errors.
