"""
Union-Find (Disjoint Set Union) - Interview Template

Essential operations:
- find(x): Find the root/representative of x's set
- union(x, y): Merge the sets containing x and y
- connected(x, y): Check if x and y are in the same set

Optimizations:
- Path compression: Make nodes point directly to root during find()
- Union by rank: Attach smaller tree under larger tree

Time Complexity: O(α(n)) ≈ O(1) amortized per operation
where α is the inverse Ackermann function (extremely slow growing)
"""

class UnionFind:
    """Clean implementation - easiest to memorize"""

    def __init__(self, n):
        """Initialize n elements (0 to n-1)"""
        self.parent = list(range(n))  # Each node is its own parent initially
        self.rank = [0] * n            # Rank for union by rank optimization
        self.count = n                 # Number of disjoint sets

    def find(self, x):
        """Find root of x with path compression"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        """Union sets containing x and y. Returns True if merged, False if already connected"""
        rootX = self.find(x)
        rootY = self.find(y)

        if rootX == rootY:
            return False  # Already in same set

        # Union by rank: attach smaller tree under larger tree
        if self.rank[rootX] < self.rank[rootY]:
            self.parent[rootX] = rootY
        elif self.rank[rootX] > self.rank[rootY]:
            self.parent[rootY] = rootX
        else:
            self.parent[rootY] = rootX
            self.rank[rootX] += 1

        self.count -= 1  # Decrease number of disjoint sets
        return True

    def connected(self, x, y):
        """Check if x and y are in the same set"""
        return self.find(x) == self.find(y)

    def get_count(self):
        """Return number of disjoint sets"""
        return self.count


class UnionFindWithSize:
    """Alternative: Track size instead of rank"""

    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n  # Size of each component
        self.count = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)

        if rootX == rootY:
            return False

        # Union by size: attach smaller to larger
        if self.size[rootX] < self.size[rootY]:
            self.parent[rootX] = rootY
            self.size[rootY] += self.size[rootX]
        else:
            self.parent[rootY] = rootX
            self.size[rootX] += self.size[rootY]

        self.count -= 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)

    def get_size(self, x):
        """Get size of the set containing x"""
        return self.size[self.find(x)]


# ============================================================================
# COMMON INTERVIEW PATTERNS
# ============================================================================

def pattern_1_number_of_connected_components():
    """Pattern 1: Count number of connected components"""
    print("="*70)
    print("PATTERN 1: Number of Connected Components")
    print("="*70)
    print()
    print("Problem: Given n nodes and list of edges, find number of components")
    print()

    n = 5
    edges = [[0,1], [1,2], [3,4]]

    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)

    print(f"Nodes: {n}")
    print(f"Edges: {edges}")
    print(f"Connected components: {uf.get_count()}")
    print(f"Expected: 2 (component {0,1,2} and component {3,4})")
    print()


def pattern_2_detect_cycle():
    """Pattern 2: Detect cycle in undirected graph"""
    print("="*70)
    print("PATTERN 2: Detect Cycle in Undirected Graph")
    print("="*70)
    print()
    print("Key idea: If both endpoints are already connected, adding edge creates cycle")
    print()

    n = 4
    edges = [[0,1], [1,2], [2,3], [3,0]]  # Forms a cycle

    uf = UnionFind(n)
    has_cycle = False

    for u, v in edges:
        if not uf.union(u, v):  # union returns False if already connected
            has_cycle = True
            print(f"Cycle detected when adding edge {[u, v]}")
            break

    print(f"Edges: {edges}")
    print(f"Has cycle: {has_cycle}")
    print()


def pattern_3_redundant_connection():
    """Pattern 3: Find redundant connection (LeetCode 684)"""
    print("="*70)
    print("PATTERN 3: Redundant Connection")
    print("="*70)
    print()
    print("Problem: Find the edge that creates a cycle")
    print()

    edges = [[1,2], [1,3], [2,3]]
    n = 3

    uf = UnionFind(n + 1)  # 1-indexed
    redundant = []

    for u, v in edges:
        if not uf.union(u, v):
            redundant = [u, v]
            break

    print(f"Edges: {edges}")
    print(f"Redundant edge: {redundant}")
    print(f"Expected: [2, 3] (creates cycle with existing path 2->1->3)")
    print()


def pattern_4_smallest_string_with_swaps():
    """Pattern 4: Group elements by connected components"""
    print("="*70)
    print("PATTERN 4: Smallest String with Swaps (LeetCode 1202)")
    print("="*70)
    print()
    print("Key idea: Indices connected by swaps can be rearranged freely")
    print()

    s = "dcab"
    pairs = [[0,3], [1,2]]

    n = len(s)
    uf = UnionFind(n)

    # Union indices that can be swapped
    for i, j in pairs:
        uf.union(i, j)

    # Group indices by their root
    from collections import defaultdict
    groups = defaultdict(list)
    for i in range(n):
        groups[uf.find(i)].append(i)

    result = list(s)
    for indices in groups.values():
        # Sort characters in this component
        chars = sorted([s[i] for i in indices])
        # Assign back to smallest positions
        indices.sort()
        for i, char in zip(indices, chars):
            result[i] = char

    print(f"String: {s}")
    print(f"Swap pairs: {pairs}")
    print(f"Result: {''.join(result)}")
    print(f"Expected: 'bacd'")
    print()
    print("Explanation:")
    print("  - Indices 0 and 3 can swap: 'd' <-> 'b'")
    print("  - Indices 1 and 2 can swap: 'c' <-> 'a'")
    print("  - Optimal: put smallest chars in each group first")
    print()


def pattern_5_accounts_merge():
    """Pattern 5: Accounts Merge (LeetCode 721)"""
    print("="*70)
    print("PATTERN 5: Accounts Merge")
    print("="*70)
    print()
    print("Key idea: Use Union-Find with dictionary mapping")
    print()

    accounts = [
        ["John", "john@mail.com", "john_work@mail.com"],
        ["John", "john@mail.com", "john_home@mail.com"],
        ["Mary", "mary@mail.com"]
    ]

    # Map email to account index
    email_to_id = {}
    uf = UnionFind(len(accounts))

    for i, account in enumerate(accounts):
        for email in account[1:]:
            if email in email_to_id:
                uf.union(i, email_to_id[email])
            else:
                email_to_id[email] = i

    # Group emails by root account
    from collections import defaultdict
    groups = defaultdict(list)
    for email, account_id in email_to_id.items():
        root = uf.find(account_id)
        groups[root].append(email)

    result = []
    for account_id, emails in groups.items():
        name = accounts[account_id][0]
        result.append([name] + sorted(emails))

    print("Accounts:")
    for acc in accounts:
        print(f"  {acc}")
    print()
    print("Merged:")
    for acc in result:
        print(f"  {acc}")
    print()


def pattern_6_earliest_friends():
    """Pattern 6: Process events chronologically"""
    print("="*70)
    print("PATTERN 6: Earliest Friends Connection")
    print("="*70)
    print()
    print("Problem: Find earliest time when all friends are connected")
    print()

    n = 4
    friendships = [
        (0, 2, 1),  # (person1, person2, timestamp)
        (1, 2, 2),
        (0, 3, 3),
    ]

    # Sort by timestamp
    friendships.sort(key=lambda x: x[2])

    uf = UnionFind(n)
    result_time = -1

    for u, v, time in friendships:
        uf.union(u, v)
        if uf.get_count() == 1:
            result_time = time
            break

    print(f"Friendships (person1, person2, time): {friendships}")
    print(f"Earliest time all connected: {result_time}")
    print()


# ============================================================================
# QUICK REFERENCE
# ============================================================================

def print_quick_reference():
    """Cheat sheet for interviews"""
    print("="*70)
    print("UNION-FIND QUICK REFERENCE (MEMORIZE THIS!)")
    print("="*70)
    print()

    print("BASIC TEMPLATE:")
    print("-" * 70)
    print("""
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        rootX, rootY = self.find(x), self.find(y)
        if rootX == rootY:
            return False

        # Union by rank
        if self.rank[rootX] < self.rank[rootY]:
            self.parent[rootX] = rootY
        elif self.rank[rootX] > self.rank[rootY]:
            self.parent[rootY] = rootX
        else:
            self.parent[rootY] = rootX
            self.rank[rootX] += 1

        self.count -= 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)
