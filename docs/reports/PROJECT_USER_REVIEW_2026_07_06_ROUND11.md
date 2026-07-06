# Project User Review · Round 11 · 2026-07-06

## Review Scope

- Mobile and desktop Web UI at `progress.html`.
- Collapsed management area behavior.
- Default learning workspace copy after terminal auto-binding.
- Task list labels versus actual button text.
- Terminal history documentation after the record workflow changes.

## Findings

1. **The management area says it is collapsed but still renders its content**
   Browser inspection showed `details.open=false`, while `#saves`, lane tabs, and other management cards still had visible layout rectangles. This directly undermines the goal of reducing page clutter.

2. **Side-rail copy still says engineering tasks need opening the terminal**
   The side-rail usage note says engineering tasks should open the terminal later, but engineering tasks now auto-bind the terminal.

3. **Inline reader empty state still says engineering tasks can bind the terminal**
   The empty reader copy still describes a manual binding model. It should match the current auto-linked workspace behavior.

4. **Task list copy says `阅读` but the actual button says `读教程`**
   The task-list helper text tells users to click `阅读`, while visible task buttons are labeled `读教程`. Small mismatch, but it adds avoidable friction.

5. **Terminal history README still references old completion buttons**
   `records/terminal/README.md` says completion is based on Web UI `完成 / 记录`, but the current workflow uses `记录并完成` plus completed-task record review.

## Fix Direction

- Explicitly hide `.secondary-tools-body` when the `details` element is closed.
- Update side-rail and inline-reader copy to describe terminal auto-linking.
- Align task-list helper text with the visible `读教程` button.
- Update terminal history docs to the current `记录并完成 / 记录回看` workflow.
