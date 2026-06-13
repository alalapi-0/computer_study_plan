#!/bin/bash
# Round 06 · Week 3 练习：SSH / rsync / crontab

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

mkdir -p ~/cli-lab/round6/week3
cd ~/cli-lab/round6/week3

cat > sync_demo.txt <<'EOF'
This file is used for rsync/scp command rehearsal.
EOF

echo "示例命令（不会自动执行远程连接）："
echo "  ssh user@host"
echo "  scp sync_demo.txt user@host:~/round6/"
echo "  rsync -avz sync_demo.txt user@host:~/round6/"
echo "  crontab -e"

echo "请手动写出一条测试 cron 表达式后按回车继续..."
read
echo "Week 3 完成。"

mark r06-w3-ex3

echo "请手动完成第3周自测后按回车继续..."
read
mark r06-w3-self
