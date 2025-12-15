"""
Count Paths That Can Form a Palindrome in a Tree - LeetCode

Problem: Given a tree with n nodes and edges labeled with characters,
count all pairs of nodes (u, v) where the path from u to v can be rearranged
to form a palindrome.

Key Insight: A string can form a palindrome if at most ONE character has odd frequency.

Approach: Use BITMASK to track character frequencies
- Each bit represents whether a character appears odd/even times
- XOR operation toggles bits (odd/even counts)
- A path forms palindrome if XOR result has ≤ 1 bit set

Time: O(n * 26)
Space: O(n)
"""

from typing import List
from collections import defaultdict

class Solution:
    def countPalindromePaths(self, parent: List[int], s: str) -> int:
        """
        Count paths that can form palindromes using bitmask + DFS

        Strategy:
        1. Build tree from parent array
        2. DFS to compute bitmask for each path from root
        3. Two paths can combine to form palindrome if their XOR has ≤ 1 bit
        """
        n = len(parent)

        # Build adjacency list
        tree = defaultdict(list)
        for i in range(1, n):
            tree[parent[i]].append(i)

        # bitmask[i] = XOR of all characters from root to node i
        # Bit j is 1 if character ('a' + j) appears odd times
        bitmasks = [0] * n

        # DFS to compute bitmask for each node
        def dfs(node):
            for child in tree[node]:
                # XOR toggles the bit for this character
                char_bit = 1 << (ord(s[child]) - ord('a'))
                bitmasks[child] = bitmasks[node] ^ char_bit
                dfs(child)

        dfs(0)

        # Count valid pairs
        result = 0

        # Frequency map: bitmask -> count
        # Two nodes with same bitmask form palindrome path (all chars even)
        freq = defaultdict(int)

        for mask in bitmasks:
            # Case 1: Same bitmask (all characters have even count difference)
            result += freq[mask]

            # Case 2: Differ by exactly 1 bit (one character has odd count)
            for i in range(26):
                # Try flipping each bit
                toggled = mask ^ (1 << i)
                result += freq[toggled]

            freq[mask] += 1

        return result


class SolutionWithExplanation:
    """Version with detailed comments for learning"""

    def countPalindromePaths(self, parent: List[int], s: str) -> int:
        n = len(parent)

        # Build tree
        tree = defaultdict(list)
        for i in range(1, n):
            tree[parent[i]].append(i)

        # Compute bitmask from root to each node
        bitmasks = [0] * n

        def dfs(node):
            for child in tree[node]:
                # XOR current bitmask with child's character
                # This toggles the bit: 0->1 (odd), 1->0 (even)
                char_idx = ord(s[child]) - ord('a')
                char_bit = 1 << char_idx
                bitmasks[child] = bitmasks[node] ^ char_bit
                dfs(child)

        dfs(0)

        # Key insight: Path from node u to node v has bitmask:
        # bitmasks[u] ^ bitmasks[v]
        # (XOR cancels common ancestors)

        result = 0
        freq = defaultdict(int)

        for mask in bitmasks:
            # For this node to form palindrome with previous nodes:

            # 1. Same mask -> all chars appear even times (perfect palindrome)
            result += freq[mask]

            # 2. Differ by 1 bit -> one char appears odd times (still palindrome)
            for i in range(26):
                # Try each possible single character difference
                toggled = mask ^ (1 << i)
                if toggled in freq:
                    result += freq[toggled]

            freq[mask] += 1

        return result


