#!/bin/bash
# Round 05 · Final 综合练习（Web UI 可运行）

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
LAB="$HOME/cli-lab/round5/final_auto"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

rm -rf "$LAB"
mkdir -p "$LAB"
cd "$LAB"

cat > pattern_selector_demo.py <<'EOF'
def choose_pattern(problem):
    text = problem.lower()
    if "有序" in text and ("查找" in text or "边界" in text):
        return "二分"
    if "连续子数组" in text or "窗口" in text:
        return "滑动窗口"
    if "全排列" in text or "组合" in text:
        return "回溯"
    if "最短路径" in text or "按层" in text:
        return "BFS"
    if "子问题重叠" in text or "最优子结构" in text:
        return "DP"
    return "先尝试建模再判断"

samples = [
    "在有序数组中查找第一个大于 x 的位置",
    "求连续子数组最大和",
    "列出字符串所有全排列",
    "网格中求最短路径",
]

for s in samples:
    print(s, "=>", choose_pattern(s))
EOF

python3 pattern_selector_demo.py

cat > final_notes.md <<'EOF'
# Round 05 Final 自动练习产物

- pattern_selector_demo.py：根据题面关键词给出初步算法模式建议。
- 这只是自动综合练习。
- 小抄 r05-fin-sheet 与验收 r05-fin-acc1 仍需用户自己阅读、解释并在 Web UI 点击“记录并完成”保存记录。
EOF

mark r05-fin-comp

echo "Round 05 Final 自动练习完成。请继续在 Web UI 点击“记录并完成”保存 r05-fin-sheet 与 r05-fin-acc1。"
