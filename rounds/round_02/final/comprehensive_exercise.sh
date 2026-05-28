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

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

mkdir -p ~/cli-lab/round2/final_pipeline_lab
cd ~/cli-lab/round2/final_pipeline_lab

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

mark r02-fin-comp

echo "请手动完成并检查 rounds/round_02/final/command_cheatsheet.md 后按回车..."
read
mark r02-fin-sheet

echo "请口头回答验收问题后按回车："
echo "1) >、>>、| 有什么区别？"
read
mark r02-fin-acc1

mkdir -p ~/cli-lab/round2/final_git_lab
cd ~/cli-lab/round2/final_git_lab
if [ ! -d .git ]; then
  git init
fi
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

echo "请确认你能解释这 3 次提交后按回车..."
read
mark r02-fin-acc2

echo "🎉 Round 02 Final 完成。"
