"""
Trie (Prefix Tree) Data Structure Implementation

A Trie is a tree-based data structure used for efficient storage and retrieval
of strings, particularly useful for:
- Autocomplete systems
- Spell checkers
- IP routing (longest prefix matching)
- Dictionary implementations

Time Complexity:
- Insert: O(m) where m is the length of the word
- Search: O(m)
- StartsWith: O(m)
- Delete: O(m)

Space Complexity: O(ALPHABET_SIZE * m * n) where n is number of words
"""


class TrieNode:
    """Node in a Trie data structure."""

    def __init__(self, char: str = ''):
        """
        Initialize a Trie node.

        Args:
            char: Character this node represents (optional, for debugging/visualization)
        """
        self.char = char  # Character this node represents (useful for debugging)
        self.children = {}  # Dictionary to store child nodes
        self.is_end_of_word = False  # Flag to mark end of a word
        self.word_count = 0  # Count of words ending at this node

    def __repr__(self):
        """String representation for debugging."""
        return f"TrieNode('{self.char}', end={self.is_end_of_word}, children={len(self.children)})"


class Trie:
    """
    Trie (Prefix Tree) implementation with insert, search, delete, and utility methods.
    """

    def __init__(self):
        """Initialize the Trie with a root node."""
        self.root = TrieNode()
        self.total_words = 0

    def insert(self, word: str) -> None:
        """
        Insert a word into the Trie.

        Args:
            word: String to insert into the Trie

        Example:
            >>> trie = Trie()
            >>> trie.insert("apple")
        """
        node = self.root

        for char in word:
            # If character doesn't exist, create new node
            if char not in node.children:
                node.children[char] = TrieNode(char)  # Store char in node
            node = node.children[char]

        # Mark the end of word
        if not node.is_end_of_word:
            self.total_words += 1
        node.is_end_of_word = True
        node.word_count += 1

    def search(self, word: str) -> bool:
        """
        Search for an exact word in the Trie.

        Args:
            word: String to search for

        Returns:
            True if word exists, False otherwise

        Example:
            >>> trie = Trie()
            >>> trie.insert("apple")
            >>> trie.search("apple")
            True
            >>> trie.search("app")
            False
        """
        node = self._find_node(word)
        return node is not None and node.is_end_of_word

    def startsWith(self, prefix: str) -> bool:
        """
        Check if there's any word in the Trie that starts with the given prefix.

        Args:
            prefix: Prefix string to search for

        Returns:
            True if prefix exists, False otherwise

        Example:
            >>> trie = Trie()
            >>> trie.insert("apple")
            >>> trie.startsWith("app")
            True
            >>> trie.startsWith("ban")
            False
        """
        return self._find_node(prefix) is not None

    def delete(self, word: str) -> bool:
        """
        Delete a word from the Trie.

        Args:
            word: String to delete

        Returns:
            True if word was deleted, False if word didn't exist

        Example:
            >>> trie = Trie()
            >>> trie.insert("apple")
            >>> trie.delete("apple")
            True
            >>> trie.delete("apple")
            False
        """
        def _delete_helper(node: TrieNode, word: str, index: int) -> bool:
            """Recursive helper to delete a word."""
            if index == len(word):
                # Reached end of word
                if not node.is_end_of_word:
                    return False  # Word doesn't exist

                node.is_end_of_word = False
                node.word_count = 0
                # Return True if node has no children (can be deleted)
                return len(node.children) == 0

            char = word[index]
            if char not in node.children:
                return False  # Word doesn't exist

            child_node = node.children[char]
            should_delete_child = _delete_helper(child_node, word, index + 1)

            # If child should be deleted, remove it
            if should_delete_child:
                del node.children[char]
                # Return True if current node has no children and is not end of another word
                return len(node.children) == 0 and not node.is_end_of_word

            return False

        if _delete_helper(self.root, word, 0) or (self.search(word) and not self.search(word)):
            self.total_words -= 1
            return True

        if self.search(word):
            self.total_words -= 1
            return True
        return False

    def get_all_words(self) -> list:
        """
        Get all words stored in the Trie.

        Returns:
            List of all words in the Trie

        Example:
            >>> trie = Trie()
            >>> trie.insert("apple")
            >>> trie.insert("app")
            >>> trie.get_all_words()
            ['app', 'apple']
        """
        words = []
        self._collect_words(self.root, "", words)
        return sorted(words)

    def get_words_with_prefix(self, prefix: str) -> list:
        """
        Get all words that start with the given prefix.

        Args:
            prefix: Prefix to search for

        Returns:
            List of words starting with the prefix

        Example:
            >>> trie = Trie()
            >>> trie.insert("apple")
            >>> trie.insert("app")
            >>> trie.insert("application")
            >>> trie.get_words_with_prefix("app")
            ['app', 'apple', 'application']
        """
        node = self._find_node(prefix)
        if node is None:
            return []

        words = []
        self._collect_words(node, prefix, words)
        return sorted(words)

    def count_words_with_prefix(self, prefix: str) -> int:
        """
        Count how many words start with the given prefix.

        Args:
            prefix: Prefix to count

        Returns:
            Number of words with the prefix
        """
        return len(self.get_words_with_prefix(prefix))

    def longest_common_prefix(self) -> str:
        """
        Find the longest common prefix among all words in the Trie.

        Returns:
            Longest common prefix string

        Example:
            >>> trie = Trie()
            >>> trie.insert("flower")
            >>> trie.insert("flow")
            >>> trie.insert("flight")
            >>> trie.longest_common_prefix()
            'fl'
        """
        if self.total_words == 0:
            return ""

        node = self.root
        prefix = ""

        while len(node.children) == 1 and not node.is_end_of_word:
            char = list(node.children.keys())[0]
            prefix += char
            node = node.children[char]

        return prefix

    def _find_node(self, prefix: str) -> TrieNode:
        """
        Helper method to find the node corresponding to a prefix.

        Args:
            prefix: Prefix to search for

        Returns:
            TrieNode if found, None otherwise
        """
        node = self.root

        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]

        return node

    def _collect_words(self, node: TrieNode, prefix: str, words: list) -> None:
        """
        Helper method to recursively collect all words from a node.

        Args:
            node: Current TrieNode
            prefix: Current prefix string
            words: List to collect words into
        """
        if node.is_end_of_word:
            words.append(prefix)

        for char, child_node in node.children.items():
            self._collect_words(child_node, prefix + char, words)

    def visualize(self, max_depth: int = 5) -> None:
        """
        Visualize the Trie structure (demonstrates usefulness of storing char in node).

        Args:
            max_depth: Maximum depth to display

        Example:
            >>> trie = Trie()
            >>> trie.insert("app")
            >>> trie.insert("apple")
            >>> trie.visualize()
        """
        print("Trie Structure:")
        print("root")
        self._visualize_helper(self.root, "", 0, max_depth)

    def _visualize_helper(self, node: TrieNode, prefix: str, depth: int, max_depth: int) -> None:
        """Helper method for visualization."""
        if depth >= max_depth:
            return

        items = sorted(node.children.items())
        for i, (char, child_node) in enumerate(items):
            is_last = (i == len(items) - 1)
            connector = "└── " if is_last else "├── "
            extension = "    " if is_last else "│   "

            # Using stored char for debugging/display
            display = f"{child_node.char}"
            if child_node.is_end_of_word:
                display += " (*)"

            print(f"{prefix}{connector}{display}")
            self._visualize_helper(child_node, prefix + extension, depth + 1, max_depth)

    def __len__(self) -> int:
        """Return the number of words in the Trie."""
        return self.total_words

    def __contains__(self, word: str) -> bool:
        """Support 'in' operator for word lookup."""
        return self.search(word)

    def __str__(self) -> str:
        """String representation of the Trie."""
        words = self.get_all_words()
        return f"Trie({len(words)} words): {words[:10]}{'...' if len(words) > 10 else ''}"


