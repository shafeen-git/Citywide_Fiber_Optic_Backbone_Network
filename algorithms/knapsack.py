"""
Phase 1: 0/1 Knapsack Dynamic Programming.
Allocates a fixed capital upgrade budget to maximize structural resilience.
Complexity: O(N * W)
"""
from typing import List, Tuple
from models import RedundancyUpgrade


def allocate_redundancy_budget(
    upgrades: List[RedundancyUpgrade], budget: int
) -> Tuple[List[RedundancyUpgrade], int, int]:
    n = len(upgrades)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        item = upgrades[i - 1]
        for w in range(budget + 1):
            if item.cost <= w:
                dp[i][w] = max(
                    dp[i - 1][w],
                    dp[i - 1][w - item.cost] + item.resilience_gain
                )
            else:
                dp[i][w] = dp[i - 1][w]

    selected: List[RedundancyUpgrade] = []
    curr_w = budget
    for i in range(n, 0, -1):
        if dp[i][curr_w] != dp[i - 1][curr_w]:
            item = upgrades[i - 1]
            selected.append(item)
            curr_w -= item.cost

    selected.reverse()
    total_gain = dp[n][budget]
    total_spent = sum(item.cost for item in selected)
    return selected, total_gain, total_spent