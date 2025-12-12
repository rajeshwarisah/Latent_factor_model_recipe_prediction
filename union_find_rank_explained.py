"""
Understanding RANK in Union-Find

Rank is used for the "Union by Rank" optimization to keep trees balanced.
"""

def explain_rank():
    print("="*70)
    print("WHAT IS RANK IN UNION-FIND?")
    print("="*70)
    print()

    print("DEFINITION:")
    print("-" * 70)
    print("Rank is an UPPER BOUND on the HEIGHT of the tree.")
    print()
    print("  - Initially, every node has rank 0 (single node tree, height 0)")
    print("  - When merging two trees of DIFFERENT rank, rank doesn't change")
    print("  - When merging two trees of SAME rank, rank increases by 1")
    print()

    print("WHY USE RANK?")
    print("-" * 70)
    print("Goal: Keep trees BALANCED (shallow) to make find() faster")
    print()
    print("Strategy: Always attach the SHORTER tree under the TALLER tree")
    print("  - This prevents the tree from growing too tall")
    print("  - Keeps find() operations fast")
    print()

    print("UNION BY RANK VISUALIZATION:")
    print("-" * 70)
    print()

    print("Example 1: Merging trees of DIFFERENT rank")
    print()
    print("  Tree A (rank=0)     Tree B (rank=1)")
    print("      0                   2")
    print("                         /")
    print("                        3")
    print()
    print("  Union(0, 2):")
    print("  - rank[rootA]=0 < rank[rootB]=1")
    print("  - Attach A under B (smaller under larger)")
    print()
    print("  Result (rank still 1):")
    print("      2")
    print("     / \\")
    print("    3   0")
    print()
    print("  ✓ Rank doesn't increase (tree height unchanged)")
    print()

    print("Example 2: Merging trees of SAME rank")
    print()
    print("  Tree A (rank=1)     Tree B (rank=1)")
    print("      0                   2")
    print("     /                   /")
    print("    1                   3")
    print()
    print("  Union(0, 2):")
    print("  - rank[rootA]==1 == rank[rootB]==1")
    print("  - Can attach either way, let's attach B under A")
    print("  - Increment rank[A] to 2")
    print()
    print("  Result (rank becomes 2):")
    print("      0")
    print("     / \\")
    print("    1   2")
    print("       /")
    print("      3")
    print()
    print("  ✓ Rank increases because tree height increased")
    print()


def rank_vs_size():
    print("="*70)
    print("RANK vs SIZE")
    print("="*70)
    print()

    print("RANK (upper bound on height):")
    print("-" * 70)
    print("  - Tells you how TALL the tree might be")
    print("  - Used in union by rank optimization")
    print("  - Goal: Attach shorter tree under taller tree")
    print("  - Rank ≤ log(n) for a set of size n")
    print()

    print("SIZE (number of elements):")
    print("-" * 70)
    print("  - Tells you how MANY nodes are in the tree")
    print("  - Used in union by size optimization")
    print("  - Goal: Attach smaller set under larger set")
    print("  - More intuitive, but slightly less theoretically optimal")
    print()

    print("BOTH WORK GREAT:")
    print("-" * 70)
    print("  - Both give O(α(n)) ≈ O(1) time complexity")
    print("  - Rank is more traditional in textbooks")
    print("  - Size is easier to understand and also useful for queries")
    print("  - Use whichever you prefer!")
    print()


