# Project User Review 2026-07-06 Round 13

## Scope

- Web UI default and engineering task flow.
- README / CLI usage copy.
- Round 01 / 02 / 12 learner-facing notes and script prompts.
- Local action logs and generated feedback state.

## Findings

1. The terminal panel still used the old heading `练习终端`, while task buttons and current docs use `终端练习`.
   This makes the same feature appear to have two names in one workflow.

2. The completion flow still surfaced old `网页打卡` / `标记完成` / `打卡脚本` wording in banners, toasts, action labels, and run confirmations.
   The current UI requires a written record before completion, so the older wording underplays the record step.

3. Round 01, Round 02, and Round 12 notes still told learners to `手动标记` or `手动打卡`.
   Those instructions no longer match the visible `记录并完成` button and can make the learner search for a missing control.

4. `records/action_logs/events.jsonl` contained demo actions from 2026-06-15 even though `progress.json` is currently empty.
   The generated feedback therefore claimed some tasks had recently been undone, creating a false "used before" state.

5. The inline reader and script file actions used vague labels such as `弹窗打开` and `看脚本`.
   In a page that already contains tutorial, terminal, and completion controls, the labels should describe the exact action.

## Fixes

- Renamed the terminal panel and terminal record README to `终端练习`.
- Replaced remaining active UI/CLI completion wording with `网页记录`, `记录完成`, or `记录并完成` language.
- Rewrote Round 01 / 02 / 12 self-test prompts to say `点击“记录并完成”保存...`.
- Cleared the tracked demo action log and regenerated `records/feedback/task_feedback.json` from the empty action state.
- Renamed the inline tutorial popout to `单独打开教程` and script file action to `查看脚本`.

## Verification

- Static checks passed: `git diff --check`, `node --check progress_ui.js`, Python compile checks, JSON validation, and relevant shell syntax checks.
- Project checks passed: `check_protocol_sync.py`, `validate_learning_data.py`, `compileall`, `bash mark_done.sh`, and `npm run check:mcp`.
- `npm run check:cursor-mcp` listed CLI-layer tools; `filesystem` still reports not approved at the Cursor CLI layer, while this thread's filesystem tools worked normally.
- Browser checks passed on desktop and 390px mobile for `progress.html?round=round_02`: `终端练习`, `记录并完成`, `读教程`, `运行脚本`, and `单独打开教程` are visible; old active wording is absent; no horizontal overflow or console errors were observed.
- Empty record validation passed: clicking `记录并完成` without a note keeps the modal open, focuses the note field, shows `请先写一条本次记录，再保存完成`, and leaves `records/action_logs/events.jsonl` empty with progress at `0/304`.
