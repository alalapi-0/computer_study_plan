# Project User Review 2026-07-06 Round 21

## Scope

- Root Round overview documents `round_16.md` through `round_21.md`.
- Web UI entry URLs, button names, and completion language in those overview pages.
- Consistency between root overview guidance and the current Web UI task flow.

## Findings

1. `round_16.md` still told learners to use “打开资料”, “运行”, “终端”, and then manually mark completion, while the current UI uses `读教程`, `运行脚本`, `终端练习`, and `记录并完成`.

2. `round_17.md` repeated the same obsolete button names and manual-completion language.

3. `round_18.md` used a relative `progress.html?round=round_18` entry and old “打开 / 运行 / 终端 / 记录” wording.

4. `round_19.md` used a relative `progress.html?round=round_19` entry and old “运行 / 终端” wording.

5. `round_20.md` told learners they could use bare `progress.html`, described notes as opening in a popup, and used old “运行 / 终端” task language.

6. `round_21.md` still instructed the learner to start the local server on port 8787 and finish through “记录 / 完成”, conflicting with the current port 8777 and `记录并完成` flow.

## Fixes

- Updated `round_16.md` and `round_17.md` to use `读教程`, `运行脚本`, `终端练习`, and `记录并完成`.
- Updated `round_18.md` and `round_19.md` to use full `http://127.0.0.1:8777/progress.html?round=...` entries and current task button names.
- Updated `round_20.md` to point to the 8777 Round route, describe inline note reading, and use current task button names.
- Updated `round_21.md` from port 8787 to port 8777 and replaced old completion wording with `记录并完成`.

## Verification

- Text scan confirmed `round_16.md` through `round_21.md` no longer contain the targeted old Web UI button names, relative Round URLs, or the stale 8787 Round 21 route.
- Static checks passed: `git diff --check`, Markdown relative link check, `node --check progress_ui.js`, Python compile checks, and JSON validation.
- Project checks passed: `check_protocol_sync.py`, `validate_learning_data.py`, `bash mark_done.sh --lane engineering --limit 3`, and `npm run check:mcp`.
- `npm run check:cursor-mcp` still reports CLI-layer tools as not loaded / needing approval, with `filesystem` not approved at the CLI layer; this thread's filesystem tools worked normally.
- Browser checks passed on Round 16 and Round 21 routes, including a 390px mobile Round 21 check, with no horizontal overflow or console errors.
