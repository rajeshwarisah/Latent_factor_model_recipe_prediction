from typing import List

class Solution:
    def calculateMinimumHP(self, dungeon: List[List[int]]) -> int:
        """
        Calculate minimum initial health for knight to reach princess.

        Strategy: Work backwards from destination to determine minimum health
        needed when entering each cell to survive till the end.

        dp[i][j] = minimum health required when entering cell (i,j) to survive
        """
        m, n = len(dungeon), len(dungeon[0])

        # Create DP table
        dp = [[float('inf')] * n for _ in range(m)]

        # Base case: bottom-right corner (destination)
        # We need at least 1 health after taking the cell's value
        # If dungeon[m-1][n-1] = -5, we need 1 - (-5) = 6 health before entering
        # If dungeon[m-1][n-1] = 10, we need max(1, 1 - 10) = 1 health before entering
        dp[m-1][n-1] = max(1, 1 - dungeon[m-1][n-1])

        # Fill last column (can only move down)
        for i in range(m - 2, -1, -1):
            # Health needed = health needed for next cell - current cell value
            # But must be at least 1
            dp[i][n-1] = max(1, dp[i+1][n-1] - dungeon[i][n-1])

        # Fill last row (can only move right)
        for j in range(n - 2, -1, -1):
            dp[m-1][j] = max(1, dp[m-1][j+1] - dungeon[m-1][j])

        # Fill rest of the table (bottom-up, right-to-left)
        for i in range(m - 2, -1, -1):
            for j in range(n - 2, -1, -1):
                # We can go right or down, choose the path requiring less health
                min_health_on_exit = min(dp[i+1][j], dp[i][j+1])
                # Health needed when entering this cell
                dp[i][j] = max(1, min_health_on_exit - dungeon[i][j])

        # The answer is the health needed at the starting position
        return dp[0][0]


# Test cases
if __name__ == "__main__":
    solution = Solution()

    # Example 1
    dungeon1 = [[-2,-3,3],[-5,-10,1],[10,30,-5]]
    result1 = solution.calculateMinimumHP(dungeon1)
    print(f"Example 1: {result1}")  # Expected: 7

    # Trace through optimal path: (0,0) -> (0,1) -> (0,2) -> (1,2) -> (2,2)
    # Start with 7: 7-2=5, 5-3=2, 2+3=5, 5+1=6, 6-5=1 ✓

    # Example 2
    dungeon2 = [[0]]
    result2 = solution.calculateMinimumHP(dungeon2)
    print(f"Example 2: {result2}")  # Expected: 1

    # Additional test
    dungeon3 = [[1, -3, 3], [0, -2, 0], [-3, -3, -3]]
    result3 = solution.calculateMinimumHP(dungeon3)
    print(f"Example 3: {result3}")
