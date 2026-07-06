# Project User Review 2026-07-06 Round 22

## Scope

- Governance and progress-rule documents that define what the repository protects and how the Web UI is maintained.
- `docs/governance/file_naming_rules.md`
- `docs/governance/repo_rules.md`
- `docs/PROGRESS_RULES.md`

## Findings

1. `docs/governance/file_naming_rules.md` still described `progress.html` as a static dashboard, not the current Web UI learning workspace.

2. The same file omitted fixed names for `rounds_data.js`, `progress_ui.js`, and `scripts/progress_server.py`, even though those are now part of the protected progress system surface.

3. `docs/governance/repo_rules.md` described the repository payload as `progress.json` plus minimal `progress.html` display, underrepresenting the local API and Web UI workflow.

4. The governance layer table still listed the progress system as only `progress.json`, `progress_data.js`, `progress.html`, and `mark_done.sh`, omitting generated Round data, UI code, the local API, action logs, and feedback.

5. `docs/PROGRESS_RULES.md` described `progress.html` mainly as a display surface and referred to a `ROUNDS` structure, missing the current learning workspace, terminal, script runner, action log, task feedback, and `rounds_data.js` reality.

## Fixes

- Updated file naming rules to classify `progress.html` as the Web UI learning workspace and added fixed names for `rounds_data.js`, `progress_ui.js`, and `scripts/progress_server.py`.
- Updated repository governance rules to protect the current Web UI / local API progress system surface.
- Updated the progress-system layer table to include action logs and task feedback.
- Updated Progress Rules section 6 to describe the learning workspace, engineering terminal, script runner, `rounds_data.js`, action log, and task feedback.
- Extended integrity constraints to forbid manual editing of `rounds_data.js` and `records/feedback/task_feedback.json`.

## Verification

- Text scan confirmed governance/progress docs no longer describe `progress.html` as a static dashboard or minimal display.
- Static checks passed: `git diff --check`, Markdown relative link check, `node --check progress_ui.js`, Python compile checks, and JSON validation.
- Project checks passed: `check_protocol_sync.py`, `validate_learning_data.py`, `bash mark_done.sh --lane engineering --limit 3`, and `npm run check:mcp`.
- `npm run check:cursor-mcp` still reports CLI-layer tools as not loaded / needing approval, with `filesystem` not approved at the CLI layer; this thread's filesystem tools worked normally.
- Browser checks passed on the default Web UI and Round 00 route with no horizontal overflow or console errors.
