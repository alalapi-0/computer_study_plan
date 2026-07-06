# Project User Review 2026-07-06 Round 14

## Scope

- Default Web UI entry, non-engineering lanes, Round 12 / Round 21, and mobile default page.
- `README.md`, `docs/PROGRESS_RULES.md`, `docs/KNOWLEDGE_MAPPING.md`.
- `plans/linux/`, `plans/soft_exam/`, and `plans/408/`.

## Findings

1. `docs/PROGRESS_RULES.md` still described progress as mainly written by `mark_done.sh`, while the current primary workflow is Web UI `记录并完成` plus JSONL action logs.

2. The same progress rules still called weekly tasks and countdowns `占位`, although the page already stores those settings in browser `localStorage`.

3. `README.md` labeled `round_12/ … round_21/` as later engineering/data/AI rounds even though they are already expanded and connected to Web UI.

4. `plans/linux/README.md` still routed Round 02 / Round 06 learners to root overview files instead of the expanded `rounds/round_02/` and `rounds/round_06/` Web UI practice directories.

5. Soft exam and 408 planning documents pointed to key P0 module files that did not exist yet: soft exam `composition.md`, `network.md`, `se.md`, plus 408 `ds.md`, `os.md`, `network.md`, and `composition.md`.
   This made the default soft exam reader feel like a list of missing next steps rather than a usable study entry.

## Fixes

- Updated progress rules to describe Web UI, local API, action logs, generated feedback, localStorage weekly tasks, and countdowns.
- Renamed the README Round 12–21 directory label so it no longer implies those rounds are only future work.
- Pointed Linux plan entries at the expanded Round 02 / Round 06 directories and current 8777 Web UI URLs.
- Added soft exam startup skeletons for computer composition, networking, and software engineering.
- Added 408 startup skeletons for data structures, operating systems, networking, and computer composition, then linked them from soft exam, 408 README, and knowledge mapping.

## Verification

- Static checks passed: `git diff --check`, Markdown relative link check, stale text scan, `node --check progress_ui.js`, Python compile checks, JSON validation, and `compileall`.
- Project checks passed: `check_protocol_sync.py`, `validate_learning_data.py`, `bash mark_done.sh`, and `npm run check:mcp`.
- `npm run check:cursor-mcp` listed CLI-layer tools; `filesystem` still reports not approved at the Cursor CLI layer, while this thread's filesystem tools worked normally.
- Browser checks passed: soft exam overview exposes and opens `composition.md`, `network.md`, and `se.md`; 408 overview exposes and opens `ds.md`, `os.md`, `network.md`, and `composition.md`.
- Desktop and 390px mobile checks showed no horizontal overflow and no console errors.
