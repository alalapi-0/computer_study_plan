#!/bin/bash
# Round 03 · Final 综合练习（Web UI 可运行）

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
LAB="$HOME/cli-lab/round3/final_auto"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

rm -rf "$LAB"
mkdir -p "$LAB"
cd "$LAB"

cat > mini_analyzer.py <<'EOF'
def summarize(labels):
    result = {}
    for x in labels:
        result[x] = result.get(x, 0) + 1
    return result

data = ["ok", "ok", "error", "warn", "ok", "error"]
print(summarize(data))

def estimate_ops(n):
    return {"linear": n, "quadratic": n * n}

for n in [10, 100]:
    print(n, estimate_ops(n))
EOF

python3 mini_analyzer.py

cat > final_notes.md <<'EOF'
# Round 03 Final 自动练习产物

- mini_analyzer.py：统计标签出现次数，并打印线性 / 平方级操作量估算。
- 这只是自动综合练习。
- 小抄 r03-fin-sheet 与验收 r03-fin-acc1 仍需用户自己阅读、解释并在 Web UI 点击“记录并完成”保存记录。
EOF

mark r03-fin-comp

echo "Round 03 Final 自动练习完成。请继续在 Web UI 点击“记录并完成”保存 r03-fin-sheet 与 r03-fin-acc1。"
