"""
Delete Node in a BST - Bug Analysis

Your code has 3 critical bugs that prevent correct deletion.
"""

from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class BuggyVersion:
    """Original buggy code"""
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        node = self.findNode(root, key)
        if node is None:
            return root

        if node.left:
            swap = node.left
            while swap.right != None:
                swap = swap.right
            node.val = swap.val
            # ❌ BUG 1: After swapping, we should delete swap.val, not key!
            return self.deleteNode(node.left, key)  # WRONG: still looking for 'key'
        elif node.right:
            swap = node.right
            while swap.left != None:
                swap = swap.left
            node.val = swap.val
            # ❌ BUG 1: Same issue here
            return self.deleteNode(node.right, key)  # WRONG: still looking for 'key'
        else:
            # ❌ BUG 2: Setting node = None doesn't delete it from parent!
            node = None
            return root  # ❌ BUG 3: Returns original root, node still in tree!

    def findNode(self, root, key):
        if root == None:
            return None
        if root.val == key:
            return root
        if root.val < key:
            return self.findNode(root.right, key)
        if root.val > key:
            return self.findNode(root.left, key)


class CorrectVersion:
    """Corrected code"""
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        if root is None:
            return None

        # Search for the node to delete
        if key < root.val:
            # Key is in left subtree
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            # Key is in right subtree
            root.right = self.deleteNode(root.right, key)
        else:
            # Found the node to delete
            # Case 1: Node has no left child
            if root.left is None:
                return root.right  # Return right child (or None if leaf)

            # Case 2: Node has no right child
            if root.right is None:
                return root.left

            # Case 3: Node has both children
            # Find inorder successor (smallest in right subtree)
            successor = root.right
            while successor.left:
                successor = successor.left

            # Replace node's value with successor's value
            root.val = successor.val

            # Delete the successor (it has at most one child)
            root.right = self.deleteNode(root.right, successor.val)

        return root


def explain_bugs():
    """Detailed explanation of each bug"""
    print("="*70)
    print("BUG ANALYSIS: Delete Node in BST")
    print("="*70)
    print()

    print("BUG 1: Wrong key in recursive call after swap")
    print("-" * 70)
    print("❌ WRONG:")
    print("    node.val = swap.val")
    print("    return self.deleteNode(node.left, key)  # Still looking for 'key'!")
    print()
    print("Why this is wrong:")
    print("  - After swapping, node.val is no longer 'key', it's 'swap.val'")
    print("  - The recursive call tries to delete 'key' which doesn't exist anymore")
    print("  - Should delete the node we swapped from: swap.val")
    print()
    print("✓ CORRECT:")
    print("    node.val = swap.val")
    print("    return self.deleteNode(node.left, swap.val)  # Delete the swapped value")
    print()

    print("BUG 2: Setting node = None doesn't delete from tree")
    print("-" * 70)
    print("❌ WRONG:")
    print("    else:")
    print("        node = None")
    print("        return root")
    print()
    print("Why this is wrong:")
    print("  - 'node' is just a local variable pointing to the TreeNode")
    print("  - Setting it to None only removes the local reference")
    print("  - The parent still points to this node!")
    print("  - The node is still in the tree")
    print()
    print("Example:")
    print("    Parent")
    print("       \\")
    print("       Node (to delete)")
    print()
    print("  After 'node = None', Parent.right still points to Node!")
    print()

    print("BUG 3: Fundamental approach issue")
    print("-" * 70)
    print("❌ WRONG approach:")
    print("  1. Find node using findNode()")
    print("  2. Try to modify/delete it")
    print("  3. Return original root")
    print()
    print("Problems:")
    print("  - No way to update parent's pointer to this node")
    print("  - Can't actually remove node from tree structure")
    print("  - Returns original root unchanged")
    print()
    print("✓ CORRECT approach:")
    print("  - Work recursively, returning the new subtree root")
    print("  - Each call returns what the parent should point to")
    print("  - Update parent's left/right with returned value")
    print()


def demonstrate_bug():
    """Show concrete example where bugs manifest"""
    print("="*70)
    print("CONCRETE EXAMPLE")
    print("="*70)
    print()

    print("Delete key=5 from this BST:")
    print()
    print("       5")
    print("      / \\")
    print("     3   7")
    print("    /   / \\")
    print("   2   6   8")
    print()

    print("Expected result:")
    print()
    print("       6        (or 3)")
    print("      / \\")
    print("     3   7")
    print("    /     \\")
    print("   2       8")
    print()

    print("What BUGGY code does:")
    print()
    print("Step 1: findNode(root, 5) finds node with val=5")
    print("Step 2: node.left exists, so find inorder predecessor")
    print("        - swap = node.left = TreeNode(3)")
    print("        - while swap.right: swap = swap.right")
    print("        - swap = TreeNode(3) (no right child)")
    print("        - node.val = 3 (swap values)")
    print()
    print("Step 3: Recursive call self.deleteNode(node.left, key=5)")
    print("        ❌ BUG: Looking for key=5 in left subtree")
    print("        But 5 doesn't exist there anymore! We changed it to 3!")
    print("        Should be: self.deleteNode(node.left, 3)")
    print()
    print("Result: Node with original value 5 is still in tree,")
    print("        just with value changed to 3. Duplicate 3's!")
    print()


def test_both_versions():
    """Test both versions"""
    print("="*70)
    print("TESTING BOTH VERSIONS")
    print("="*70)
    print()

    # Build tree: 5,3,7,2,null,6,8
    def build_tree():
        root = TreeNode(5)
        root.left = TreeNode(3)
        root.right = TreeNode(7)
        root.left.left = TreeNode(2)
        root.right.left = TreeNode(6)
        root.right.right = TreeNode(8)
        return root

    def inorder(root):
        if not root:
            return []
        return inorder(root.left) + [root.val] + inorder(root.right)

    print("Original tree (inorder): [2, 3, 5, 6, 7, 8]")
    print("Delete key = 3")
    print()

    # Test buggy version
    print("Buggy version:")
    buggy_tree = build_tree()
    buggy = BuggyVersion()
    result = buggy.deleteNode(buggy_tree, 3)
    print(f"  Result: {inorder(result)}")
    print(f"  Expected: [2, 5, 6, 7, 8]")
    print()

    # Test correct version
    print("Correct version:")
    correct_tree = build_tree()
    correct = CorrectVersion()
    result = correct.deleteNode(correct_tree, 3)
    print(f"  Result: {inorder(result)}")
    print(f"  Expected: [2, 5, 6, 7, 8]")
    print()


if __name__ == "__main__":
    explain_bugs()
    print()
    demonstrate_bug()
    print()
    test_both_versions()

    print("="*70)
    print("SUMMARY OF FIXES")
    print("="*70)
    print()
    print("1. Don't use separate findNode - work recursively")
    print("2. Return the new subtree root at each step")
    print("3. Parent updates its left/right pointer with returned value")
    print("4. When swapping with successor/predecessor, delete swap.val not key")
    print("5. For leaf nodes, return None (not the original root)")
    print("="*70)
