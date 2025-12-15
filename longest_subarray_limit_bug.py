"""
Longest Continuous Subarray With Absolute Diff Less Than Limit

Problem: Find the longest subarray where |max - min| <= limit

Approach: Sliding window with monotonic deques
- maxQueue tracks maximum in current window
- minQueue tracks minimum in current window

CRITICAL BUG: Removing from wrong end of deque!
"""

from typing import List
from collections import deque

class BuggyVersion:
    """Original buggy code"""
    def longestSubarray(self, nums: List[int], limit: int) -> int:
        if len(nums) == 0:
            return 0
        maxQueue = deque()
        minQueue = deque()
        left = 0
        ans = 0

        for i, num in enumerate(nums):
            # ❌ BUG 1: Removing from FRONT when building monotonic deque!
            while maxQueue and maxQueue[0][0] <= num:
                maxQueue.popleft()  # ❌ WRONG END!
            maxQueue.append((num, i))

            # ❌ BUG 1: Same issue
            while minQueue and minQueue[0][0] >= num:
                minQueue.popleft()  # ❌ WRONG END!
            minQueue.append((num, i))

            # Check if window valid
            while maxQueue and minQueue and maxQueue[0][0] - minQueue[0][0] > limit:
                left += 1
                if minQueue[0][1] < left:
                    minQueue.popleft()
                if maxQueue[0][1] < left:
                    maxQueue.popleft()

            ans = max(ans, i - left + 1)
        return ans


class CorrectVersion:
    """Fixed version"""
    def longestSubarray(self, nums: List[int], limit: int) -> int:
        minQueue = deque()
        maxQueue = deque()
        left = 0
        maxLen = 0

        for right, num in enumerate(nums):
            # ✓ CORRECT: Remove from BACK to maintain monotonicity
            while len(minQueue) > 0 and nums[minQueue[-1]] >= num:
                minQueue.pop()  # ✓ Remove from BACK!
            minQueue.append(right)

            while len(maxQueue) > 0 and nums[maxQueue[-1]] <= num:
                maxQueue.pop()  # ✓ Remove from BACK!
            maxQueue.append(right)

            # Shrink window if invalid
            while nums[maxQueue[0]] - nums[minQueue[0]] > limit:
                left += 1
                # ✓ CORRECT: Remove from FRONT when element outside window
                if maxQueue[0] < left:
                    maxQueue.popleft()  # Remove from FRONT
                if minQueue[0] < left:
                    minQueue.popleft()  # Remove from FRONT

            maxLen = max(maxLen, right - left + 1)

        return maxLen


def explain_differences():
    """Detailed comparison"""
    print("="*70)
    print("KEY DIFFERENCES: Buggy vs Correct")
    print("="*70)
    print()

    print("DIFFERENCE 1: What to Store in Deque")
    print("-" * 70)
    print("❌ BUGGY: Stores (value, index) tuples")
    print("    maxQueue.append((num, i))")
    print()
    print("✓ CORRECT: Stores only indices")
    print("    maxQueue.append(right)")
    print("    Access value via: nums[maxQueue[0]]")
    print()
    print("Why correct is better:")
    print("  - More memory efficient")
    print("  - Cleaner code")
    print("  - Same functionality (can get value via nums[index])")
    print()

    print("DIFFERENCE 2: WHERE to Remove When Building Monotonic Deque")
    print("-" * 70)
    print("This is the CRITICAL BUG!")
    print()
    print("❌ BUGGY: Removes from FRONT")
    print("    while maxQueue and maxQueue[0][0] <= num:")
    print("        maxQueue.popleft()  # ❌ WRONG!")
    print()
    print("✓ CORRECT: Removes from BACK")
    print("    while maxQueue and nums[maxQueue[-1]] <= num:")
    print("        maxQueue.pop()  # ✓ CORRECT!")
    print()

    print("Why this matters:")
    print("-" * 70)
    print("Monotonic deque has TWO operations:")
    print()
    print("1. BUILDING MONOTONICITY (when adding new element):")
    print("   - Remove from BACK elements that break monotonicity")
    print("   - This maintains the sorted property")
    print()
    print("2. REMOVING EXPIRED ELEMENTS (outside window):")
    print("   - Remove from FRONT elements outside window")
    print("   - Front has oldest elements")
    print()
    print("BUGGY CODE CONFUSES THESE TWO OPERATIONS!")
    print()


