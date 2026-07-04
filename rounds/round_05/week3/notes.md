# Round 05 · Week 3 笔记（贪心 / DP 入门）

## 本周目标

- 区分“局部最优即可”的贪心问题和“子问题重叠”的 DP 问题。
- 完成一个最小 DP 例题（如爬楼梯）。

## 在 Web UI 中怎么学

1. 点“练习：贪心选择与 DP 爬楼梯”的“运行”，查看自动生成的 `greedy_dp_demo.py`。
2. 点“自测：自己写 coin_change_dp.py”的“终端”，在 `~/cli-lab/round5` 下完成自测脚本。
3. 推荐自测命令：

```bash
mkdir week3_self
cd week3_self
printf 'def coin_change(amount, coins):\n    dp = [0] + [10**9] * amount\n    for x in range(1, amount + 1):\n        for coin in coins:\n            if x >= coin:\n                dp[x] = min(dp[x], dp[x - coin] + 1)\n    return dp[amount] if dp[amount] < 10**9 else -1\n\nprint(coin_change(6, [1, 3, 4]))\nprint(coin_change(7, [2, 4]))\n' > coin_change_dp.py
python3 coin_change_dp.py
```

4. 能解释 `dp[x]` 表示什么、为什么贪心不一定总最优后，再手动记录自测完成。

## 贪心和 DP 的差异

- 贪心：每一步做眼前看起来最好的选择，并且这个选择不会破坏全局最优。
- DP：问题能拆成子问题，而且子问题会重复出现；用状态数组保存中间结果。
- 判断不出时，先尝试写出“状态是什么、转移是什么”，再决定是否是 DP。

## DP 三问

1. 状态是什么？例如 `dp[i]` 表示到第 `i` 阶的方法数。
2. 转移是什么？例如 `dp[i] = dp[i-1] + dp[i-2]`。
3. 初始值是什么？例如 `dp[1] = 1`，`dp[2] = 2`。

## 本周自查

- [ ] 能说明贪心与 DP 的判断差异
- [ ] 能手写一版基础 DP 状态转移
- [ ] 能解释一个贪心失败而 DP 可行的例子