def explain_concept():
    """Explain the bitmask approach"""
    print("="*70)
    print("CONCEPT: Using Bitmask for Palindrome Path Counting")
    print("="*70)
    print()

    print("KEY INSIGHT: Palindrome Condition")
    print("-" * 70)
    print("A string can be rearranged to form a palindrome if:")
    print("  - At most ONE character has ODD frequency")
    print()
    print("Examples:")
    print("  'aab' → 'aba' ✓ (one 'b' is odd)")
    print("  'abc' → cannot form palindrome ✗ (three chars are odd)")
    print("  'aabb' → 'abba' ✓ (all even)")
    print()

    print("BITMASK REPRESENTATION:")
    print("-" * 70)
    print("Use a 26-bit integer where bit i represents character ('a' + i)")
    print("  - Bit = 0: character appears EVEN times (or not at all)")
    print("  - Bit = 1: character appears ODD times")
    print()
    print("Example: 'aabbc'")
    print("  a: 2 times (even) → bit 0 = 0")
    print("  b: 2 times (even) → bit 1 = 0")
    print("  c: 1 time  (odd)  → bit 2 = 1")
    print("  Bitmask: 0b100 = 4")
    print()

    print("XOR OPERATION:")
    print("-" * 70)
    print("XOR toggles bits (tracks odd/even parity)")
    print("  0 XOR 1 = 1 (even + one = odd)")
    print("  1 XOR 1 = 0 (odd + one = even)")
    print()
    print("Building path bitmask:")
    print("  Start: mask = 0")
    print("  See 'a': mask = mask XOR (1 << 0)")
    print("  See 'a': mask = mask XOR (1 << 0)  (back to 0!)")
    print("  See 'b': mask = mask XOR (1 << 1)")
    print()

    print("PATH BITMASK:")
    print("-" * 70)
    print("For path from node u to node v:")
    print("  path_mask = bitmask[u] XOR bitmask[v]")
    print()
    print("Why? XOR cancels out common ancestors!")
    print()
    print("Example tree:")
    print("       0(a)")
    print("      / \\")
    print("    1(b) 2(c)")
    print("    /")
    print("  3(a)")
    print()
    print("Path from root to each node:")
    print("  Node 0: '' → mask = 0")
    print("  Node 1: 'b' → mask = 0b010 = 2")
    print("  Node 2: 'c' → mask = 0b100 = 4")
    print("  Node 3: 'ba' → mask = 0b011 = 3")
    print()
    print("Path from node 1 to node 3:")
    print("  Direct path: 'a'")
    print("  Using XOR: bitmask[3] ^ bitmask[1] = 3 ^ 2 = 1 = 0b001")
    print("  This represents 'a' (one 'a', odd) ✓")
    print()

    print("CHECKING PALINDROME:")
    print("-" * 70)
    print("A bitmask represents a valid palindrome if:")
    print("  - mask = 0 (all even) OR")
    print("  - mask has exactly 1 bit set (one odd character)")
    print()
    print("Check if has ≤ 1 bit set:")
    print("  Method 1: mask = 0 or (mask & (mask - 1)) == 0")
    print("  Method 2: Count set bits ≤ 1")
    print()
    print("Examples:")
    print("  0b000 = 0 → 0 bits set ✓ palindrome")
    print("  0b001 = 1 → 1 bit set ✓ palindrome")
    print("  0b010 = 2 → 1 bit set ✓ palindrome")
    print("  0b011 = 3 → 2 bits set ✗ not palindrome")
    print()


