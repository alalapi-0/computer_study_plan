# Project User Review 2026-07-06 Round 17

## Scope

- Master roadmap and knowledge mapping consistency after the soft exam module count changes.
- Math2 and 408 plan links against actual files under `plans/`.
- 408 / 0854 tasks in Web UI generated data.

## Findings

1. `docs/MASTER_STUDY_ROADMAP.md` still referred to the knowledge mapping as a 20-module table after the table had moved to 24 learning modules.

2. `docs/KNOWLEDGE_MAPPING.md` pointed math2 rows to `plans/math2/calculus.md` and `plans/math2/linear_algebra.md`, but the actual startup skeletons are `limits.md` and `la_matrix.md`.

3. `plans/408/README.md` still labeled its module skeleton column as "on demand" even though all four 408 skeletons now exist.

4. The Web UI exposed only one `cs408` task even though `plans/408/` now has four module skeletons plus the overview.

5. The only `cs408` task used ID `cs408-ds-start` while opening `plans/408/README.md`, so the data-structure task ID did not point to the data-structure skeleton.

## Fixes

- Updated the master roadmap reference from 20 modules to 24 learning modules.
- Updated math2 knowledge mapping rows to point at the real `limits.md` and `la_matrix.md` startup skeletons.
- Changed the 408 README table header to describe existing skeleton files, not files still to create.
- Changed the math2 README table headers to the same neutral skeleton-file wording while leaving not-yet-created modules as plain future filenames.
- Added `cs408-overview-start`, `cs408-composition-start`, `cs408-os-start`, and `cs408-network-start` to generated plan tasks.
- Retargeted `cs408-ds-start` to `plans/408/ds.md` and rebuilt `rounds_data.js`, `progress.json`, `progress_data.js`, and task feedback.

## Verification

- Before browser check confirmed `progress.html?lane=cs408` only showed `0/1` and no 408 module skeleton tasks.
- Generated data now contains five `cs408` tasks: overview, data structures, composition, operating systems, and networks.
- Static checks passed: `git diff --check`, Markdown relative link check, `node --check progress_ui.js`, Python compile checks, and JSON validation.
- Project checks passed: `check_protocol_sync.py`, `validate_learning_data.py`, `compileall`, `bash mark_done.sh --lane cs408`, and `npm run check:mcp`.
- `npm run check:cursor-mcp` still reports CLI-layer tools as not loaded / needing approval, with `filesystem` not approved at the CLI layer; this thread's filesystem tools worked normally.
- After browser check confirmed `progress.html?lane=cs408` shows `0/5`, all five 408 tasks are visible, `cs408-ds-start` opens `plans/408/ds.md`, desktop/mobile checks showed no horizontal overflow, and no console errors were recorded.
