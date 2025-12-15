"""
Minimum Edge Reversals So Every Node Is Reachable

Problem: Given a directed graph, for each node, find the minimum number of
edge reversals needed to make all other nodes reachable from that node.

Key Insight: Use Re-rooting Technique
1. Calculate answer for node 0 (root)
2. Use that answer to calculate answers for all other nodes

Time: O(n)
Space: O(n)
"""

from typing import List
from collections import defaultdict

class Solution:
    def minEdgeReversals(self, n: int, edges: List[List[int]]) -> List[int]:
        """
        Two-pass DFS solution using re-rooting technique
        """
        # Build bidirectional graph with edge direction info
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append((v, 0))  # Forward edge, cost = 0
            graph[v].append((u, 1))  # Backward edge, cost = 1 (needs reversal)

        # First DFS: Calculate cost for root (node 0)
        reversals_from_0 = [0] * n

        def dfs1(node, parent):
            """Count reversals needed to reach all nodes from node 0"""
            for neighbor, cost in graph[node]:
                if neighbor == parent:
                    continue
                reversals_from_0[0] += cost
                dfs1(neighbor, node)

        dfs1(0, -1)

        # Second DFS: Calculate cost for all other nodes
        result = [0] * n
        result[0] = reversals_from_0[0]

        def dfs2(node, parent):
            """
            Use parent's answer to calculate current node's answer

            When moving from parent to child:
            - If edge was forward (parent → child), reversing root costs +1
            - If edge was backward (child → parent), reversing root costs -1
            """
            for neighbor, cost in graph[node]:
                if neighbor == parent:
                    continue

                # Key formula: child_cost = parent_cost - cost + (1 - cost)
                # Simplified: child_cost = parent_cost + 1 - 2*cost
                if cost == 0:
                    # Edge goes node → neighbor (forward)
                    # When neighbor becomes root, this edge needs reversal
                    result[neighbor] = result[node] + 1
                else:
                    # Edge goes neighbor → node (backward, already reversed)
                    # When neighbor becomes root, we save a reversal
                    result[neighbor] = result[node] - 1

                dfs2(neighbor, node)

        dfs2(0, -1)

        return result


class SolutionWithExplanation:
    """Version with detailed comments"""

    def minEdgeReversals(self, n: int, edges: List[List[int]]) -> List[int]:
        # Build graph with costs
        graph = defaultdict(list)
        for u, v in edges:
            # For edge u → v:
            # - Going u to v costs 0 (follow direction)
            # - Going v to u costs 1 (reverse direction)
            graph[u].append((v, 0))
            graph[v].append((u, 1))

        # Pass 1: Calculate answer for node 0
        def dfs1(node, parent):
            reversals = 0
            for neighbor, cost in graph[node]:
                if neighbor == parent:
                    continue
                # Cost represents if we need to reverse this edge
                reversals += cost
                reversals += dfs1(neighbor, node)
            return reversals

        result = [0] * n
        result[0] = dfs1(0, -1)

        # Pass 2: Calculate answers for all other nodes
        def dfs2(node, parent):
            for neighbor, cost in graph[node]:
                if neighbor == parent:
                    continue

                # When moving root from 'node' to 'neighbor':
                # - If edge was node→neighbor (cost=0): need to reverse it (+1)
                # - If edge was neighbor→node (cost=1): save a reversal (-1)
                result[neighbor] = result[node] + (1 if cost == 0 else -1)

                dfs2(neighbor, node)

        dfs2(0, -1)

        return result


def explain_concept():
    """Explain the re-rooting technique"""
    print("="*70)
    print("CONCEPT: Re-rooting Technique")
    print("="*70)
    print()

    print("Problem Setup:")
    print("-" * 70)
    print("Given: Directed graph with edges u → v")
    print("Goal: For each node as root, find min reversals to reach all nodes")
    print()

    print("Naive Approach: O(n²)")
    print("-" * 70)
    print("For each node:")
    print("  - Do DFS/BFS")
    print("  - Count how many edges need reversal")
    print("  - Total: n * O(n) = O(n²)")
    print()

    print("Smart Approach: O(n) using Re-rooting")
    print("-" * 70)
    print("1. Calculate answer for one node (say node 0)")
    print("2. Use that to calculate answers for all other nodes")
    print("   - When moving root from parent to child:")
    print("     * If edge was parent→child: cost increases by 1")
    print("     * If edge was child→parent: cost decreases by 1")
    print()


def visual_example():
    """Visual walkthrough"""
    print("="*70)
    print("VISUAL EXAMPLE")
    print("="*70)
    print()

    print("Graph: 0→1, 1→2, 0→3")
    print()
    print("       0")
    print("      ↙ ↘")
    print("     1   3")
    print("     ↓")
    print("     2")
    print()

    print("Step 1: Calculate for node 0 (root)")
    print("-" * 70)
    print("From node 0:")
    print("  0→1: cost 0 (follow direction)")
    print("  1→2: cost 0 (follow direction)")
    print("  0→3: cost 0 (follow direction)")
    print("Total reversals = 0")
    print()

    print("Step 2: Calculate for node 1")
    print("-" * 70)
    print("Move root from 0 to 1:")
    print("  Edge 0→1 needs reversal (was going away from 1)")
    print("  result[1] = result[0] + 1 = 0 + 1 = 1")
    print()
    print("From node 1:")
    print("  1→0: cost 1 (reversed)")
    print("  0→3: cost 0 (via 0)")
    print("  1→2: cost 0")
    print("Total = 1 ✓")
    print()

    print("Step 2: Calculate for node 2")
    print("-" * 70)
    print("Move root from 1 to 2:")
    print("  Edge 1→2 needs reversal")
    print("  result[2] = result[1] + 1 = 1 + 1 = 2")
    print()

    print("Step 2: Calculate for node 3")
    print("-" * 70)
    print("Move root from 0 to 3:")
    print("  Edge 0→3 needs reversal")
    print("  result[3] = result[0] + 1 = 0 + 1 = 1")
    print()

    print("Final answer: [0, 1, 2, 1]")
    print()


