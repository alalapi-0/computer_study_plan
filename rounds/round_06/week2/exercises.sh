#!/bin/bash
# Round 06 · Week 2 练习：进程管理与长任务

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

mkdir -p ~/cli-lab/round6/week2
cd ~/cli-lab/round6/week2

cat > sleep_worker.sh <<'EOF'
#!/bin/bash
echo "worker started: $(date)"
sleep 3
echo "worker finished: $(date)"
EOF

chmod +x sleep_worker.sh
./sleep_worker.sh

echo "当前 shell 相关进程（示例）："
ps aux | grep -E "sleep|bash" | grep -v grep || true

mark r06-w2-ex2

echo "请手动尝试一次 nohup 或 tmux 后按回车继续..."
read
mark r06-w2-self

echo "Week 2 完成。"
