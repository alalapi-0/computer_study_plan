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

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

LAB="$HOME/cli-lab/round2/week1/script_lab"
echo ">>> 准备工作：创建 $LAB"
mkdir -p "$LAB"
cd "$LAB"

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

cat > next_steps.txt <<'EOF'
Week 1 下一步：
- 在 Web UI “终端练习”中进入 ~/cli-lab/round2/week1/self_check。
- 自己创建 app.log。
- 手敲 grep "error" app.log | wc -l。
- 确认能解释 >、>>、| 后，再点击“记录并完成”保存 r02-w1-self。
EOF

echo "脚本已完成 r02-w1-ex1 / r02-w1-ex2 / r02-w1-ex3。"
echo "阅读任务与自测任务请在 Web UI 中点击“记录并完成”保存记录。"