def demo_autocomplete():
    """Demonstrate autocomplete functionality using Trie."""
    print("=== Autocomplete Demo ===\n")

    trie = Trie()
    words = ["apple", "app", "application", "apply", "banana", "band", "bandana", "can", "cat", "catch"]

    print("Inserting words:", words)
    for word in words:
        trie.insert(word)

    print(f"\nTotal words in Trie: {len(trie)}\n")

    # Test autocomplete with different prefixes
    prefixes = ["app", "ban", "ca", "z"]

    for prefix in prefixes:
        suggestions = trie.get_words_with_prefix(prefix)
        if suggestions:
            print(f"Words starting with '{prefix}': {suggestions}")
        else:
            print(f"No words found starting with '{prefix}'")


def run_tests():
    """Run comprehensive tests for Trie implementation."""
    print("=== Running Trie Tests ===\n")

    trie = Trie()

    # Test 1: Insert and Search
    print("Test 1: Insert and Search")
    trie.insert("apple")
    print(f"  Search 'apple': {trie.search('apple')}")  # True
    print(f"  Search 'app': {trie.search('app')}")      # False
    print(f"  StartsWith 'app': {trie.startsWith('app')}")  # True
    print()

    # Test 2: Insert prefix
    print("Test 2: Insert prefix of existing word")
    trie.insert("app")
    print(f"  Search 'app': {trie.search('app')}")      # True
    print(f"  Search 'apple': {trie.search('apple')}")  # True
    print()

    # Test 3: Delete
    print("Test 3: Delete operation")
    trie.insert("application")
    print(f"  Before delete - Search 'app': {trie.search('app')}")
    trie.delete("app")
    print(f"  After delete - Search 'app': {trie.search('app')}")
    print(f"  Search 'apple': {trie.search('apple')}")  # Still exists
    print(f"  Search 'application': {trie.search('application')}")  # Still exists
    print()

    # Test 4: Get all words
    print("Test 4: Get all words")
    print(f"  All words: {trie.get_all_words()}")
    print()

    # Test 5: Words with prefix
    print("Test 5: Words with prefix")
    trie.insert("apply")
    trie.insert("appreciate")
    print(f"  Words with prefix 'app': {trie.get_words_with_prefix('app')}")
    print()

    # Test 6: Longest common prefix
    print("Test 6: Longest common prefix")
    trie2 = Trie()
    trie2.insert("flower")
    trie2.insert("flow")
    trie2.insert("flight")
    print(f"  Words: {trie2.get_all_words()}")
    print(f"  Longest common prefix: '{trie2.longest_common_prefix()}'")
    print()

    # Test 7: Contains operator
    print("Test 7: 'in' operator")
    print(f"  'apple' in trie: {'apple' in trie}")
    print(f"  'banana' in trie: {'banana' in trie}")
    print()

    print("✓ All tests completed!\n")


