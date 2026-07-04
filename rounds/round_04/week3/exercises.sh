#!/bin/bash
# Round 04 · Week 3 练习：dict 计数与 set 去重（Web UI 可运行）

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
LAB="$HOME/cli-lab/round4/week3_auto"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

rm -rf "$LAB"
mkdir -p "$LAB"
cd "$LAB"

cat > hash_demo.py <<'EOF'
labels = ["ok", "blur", "ok", "bad", "blur", "ok"]
freq = {}
for x in labels:
    freq[x] = freq.get(x, 0) + 1
print("freq:", freq)
print("unique:", sorted(set(labels)))
print("has bad:", "bad" in set(labels))
EOF

python3 hash_demo.py

cat > next_steps.txt <<'EOF'
Week 3 自动练习已生成 hash_demo.py。

自测请在 Web UI 点 r04-w3-self 的“终端”，进入 ~/cli-lab/round4 后自己完成：
1. 新建 week3_self 目录。
2. 写一个 tag_report.py，使用 dict.get 计数并用 set 去重。
3. 运行 python3 tag_report.py。
4. 能解释 dict、set 与 list 遍历查找的差异后，手动点“记录 / 完成”。
EOF

mark r04-w3-ex3

echo "Week 3 自动练习完成。请继续手动完成 r04-w3-self。"
