"""
Number of Islands II - Bug Analysis and Fix

Problem: Given an m x n grid, positions are added one by one.
After each position, return the number of islands.

Bugs in the original code:
1. def init instead of def __init__
2. grid initialization references undefined grid
3. find() has incorrect recursion
4. union() doesn't decrement count
5. Method name mismatch: addSet vs add
"""

from typing import List

class BuggySetUnion:
    """Original buggy code"""
    def init(self, row, col):  # ❌ BUG 1: Should be __init__
        self.row = row
        self.col = col
        self.parent = {}
        self.count = 0
        self.rank = {}

    def addSet(self, x, y):  # ❌ BUG 5: Called as 'add' but named 'addSet'
        if (x,y) not in self.parent:
            self.parent[(x,y)] = (x,y)
            self.count += 1
            self.rank[(x,y)] = 0

    def hashRowCol(self, x, y):  # Not used, also has bug
        val = row * self.col + y + 1  # ❌ 'row' should be 'x'
        return val

    def find(self, i, j):
        if (i,j) != self.parent[(i,j)]:
            # ❌ BUG 3: Infinite recursion! Calls find(i,j) again
            self.parent[(i,j)] = self.find(i,j)
        return self.parent[(i,j)]

    def union(self, x1, y1, x2, y2):
        s_x = self.find(x1, y1)
        s_y = self.find(x2, y2)
        if s_x == s_y:
            return False
        else:
            if self.rank[s_x] < self.rank[s_y]:
                self.parent[s_x] = s_y
            elif self.rank[s_x] > self.rank[s_y]:
                self.parent[s_y] = s_x
            else:
                self.parent[s_x] = s_y
                self.rank[s_y] += 1
        # ❌ BUG 4: Missing self.count -= 1
        return True


class CorrectSetUnion:
    """Fixed version"""
    def __init__(self, row, col):  # ✓ FIX 1: Double underscores!
        self.row = row
        self.col = col
        self.parent = {}
        self.count = 0
        self.rank = {}

    def add(self, x, y):  # ✓ FIX 5: Match the method name
        if (x, y) not in self.parent:
            self.parent[(x, y)] = (x, y)
            self.count += 1
            self.rank[(x, y)] = 0

    def find(self, x, y):
        if (x, y) not in self.parent:
            return None

        # ✓ FIX 3: Path compression - recursively find parent's coordinates
        if self.parent[(x, y)] != (x, y):
            self.parent[(x, y)] = self.find(*self.parent[(x, y)])
        return self.parent[(x, y)]

    def union(self, x1, y1, x2, y2):
        root1 = self.find(x1, y1)
        root2 = self.find(x2, y2)

        if root1 is None or root2 is None:
            return False

        if root1 == root2:
            return False  # Already connected

        # Union by rank
        if self.rank[root1] < self.rank[root2]:
            self.parent[root1] = root2
        elif self.rank[root1] > self.rank[root2]:
            self.parent[root2] = root1
        else:
            self.parent[root1] = root2
            self.rank[root2] += 1

        self.count -= 1  # ✓ FIX 4: Decrement count when merging!
        return True

    def connected(self, x1, y1, x2, y2):
        return self.find(x1, y1) == self.find(x2, y2)


class Solution:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        uf = CorrectSetUnion(m, n)
        ans = []
        # ✓ FIX 2: Use m and n, not undefined grid!
        grid = [[0 for _ in range(n)] for _ in range(m)]
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

        for x, y in positions:
            # Skip if already processed
            if grid[x][y] == 1:
                ans.append(uf.count)
                continue

            grid[x][y] = 1
            uf.add(x, y)

            # Check all 4 neighbors
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < m and 0 <= new_y < n and grid[new_x][new_y] == 1:
                    uf.union(x, y, new_x, new_y)

            ans.append(uf.count)

        return ans


