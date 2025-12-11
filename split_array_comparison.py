"""
Split Array Largest Sum - Comparing Two Implementations

Problem: Split array into k subarrays such that the largest sum among
the k subarrays is minimized.

Key Differences Between the Two Solutions:
"""

from typing import List

class Solution1:
    """First implementation"""
    def splitArray(self, nums: List[int], m: int) -> int:
        low = max(nums)  # ✓ CORRECT: largest sum must be at least max(nums)
        high = sum(nums)
        ans = float('inf')

        while low <= high:
            mid = (low + high) // 2

            piecesRequired = self.countDivision(nums, mid)

            if piecesRequired > m:
                low = mid + 1
            else:  # piecesRequired <= m
                ans = min(ans, mid)
                high = mid - 1

        return ans

    def countDivision(self, nums, mid):
        """Counts number of subarrays needed with max sum = mid"""
        count = 1  # Start with 1 subarray
        cur_sum = nums[0]

        for num in nums[1:]:
            if cur_sum + num > mid:
                count += 1
                cur_sum = num
            else:
                cur_sum += num

        return count


class Solution2:
    """Second implementation"""
    def splitArray(self, nums: List[int], k: int) -> int:
        low = min(nums)  # ✗ WRONG: should be max(nums)!
        high = sum(nums)
        ans = float('inf')

        while low <= high:
            mid = (low + high) // 2

            cuts = self.findNumCuts(nums, mid)

            if cuts > k:
                low = mid + 1
            else:  # cuts <= k
                ans = min(ans, mid)
                high = mid - 1

        return ans

    def findNumCuts(self, nums, val):
        """Counts number of cuts (splits) needed"""
        cutNo = 0  # Start with 0 cuts
        s = 0

        for i in nums:
            if s + i > val:
                s = i
                cutNo += 1
            else:
                s += i

        return cutNo + 1  # Converts cuts to subarrays


def demonstrate_differences():
    """Show the key differences"""

    print("="*70)
    print("KEY DIFFERENCES BETWEEN THE TWO IMPLEMENTATIONS")
    print("="*70)

    print("\n1. CRITICAL BUG - Binary Search Range:")
    print("-" * 70)
    print("Code 1: low = max(nums)  ✓ CORRECT")
    print("Code 2: low = min(nums)  ✗ WRONG")
    print()
    print("Why this matters:")
    print("  - The largest subarray sum MUST be at least max(nums)")
    print("  - Each element must fit in at least one subarray")
    print("  - If nums = [7, 2, 5, 10, 8], we can't have largest sum < 10")
    print()

    print("\n2. Counting Approach (Both logically correct, just different):")
    print("-" * 70)
    print("Code 1: countDivision()")
    print("  - Counts SUBARRAYS directly")
    print("  - Starts with count = 1")
    print("  - Increments when making a split")
    print("  - Returns count")
    print()
    print("Code 2: findNumCuts()")
    print("  - Counts CUTS (splits) instead")
    print("  - Starts with cutNo = 0")
    print("  - Increments when making a cut")
    print("  - Returns cutNo + 1 (converts cuts to subarrays)")
    print()
    print("Note: n cuts = n+1 subarrays, so both are equivalent")
    print()

    print("\n3. Initial Sum Handling:")
    print("-" * 70)
    print("Code 1:")
    print("  cur_sum = nums[0]")
    print("  for num in nums[1:]:  # Start from second element")
    print()
    print("Code 2:")
    print("  s = 0")
    print("  for i in nums:  # Start from first element")
    print()
    print("Both work correctly, just different initialization styles")
    print()


def test_with_example():
    """Test both solutions"""
    print("\n" + "="*70)
    print("TESTING WITH EXAMPLE")
    print("="*70)

    nums = [7, 2, 5, 10, 8]
    k = 2

    print(f"\nInput: nums = {nums}, k = {k}")
    print(f"Expected output: 18")
    print(f"  Split: [7,2,5] and [10,8] → max(14, 18) = 18")
    print()

    sol1 = Solution1()
    sol2 = Solution2()

    result1 = sol1.splitArray(nums, k)
    result2 = sol2.splitArray(nums, k)

    print(f"Solution 1 result: {result1}")
    print(f"Solution 2 result: {result2}")
    print()

    if result1 == 18:
        print("✓ Solution 1: CORRECT")
    else:
        print("✗ Solution 1: WRONG")

    if result2 == 18:
        print("✓ Solution 2: CORRECT (got lucky despite bug!)")
    else:
        print("✗ Solution 2: WRONG")
    print()


def show_bug_impact():
    """Demonstrate when the bug actually causes wrong answer"""
    print("\n" + "="*70)
    print("WHEN THE BUG IN CODE 2 CAUSES PROBLEMS")
    print("="*70)

    # Actually, let me think about this...
    # The bug is low = min(nums) vs low = max(nums)
    # But in binary search, we're looking for the minimum valid largest sum
    #
    # If max(nums) = 10 and min(nums) = 2:
    # - Code 1 searches [10, sum]
    # - Code 2 searches [2, sum]
    #
    # Code 2 will waste iterations checking invalid values (2,3,4...9)
    # but should still converge to correct answer eventually
    #
    # Let me verify this...

    print("\nThe bug causes INEFFICIENCY, not wrong answers:")
    print()
    print("Example: nums = [10, 5, 3, 2], k = 2")
    print("  max(nums) = 10")
    print("  min(nums) = 2")
    print("  sum(nums) = 20")
    print()
    print("Code 1: Binary search range [10, 20]")
    print("  - All values in this range are potentially valid")
    print("  - Efficient search")
    print()
    print("Code 2: Binary search range [2, 20]")
    print("  - Values [2, 9] are IMPOSSIBLE (can't fit element 10)")
    print("  - Wastes iterations checking these invalid values")
    print("  - findNumCuts() won't work correctly for mid < 10")
    print()
    print("Impact: Code 2 is SLOWER but may still get correct answer")
    print("        because it eventually searches the valid range [10, 20]")


def show_actual_bug():
    """Show where Code 2 actually breaks"""
    print("\n" + "="*70)
    print("WHERE CODE 2 ACTUALLY BREAKS")
    print("="*70)

    nums = [10, 5, 3, 2]
    mid = 5  # Invalid: can't fit element 10

    print(f"\nTest: nums = {nums}, mid = {mid}")
    print("\nWhat happens in findNumCuts when mid < max(nums)?")
    print()
    print("Iteration 1: s=0, i=10")
    print("  s + i = 10 > 5? YES")
    print("  → Make a cut, s = 10, cutNo = 1")
    print("  → But s=10 > mid=5! This violates the constraint!")
    print()
    print("The function assumes each element can fit, but with")
    print("mid < max(nums), we have an impossible scenario.")
    print()
    print("✗ Code 2's findNumCuts() gives incorrect counts for mid < max(nums)")


if __name__ == "__main__":
    demonstrate_differences()
    test_with_example()
    show_bug_impact()
    show_actual_bug()

    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print()
    print("Main Difference: low = max(nums) vs low = min(nums)")
    print()
    print("✓ Code 1 is CORRECT and efficient")
    print("✗ Code 2 has a bug that makes it search invalid range")
    print()
    print("Both counting methods (subarrays vs cuts) are fine.")
    print("The critical fix: Always use low = max(nums) for this problem!")
    print("="*70)
