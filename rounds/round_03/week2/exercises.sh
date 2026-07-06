#!/bin/bash
# Round 03 · Week 2 练习：list/dict 与函数拆分（Web UI 可运行）

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
LAB="$HOME/cli-lab/round3/week2_auto"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

rm -rf "$LAB"
mkdir -p "$LAB"
cd "$LAB"

cat > stats.py <<'EOF'
def count_labels(items):
    result = {}
    for item in items:
        result[item] = result.get(item, 0) + 1
    return result

labels = ["error", "info", "error", "warn", "info"]
print(count_labels(labels))
EOF

python3 stats.py

cat > report.py <<'EOF'
def load_scores():
    return [
        {"name": "alice", "score": 82},
        {"name": "bob", "score": 57},
        {"name": "carol", "score": 91},
    ]

def passing_names(rows):
    result = []
    for row in rows:
        if row["score"] >= 60:
            result.append(row["name"])
    return result

def main():
    rows = load_scores()
    print("passing:", passing_names(rows))

main()
EOF

python3 report.py

cat > next_steps.txt <<'EOF'
Week 2 自动练习已生成 stats.py 和 report.py。

自测请在 Web UI 点 r03-w2-self 的“终端练习”，进入 ~/cli-lab/round3 后自己完成：
1. 新建 week2_self 目录。
2. 写一个 count_words.py，使用 list、dict 和函数。
3. 运行 python3 count_words.py。
4. 能解释 dict.get(key, 0) 后，点击“记录并完成”。
EOF

mark r03-w2-ex2

echo "Week 2 自动练习完成。请继续在 Web UI 点击“记录并完成”保存 r03-w2-self。"