def example_walkthrough():
    """Walk through a complete example"""
    print("="*70)
    print("COMPLETE EXAMPLE")
    print("="*70)
    print()

    parent = [-1, 0, 0, 1, 1, 2]
    s = "acaabc"

    print(f"Input:")
    print(f"  parent = {parent}")
    print(f"  s = '{s}'")
    print()

    print("Tree structure:")
    print("       0(a)")
    print("      / \\")
    print("    1(c)  2(a)")
    print("    / \\    |")
    print("  3(a) 4(a) 5(b)")
    print()

    print("Step 1: Compute bitmask for each node (from root)")
    print("-" * 70)

    # Manually compute
    masks = [0] * 6
    # Node 1: path "c" from root
    masks[1] = 0 ^ (1 << 2)  # 0b100 = 4
    # Node 2: path "a" from root
    masks[2] = 0 ^ (1 << 0)  # 0b001 = 1
    # Node 3: path "ca" from root
    masks[3] = masks[1] ^ (1 << 0)  # 4 ^ 1 = 5 = 0b101
    # Node 4: path "ca" from root
    masks[4] = masks[1] ^ (1 << 0)  # 4 ^ 1 = 5 = 0b101
    # Node 5: path "ab" from root
    masks[5] = masks[2] ^ (1 << 1)  # 1 ^ 2 = 3 = 0b011

    for i, mask in enumerate(masks):
        path_chars = []
        if i == 0:
            path = ""
        elif i == 1:
            path = "c"
        elif i == 2:
            path = "a"
        elif i == 3:
            path = "ca"
        elif i == 4:
            path = "ca"
        else:
            path = "ab"
        print(f"  Node {i}: path='{path}' → mask={mask:3d} = {bin(mask)}")
    print()

    print("Step 2: Count valid pairs")
    print("-" * 70)
    print("For each node, check if it can form palindrome with previous nodes")
    print()

    freq = defaultdict(int)
    result = 0

    for i, mask in enumerate(masks):
        print(f"Node {i} (mask={mask}):")

        # Same mask
        if mask in freq and freq[mask] > 0:
            print(f"  Same mask ({mask}): +{freq[mask]} pairs")
            result += freq[mask]

        # Differ by 1 bit
        count = 0
        for j in range(26):
            toggled = mask ^ (1 << j)
            if toggled in freq and freq[toggled] > 0:
                count += freq[toggled]
        if count > 0:
            print(f"  Differ by 1 bit: +{count} pairs")
            result += count

        freq[mask] += 1
        print(f"  Total so far: {result}")
        print()

    print(f"Final answer: {result}")
    print()

    # Run actual solution
    solution = Solution()
    actual = solution.countPalindromePaths(parent, s)
    print(f"Verified with solution: {actual}")
    print()


def common_mistakes():
    """Common mistakes and pitfalls"""
    print("="*70)
    print("COMMON MISTAKES")
    print("="*70)
    print()

    print("MISTAKE 1: Checking ALL pairs naively")
    print("-" * 70)
    print("❌ WRONG: O(n²) - check every pair of nodes")
    print("✓ CORRECT: O(n * 26) - use frequency map")
    print()

    print("MISTAKE 2: Forgetting path XOR property")
    print("-" * 70)
    print("❌ WRONG: Computing path string for every pair")
    print("✓ CORRECT: path[u→v] = bitmask[u] XOR bitmask[v]")
    print()

    print("MISTAKE 3: Not handling node 0")
    print("-" * 70)
    print("❌ WRONG: Starting from node 1")
    print("✓ CORRECT: Include node 0 (root has mask=0)")
    print()

    print("MISTAKE 4: Counting pairs twice")
    print("-" * 70)
    print("❌ WRONG: Counting both (u,v) and (v,u)")
    print("✓ CORRECT: Process nodes in order, use frequency of PREVIOUS nodes")
    print()


if __name__ == "__main__":
    explain_concept()
    print()
    example_walkthrough()
    print()
    common_mistakes()

    print("="*70)
    print("ALGORITHM TEMPLATE")
    print("="*70)
    print("""
def countPalindromePaths(parent, s):
    n = len(parent)

    # 1. Build tree
    tree = defaultdict(list)
    for i in range(1, n):
        tree[parent[i]].append(i)

    # 2. Compute bitmask for each node
    bitmasks = [0] * n
    def dfs(node):
        for child in tree[node]:
            char_bit = 1 << (ord(s[child]) - ord('a'))
            bitmasks[child] = bitmasks[node] ^ char_bit
            dfs(child)
    dfs(0)

    # 3. Count valid pairs using frequency map
    result = 0
    freq = defaultdict(int)
    for mask in bitmasks:
        # Same mask (all even)
        result += freq[mask]
        # Differ by 1 bit (one odd)
        for i in range(26):
            result += freq[mask ^ (1 << i)]
        freq[mask] += 1

    return result
    """)
    print("="*70)
