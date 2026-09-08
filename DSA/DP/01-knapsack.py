def knapsackDP(wt, value, capacity):
    n= len(wt)
    dp = [[0]*(capacity +  1) for _ in range(n+1)]

    for i in range(1,n+1):
        for w in range(capacity+1):
            if wt[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - wt[i-1]]  + value[i-1])
            else:
                dp[i][w] = dp[i-1][w]

    print("Max Profit is ", dp[n][capacity])


weights = [2,3,4,5]
values = [3,4,5,6]

knapsackDP(weights, values, 5)