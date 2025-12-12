"""
Maximum Detonation - Bug Analysis

Problem: Find maximum number of bombs that can be detonated starting from one bomb.
Each bomb can trigger other bombs within its radius in a chain reaction.

Key insight: This is a DIRECTED graph problem, not undirected!
"""

from typing import List
from collections import defaultdict, deque

class BuggyVersion:
    """Original buggy code with issues identified"""
    def maximumDetonation(self, bombs: List[List[int]]) -> int:
        graph = defaultdict(list)

        # ❌ BUG 1: Graph construction is WRONG - making it bidirectional!
        for i, b1 in enumerate(bombs):
            for j in range(i+1, len(bombs)):
                b2 = bombs[j]
                if self.isrange(b1, b2[0], b2[1]):
                    graph[i].append(j)
                    graph[j].append(i)  # ❌ WRONG! Should be directed, not bidirectional
                elif self.isrange(b2, b1[0], b1[1]):
                    graph[j].append(i)
                    graph[i].append(j)  # ❌ WRONG! Should be directed, not bidirectional

        # ❌ BUG 3: Wrong algorithm - finds connected components,
        # but we need to try starting from EACH bomb!
        visited = {}
        vno = 0
        vnoDict = {}

        for i in range(len(bombs)):
            vno += 1
            if i not in visited:  # ❌ Only processes unvisited - WRONG!
                queue = deque()
                queue.append(i)
                visited[i] = vno
                vnoDict[vno] = 1
                while queue:
                    b = queue.popleft()
                    for n in graph[b]:
                        if n not in visited:
                            visited[n] = vno
                            vnoDict[vno] += 1
                            queue.append(n)

        return max(list(vnoDict.values()))

    def isrange(self, bomb, x, y):
        if (bomb[0] - x) ** 2 + (bomb[1] - y) ** 2 <= bomb[2] ** 2:
            return True
        else:
            False  # ❌ BUG 2: Missing "return" statement!


