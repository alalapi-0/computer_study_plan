# Project User Review · Round 7 · 2026-07-06

## Review Scope

- Default Web UI desktop and 390px mobile behavior at `progress.html`.
- Current task flow, record modal, terminal binding, and engineering fallback at `round=round_02`.
- README, Stage plan, soft-exam/math2/408 startup pages, and terminal path consistency after the Round 6 fixes.
- Tooling state: `npm run check:mcp` passed. Cursor CLI MCP status is known to report `needs approval` for some servers; live UI inspection used the available in-app browser path.

## Findings

1. **The completion instructions describe the wrong order**  
   README and the task-flow copy say to write a record and then click `记录并完成`, but the actual UI opens the record editor after clicking that button. Users should be told to click the button, write the record in the modal, then save.

2. **The record modal examples are not task-aware**  
   The note placeholder always uses a soft-exam example, and the evidence placeholder always points to `~/cli-lab/round0/week1`. That is misleading for math2, 408, soft-exam overview, and later engineering rounds.

3. **Terminal binding shows a shorthand path that conflicts with the docs**  
   The terminal panel explains the sandbox as `~/cli-lab`, but after binding Round 02 it displays `~/round2`. Some Round 21 instructions also use `~/round21/...`. Outside the browser terminal those paths mean a different location, so users can copy the wrong command into a real shell.

4. **Stage 2 still describes the soft-exam entry as an empty Stage 0 artifact**  
   `docs/STAGE_PLAN.md` says `plans/soft_exam/README.md` is a module list plus progress table created empty in Stage 0. The file now has live links and startup skeletons, so the stage plan is stale.

5. **Startup pages do not say what counts as a completed reading task**  
   The Web UI has reading tasks for soft-exam, math2, and 408 startup materials, but those pages mostly list modules and pacing. A learner can read them without knowing what concrete artifact to write before clicking `记录并完成`.

## Fix Direction

- Rewrite README and in-page task flow copy around the actual record modal.
- Generate record/evidence placeholders from the task lane and file path.
- Display terminal cwd as `~/cli-lab/...` and remove remaining `~/roundN` user-facing commands.
- Update Stage 2 wording to match the current soft-exam startup state.
- Add lightweight "minimum artifact" sections to startup pages so reading tasks have a clear completion bar.
