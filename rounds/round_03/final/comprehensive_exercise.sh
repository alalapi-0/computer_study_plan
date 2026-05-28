#!/bin/bash
# Round 03 · Final 综合练习

set -e

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
echo "Final 完成。"