def detailed_walkthrough():
    """Detailed step-by-step"""
    print("="*70)
    print("DETAILED WALKTHROUGH")
    print("="*70)
    print()

    edges = [[0,1], [1,2], [0,3]]
    n = 4

    print(f"Input: n = {n}, edges = {edges}")
    print()

    print("Build Bidirectional Graph with Costs:")
    print("-" * 70)
    print("For each directed edge u → v:")
    print("  Add u → v with cost 0 (following direction)")
    print("  Add v → u with cost 1 (reversing direction)")
    print()

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append((v, 0))
        graph[v].append((u, 1))

    print("Graph:")
    for node in sorted(graph.keys()):
        print(f"  {node}: {graph[node]}")
    print()

    print("DFS 1: Calculate reversals from node 0")
    print("-" * 70)

    def dfs1(node, parent, depth=0):
        indent = "  " * depth
        print(f"{indent}Visit node {node}")
        reversals = 0
        for neighbor, cost in graph[node]:
            if neighbor == parent:
                continue
            print(f"{indent}  Edge to {neighbor}, cost={cost}")
            reversals += cost
            reversals += dfs1(neighbor, node, depth + 1)
        print(f"{indent}  Subtree reversals: {reversals}")
        return reversals

    total = dfs1(0, -1)
    print(f"Result for node 0: {total} reversals")
    print()

    print("DFS 2: Calculate for all other nodes")
    print("-" * 70)

    result = [0] * n
    result[0] = total

    def dfs2(node, parent, depth=0):
        indent = "  " * depth
        print(f"{indent}At node {node}, result={result[node]}")
        for neighbor, cost in graph[node]:
            if neighbor == parent:
                continue
            change = 1 if cost == 0 else -1
            result[neighbor] = result[node] + change
            print(f"{indent}  Move to {neighbor}: cost={cost}, change={change:+d}")
            print(f"{indent}  result[{neighbor}] = {result[node]} + {change} = {result[neighbor]}")
            dfs2(neighbor, node, depth + 1)

    dfs2(0, -1)

    print()
    print(f"Final result: {result}")
    print()


def formula_explanation():
    """Explain the formula"""
    print("="*70)
    print("THE KEY FORMULA")
    print("="*70)
    print()

    print("When moving root from parent to child:")
    print("-" * 70)
    print()

    print("Case 1: Edge is parent → child (cost = 0)")
    print("  - Currently: edge points away from child")
    print("  - When child becomes root: need to reverse this edge")
    print("  - Change: +1")
    print()
    print("  Example:")
    print("    Parent    Child")
    print("      P   →   C      (cost=0, following direction)")
    print()
    print("    When C is root, need:")
    print("      P   ←   C      (reversed, +1 reversal)")
    print()

    print("Case 2: Edge is child → parent (cost = 1)")
    print("  - Currently: edge already reversed to reach child")
    print("  - When child becomes root: don't need this reversal anymore")
    print("  - Change: -1")
    print()
    print("  Example:")
    print("    Parent    Child")
    print("      P   ←   C      (cost=1, was reversed)")
    print()
    print("    When C is root, need:")
    print("      P   ←   C      (already correct, -1 reversal)")
    print()

    print("Formula:")
    print("  result[child] = result[parent] + (1 if cost == 0 else -1)")
    print()


def test_solution():
    """Test the solution"""
    print("="*70)
    print("TESTING SOLUTION")
    print("="*70)
    print()

    solution = Solution()

    # Test case 1
    n = 4
    edges = [[0,1], [1,2], [0,3]]
    result = solution.minEdgeReversals(n, edges)

    print(f"Test 1:")
    print(f"  n = {n}")
    print(f"  edges = {edges}")
    print(f"  result = {result}")
    print(f"  expected = [0, 1, 2, 1]")
    print()

    # Test case 2
    n = 3
    edges = [[0,1], [2,0]]
    result = solution.minEdgeReversals(n, edges)

    print(f"Test 2:")
    print(f"  n = {n}")
    print(f"  edges = {edges}")
    print(f"  result = {result}")
    print(f"  expected = [1, 2, 0]")
    print()


if __name__ == "__main__":
    explain_concept()
    print()
    visual_example()
    print()
    formula_explanation()
    print()
    detailed_walkthrough()
    print()
    test_solution()

    print("="*70)
    print("ALGORITHM TEMPLATE")
    print("="*70)
    print("""
def minEdgeReversals(n, edges):
    # Build bidirectional graph with costs
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append((v, 0))  # Forward: free
        graph[v].append((u, 1))  # Backward: costs 1

    # DFS 1: Calculate for root (node 0)
    def dfs1(node, parent):
        reversals = 0
        for neighbor, cost in graph[node]:
            if neighbor != parent:
                reversals += cost
                reversals += dfs1(neighbor, node)
        return reversals

    result = [0] * n
    result[0] = dfs1(0, -1)

    # DFS 2: Calculate for all other nodes
    def dfs2(node, parent):
        for neighbor, cost in graph[node]:
            if neighbor != parent:
                # If forward edge: +1, if backward: -1
                result[neighbor] = result[node] + (1 if cost == 0 else -1)
                dfs2(neighbor, node)

    dfs2(0, -1)
    return result
    """)
    print("="*70)
