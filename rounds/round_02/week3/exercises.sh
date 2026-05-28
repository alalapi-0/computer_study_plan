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

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

mkdir -p ~/cli-lab/round2/week3/git_lab
cd ~/cli-lab/round2/week3/git_lab

if [ ! -d .git ]; then
  git init
fi

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

echo "========================================"
echo "第 3 周自测"
echo "========================================"
echo "请手敲并解释：git status / git log --oneline"
echo "完成后按回车继续..."
read
mark r02-w3-self

echo "🎉 Round 02 Week 3 完成。阅读任务请手动打卡：bash mark_done.sh r02-w3-read"
