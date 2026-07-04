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
day1: linux practice
day2: learned pwd ls cd
day3: learned mkdir touch
day4: learned cp mv rm
day5: learned cat
day6: learned less
day7: learned head tail
day8: reviewed paths
day9: reviewed files
day10: reviewed commands
EOF

echo "Round 01 Week 3：查看文本与帮助"
echo
echo "cat 输出："
cat study_log.txt

echo
echo "head -n 3 输出："
head -n 3 study_log.txt

echo
echo "tail -n 4 输出："
tail -n 4 study_log.txt

mark r01-w3-ex3

echo
echo "脚本已完成练习任务 r01-w3-ex3。"
echo "下一步：在 Web UI 的练习终端中手动执行 less study_log.txt 和 man ls；浏览器会直接显示输出，确认理解后再标记 r01-w3-self。"
