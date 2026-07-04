#!/bin/bash
# =============================================================
# Round 02 · Final 综合练习
# 主题：管道过滤 + Git 最小闭环
# 用法：bash rounds/round_02/final/comprehensive_exercise.sh
#
# 本脚本对应 progress.json 中的任务：
#   r02-fin-comp  → 综合练习执行
#   r02-fin-sheet → 完成 command_cheatsheet.md（手动确认后打卡）
#   r02-fin-acc1  → 验收1：解释重定向/管道
#   r02-fin-acc2  → 验收2：完成 3 次提交并查看历史
# =============================================================

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

PIPELINE_LAB="$HOME/cli-lab/round2/final_pipeline_lab_auto"
GIT_LAB="$HOME/cli-lab/round2/final_git_lab_auto"

rm -rf "$PIPELINE_LAB" "$GIT_LAB"
mkdir -p "$PIPELINE_LAB"
cd "$PIPELINE_LAB"

cat > app.log <<'EOF'
error: login failed
info: job started
warning: timeout
error: file missing
info: job finished
EOF

grep "error" app.log > errors_only.txt
grep "info" app.log > info_only.txt
grep "error" app.log | wc -l > error_count.txt

echo ">>> errors_only.txt"
cat errors_only.txt
echo ">>> error_count.txt"
cat error_count.txt

mkdir -p "$GIT_LAB"
cd "$GIT_LAB"
git init -b main >/dev/null 2>&1 || git init >/dev/null
git config user.name "Round 02 Bot"
git config user.email "round02@example.local"
git config commit.gpgsign false

echo "# final git lab" > README.md
git add README.md
git commit -m "init"
echo "round2 practice repo" >> README.md
git add README.md
git commit -m "add description"
echo "todo: learn git branch later" > todo.txt
git add todo.txt
git commit -m "add todo"
git log --oneline -n 5

mark r02-fin-comp

echo "脚本已完成综合练习 r02-fin-comp。"
echo "下一步：在 Web UI 中检查 command_cheatsheet.md，确认能解释重定向/管道和 3 次 Git 提交后，手动标记 r02-fin-sheet / r02-fin-acc1 / r02-fin-acc2。"