""")

    print("\nCOMMON PATTERNS:")
    print("-" * 70)
    print("1. Count components: return uf.count")
    print("2. Detect cycle: if not uf.union(u,v): cycle found")
    print("3. Find redundant edge: first edge where union() returns False")
    print("4. Group by component: use dict[uf.find(i)].append(i)")
    print("5. Process chronologically: sort events by time, union incrementally")
    print()

    print("TIME COMPLEXITY:")
    print("-" * 70)
    print("find():  O(α(n)) ≈ O(1) amortized")
    print("union(): O(α(n)) ≈ O(1) amortized")
    print("α(n) = inverse Ackermann (grows EXTREMELY slowly)")
    print("For all practical values of n, α(n) ≤ 4")
    print()

    print("WHEN TO USE:")
    print("-" * 70)
    print("✓ Detecting cycles in undirected graph")
    print("✓ Counting connected components")
    print("✓ Finding redundant connections")
    print("✓ Grouping elements by connectivity")
    print("✓ Minimum spanning tree (Kruskal's algorithm)")
    print("✓ Dynamic connectivity queries")
    print()

    print("COMMON MISTAKES TO AVOID:")
    print("-" * 70)
    print("❌ Forgetting path compression in find()")
    print("❌ Not checking if union() succeeded (for cycle detection)")
    print("❌ Off-by-one errors (0-indexed vs 1-indexed)")
    print("❌ Forgetting to decrement count in union()")
    print("❌ Using on directed graphs (doesn't work!)")
    print()


if __name__ == "__main__":
    print_quick_reference()

    print("\n" + "="*70)
    print("PATTERN EXAMPLES")
    print("="*70)
    print()

    pattern_1_number_of_connected_components()
    pattern_2_detect_cycle()
    pattern_3_redundant_connection()
    pattern_4_smallest_string_with_swaps()
    pattern_5_accounts_merge()
    pattern_6_earliest_friends()

    print("="*70)
    print("PRACTICE PROBLEMS:")
    print("="*70)
    print()
    print("Easy:")
    print("  - LeetCode 547: Number of Provinces")
    print("  - LeetCode 684: Redundant Connection")
    print("  - LeetCode 1971: Find if Path Exists in Graph")
    print()
    print("Medium:")
    print("  - LeetCode 200: Number of Islands (can also use DFS/BFS)")
    print("  - LeetCode 323: Number of Connected Components (Premium)")
    print("  - LeetCode 721: Accounts Merge")
    print("  - LeetCode 1202: Smallest String With Swaps")
    print("  - LeetCode 990: Satisfiability of Equality Equations")
    print()
    print("Hard:")
    print("  - LeetCode 685: Redundant Connection II")
    print("  - LeetCode 765: Couples Holding Hands")
    print("  - LeetCode 1579: Remove Max Number of Edges to Keep Graph Traversable")
    print("="*70)
