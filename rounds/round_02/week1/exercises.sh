#!/bin/bash
# =============================================================
# Round 02 · Week 1 练习脚本
# 主题：重定向与管道
# 用法：bash rounds/round_02/week1/exercises.sh
#
# 本脚本对应 progress.json 中的任务：
#   r02-w1-read  → 阅读 week1/notes.md（手动打卡）
#   r02-w1-ex1   → 练习1：覆盖与追加
#   r02-w1-ex2   → 练习2：去重统计
#   r02-w1-ex3   → 练习3：日志过滤
#   r02-w1-self  → 第1周自测
# =============================================================

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

echo ">>> 准备工作：创建 ~/cli-lab/round2/week1"
mkdir -p ~/cli-lab/round2/week1
cd ~/cli-lab/round2/week1

echo "========================================"
echo "练习 1：覆盖与追加"
echo "========================================"
echo "apple" > fruits.txt
echo "banana" >> fruits.txt
echo "orange" >> fruits.txt
cat fruits.txt
mark r02-w1-ex1

echo "========================================"
echo "练习 2：去重统计"
echo "========================================"
cat > animals.txt <<'EOF'
cat
dog
cat
bird
dog
cat
EOF
sort animals.txt | uniq > animals_unique.txt
sort animals.txt | uniq | wc -l > animal_kinds.txt
cat animals_unique.txt
cat animal_kinds.txt
mark r02-w1-ex2

echo "========================================"
echo "练习 3：日志过滤"
echo "========================================"
cat > app.log <<'EOF'
error: login failed
info: job started
error: file missing
info: job finished
EOF
grep "error" app.log > errors_only.txt
grep "info" app.log | wc -l > info_count.txt
cat errors_only.txt
cat info_count.txt
mark r02-w1-ex3

echo "========================================"
echo "第 1 周自测"
echo "========================================"
echo "请手敲一条命令：grep \"error\" app.log | wc -l"
echo "完成后按回车继续..."
read
mark r02-w1-self

echo "🎉 Round 02 Week 1 完成。阅读任务请手动打卡：bash mark_done.sh r02-w1-read"
