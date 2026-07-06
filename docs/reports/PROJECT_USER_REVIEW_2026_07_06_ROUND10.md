# Project User Review · Round 10 · 2026-07-06

## Review Scope

- Default Web UI learning workspace and collapsed management area.
- Record modal validation for the default soft-exam task.
- Math2 route via `progress.html?lane=math2`.
- Plan docs under `plans/soft_exam/`, `plans/math2/`, and `plans/408/`.
- Local generated record files and Git cleanliness after normal Web UI use.

## Findings

1. **Soft-exam README has duplicate section numbers**
   The inline reader shows `## 6. 笔记写作规则` followed by another `## 6. 配套文件`. This makes the plan look less deliberate and harder to reference.

2. **Math2 overview contradicts the actual files**
   `plans/math2/README.md` says all note files are not pre-created, but `limits.md` and `la_matrix.md` already exist and are part of the current startup flow.

3. **Stage 3 mock-exam path is stale**
   `docs/STAGE_PLAN.md` points to `plans/soft_exam/mock_exams.md`, while the current records convention uses `records/weekly_reviews/mock_exams/` for mock exam records.

4. **Save snapshots can pollute Git status**
   Web UI save files are local JSON snapshots under `records/saves/`, but `.gitignore` did not exclude `records/saves/*.json`. A learner creating a normal save would see untracked files in Git.

5. **Terminal command history can also pollute Git status**
   Browser terminal history is written to `records/terminal/commands.jsonl`, but that generated local history was not ignored. Routine terminal practice would create another untracked file.

## Fix Direction

- Renumber soft-exam README sections.
- Update math2 overview to link the two existing startup skeleton files and describe only the remaining files as on-demand.
- Align Stage 3 mock-exam output path with the records convention.
- Ignore generated save snapshots and terminal command history while keeping their README files tracked.
- Document the local-only status of generated save and terminal history files.
