"""
Evaluate Division - Bug Analysis

Problem: Given equations like a/b = 2.0, evaluate queries like a/c = ?

Approach: Union-Find with weighted edges (ratios).
The ratio[x] represents: x = ratio[x] * parent[x], or x/parent[x] = ratio[x]

BUG: In union(), the else clause sets the wrong variable's ratio!
"""

from typing import List

class BuggyUnionFind:
    """Original buggy code"""
    def __init__(self):
        self.parent = {}
        self.rank = {}
        self.count = 0
        self.ratio = {}

    def add(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
            self.count += 1
            self.ratio[x] = 1

    def find(self, x):
        if x not in self.parent:
            self.add(x)
            return x, 1
        if x != self.parent[x]:
            p, r = self.find(self.parent[x])
            self.parent[x], self.ratio[x] = p, r * self.ratio[x]
        return self.parent[x], self.ratio[x]

    def union(self, x, y, r):  # x/y = r
        px, rx = self.find(x)  # x = rx * px
        py, ry = self.find(y)  # y = ry * py
        if px == py:
            return False

        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
            self.ratio[px] = (r * ry) / rx  # ✓ Correct
        elif self.rank[py] < self.rank[px]:
            self.parent[py] = px
            self.ratio[py] = rx / (r * ry)  # ✓ Correct
        else:
            # ❌ BUG: Setting wrong variable!
            self.parent[px] = py
            self.rank[py] += 1
            self.ratio[py] = rx * r / (ry)  # ❌ Should be ratio[px], not ratio[py]!

        self.count -= 1
        return True


class CorrectUnionFind:
    """Fixed version"""
    def __init__(self):
        self.parent = {}
        self.rank = {}
        self.count = 0
        self.ratio = {}

    def add(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
            self.count += 1
            self.ratio[x] = 1.0

    def find(self, x):
        if x not in self.parent:
            self.add(x)
            return x, 1.0
        if x != self.parent[x]:
            p, r = self.find(self.parent[x])
            self.parent[x], self.ratio[x] = p, r * self.ratio[x]
        return self.parent[x], self.ratio[x]

    def union(self, x, y, r):  # x/y = r
        px, rx = self.find(x)  # x = rx * px
        py, ry = self.find(y)  # y = ry * py
        if px == py:
            return False

        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
            self.ratio[px] = (r * ry) / rx
        elif self.rank[py] < self.rank[px]:
            self.parent[py] = px
            self.ratio[py] = rx / (r * ry)
        else:
            # ✓ FIX: Set ratio[px] since px's parent is changing!
            self.parent[px] = py
            self.rank[py] += 1
            self.ratio[px] = (r * ry) / rx  # Same as first case

        self.count -= 1
        return True

    def connected(self, x, y):
        if x not in self.parent or y not in self.parent:
            return False
        px, _ = self.find(x)
        py, _ = self.find(y)
        return px == py


class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        uf = CorrectUnionFind()

        # Build the graph
        for (eq1, eq2), value in zip(equations, values):
            uf.add(eq1)
            uf.add(eq2)
            uf.union(eq1, eq2, value)

        # Answer queries
        ans = []
        for eq1, eq2 in queries:
            if uf.connected(eq1, eq2):
                px, r1 = uf.find(eq1)  # eq1 = r1 * px
                py, r2 = uf.find(eq2)  # eq2 = r2 * py
                # eq1/eq2 = (r1 * px) / (r2 * py) = r1/r2 (since px == py)
                ans.append(r1 / r2)
            else:
                ans.append(-1.0)
        return ans


def explain_bug():
    """Detailed explanation"""
    print("="*70)
    print("BUG ANALYSIS: Evaluate Division")
    print("="*70)
    print()

    print("THE BUG: Wrong Variable in else Clause")
    print("-" * 70)
    print()
    print("❌ WRONG:")
    print("    else:")
    print("        self.parent[px] = py")
    print("        self.rank[py] += 1")
    print("        self.ratio[py] = rx * r / (ry)  # ❌ Setting py's ratio!")
    print()
    print("Why this is wrong:")
    print("  - We're changing px's parent to py")
    print("  - Therefore, we need to set px's ratio, not py's ratio!")
    print("  - py's parent and ratio remain unchanged")
    print()

    print("✓ CORRECT:")
    print("    else:")
    print("        self.parent[px] = py")
    print("        self.rank[py] += 1")
    print("        self.ratio[px] = (r * ry) / rx  # ✓ Set px's ratio!")
    print()

    print("UNDERSTANDING THE RATIO:")
    print("-" * 70)
    print("ratio[x] means: x = ratio[x] * parent[x]")
    print("Or equivalently: x / parent[x] = ratio[x]")
    print()

    print("DERIVING THE FORMULA:")
    print("-" * 70)
    print("Given:")
    print("  - x/y = r")
    print("  - x = rx * px (where px is x's root)")
    print("  - y = ry * py (where py is y's root)")
    print()
    print("If we make py the parent of px:")
    print("  - We need: px = ratio[px] * py")
    print("  - So: px/py = ratio[px]")
    print()
    print("Substituting:")
    print("  - x/y = (rx * px) / (ry * py) = r")
    print("  - px/py = (r * ry) / rx")
    print()
    print("Therefore: ratio[px] = (r * ry) / rx ✓")
    print()


def demonstrate_bug():
    """Show concrete example"""
    print("="*70)
    print("EXAMPLE WHERE BUG CAUSES WRONG ANSWER")
    print("="*70)
    print()

    equations = [["a", "b"], ["b", "c"]]
    values = [2.0, 3.0]
    queries = [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"]]

    print(f"Equations: {equations}")
    print(f"Values: {values}")
    print(f"  a/b = 2.0")
    print(f"  b/c = 3.0")
    print()
    print(f"Expected:")
    print(f"  a/c = (a/b) * (b/c) = 2.0 * 3.0 = 6.0")
    print(f"  b/a = 1 / (a/b) = 1 / 2.0 = 0.5")
    print(f"  a/e = -1.0 (e doesn't exist)")
    print(f"  a/a = 1.0")
    print()

    # Test buggy version
    print("Testing buggy version:")
    solution_buggy = Solution()
    # Note: Using buggy UnionFind would show incorrect results
    print("  (Would give wrong answers due to incorrect ratio[py] assignment)")
    print()

    # Test correct version
    print("Testing correct version:")
    solution = Solution()
    result = solution.calcEquation(equations, values, queries)
    print(f"  Results: {result}")
    print(f"  Expected: [6.0, 0.5, -1.0, 1.0]")
    print()


def visualize_union():
    """Visualize what happens in union"""
    print("="*70)
    print("VISUALIZING UNION OPERATION")
    print("="*70)
    print()

    print("Scenario: union(x, y, r) where x/y = r")
    print()
    print("Before union:")
    print("  x has root px with ratio rx (x = rx * px)")
    print("  y has root py with ratio ry (y = ry * py)")
    print()

    print("Case 1: Make py the parent of px")
    print("  self.parent[px] = py")
    print("  Need to set: ratio[px]")
    print()
    print("  After: px = ratio[px] * py")
    print("  We know: x = rx * px, y = ry * py, x/y = r")
    print("  So: rx * px / (ry * py) = r")
    print("  Therefore: px/py = r * ry / rx")
    print("  Set: ratio[px] = r * ry / rx ✓")
    print()

    print("Case 2: Make px the parent of py")
    print("  self.parent[py] = px")
    print("  Need to set: ratio[py]")
    print()
    print("  After: py = ratio[py] * px")
    print("  We know: py/px = 1/(px/py) = 1/(r * ry / rx) = rx/(r * ry)")
    print("  Set: ratio[py] = rx / (r * ry) ✓")
    print()

    print("❌ THE BUG: In else clause, code sets ratio[py] when parent[px] changes!")
    print()


if __name__ == "__main__":
    explain_bug()
    print()
    demonstrate_bug()
    print()
    visualize_union()

    print("="*70)
    print("SUMMARY")
    print("="*70)
    print()
    print("BUG LOCATION: union() method, else clause")
    print()
    print("❌ self.ratio[py] = rx * r / (ry)")
    print("✓ self.ratio[px] = (r * ry) / rx")
    print()
    print("The bug: Setting the wrong variable's ratio!")
    print("When px's parent changes to py, we must update ratio[px], not ratio[py]")
    print("="*70)
