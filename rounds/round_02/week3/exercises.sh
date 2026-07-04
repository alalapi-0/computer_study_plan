#!/bin/bash
# =============================================================
# Round 02 · Week 3 练习脚本
# 主题：Git 最小工作流
# 用法：bash rounds/round_02/week3/exercises.sh
#
# 本脚本对应 progress.json 中的任务：
#   r02-w3-read  → 阅读 week3/notes.md（手动打卡）
#   r02-w3-ex7   → 练习7：初始化与首次提交
#   r02-w3-ex8   → 练习8：第二次提交
#   r02-w3-ex9   → 练习9：新增文件再提交
#   r02-w3-self  → 第3周自测
# =============================================================

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

LAB="$HOME/cli-lab/round2/week3/git_lab_auto"
rm -rf "$LAB"
mkdir -p "$LAB"
cd "$LAB"

git init -b main >/dev/null 2>&1 || git init >/dev/null
git config user.name "Round 02 Bot"
git config user.email "round02@example.local"
git config commit.gpgsign false

echo "========================================"
echo "练习 7：首次提交"
echo "========================================"
echo "# round2 git lab" > README.md
git status
git add README.md
git commit -m "init repository"
git log --oneline -n 3
mark r02-w3-ex7

echo "========================================"
echo "练习 8：第二次提交"
echo "========================================"
echo "this repo is for round2 practice" >> README.md
git status
git add README.md
git commit -m "update readme"
git log --oneline -n 3
mark r02-w3-ex8

echo "========================================"
echo "练习 9：新增文件提交"
echo "========================================"
echo "pipeline practice notes" > notes.txt
git status
git add notes.txt
git commit -m "add notes"
git log --oneline -n 5
mark r02-w3-ex9

cat > next_steps.txt <<'EOF'
Week 3 下一步：
- 在 Web UI 练习终端中进入 ~/cli-lab/round2/week3/git_lab_manual。
- 自己完成 git init / status / add / commit / log。
- 确认能解释 status 与 log 后，再手动标记 r02-w3-self。
EOF

echo "脚本已完成 r02-w3-ex7 / r02-w3-ex8 / r02-w3-ex9。"
echo "阅读任务与自测任务请在 Web UI 中确认后手动完成。"
