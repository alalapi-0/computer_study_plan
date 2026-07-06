# Project User Review 2026-07-06 Round 18

## Scope

- Engineering Round learning notes that are opened through the Web UI inline reader.
- Sandbox path consistency between written instructions and the current browser terminal mapping.
- Round 21 entry URL consistency.

## Findings

1. `rounds/round_12/week1/notes.md` told the learner to work under `~/round12`, but the Web UI terminal maps Round 12 to `~/cli-lab/round12`.

2. `rounds/round_18/week1/notes.md` told the learner to work under `~/round18`, creating a mismatch with the actual `~/cli-lab/round18` sandbox.

3. `rounds/round_18/week2/notes.md` told the learner to record `~/round18` as evidence, which would point to the wrong local path.

4. Round 20 Week 1-3 self-test command blocks used `cd ~/round20/...` even though generated practice artifacts live under `~/cli-lab/round20/...`.

5. Round 21 Week 1-3 self-test command blocks used `cd ~/round21/...`; Week 1 also used a bare `progress.html?round=round_21` entry instead of the current local-service URL.

## Fixes

- Updated Round 12 Week 1 to use `~/cli-lab/round12`.
- Updated Round 18 Week 1 and Week 2 to use `~/cli-lab/round18`.
- Updated Round 20 Week 1-3 command blocks to use `~/cli-lab/round20/...`.
- Updated Round 21 Week 1-3 command blocks to use `~/cli-lab/round21/...`.
- Updated the Round 21 Week 1 entry step to the current `http://127.0.0.1:8777/progress.html?round=round_21` URL.

## Verification

- Text scan confirmed no remaining `~/round12`, `~/round18`, `~/round20`, or `~/round21` in the affected Round notes.
- Static checks passed: `git diff --check`, Markdown relative link check, `node --check progress_ui.js`, Python compile checks, and JSON validation.
- Project checks passed: `check_protocol_sync.py`, `validate_learning_data.py`, `bash mark_done.sh --lane engineering --limit 3`, and `npm run check:mcp`.
- `npm run check:cursor-mcp` still reports CLI-layer tools as not loaded / needing approval, with `filesystem` not approved at the CLI layer; this thread's filesystem tools worked normally.
- Browser checks passed on `progress.html?round=round_21`: the first Round 21 reader opens, the inline tutorial contains the new `~/cli-lab/round21/...` path and the full 8777 URL, desktop/mobile checks showed no horizontal overflow, and no console errors were recorded.