def show_rank_evolution():
    """Show how rank evolves step by step"""
    print("="*70)
    print("STEP-BY-STEP RANK EVOLUTION")
    print("="*70)
    print()

    class UnionFind:
        def __init__(self, n):
            self.parent = list(range(n))
            self.rank = [0] * n

        def find(self, x):
            if self.parent[x] != x:
                self.parent[x] = self.find(self.parent[x])
            return self.parent[x]

        def union(self, x, y):
            rootX, rootY = self.find(x), self.find(y)
            if rootX == rootY:
                return

            if self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
                print(f"  Attach tree {rootX} (rank={self.rank[rootX]}) "
                      f"under tree {rootY} (rank={self.rank[rootY]})")
            elif self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
                print(f"  Attach tree {rootY} (rank={self.rank[rootY]}) "
                      f"under tree {rootX} (rank={self.rank[rootX]})")
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1
                print(f"  Attach tree {rootY} (rank={self.rank[rootY]}) "
                      f"under tree {rootX} (rank={self.rank[rootY]})")
                print(f"  → Increment rank[{rootX}] from {self.rank[rootX]-1} to {self.rank[rootX]}")

        def show_state(self):
            print(f"  Parent: {self.parent}")
            print(f"  Rank:   {self.rank}")

    uf = UnionFind(5)
    print("Initial state (5 nodes):")
    uf.show_state()
    print()

    print("Union(0, 1):")
    uf.union(0, 1)
    uf.show_state()
    print()

    print("Union(2, 3):")
    uf.union(2, 3)
    uf.show_state()
    print()

    print("Union(0, 2) - merging two trees of rank 1:")
    uf.union(0, 2)
    uf.show_state()
    print()

    print("Union(0, 4):")
    uf.union(0, 4)
    uf.show_state()
    print()


def why_path_compression_affects_rank():
    print("="*70)
    print("IMPORTANT NOTE: Path Compression and Rank")
    print("="*70)
    print()

    print("With path compression, rank is no longer the EXACT height.")
    print("It becomes an UPPER BOUND on the height.")
    print()

    print("Example:")
    print()
    print("  Before path compression:")
    print("      0 (rank=2)")
    print("     / \\")
    print("    1   2")
    print("       /")
    print("      3")
    print()
    print("  After find(3) with path compression:")
    print("      0 (rank=2)")
    print("     /|\\")
    print("    1 2 3")
    print()
    print("  - Tree height is now 1, but rank is still 2")
    print("  - Rank is now an UPPER BOUND, not exact height")
    print("  - This is fine! Rank still helps keep trees balanced")
    print()

    print("WHY DON'T WE UPDATE RANK?")
    print("-" * 70)
    print("  - Updating rank after path compression is expensive")
    print("  - Using rank as upper bound still works perfectly")
    print("  - The algorithm still achieves O(α(n)) time")
    print()


def interview_tip():
    print("="*70)
    print("INTERVIEW TIP: What to Say About Rank")
    print("="*70)
    print()

    print('If interviewer asks "What is rank?"')
    print()
    print('Good answer:')
    print('  "Rank is an upper bound on the height of the tree."')
    print('  "It helps us keep trees balanced by attaching shorter"')
    print('  "trees under taller trees during union operations."')
    print()

    print('If interviewer asks "Why not use size?"')
    print()
    print('Good answer:')
    print('  "Both work! Rank and size both give O(α(n)) complexity."')
    print('  "Rank is traditional, size is more intuitive. I can use"')
    print('  "either depending on if we need size information later."')
    print()

    print('If interviewer asks "Does rank change with path compression?"')
    print()
    print('Good answer:')
    print('  "No, we don\'t update rank during path compression. After"')
    print('  "path compression, rank becomes an upper bound rather than"')
    print('  "exact height, which is fine for the algorithm."')
    print()


if __name__ == "__main__":
    explain_rank()
    rank_vs_size()
    show_rank_evolution()
    why_path_compression_affects_rank()
    interview_tip()

    print("="*70)
    print("SUMMARY")
    print("="*70)
    print()
    print("Rank = Upper bound on tree height")
    print()
    print("Union by rank rule:")
    print("  1. If ranks different: attach smaller rank under larger rank")
    print("  2. If ranks same: attach either way, increment rank of new root")
    print()
    print("Purpose: Keep trees balanced → make find() fast")
    print()
    print("With path compression: rank becomes upper bound, not exact height")
    print()
    print("Alternative: Can use 'size' instead (same time complexity)")
    print("="*70)