def explain_bugs():
    """Detailed explanation of each bug"""
    print("="*70)
    print("BUG ANALYSIS: Number of Islands II")
    print("="*70)
    print()

    print("BUG 1: Constructor Name")
    print("-" * 70)
    print("❌ WRONG:")
    print("    def init(self, row, col):")
    print()
    print("Why this fails:")
    print("  - Python constructors must be named __init__ (double underscores)")
    print("  - Without __init__, the class has no constructor")
    print("  - Error: 'SetUnion() takes no arguments'")
    print()
    print("✓ CORRECT:")
    print("    def __init__(self, row, col):")
    print()

    print("BUG 2: Grid Initialization")
    print("-" * 70)
    print("❌ WRONG:")
    print("    grid = [[0 for i in range(len(grid[0]))] for j in range(len(grid))]")
    print()
    print("Why this fails:")
    print("  - References 'grid' before it's defined!")
    print("  - grid doesn't exist yet, so len(grid) and len(grid[0]) fail")
    print()
    print("✓ CORRECT:")
    print("    grid = [[0 for _ in range(n)] for _ in range(m)]")
    print("    # Use the parameters m and n!")
    print()

    print("BUG 3: Infinite Recursion in find()")
    print("-" * 70)
    print("❌ WRONG:")
    print("    def find(self, i, j):")
    print("        if (i,j) != self.parent[(i,j)]:")
    print("            self.parent[(i,j)] = self.find(i,j)  # Calls itself with same args!")
    print()
    print("Why this fails:")
    print("  - find(i, j) calls find(i, j) → infinite recursion!")
    print("  - Should recurse on the PARENT's coordinates")
    print()
    print("✓ CORRECT:")
    print("    def find(self, x, y):")
    print("        if self.parent[(x, y)] != (x, y):")
    print("            self.parent[(x, y)] = self.find(*self.parent[(x, y)])")
    print("            # Unpack parent tuple and recurse on those coordinates")
    print()

    print("BUG 4: Missing Count Decrement")
    print("-" * 70)
    print("❌ WRONG:")
    print("    def union(self, x1, y1, x2, y2):")
    print("        # ... merge logic ...")
    print("        return True  # Missing count decrement!")
    print()
    print("Why this is wrong:")
    print("  - When two islands merge, total count should decrease by 1")
    print("  - Without this, count keeps growing even when islands merge")
    print()
    print("✓ CORRECT:")
    print("    def union(self, x1, y1, x2, y2):")
    print("        # ... merge logic ...")
    print("        self.count -= 1  # Decrement when merging!")
    print("        return True")
    print()

    print("BUG 5: Method Name Mismatch")
    print("-" * 70)
    print("❌ WRONG:")
    print("    class SetUnion:")
    print("        def addSet(self, x, y):  # Named 'addSet'")
    print()
    print("    # But called as:")
    print("    setUnion.add(x, y)  # Called as 'add'")
    print()
    print("✓ CORRECT:")
    print("    Either rename method to 'add' OR call it as 'addSet'")
    print()


def test_solution():
    """Test the corrected solution"""
    print("="*70)
    print("TESTING CORRECTED SOLUTION")
    print("="*70)
    print()

    solution = Solution()

    # Test case
    m, n = 3, 3
    positions = [[0,0], [0,1], [1,2], [2,1]]

    print(f"Grid: {m}x{n}")
    print(f"Positions: {positions}")
    print()

    result = solution.numIslands2(m, n, positions)

    print("Step-by-step:")
    for i, (x, y) in enumerate(positions):
        print(f"  After adding ({x},{y}): {result[i]} island(s)")

    print()
    print(f"Result: {result}")
    print(f"Expected: [1, 1, 2, 3]")
    print()


if __name__ == "__main__":
    explain_bugs()
    print()
    test_solution()

    print("="*70)
    print("SUMMARY OF FIXES")
    print("="*70)
    print()
    print("1. def init → def __init__ (constructor needs double underscores)")
    print("2. grid = [[...grid...]] → grid = [[...m,n...]] (use parameters)")
    print("3. find(i,j) → find(*parent[(i,j)]) (recurse on parent coords)")
    print("4. Add self.count -= 1 in union() when merging")
    print("5. Rename addSet to add OR call it as addSet consistently")
    print("="*70)
