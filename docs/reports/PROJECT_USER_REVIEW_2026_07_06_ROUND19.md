# Project User Review 2026-07-06 Round 19

## Scope

- Engineering Round README and final review pages that are likely to be copied by the learner.
- Consistency between written Web UI entry points and the current local service at port 8777.
- Residual relative `progress.html` routes outside historical status logs.

## Findings

1. `rounds/round_01/README.md` described the learner opening bare `progress.html`, which does not tell the learner to use the current local API service.

2. `rounds/round_02/README.md` repeated the same bare `progress.html` entry even though Round 02 relies on the same Web UI / terminal flow.

3. `rounds/round_10/final/python_engineering_cheatsheet.md` told the learner to open `progress.html?round=round_10`, leaving the host and port implicit.

4. `rounds/round_11/final/sqlite_persistence_cheatsheet.md` used the same relative Web UI route for the final review path.

5. `rounds/round_16/README.md` and `rounds/round_17/README.md` started with relative `progress.html?round=...` links before later showing the full 8777 URL, creating inconsistent entry guidance inside the same page.

## Fixes

- Replaced the Round 01 and Round 02 intro URLs with full `http://127.0.0.1:8777/progress.html?round=...` entries.
- Replaced the Round 10 and Round 11 final cheatsheet Web UI paths with full local-service URLs.
- Replaced the Round 16 and Round 17 intro URLs with the same full local-service format used in their Web UI path sections.

## Verification

- Text scan confirmed the affected Round files no longer contain relative `progress.html?round=round_...` entry points.
- Static checks passed: `git diff --check`, Markdown relative link check, `node --check progress_ui.js`, Python compile checks, and JSON validation.
- Project checks passed: `check_protocol_sync.py`, `validate_learning_data.py`, `bash mark_done.sh --lane engineering --limit 3`, and `npm run check:mcp`.
- `npm run check:cursor-mcp` still reports CLI-layer tools as not loaded / needing approval, with `filesystem` not approved at the CLI layer; this thread's filesystem tools worked normally.
- Browser checks passed on Round 01, Round 10, Round 16, and mobile Round 17 routes with no horizontal overflow or console errors.
