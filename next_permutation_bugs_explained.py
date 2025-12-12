"""
Bugs in the Original Next Permutation Code

Original code had 3 critical issues:
1. In-place modification not working correctly
2. Wrong swap position logic
3. Wrong suffix reversal logic
"""

from typing import List

class OriginalBuggy:
    """The original buggy code"""
    def nextPermutation(self, nums: List[int]) -> None:
        j = len(nums) - 1
        while j > 0 and nums[j] <= nums[j-1]:
            j -= 1

        if j == 0:
            nums = nums[::-1]  # ❌ BUG 1: Doesn't modify in-place!
            print(nums)
            return
        else:
            k = j - 1
            i = j
            while i < len(nums) and nums[k] < nums[i]:
                i += 1
            # ❌ BUG 2: After loop, i points to WRONG position!
            if i == len(nums):
                i = len(nums) - 1
            nums[i], nums[k] = nums[k], nums[i]
            # ❌ BUG 3: Wrong slice indices for reversal!
            nums = nums[:i+1] + nums[i+1::-1]  # Also doesn't modify in-place


class Fixed:
    """The corrected code"""
    def nextPermutation(self, nums: List[int]) -> None:
        n = len(nums)
        i = n - 2

        # Find pivot
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1

        if i == -1:
            nums.reverse()  # ✓ FIX 1: Use reverse() or nums[:] = nums[::-1]
            return

        # Find swap position from RIGHT to LEFT
        j = n - 1
        while nums[j] <= nums[i]:  # ✓ FIX 2: Scan from right, find rightmost > nums[i]
            j -= 1

        nums[i], nums[j] = nums[j], nums[i]
        nums[i + 1:] = nums[i + 1:][::-1]  # ✓ FIX 3: Reverse from i+1, use slice assignment


def explain_bug_1():
    """Bug 1: Not modifying in-place"""
    print("="*70)
    print("BUG 1: IN-PLACE MODIFICATION")
    print("="*70)
    print()
    print("❌ WRONG:")
    print("  nums = nums[::-1]")
    print()
    print("Why this doesn't work:")
    print("  - Creates a NEW list and assigns it to local variable 'nums'")
    print("  - The original list passed to the function is NOT modified")
    print("  - The caller won't see any changes")
    print()
    print("✓ CORRECT options:")
    print("  1. nums.reverse()              # Built-in reverse method")
    print("  2. nums[:] = nums[::-1]        # Slice assignment")
    print("  3. nums[:] = reversed(nums)    # Using reversed()")
    print()

    # Demonstration
    def wrong_way(lst):
        lst = lst[::-1]  # Doesn't modify original

    def right_way(lst):
        lst[:] = lst[::-1]  # Modifies original

    original = [1, 2, 3]
    test1 = original.copy()
    wrong_way(test1)
    print(f"After wrong_way: {test1}  (unchanged)")

    test2 = original.copy()
    right_way(test2)
    print(f"After right_way: {test2}  (modified!)")
    print()


def explain_bug_2():
    """Bug 2: Wrong swap position"""
    print("="*70)
    print("BUG 2: FINDING SWAP POSITION")
    print("="*70)
    print()

    nums = [4, 3, 6, 4, 3, 2]
    print(f"Example: {nums}")
    print(f"Pivot at k=1 (value=3)")
    print(f"Suffix [6, 4, 3, 2] is DESCENDING")
    print()

    print("❌ WRONG approach (scanning LEFT to RIGHT):")
    print("  i = j")
    print("  while i < len(nums) and nums[k] < nums[i]:")
    print("      i += 1")
    print()
    print("  Starting from i=2:")
    print("    - i=2: nums[1]=3 < nums[2]=6? YES, i=3")
    print("    - i=3: nums[1]=3 < nums[3]=4? YES, i=4")
    print("    - i=4: nums[1]=3 < nums[4]=3? NO, exit loop")
    print("  → i=4, but after loop i points to first element NOT greater!")
    print("  → Should swap with i-1=3, not i=4")
    print()

    print("✓ CORRECT approach (scanning RIGHT to LEFT):")
    print("  j = n - 1")
    print("  while nums[j] <= nums[i]:")
    print("      j -= 1")
    print()
    print("  Starting from j=5:")
    print("    - j=5: nums[5]=2 > nums[1]=3? NO, j=4")
    print("    - j=4: nums[4]=3 > nums[1]=3? NO, j=3")
    print("    - j=3: nums[3]=4 > nums[1]=3? YES, exit loop")
    print("  → j=3, correctly identifies rightmost element > pivot")
    print()

    print("Why RIGHT to LEFT?")
    print("  - Suffix is in DESCENDING order")
    print("  - We want the SMALLEST element that's still > pivot")
    print("  - That's the RIGHTMOST element > pivot in descending array")
    print()


