# Project User Review · Round 9 · 2026-07-06

## Review Scope

- CLI status flow via `bash mark_done.sh`, including output size and learner-facing filters.
- README quick start, daily workflow, and Web UI / CLI descriptions after Round 8.
- Default Web UI desktop page at `progress.html`.
- Engineering task flow at `progress.html?round=round_00`, including auto-bound terminal and quick commands.
- Stage 0-7 panel wording and visual interpretation.

## Findings

1. **CLI default status is still too large for quick review**
   `bash mark_done.sh` now shows readable task titles, but the no-argument output is still 316 lines. For a daily status command, that feels like a report dump rather than a quick next-step view.

2. **CLI has no useful filters for the learner's current lane**
   The README only documented full status, mark done, and undo. A learner who only wants soft exam or engineering tasks has no discoverable way to narrow the output.

3. **Terminal copy is stale after auto-binding**
   README and Web UI still describe the terminal as something that appears when the task row shows `终端练习`. After Round 8 the right terminal auto-binds for engineering tasks, so the docs make the improved behavior sound manual.

4. **Terminal quick commands include a missing file**
   The quick command list offered `cat next_steps.txt`, but the default Round 00 sandbox does not contain that file. The first guided command should not lead to a `No such file` result.

5. **Stage panel reads like exact stage progress even though it is approximate**
   Stage 2 and Stage 3 both mirror `soft_exam`, while Stage 5 and Stage 6 both mirror `cs408`. Without explicit wording, duplicate lane percentages look like real stage acceptance progress.

## Fix Direction

- Make no-argument CLI status compact by default, while keeping `--all` for the complete list.
- Add `--lane` and `--limit` status options and document them in README.
- Update terminal copy to say engineering tasks auto-bind, and `终端练习` switches or refocuses.
- Replace unsafe quick commands with commands that work in the default sandbox, adding week-specific navigation only when applicable.
- Rename the Stage panel to a reference view and mark lane-derived percentages as approximate.
