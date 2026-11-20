"""0/1 Knapsack by Dynamic Programming: choose parcels for one trip.

weight   -> parcel weight (kg)
value    -> parcel priority score
capacity -> truck capacity (kg)
Time O(n*W), space O(n*W) for the full table (needed to backtrack).
"""


def knapsack(parcels, capacity):
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w, v = parcels[i - 1]["weight"], parcels[i - 1]["priority"]
        for c in range(capacity + 1):
            dp[i][c] = dp[i - 1][c]                       # skip parcel i
            if w <= c and dp[i - 1][c - w] + v > dp[i][c]:
                dp[i][c] = dp[i - 1][c - w] + v           # take parcel i

    # Backtrack to recover which parcels were chosen
    chosen, c = [], capacity
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            chosen.append(parcels[i - 1])
            c -= parcels[i - 1]["weight"]
    chosen.reverse()
    return dp[n][capacity], chosen, dp


def print_dp_table(dp, parcels, max_cols=15):
    """Print the DP table (first max_cols capacities) as evidence."""
    cols = min(len(dp[0]), max_cols)
    print("DP table (rows = parcels considered, cols = capacity 0.." + str(cols - 1) + ")")
    print("        " + " ".join(f"{c:>4}" for c in range(cols)))
    for i, row in enumerate(dp):
        label = "none" if i == 0 else parcels[i - 1]["id"]
        print(f"{label:>7} " + " ".join(f"{v:>4}" for v in row[:cols]))
