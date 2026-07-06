#!/bin/bash
# Round 01 · Week 1 练习：路径与目录切换

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

mkdir -p ~/cli-lab/round1/{notes,practice,test}
cd ~/cli-lab/round1

echo "Round 01 Week 1：路径切换实验"
echo
echo "当前路径："
pwd

echo "目录内容："
ls

echo
echo "依次进入 notes、practice、test，观察 pwd 输出："
cd notes
pwd
cd ..
cd practice
pwd
cd ../test
pwd
cd ~/cli-lab/round1

mark r01-w1-ex1

cat > path_review.txt <<'EOF'
Week 1 复盘提示：
- pwd 告诉你当前目录。
- cd notes 使用相对路径。
- cd ~/cli-lab/round1 使用绝对路径（从家目录开始）。
- cd .. 回到上一级目录。
EOF

echo
echo "脚本已完成练习任务 r01-w1-ex1。"
echo "下一步：在 Web UI 的“终端练习”中不看提示完成自测，再点击“记录并完成”保存 r01-w1-self。"
