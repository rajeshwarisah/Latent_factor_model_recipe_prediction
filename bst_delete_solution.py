"""
Delete Node in a BST - Correct Solution

Key insight: Work recursively, returning the new subtree root.
Each recursive call returns what the parent should point to.
"""

from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        """
        Delete node with given key from BST.
        Returns the new root of the (possibly modified) subtree.
        """
        if root is None:
            return None

        # Step 1: Search for the node to delete
        if key < root.val:
            # Key is in left subtree
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            # Key is in right subtree
            root.right = self.deleteNode(root.right, key)
        else:
            # Found the node to delete (root.val == key)

            # Case 1: Node has no left child (or is leaf)
            if root.left is None:
                return root.right  # Return right child (could be None)

            # Case 2: Node has no right child
            if root.right is None:
                return root.left

            # Case 3: Node has both children
            # Find inorder successor (smallest node in right subtree)
            successor = root.right
            while successor.left:
                successor = successor.left

            # Replace root's value with successor's value
            root.val = successor.val

            # Delete the successor from right subtree
            # (successor has at most one child - the right one)
            root.right = self.deleteNode(root.right, successor.val)

        return root


class SolutionWithPredecessor:
    """Alternative: Use inorder predecessor instead of successor"""
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        if root is None:
            return None

        if key < root.val:
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            root.right = self.deleteNode(root.right, key)
        else:
            # Found the node to delete
            if root.left is None:
                return root.right
            if root.right is None:
                return root.left

            # Has both children - use predecessor (largest in left subtree)
            predecessor = root.left
            while predecessor.right:
                predecessor = predecessor.right

            root.val = predecessor.val
            root.left = self.deleteNode(root.left, predecessor.val)

        return root


# Helper functions for testing
def build_tree_from_list(values):
    """Build BST from level-order list (None for missing nodes)"""
    if not values:
        return None

    root = TreeNode(values[0])
    queue = [root]
    i = 1

    while queue and i < len(values):
        node = queue.pop(0)

        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1

        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1

    return root


def inorder_traversal(root):
    """Return inorder traversal as list"""
    if not root:
        return []
    return inorder_traversal(root.left) + [root.val] + inorder_traversal(root.right)


def tree_to_list(root):
    """Convert tree to level-order list for visualization"""
    if not root:
        return []

    result = []
    queue = [root]

    while queue:
        node = queue.pop(0)
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)

    # Remove trailing Nones
    while result and result[-1] is None:
        result.pop()

    return result


def test_cases():
    """Run test cases"""
    solution = Solution()

    print("="*70)
    print("TEST CASES")
    print("="*70)
    print()

    # Test 1: Delete node with two children
    print("Test 1: Delete node with two children")
    tree = build_tree_from_list([5, 3, 6, 2, 4, None, 7])
    print(f"Original: {tree_to_list(tree)}")
    print(f"Inorder:  {inorder_traversal(tree)}")
    result = solution.deleteNode(tree, 3)
    print(f"Delete 3: {tree_to_list(result)}")
    print(f"Inorder:  {inorder_traversal(result)}")
    print(f"Expected inorder: [2, 4, 5, 6, 7]")
    print()

    # Test 2: Delete root
    print("Test 2: Delete root")
    tree = build_tree_from_list([5, 3, 6, 2, 4, None, 7])
    print(f"Original: {tree_to_list(tree)}")
    result = solution.deleteNode(tree, 5)
    print(f"Delete 5: {tree_to_list(result)}")
    print(f"Inorder:  {inorder_traversal(result)}")
    print(f"Expected inorder: [2, 3, 4, 6, 7]")
    print()

    # Test 3: Delete leaf node
    print("Test 3: Delete leaf node")
    tree = build_tree_from_list([5, 3, 6, 2, 4, None, 7])
    print(f"Original: {tree_to_list(tree)}")
    result = solution.deleteNode(tree, 7)
    print(f"Delete 7: {tree_to_list(result)}")
    print(f"Inorder:  {inorder_traversal(result)}")
    print(f"Expected inorder: [2, 3, 4, 5, 6]")
    print()

    # Test 4: Delete non-existent node
    print("Test 4: Delete non-existent node")
    tree = build_tree_from_list([5, 3, 6, 2, 4, None, 7])
    print(f"Original: {tree_to_list(tree)}")
    result = solution.deleteNode(tree, 10)
    print(f"Delete 10: {tree_to_list(result)}")
    print(f"Inorder:  {inorder_traversal(result)}")
    print(f"Expected: unchanged")
    print()

    # Test 5: Empty tree
    print("Test 5: Empty tree")
    result = solution.deleteNode(None, 5)
    print(f"Delete from empty tree: {result}")
    print(f"Expected: None")
    print()


def explain_algorithm():
    """Explain the algorithm step by step"""
    print("="*70)
    print("ALGORITHM EXPLANATION")
    print("="*70)
    print()

    print("The key insight: Return the new subtree root at each step")
    print()

    print("Three cases when deleting a node:")
    print()

    print("Case 1: Node has no left child")
    print("    Before:  Parent     After:  Parent")
    print("               \\                   \\")
    print("               Node                Right")
    print("                 \\")
    print("                 Right")
    print("    → Simply return the right child")
    print()

    print("Case 2: Node has no right child")
    print("    Before:  Parent     After:  Parent")
    print("               \\                   \\")
    print("               Node                Left")
    print("               /")
    print("             Left")
    print("    → Simply return the left child")
    print()

    print("Case 3: Node has both children")
    print("    Before:      5           After:      6")
    print("                / \\                     / \\")
    print("               3   7                   3   7")
    print("              /   / \\                 /     \\")
    print("             2   6   8               2       8")
    print()
    print("    Steps:")
    print("    1. Find inorder successor (smallest in right subtree)")
    print("       → successor = 6")
    print("    2. Copy successor's value to current node")
    print("       → node.val = 6")
    print("    3. Delete successor from right subtree")
    print("       → root.right = deleteNode(root.right, 6)")
    print()

    print("Why use successor?")
    print("  - Successor has at most one child (only right child)")
    print("  - This simplifies deletion to Case 1 or 2")
    print("  - Maintains BST property (all left < node < all right)")
    print()


if __name__ == "__main__":
    explain_algorithm()
    test_cases()