class CorrectVersion:
    """Fixed version"""
    def maximumDetonation(self, bombs: List[List[int]]) -> int:
        n = len(bombs)
        graph = defaultdict(list)

        # ✓ Build DIRECTED graph
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                # Check if bomb i can detonate bomb j
                if self.in_range(bombs[i], bombs[j]):
                    graph[i].append(j)  # Only add i -> j, not both directions!

        # ✓ Try starting from EACH bomb
        max_detonated = 0
        for start in range(n):
            # BFS from this starting bomb
            visited = set([start])
            queue = deque([start])

            while queue:
                curr = queue.popleft()
                for neighbor in graph[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

            max_detonated = max(max_detonated, len(visited))

        return max_detonated

    def in_range(self, bomb1, bomb2):
        """Check if bomb1 can detonate bomb2"""
        x1, y1, r1 = bomb1
        x2, y2, _ = bomb2
        dist_squared = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return dist_squared <= r1 ** 2


def explain_bugs():
    """Detailed explanation of each bug"""
    print("="*70)
    print("BUG ANALYSIS: Maximum Detonation")
    print("="*70)
    print()

    print("BUG 1: Graph Construction - Wrong Directionality")
    print("-" * 70)
    print("❌ WRONG:")
    print("    if self.isrange(b1, b2[0], b2[1]):")
    print("        graph[i].append(j)")
    print("        graph[j].append(i)  # Adding BOTH directions!")
    print()
    print("Why this is wrong:")
    print("  - Bomb A with radius 5 can detonate bomb B at distance 3")
    print("  - But bomb B with radius 1 CANNOT detonate bomb A!")
    print("  - This is a DIRECTED graph, not undirected")
    print()
    print("✓ CORRECT:")
    print("    if self.in_range(bombs[i], bombs[j]):")
    print("        graph[i].append(j)  # Only add i -> j")
    print()

    print("BUG 2: Missing Return Statement")
    print("-" * 70)
    print("❌ WRONG:")
    print("    def isrange(self, bomb, x, y):")
    print("        if condition:")
    print("            return True")
    print("        else:")
    print("            False  # Missing 'return'! Returns None!")
    print()
    print("✓ CORRECT:")
    print("    def in_range(self, bomb, x, y):")
    print("        if condition:")
    print("            return True")
    print("        else:")
    print("            return False")
    print()
    print("Or simpler:")
    print("    return (bomb[0] - x) ** 2 + (bomb[1] - y) ** 2 <= bomb[2] ** 2")
    print()

    print("BUG 3: Wrong Algorithm - Connected Components vs Reachability")
    print("-" * 70)
    print("❌ WRONG approach:")
    print("  - Find connected components")
    print("  - Only process unvisited nodes")
    print("  - Return size of largest component")
    print()
    print("Why this is wrong:")
    print("  - Problem asks: start from ONE bomb, how many can you detonate?")
    print("  - Need to try EVERY bomb as starting point")
    print("  - Find maximum reachable from any single starting bomb")
    print()
    print("✓ CORRECT approach:")
    print("  - Try starting from EACH bomb (0 to n-1)")
    print("  - For each start, do BFS/DFS to count reachable bombs")
    print("  - Return the maximum count")
    print()


def demonstrate_bug1():
    """Show why directed graph matters"""
    print("="*70)
    print("EXAMPLE: Why Graph Must Be Directed")
    print("="*70)
    print()

    bombs = [[1, 2, 3], [2, 1, 1]]
    print("Bombs: [[1, 2, 3], [2, 1, 1]]")
    print("  Bomb 0: position (1, 2), radius 3")
    print("  Bomb 1: position (2, 1), radius 1")
    print()

    # Calculate distance
    dist = ((1-2)**2 + (2-1)**2) ** 0.5
    print(f"Distance between bombs: {dist:.2f}")
    print()

    print("Can bomb 0 detonate bomb 1?")
    print(f"  Distance {dist:.2f} <= radius 3? YES ✓")
    print("  → Add edge 0 -> 1")
    print()

    print("Can bomb 1 detonate bomb 0?")
    print(f"  Distance {dist:.2f} <= radius 1? NO ✗")
    print("  → Do NOT add edge 1 -> 0")
    print()

    print("CORRECT graph: 0 -> 1 (one-way)")
    print()
    print("BUGGY code would add:")
    print("  - In first check: adds 0 -> 1 AND 1 -> 0 (WRONG!)")
    print("  - This incorrectly says bomb 1 can detonate bomb 0")
    print()


def demonstrate_bug3():
    """Show why we need to try all starting points"""
    print("="*70)
    print("EXAMPLE: Why Try All Starting Points")
    print("="*70)
    print()

    print("Bombs with directed edges:")
    print("  Bomb 0 -> Bomb 1 -> Bomb 2")
    print("  Bomb 3 -> Bomb 4")
    print()
    print("Two separate chains.")
    print()

    print("❌ BUGGY approach (connected components):")
    print("  - Finds 2 components of sizes 3 and 2")
    print("  - Returns 3")
    print("  - But this assumes bidirectional connections!")
    print()

    print("✓ CORRECT approach (try each start):")
    print("  - Start from bomb 0: detonates 0, 1, 2 → count = 3")
    print("  - Start from bomb 1: detonates 1, 2 → count = 2")
    print("  - Start from bomb 2: detonates only 2 → count = 1")
    print("  - Start from bomb 3: detonates 3, 4 → count = 2")
    print("  - Start from bomb 4: detonates only 4 → count = 1")
    print("  - Maximum = 3 ✓")
    print()


def test_both_versions():
    """Test with example"""
    print("="*70)
    print("TESTING BOTH VERSIONS")
    print("="*70)
    print()

    bombs = [[2,1,3],[6,1,4]]
    print(f"Bombs: {bombs}")
    print("  Bomb 0 at (2,1) with radius 3")
    print("  Bomb 1 at (6,1) with radius 4")
    print()

    # Distance between them
    dist_sq = (2-6)**2 + (1-1)**2
    print(f"Distance squared: {dist_sq}")
    print(f"Bomb 0 radius squared: 9")
    print(f"Bomb 1 radius squared: 16")
    print()
    print(f"Can bomb 0 reach bomb 1? {dist_sq} <= 9? NO")
    print(f"Can bomb 1 reach bomb 0? {dist_sq} <= 16? YES")
    print()
    print("Correct graph: 1 -> 0 (only one direction)")
    print()

    correct = CorrectVersion()
    result = correct.maximumDetonation(bombs)
    print(f"Correct result: {result}")
    print("  - Start from bomb 0: detonates only bomb 0 → 1")
    print("  - Start from bomb 1: detonates bomb 1 and 0 → 2")
    print("  - Maximum: 2 ✓")
    print()


if __name__ == "__main__":
    explain_bugs()
    print()
    demonstrate_bug1()
    print()
    demonstrate_bug3()
    print()
    test_both_versions()

    print("="*70)
    print("SUMMARY OF FIXES")
    print("="*70)
    print()
    print("1. Graph must be DIRECTED - only add i->j if bomb i can reach j")
    print("2. Add 'return' before False in isrange function")
    print("3. Try EVERY bomb as starting point, not just connected components")
    print("4. For each start, count ALL reachable bombs via BFS/DFS")
    print("="*70)
