# Project User Review · Round 12 · 2026-07-06

## Review Scope

- README first-run path, repository tree, and progress wording.
- Round 00–21 README / notes / exercise prompts that a learner sees while following the Web UI.
- Current architecture and automation docs that guide future Codex rounds.
- URL and button-label consistency against the current Web UI labels: `读教程`、`运行脚本`、`终端练习`、`记录并完成`.

## Findings

1. **README still labeled Round 00 as completed**
   The repository tree described `rounds/round_00/` as `终端入门（已完成）`, while the current progress source has no real learner completion record. This makes an empty learning state look finished.

2. **Round 00 still told users to open the static page or `http.server 8000`**
   `rounds/round_00/README.md` and the final script both pointed at `open progress.html` / `python3 -m http.server 8000`, bypassing the current `scripts/progress_server.py` workflow and record API.

3. **Many Round README files used stale or inconsistent ports**
   Several Round entry pages still pointed to `8765`, `8778`, `8787`, or relative `progress.html?round=...` URLs. A learner following those instructions would not reliably land in the same Web UI described by the README.

4. **Round instructions used old button names**
   Round README files, notes, and script prompts still said `打开`、`阅读`、`运行`、`终端`、`记录 / 完成` or `完成 / 记录`, while the current page uses `读教程`、`运行脚本`、`终端练习` and `记录并完成`.

5. **Architecture / automation docs still reflected the early prototype**
   `docs/DECISIONS.md` still described `progress.html` as a limited static page, and the auto-advance protocol did not list all files required by the current repository rules.

## Fix Direction

- Reword Round 00 as material that is expanded and connected to Web UI, not learner-completed.
- Route Round 00 and all Round entry pages through `http://127.0.0.1:8777/progress.html?...`.
- Normalize learner-facing button names across Round README, notes, exercise output prompts, and final cheat sheets.
- Refresh ADR wording to match the current local API + JSON/JSONL architecture.
- Align auto-advance prerequisites with the current required reading list.