def explain_bug_3():
    """Bug 3: Wrong reversal indices"""
    print("="*70)
    print("BUG 3: REVERSING THE SUFFIX")
    print("="*70)
    print()

    print("After swapping at position k=1:")
    nums = [4, 4, 6, 3, 3, 2]
    print(f"Array: {nums}")
    print(f"Need to reverse suffix starting from k+1=2")
    print()

    print("❌ WRONG (from original code):")
    print("  nums = nums[:i+1] + nums[i+1::-1]")
    print()
    print("Issues:")
    print("  1. Uses 'i' instead of 'k' (i was the swap position, not pivot)")
    print("  2. nums[i+1::-1] reverses from i+1 back to START, not end!")
    print("  3. Doesn't modify in-place")
    print()

    print("Example with i=3, k=1:")
    i, k = 3, 1
    result = nums[:i+1] + nums[i+1::-1]
    print(f"  nums[:i+1] = nums[:4] = {nums[:4]}")
    print(f"  nums[i+1::-1] = nums[3::-1] = {nums[3::-1]} (reversed to start!)")
    print(f"  Result: {result}  ❌ WRONG!")
    print()

    print("✓ CORRECT:")
    print("  nums[k+1:] = nums[k+1:][::-1]")
    print("  OR")
    print("  nums[i+1:] = nums[i+1:][::-1]  (if i is the pivot)")
    print()
    print(f"  nums[k+1:] = nums[2:] = {nums[2:]}")
    print(f"  Reversed: {nums[2:][::-1]}")
    nums[k+1:] = nums[k+1:][::-1]
    print(f"  Result: {nums}  ✓ CORRECT!")
    print()


def demonstrate_all_bugs():
    """Show how original code fails"""
    print("="*70)
    print("DEMONSTRATING ALL BUGS WITH EXAMPLE")
    print("="*70)
    print()

    # Test case that shows the bugs
    class BuggyVersion:
        def nextPermutation(self, nums: List[int]) -> None:
            j = len(nums) - 1
            while j > 0 and nums[j] <= nums[j-1]:
                j -= 1

            if j == 0:
                nums = nums[::-1]
                return
            else:
                k = j - 1
                i = j
                while i < len(nums) and nums[k] < nums[i]:
                    i += 1
                if i == len(nums):
                    i = len(nums) - 1
                nums[i], nums[k] = nums[k], nums[i]
                # This line doesn't modify nums in place!
                temp = nums[:i+1] + nums[i+1::-1]
                print(f"  Temp result: {temp} (but nums not modified in-place!)")

    nums = [4, 3, 6, 4, 3, 2]
    print(f"Input: {nums}")
    print(f"Expected: [4, 4, 2, 3, 3, 6]")
    print()

    buggy = BuggyVersion()
    buggy.nextPermutation(nums)
    print(f"Actual (buggy): {nums}")
    print()
    print("The bugs caused incorrect behavior!")


if __name__ == "__main__":
    explain_bug_1()
    explain_bug_2()
    explain_bug_3()
    demonstrate_all_bugs()

    print("\n" + "="*70)
    print("SUMMARY OF FIXES")
    print("="*70)
    print()
    print("1. Use nums.reverse() or nums[:] = nums[::-1] for in-place modification")
    print("2. Scan RIGHT to LEFT to find swap position in descending suffix")
    print("3. Reverse from i+1 (not from wrong position), use slice assignment")
    print("="*70)
