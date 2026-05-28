#!/bin/bash
# Round 01 · Week 1 练习：路径与目录切换

set -e

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

echo "Week 1 完成。"