def visualize_bug():
    """Show what goes wrong"""
    print("="*70)
    print("VISUALIZING THE BUG")
    print("="*70)
    print()

    nums = [8, 2, 4, 7]
    limit = 4

    print(f"Input: nums = {nums}, limit = {limit}")
    print()

    print("BUGGY EXECUTION (maxQueue for tracking max):")
    print("-" * 70)
    print()

    print("i=0, num=8:")
    print("  maxQueue is empty")
    print("  Append (8, 0)")
    print("  maxQueue: [(8, 0)]")
    print()

    print("i=1, num=2:")
    print("  Check: maxQueue[0][0] <= num? Is 8 <= 2? NO")
    print("  Append (2, 1)")
    print("  maxQueue: [(8, 0), (2, 1)]")
    print("  ❌ WRONG! Should be [(8, 0)] only!")
    print("  (2 should be removed since it's smaller)")
    print()

    print("i=2, num=4:")
    print("  Check: maxQueue[0][0] <= num? Is 8 <= 4? NO")
    print("  Append (4, 2)")
    print("  maxQueue: [(8, 0), (2, 1), (4, 2)]")
    print("  ❌ WRONG! Queue is not monotonic!")
    print()

    print("Result: Monotonic property BROKEN!")
    print("The queue should be decreasing but has: 8, 2, 4")
    print()

    print("CORRECT EXECUTION:")
    print("-" * 70)
    print()

    print("i=0, num=8:")
    print("  maxQueue is empty")
    print("  Append 0")
    print("  maxQueue: [0] → values: [8]")
    print()

    print("i=1, num=2:")
    print("  Check: nums[maxQueue[-1]] <= num? Is nums[0]=8 <= 2? NO")
    print("  Append 1")
    print("  maxQueue: [0, 1] → values: [8, 2]")
    print("  ✓ Decreasing: 8 > 2")
    print()

    print("i=2, num=4:")
    print("  Check: nums[maxQueue[-1]] <= num? Is nums[1]=2 <= 4? YES")
    print("  Pop from back! maxQueue: [0]")
    print("  Check again: nums[0]=8 <= 4? NO")
    print("  Append 2")
    print("  maxQueue: [0, 2] → values: [8, 4]")
    print("  ✓ Decreasing: 8 > 4")
    print()


def monotonic_deque_concept():
    """Explain monotonic deque concept"""
    print("="*70)
    print("MONOTONIC DEQUE CONCEPT")
    print("="*70)
    print()

    print("What is a Monotonic Deque?")
    print("-" * 70)
    print("A deque that maintains elements in sorted order")
    print("  - Monotonic increasing: front → back increasing")
    print("  - Monotonic decreasing: front → back decreasing")
    print()

    print("For Maximum Tracking:")
    print("-" * 70)
    print("Use DECREASING monotonic deque")
    print("  - Front always has the maximum")
    print("  - Example: [10, 7, 5, 3]")
    print()

    print("For Minimum Tracking:")
    print("-" * 70)
    print("Use INCREASING monotonic deque")
    print("  - Front always has the minimum")
    print("  - Example: [1, 3, 5, 7]")
    print()

    print("TWO OPERATIONS:")
    print("-" * 70)
    print()
    print("1. ADD element (maintain monotonicity):")
    print("   ┌─────────────┐")
    print("   │ Remove BACK │ ← Pop elements that break order")
    print("   └─────────────┘")
    print("   Example (decreasing): Adding 6 to [10, 7, 5]")
    print("     - 5 < 6? YES → pop 5")
    print("     - 7 > 6? YES → stop")
    print("     - Result: [10, 7, 6]")
    print()

    print("2. REMOVE expired (outside window):")
    print("   ┌──────────────┐")
    print("   │ Remove FRONT │ ← Front has oldest elements")
    print("   └──────────────┘")
    print("   Check if front index < window_left")
    print()


def test_both():
    """Test both versions"""
    print("="*70)
    print("TESTING BOTH VERSIONS")
    print("="*70)
    print()

    nums = [8, 2, 4, 7]
    limit = 4

    print(f"Input: nums = {nums}, limit = {limit}")
    print()

    buggy = BuggyVersion()
    correct = CorrectVersion()

    result_buggy = buggy.longestSubarray(nums, limit)
    result_correct = correct.longestSubarray(nums, limit)

    print(f"Buggy result: {result_buggy}")
    print(f"Correct result: {result_correct}")
    print()
    print("Expected: 2 (subarray [2, 4])")
    print()


if __name__ == "__main__":
    explain_differences()
    print()
    visualize_bug()
    print()
    monotonic_deque_concept()
    print()
    test_both()

    print("="*70)
    print("SUMMARY")
    print("="*70)
    print()
    print("The critical bug: Removing from WRONG END when building monotonic deque")
    print()
    print("❌ BUGGY: maxQueue.popleft() (removes from FRONT)")
    print("✓ CORRECT: maxQueue.pop() (removes from BACK)")
    print()
    print("Remember:")
    print("  - Building monotonicity: Remove from BACK")
    print("  - Removing expired: Remove from FRONT")
    print("="*70)
