#!/bin/bash
# Round 01 · Week 2 练习：文件创建与整理

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

mkdir -p ~/cli-lab/round1/week2/{input,output,backup}
cd ~/cli-lab/round1/week2

touch input/a.txt input/b.txt
cp input/a.txt backup/a_copy.txt
mv input/b.txt output/result.txt
touch delete_me.txt
rm delete_me.txt

echo "当前结构："
ls -R
mark r01-w2-ex2

echo "请手动完成第2周自测后按回车继续..."
read
mark r01-w2-self

echo "Week 2 完成。"
