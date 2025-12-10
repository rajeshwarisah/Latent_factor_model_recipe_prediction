"""
Minimum Operations to Reduce Number to Zero

Problem: Given a positive integer n, you can do the following operation any number of times:
- Add or subtract a power of 2 from n.
Return the minimum number of operations to make n equal to 0.

Approach:
The key insight is to analyze the binary representation of the number.
- Consecutive 1s in binary can be optimized: instead of subtracting each power of 2,
  we can ADD at the lowest position to create a carry, which converts multiple 1s
  into a single 1 at a higher position.
- Isolated 1s should be subtracted directly.

Algorithm:
1. Check if the least significant bit (LSB) is 1
2. If LSB is 1 and the next bit is also 1: ADD 1 (creates carry, converts consecutive 1s)
3. If LSB is 1 but next bit is 0: SUBTRACT 1 (removes isolated 1)
4. Shift right and repeat
5. Count total operations

Time Complexity: O(log n) - we process each bit once
Space Complexity: O(1)
"""


def minOperations(n: int) -> int:
    """
    Calculate minimum operations to reduce n to 0 using powers of 2.

    Args:
        n: positive integer (1 <= n <= 10^5)

    Returns:
        Minimum number of add/subtract operations needed

    Examples:
        >>> minOperations(39)
        3
        >>> minOperations(54)
        3
    """
    operations = 0

    while n > 0:
        # Check if least significant bit is 1
        if n & 1:
            operations += 1
            # If next bit is also 1, add to create carry (optimize consecutive 1s)
            # Otherwise, subtract to clear this isolated 1
            if n & 2:
                n += 1  # Add 2^0, creates carry chain
            else:
                n -= 1  # Subtract 2^0

        # Shift right to check next bit
        n >>= 1

    return operations


def minOperations_verbose(n: int) -> int:
    """
    Verbose version with detailed explanation of steps.
    """
    operations = 0
    original_n = n

    print(f"Starting with n = {n} (binary: {bin(n)})")

    while n > 0:
        if n & 1:
            operations += 1
            if n & 2:
                print(f"  Found consecutive 1s at LSB, adding 1: {n} + 1 = {n+1} (binary: {bin(n+1)})")
                n += 1
            else:
                print(f"  Found isolated 1 at LSB, subtracting 1: {n} - 1 = {n-1} (binary: {bin(n-1) if n > 1 else '0b0'})")
                n -= 1

        n >>= 1

    print(f"Total operations: {operations}\n")
    return operations


# Test cases
if __name__ == "__main__":
    # Example test cases from the problem
    test_cases = [
        (39, 3),
        (54, 3),
        (1, 1),
        (7, 2),   # 111 -> add 1 to get 1000, then subtract 8
        (15, 2),  # 1111 -> add 1 to get 10000, then subtract 16
        (8, 1),   # 1000 -> subtract 8
        (255, 2), # 11111111 -> add 1 to get 100000000, then subtract 256
    ]

    print("Testing minOperations function:\n")
    all_passed = True

    for n, expected in test_cases:
        result = minOperations(n)
        status = "✓" if result == expected else "✗"
        print(f"{status} n={n}, expected={expected}, got={result}")

        if result != expected:
            all_passed = False
            print(f"  FAILED! Running verbose version:")
            minOperations_verbose(n)

    if all_passed:
        print("\n✓ All test cases passed!")
    else:
        print("\n✗ Some test cases failed!")

    # Demonstrate with examples from problem
    print("\n" + "="*60)
    print("Detailed walkthrough of examples:")
    print("="*60 + "\n")

    print("Example 1: n = 39")
    minOperations_verbose(39)

    print("Example 2: n = 54")
    minOperations_verbose(54)
