"""
Dynamic Union-Find (Disjoint Set Union)

Supports adding elements dynamically - not just fixed 0 to n-1!

Key difference from standard Union-Find:
- Uses dictionaries instead of lists
- Can handle any hashable type (strings, tuples, etc.)
- Elements are added on-demand
"""

class DynamicUnionFind:
    """Union-Find that supports dynamic element addition"""

    def __init__(self):
        """Initialize empty Union-Find"""
        self.parent = {}  # element -> parent
        self.rank = {}    # element -> rank
        self.count = 0    # number of disjoint sets

    def add(self, x):
        """Add a new element to the Union-Find structure"""
        if x not in self.parent:
            self.parent[x] = x  # Element is its own parent
            self.rank[x] = 0
            self.count += 1

    def find(self, x):
        """Find root of x with path compression. Auto-adds if not exists."""
        # Auto-add element if it doesn't exist
        if x not in self.parent:
            self.add(x)

        # Path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """
        Union sets containing x and y.
        Auto-adds elements if they don't exist.
        Returns True if merged, False if already connected.
        """
        # Auto-add elements if they don't exist
        if x not in self.parent:
            self.add(x)
        if y not in self.parent:
            self.add(y)

        rootX = self.find(x)
        rootY = self.find(y)

        if rootX == rootY:
            return False  # Already in same set

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
        """Check if x and y are in the same set"""
        return self.find(x) == self.find(y)

    def get_count(self):
        """Return number of disjoint sets"""
        return self.count

    def get_size(self, x):
        """Get size of the set containing x"""
        root = self.find(x)
        return sum(1 for elem in self.parent if self.find(elem) == root)

    def get_all_sets(self):
        """Return all disjoint sets as a dictionary: root -> [members]"""
        from collections import defaultdict
        sets = defaultdict(list)
        for elem in self.parent:
            root = self.find(elem)
            sets[root].append(elem)
        return dict(sets)


class DynamicUnionFindWithSize:
    """Alternative: Track size instead of rank"""

    def __init__(self):
        self.parent = {}
        self.size = {}    # Track size instead of rank
        self.count = 0

    def add(self, x):
        """Add a new element"""
        if x not in self.parent:
            self.parent[x] = x
            self.size[x] = 1
            self.count += 1

    def find(self, x):
        """Find with path compression, auto-add if needed"""
        if x not in self.parent:
            self.add(x)

        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """Union with auto-add"""
        if x not in self.parent:
            self.add(x)
        if y not in self.parent:
            self.add(y)

        rootX = self.find(x)
        rootY = self.find(y)

        if rootX == rootY:
            return False

        # Union by size
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
        """Get size of set containing x"""
        return self.size[self.find(x)]


# ============================================================================
# EXAMPLES AND USE CASES
# ============================================================================

def example_1_string_elements():
    """Example: Using strings as elements"""
    print("="*70)
    print("EXAMPLE 1: String Elements")
    print("="*70)
    print()

    uf = DynamicUnionFind()

    # Add elements dynamically
    print("Adding and connecting people:")
    uf.union("Alice", "Bob")
    print(f"  Connect Alice and Bob")
    print(f"  Sets: {uf.get_all_sets()}")
    print()

    uf.union("Bob", "Charlie")
    print(f"  Connect Bob and Charlie")
    print(f"  Sets: {uf.get_all_sets()}")
    print()

    uf.union("David", "Eve")
    print(f"  Connect David and Eve")
    print(f"  Sets: {uf.get_all_sets()}")
    print()

    print(f"Number of groups: {uf.get_count()}")
    print(f"Are Alice and Charlie connected? {uf.connected('Alice', 'Charlie')}")
    print(f"Are Alice and David connected? {uf.connected('Alice', 'David')}")
    print()


def example_2_auto_add():
    """Example: Elements added automatically during operations"""
    print("="*70)
    print("EXAMPLE 2: Auto-Add Elements")
    print("="*70)
    print()

    uf = DynamicUnionFind()

    print("No need to pre-add elements! They're added automatically:")
    print()

    # Elements added automatically during union/find
    uf.union(1, 2)
    print(f"union(1, 2): {uf.get_all_sets()}")

    uf.union(3, 4)
    print(f"union(3, 4): {uf.get_all_sets()}")

    uf.union(2, 3)
    print(f"union(2, 3): {uf.get_all_sets()}")
    print()

    # Finding an element that doesn't exist yet
    print(f"find(5) auto-adds 5: {uf.find(5)}")
    print(f"All sets: {uf.get_all_sets()}")
    print()


def example_3_social_network():
    """Example: Dynamic social network"""
    print("="*70)
    print("EXAMPLE 3: Social Network (Friends)")
    print("="*70)
    print()

    friends = DynamicUnionFind()

    friendships = [
        ("Alice", "Bob"),
        ("Bob", "Charlie"),
        ("David", "Eve"),
        ("Frank", "Grace"),
        ("Charlie", "David"),
    ]

    print("Building friendship network:")
    for person1, person2 in friendships:
        friends.union(person1, person2)
        print(f"  {person1} and {person2} are now friends")

    print()
    print(f"Total friend groups: {friends.get_count()}")
    print()

    # Show all friend groups
    groups = friends.get_all_sets()
    for i, (root, members) in enumerate(groups.items(), 1):
        print(f"Group {i}: {sorted(members)}")
    print()

    # Queries
    print("Queries:")
    print(f"  Are Alice and Eve connected? {friends.connected('Alice', 'Eve')}")
    print(f"  Are Alice and Frank connected? {friends.connected('Alice', 'Frank')}")
    print(f"  Size of Alice's group: {friends.get_size('Alice')}")
    print()


def example_4_tuple_elements():
    """Example: Using tuples as elements (coordinates)"""
    print("="*70)
    print("EXAMPLE 4: Grid Coordinates as Elements")
    print("="*70)
    print()

    uf = DynamicUnionFind()

    # Connect adjacent cells in a grid
    connections = [
        ((0, 0), (0, 1)),
        ((0, 1), (0, 2)),
        ((1, 0), (1, 1)),
        ((2, 2), (2, 3)),
    ]

    print("Connecting adjacent cells:")
    for cell1, cell2 in connections:
        uf.union(cell1, cell2)
        print(f"  Connect {cell1} and {cell2}")

    print()
    print(f"Number of islands: {uf.get_count()}")
    print()

    groups = uf.get_all_sets()
    for i, (root, members) in enumerate(groups.items(), 1):
        print(f"Island {i}: {sorted(members)}")
    print()


def example_5_accounts_merge():
    """Example: LeetCode 721 - Accounts Merge"""
    print("="*70)
    print("EXAMPLE 5: Accounts Merge (LeetCode 721)")
    print("="*70)
    print()

    accounts = [
        ["John", "john@mail.com", "john_work@mail.com"],
        ["John", "john@mail.com", "john_home@mail.com"],
        ["Mary", "mary@mail.com"],
        ["John", "john_personal@mail.com"]
    ]

    uf = DynamicUnionFind()

    # Map email to account owner
    email_to_name = {}

    # Union emails in same account
    for account in accounts:
        name = account[0]
        first_email = account[1]

        for email in account[1:]:
            email_to_name[email] = name
            uf.union(first_email, email)

    # Group emails by their root
    from collections import defaultdict
    groups = defaultdict(list)
    for email in email_to_name:
        root = uf.find(email)
        groups[root].append(email)

    # Format result
    result = []
    for root, emails in groups.items():
        name = email_to_name[root]
        result.append([name] + sorted(emails))

    print("Original accounts:")
    for acc in accounts:
        print(f"  {acc}")
    print()

    print("Merged accounts:")
    for acc in result:
        print(f"  {acc}")
    print()


def comparison_with_static():
    """Compare static vs dynamic Union-Find"""
    print("="*70)
    print("STATIC vs DYNAMIC UNION-FIND")
    print("="*70)
    print()

    print("STATIC Union-Find:")
    print("-" * 70)
    print("class UnionFind:")
    print("    def __init__(self, n):")
    print("        self.parent = list(range(n))  # Fixed size!")
    print("        self.rank = [0] * n")
    print()
    print("Pros:")
    print("  ✓ Slightly faster (list access vs dict)")
    print("  ✓ Uses less memory")
    print()
    print("Cons:")
    print("  ✗ Must know n upfront")
    print("  ✗ Only works with integers 0 to n-1")
    print("  ✗ Can't add elements dynamically")
    print()

    print("DYNAMIC Union-Find:")
    print("-" * 70)
    print("class DynamicUnionFind:")
    print("    def __init__(self):")
    print("        self.parent = {}  # Can grow!")
    print("        self.rank = {}")
    print()
    print("Pros:")
    print("  ✓ Add elements anytime")
    print("  ✓ Works with any hashable type (strings, tuples, etc.)")
    print("  ✓ More flexible")
    print()
    print("Cons:")
    print("  ✗ Slightly slower (dict overhead)")
    print("  ✗ Uses more memory")
    print()

    print("WHEN TO USE WHICH:")
    print("-" * 70)
    print("Use STATIC when:")
    print("  - You know the number of elements upfront")
    print("  - Elements are 0, 1, 2, ..., n-1")
    print("  - Maximum performance needed")
    print()
    print("Use DYNAMIC when:")
    print("  - Elements added/discovered during processing")
    print("  - Working with strings, tuples, or other types")
    print("  - Flexibility more important than raw speed")
    print("  - Examples: social networks, email merging, etc.")
    print()


if __name__ == "__main__":
    example_1_string_elements()
    example_2_auto_add()
    example_3_social_network()
    example_4_tuple_elements()
    example_5_accounts_merge()
    comparison_with_static()

    print("="*70)
    print("QUICK REFERENCE: Dynamic Union-Find Template")
    print("="*70)
    print()
    print("""
class DynamicUnionFind:
    def __init__(self):
        self.parent = {}
        self.rank = {}
        self.count = 0

    def add(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
            self.count += 1

    def find(self, x):
        if x not in self.parent:
            self.add(x)
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        if x not in self.parent:
            self.add(x)
        if y not in self.parent:
            self.add(y)

        rootX, rootY = self.find(x), self.find(y)
        if rootX == rootY:
            return False

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
    print("="*70)
