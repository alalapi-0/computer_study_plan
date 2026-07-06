#!/bin/bash
# Round 06 · Week 2 练习：进程查看与长任务日志（Web UI 可运行）

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
LAB="$HOME/cli-lab/round6/week2_auto"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

rm -rf "$LAB"
mkdir -p "$LAB"
cd "$LAB"

cat > worker.py <<'EOF'
import time

print("worker started")
time.sleep(0.2)
print("worker finished")
EOF

python3 worker.py > worker.log

echo "worker-log:"
cat worker.log

echo "process-sample:"
ps aux | grep -E "python|bash|zsh" | grep -v grep | head -5 | tee process_snapshot.txt || true

cat > long_task_notes.txt <<'EOF'
Week 2 自动练习已生成 worker.py、worker.log 和 process_snapshot.txt。

自测请在 Web UI 点 r06-w2-self 的“终端练习”，进入 ~/cli-lab/round6 后自己完成：
1. 新建 week2_self 目录。
2. 写一个 worker.py，让它 sleep 2 秒。
3. 用 python3 worker.py > worker.log & 放到后台运行。
4. 用 ps aux | grep worker.py 观察进程，用 cat worker.log 看输出。
5. 能解释后台运行、nohup、tmux 的差异后，点击“记录并完成”。
EOF

mark r06-w2-ex2

echo "Week 2 自动练习完成。请继续在 Web UI 点击“记录并完成”保存 r06-w2-self。"
