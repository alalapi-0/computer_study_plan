#!/bin/bash
# Round 05 · Final 综合练习

set -e

mkdir -p ~/cli-lab/round5/final
cd ~/cli-lab/round5/final

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

echo "请完成一题算法模式归类并记录结论后按回车..."
read
echo "Final 完成。"
