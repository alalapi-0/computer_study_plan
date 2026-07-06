# Project User Review · Round 8 · 2026-07-06

## Review Scope

- CLI status flow via `bash mark_done.sh`.
- Default Web UI desktop page at `progress.html`.
- 390px mobile view of the default learning workspace.
- Engineering task flow at `progress.html?round=round_00`, including inline reader and browser terminal.
- README, project state, and next-action queue after the Round 7 fixes.

## Findings

1. **CLI status output is not readable enough for learners**
   `bash mark_done.sh` groups by lane, but each row only shows a task id such as `soft_exam-ds-start`. A learner has to cross-reference the Web UI or `rounds_data.js` to know what the id means.

2. **Stage 0 looks unfinished even though governance setup is complete**
   The Stage panel shows `Stage 0 · 治理准备` with `—`. In the current repo, Stage 0 governance is complete as repository setup, while user learning progress is tracked by later stages. The dash reads like missing data.

3. **The weak-lane rule hides all current exam startup lanes**
   The UI says weak items require task count >= 5 and some started progress. Current soft-exam, math2, and 408 startup lanes have fewer tasks and 0%, so the panel says nothing useful at the exact moment when the learner needs a startup prompt.

4. **Engineering terminal is visible but starts unbound**
   At `round=round_00`, the current task, reader, and terminal are on the same desktop screen, but the terminal initially says `未绑定任务`. The user must click `终端练习` before the right pane matches the current tutorial.

5. **README undersells the difference between Web UI and CLI**
   README lists the CLI commands, but it does not explain that Web UI is the recommended learning flow and CLI is best for quick status,补标记, and undo. That makes the two entry points feel equally complete when they are not.

## Fix Direction

- Enrich CLI rows with task title and week/group context from `rounds_data.js`.
- Show Stage 0 as a completed governance state instead of `—`.
- Replace the weak-only panel with a current attention model: small 0% startup lanes show `启动中`, while started low-progress lanes show `薄弱项`.
- Auto-bind the terminal to the current engineering task without stealing focus or scrolling.
- Clarify README CLI usage and update project state / next action queue for this round.
