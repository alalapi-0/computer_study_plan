# Project User Review 2026-07-06 Round 16

## Scope

- Soft exam module coverage in `docs/STAGE_PLAN.md`, `docs/MASTER_STUDY_ROADMAP.md`, and `docs/ERROR_REVIEW_SYSTEM.md`.
- Knowledge mapping consistency in `docs/KNOWLEDGE_MAPPING.md`.
- Progress task ID examples in `docs/PROGRESS_RULES.md`.

## Findings

1. `docs/STAGE_PLAN.md` still listed only 11 soft exam modules after the Web UI and soft exam README had moved to 12 modules.

2. The Stage 2 exit criteria still said 11 modules should each have a concept-map marker, which would leave the English reading module outside the checklist.

3. `docs/MASTER_STUDY_ROADMAP.md` omitted English reading from the soft exam main-line knowledge list, even though the module now exists and is registered in the UI.

4. `docs/ERROR_REVIEW_SYSTEM.md` described soft exam categories as "11 + English", which made English look separate from the actual 12-module soft exam closure.

5. `docs/KNOWLEDGE_MAPPING.md` still had 23 rows and no English-reading row, while `docs/PROGRESS_RULES.md` still showed the stale unregistered `soft-os-ch01` task ID.

## Fixes

- Added English reading to the Stage 2 soft exam module list and changed the exit criterion from 11 modules to 12 modules.
- Added English reading to the master roadmap soft exam knowledge list.
- Renamed the error-review soft exam category heading to "12 modules".
- Added a soft exam English reading row to the knowledge mapping table and updated the total row explanation from 23 to 24.
- Updated progress-rule task ID examples to use real current IDs such as `soft_exam-os-start`.
- Cleaned a template-only URL placeholder in `CONVERSION_PROTOCOL.md` so Markdown link checks do not treat it as a broken relative link.

## Verification

- Text scan confirmed no remaining `11 个模块`, `11 + 英语`, `23 行`, `soft-os-ch01`, `soft-<module>`, or `vps-05-readonly` in active docs outside historical reports.
- Static checks passed: `git diff --check`, Markdown relative link check, `node --check progress_ui.js`, Python compile checks, and JSON validation.
- Project checks passed: `check_protocol_sync.py`, `validate_learning_data.py`, `compileall`, `bash mark_done.sh`, and `npm run check:mcp`.
- `npm run check:cursor-mcp` still reports CLI-layer tools as not loaded / needing approval, with `filesystem` not approved at the CLI layer; this thread's filesystem tools worked normally.
- Browser checks passed on `progress.html?lane=soft_exam`: the page shows soft exam `0/13`, the English reading task appears, its inline tutorial opens to `英语阅读模块骨架`, desktop/mobile checks showed no horizontal overflow, and no console errors were recorded.
