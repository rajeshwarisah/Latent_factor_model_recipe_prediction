"""
Next Permutation - LeetCode Problem

Find the next lexicographically greater permutation.
If not possible, return the lowest permutation (sorted ascending).

Algorithm:
1. Find the rightmost position i where nums[i] < nums[i+1] (the "pivot")
2. If no such position exists, reverse the entire array
3. Otherwise:
   - Find the rightmost position j where nums[j] > nums[i]
   - Swap nums[i] and nums[j]
   - Reverse the suffix starting from i+1
"""

from typing import List

class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)

        # Step 1: Find the pivot (rightmost position where nums[i] < nums[i+1])
        i = n - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1

        # Step 2: If no pivot found, array is in descending order
        # Reverse it to get the smallest permutation
        if i == -1:
            nums.reverse()  # In-place reverse
            return

        # Step 3: Find the rightmost element greater than nums[i]
        # The suffix nums[i+1:] is in descending order
        j = n - 1
        while j > i and nums[j] <= nums[i]:
            j -= 1

        # Step 4: Swap nums[i] and nums[j]
        nums[i], nums[j] = nums[j], nums[i]

        # Step 5: Reverse the suffix starting from i+1
        # This makes it the smallest possible arrangement
        nums[i + 1:] = nums[i + 1:][::-1]  # In-place reverse of suffix


class SolutionWithExplanation:
    """Version with detailed comments"""
    def nextPermutation(self, nums: List[int]) -> None:
        n = len(nums)

        # Find the pivot: rightmost ascending pair
        # Example: [4, 3, 6, 4, 3, 2]
        #           i=1 (3 < 6, this is our pivot)
        i = n - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1

        if i == -1:
            # Array is completely descending, reverse it
            nums.reverse()
            return

        # Find swap position: rightmost element > nums[i]
        # Suffix nums[i+1:] is descending: [6, 4, 3, 2]
        # We need smallest element > nums[i]=3, which is 4 at position j=3
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1

        # Swap pivot with the found element
        # [4, 3, 6, 4, 3, 2] -> [4, 4, 6, 3, 3, 2]
        nums[i], nums[j] = nums[j], nums[i]

        # Reverse suffix to get next smallest arrangement
        # [4, 4, 6, 3, 3, 2] -> [4, 4, 2, 3, 3, 6]
        nums[i + 1:] = nums[i + 1:][::-1]


# Test cases
def test_next_permutation():
    solution = Solution()

    # Test 1
    nums1 = [4, 3, 6, 4, 3, 2]
    print(f"Original: {nums1}")
    solution.nextPermutation(nums1)
    print(f"Next:     {nums1}")
    print(f"Expected: [4, 4, 2, 3, 3, 6]")
    print()

    # Test 2: Simple case
    nums2 = [1, 2, 3]
    print(f"Original: {nums2}")
    solution.nextPermutation(nums2)
    print(f"Next:     {nums2}")
    print(f"Expected: [1, 3, 2]")
    print()

    # Test 3: Descending order (wrap around)
    nums3 = [3, 2, 1]
    print(f"Original: {nums3}")
    solution.nextPermutation(nums3)
    print(f"Next:     {nums3}")
    print(f"Expected: [1, 2, 3]")
    print()

    # Test 4: With duplicates
    nums4 = [1, 3, 2]
    print(f"Original: {nums4}")
    solution.nextPermutation(nums4)
    print(f"Next:     {nums4}")
    print(f"Expected: [2, 1, 3]")
    print()

    # Test 5: Single swap needed
    nums5 = [1, 5, 1]
    print(f"Original: {nums5}")
    solution.nextPermutation(nums5)
    print(f"Next:     {nums5}")
    print(f"Expected: [5, 1, 1]")
    print()


def visualize_algorithm():
    """Step-by-step visualization"""
    print("="*70)
    print("ALGORITHM VISUALIZATION: [4, 3, 6, 4, 3, 2]")
    print("="*70)
    print()

    nums = [4, 3, 6, 4, 3, 2]
    print(f"Original: {nums}")
    print()

    # Step 1: Find pivot
    print("Step 1: Find pivot (rightmost i where nums[i] < nums[i+1])")
    print("  Index: 5 4 3 2 1 0")
    print(f"  Array: {nums}")
    print("         ^ ^ ^ ^")
    print("  Scanning right to left:")
    print("    - nums[4]=3 >= nums[5]=2? YES, continue")
    print("    - nums[3]=4 >= nums[4]=3? YES, continue")
    print("    - nums[2]=6 >= nums[3]=4? YES, continue")
    print("    - nums[1]=3 >= nums[2]=6? NO! Found pivot at i=1")
    print()

    # Step 2: Find swap position
    print("Step 2: Find rightmost j where nums[j] > nums[i=1]=3")
    print(f"  Suffix nums[2:] = {nums[2:]} (descending)")
    print("  Scanning right to left:")
    print("    - nums[5]=2 > 3? NO")
    print("    - nums[4]=3 > 3? NO")
    print("    - nums[3]=4 > 3? YES! Found j=3")
    print()

    # Step 3: Swap
    print(f"Step 3: Swap nums[1] and nums[3]")
    print(f"  Before: {nums}")
    nums[1], nums[3] = nums[3], nums[1]
    print(f"  After:  {nums}")
    print()

    # Step 4: Reverse suffix
    print(f"Step 4: Reverse suffix nums[2:]")
    print(f"  Before: {nums}")
    print(f"  Suffix: {nums[2:]}")
    nums[2:] = nums[2:][::-1]
    print(f"  After:  {nums}")
    print()
    print(f"✓ Result: {nums}")
    print("="*70)


if __name__ == "__main__":
    print("TESTING NEXT PERMUTATION\n")
    test_next_permutation()
    print()
    visualize_algorithm()
