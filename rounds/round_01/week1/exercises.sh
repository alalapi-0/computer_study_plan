#!/bin/bash
# Round 01 · Week 1 练习：路径与目录切换

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

mkdir -p ~/cli-lab/round1/{notes,practice,test}
cd ~/cli-lab/round1

echo "当前路径："
pwd

echo "目录内容："
ls

cd notes
pwd
cd ..
cd practice
pwd
cd ../test
pwd
cd ~/cli-lab/round1

mark r01-w1-ex1

echo "请手动完成第1周自测后按回车继续..."
read
mark r01-w1-self

echo "Week 1 完成。"
