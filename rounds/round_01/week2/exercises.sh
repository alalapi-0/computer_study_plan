#!/bin/bash
# Round 01 · Week 2 练习：文件创建与整理

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

mkdir -p ~/cli-lab/round1/week2/{input,output,backup}
cd ~/cli-lab/round1/week2

echo "Round 01 Week 2：创建、复制、改名、删除"
echo

touch input/x.txt input/y.txt
cp input/x.txt backup/x_copy.txt
mv input/y.txt output/result.txt
touch delete_me.txt

echo "删除前确认："
pwd
ls
rm delete_me.txt

echo "当前结构："
find . -maxdepth 3 -type f | sort
mark r01-w2-ex2

echo
echo "脚本已完成练习任务 r01-w2-ex2。"
echo "下一步：在 Web UI 的“终端练习”中独立整理 week2_test，再点击“记录并完成”保存 r01-w2-self。"
