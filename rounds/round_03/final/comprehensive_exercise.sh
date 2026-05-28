#!/bin/bash
# Round 03 · Final 综合练习

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

mkdir -p ~/cli-lab/round3/final
cd ~/cli-lab/round3/final

cat > mini_analyzer.py <<'EOF'
def summarize(labels):
    result = {}
    for x in labels:
        result[x] = result.get(x, 0) + 1
    return result

data = ["ok", "ok", "error", "warn", "ok", "error"]
print(summarize(data))
EOF

python3 mini_analyzer.py

mark r03-fin-comp

echo "请检查 rounds/round_03/final/complexity_cheatsheet.md 后按回车..."
read
mark r03-fin-sheet

echo "请确认你能解释线性与平方级复杂度差异后按回车..."
read
mark r03-fin-acc1

echo "Final 完成。"
