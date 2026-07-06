# Project User Review 2026-07-06 Round 20

## Scope

- `CONVERSION_PROTOCOL.md`, especially the new Round flow and progress-system maintenance rules.
- Workspace documentation for the `progress.html` launch path.
- Residual guidance that could make the next maintainer edit generated files or open the wrong UI mode.

## Findings

1. `CONVERSION_PROTOCOL.md` still told maintainers to run `bash mark_done.sh` merely to sync `progress_data.js`, missing the current `npm run build:rounds`, `npm run sync:progress`, and task-feedback generation workflow.

2. The new Round flow still instructed maintainers to append Round metadata to a `ROUNDS` array inside `progress.html`; current metadata is generated into `rounds_data.js` by `scripts/build_rounds_data.py`.

3. The progress-system table described `progress.html` as a read-only board and did not mention `scripts/progress_server.py`, Web UI writes, action logs, saves, or task feedback.

4. The protocol said every state change must go through `mark_done.sh`, contradicting the current Web UI flow where `记录并完成` and `撤销完成` write through the local API and keep action logs.

5. The protocol still recommended double-clicking `progress.html` or running `python3 -m http.server 8000`; `docs/WORKSPACE.md` also described `progress.html` as a file to open, which downplays the current 8777 local-service entry required for records, terminal linkage, and script execution.

## Fixes

- Updated the new Round flow to use `scripts/build_rounds_data.py`, `npm run build:rounds`, `npm run sync:progress`, and `scripts/generate_task_feedback.py`.
- Replaced the obsolete `progress.html` `ROUNDS` section with current `rounds_data.js` / generator guidance.
- Updated the progress-system table to include `rounds_data.js`, `scripts/progress_server.py`, Web UI files, action logs, and task feedback.
- Reframed `mark_done.sh` as a CLI compatibility and backfill tool while making Web UI `记录并完成` the preferred state-change path.
- Updated `CONVERSION_PROTOCOL.md` and `docs/WORKSPACE.md` to make `http://127.0.0.1:8777/progress.html` the normal learning entry and static opening read-only only.

## Verification

- Text scan confirmed `CONVERSION_PROTOCOL.md` no longer contains the old `python3 -m http.server 8000`, `localhost:8000/progress.html`, or “ROUNDS 数组（progress.html）” guidance.
- Static checks passed: `git diff --check`, Markdown relative link check, `node --check progress_ui.js`, Python compile checks, and JSON validation.
- Project checks passed: `check_protocol_sync.py`, `validate_learning_data.py`, `bash mark_done.sh --lane engineering --limit 3`, and `npm run check:mcp`.
- `npm run check:cursor-mcp` still reports CLI-layer tools as not loaded / needing approval, with `filesystem` not approved at the CLI layer; this thread's filesystem tools worked normally.
- Browser checks passed on the default Web UI and a Round 02 engineering route with no horizontal overflow or console errors.
