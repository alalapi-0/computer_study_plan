#!/bin/bash
# Round 01 · Week 3 练习：查看文本与帮助

set -e

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

echo "建议手动执行并退出：man ls"
echo "Week 3 完成。"