if __name__ == "__main__":
    run_tests()
    print("\n" + "="*60 + "\n")
    demo_autocomplete()

    # Interactive example
    print("\n" + "="*60)
    print("=== LeetCode-style Example ===\n")

    trie = Trie()
    operations = [
        ("insert", "apple"),
        ("search", "apple"),
        ("search", "app"),
        ("startsWith", "app"),
        ("insert", "app"),
        ("search", "app"),
    ]

    print("Operations:")
    for op, word in operations:
        if op == "insert":
            trie.insert(word)
            print(f"  trie.insert('{word}') -> None")
        elif op == "search":
            result = trie.search(word)
            print(f"  trie.search('{word}') -> {result}")
        elif op == "startsWith":
            result = trie.startsWith(word)
            print(f"  trie.startsWith('{word}') -> {result}")

    # Visualization demo (shows why storing char in node is useful)
    print("\n" + "="*60)
    print("=== Visualization Demo (using stored char) ===\n")

    trie_viz = Trie()
    words_viz = ["app", "apple", "apply", "cat", "car"]
    print(f"Inserting words: {words_viz}\n")
    for word in words_viz:
        trie_viz.insert(word)

    trie_viz.visualize()

    print("\nNote: The (*) marks indicate end of a word.")
    print("The char field in each TrieNode makes this visualization possible!")
