#!/bin/bash
# Round 01 · Week 2 练习：文件创建与整理

set -e

mkdir -p ~/cli-lab/round1/week2/{input,output,backup}
cd ~/cli-lab/round1/week2

touch input/a.txt input/b.txt
cp input/a.txt backup/a_copy.txt
mv input/b.txt output/result.txt
touch delete_me.txt
rm delete_me.txt

echo "当前结构："
ls -R
echo "Week 2 完成。"
