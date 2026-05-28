#!/bin/bash
# Round 01 · Week 3 练习：查看文本与帮助

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

mkdir -p ~/cli-lab/round1/week3
cd ~/cli-lab/round1/week3

cat > study_log.txt <<'EOF'
day1: pwd ls cd
day2: mkdir touch
day3: cp mv rm
day4: cat less
day5: head tail
EOF

cat study_log.txt
head -n 2 study_log.txt
tail -n 2 study_log.txt

mark r01-w3-ex3

echo "建议手动执行并退出：man ls"
echo "完成后按回车继续..."
read
mark r01-w3-self

echo "Week 3 完成。"
