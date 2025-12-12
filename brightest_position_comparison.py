"""
Brightest Position - Comparing Two Implementations

Problem: Find the position with maximum overlapping light ranges.
Each light at position[i] with range[i] illuminates [position[i]-range[i], position[i]+range[i]]

Approach: Use sweep line with min heap to track active intervals.
"""

from typing import List
import heapq

class Solution1:
    """First implementation - HAS A BUG!"""
    def brightestPosition(self, lights: List[List[int]]) -> int:
        intervals = [[l[0]-l[1], l[0]+l[1]] for l in lights]
        heap = []
        intervals = sorted(intervals)
        ans = 0
        point = lights[0][0]  # ❌ BUG: Uses original lights[0][0], not sorted intervals

        for s, e in intervals:
            # ❌ CRITICAL BUG: Condition is BACKWARDS!
            while heap and heap[0] > s:  # Should be heap[0] < s
                heapq.heappop(heap)
            heapq.heappush(heap, e)

            if ans < len(heap):
                ans = len(heap)
                point = s

        return point


class Solution2:
    """Second implementation - CORRECT"""
    def brightestPosition(self, lights: List[List[int]]) -> int:
        lights.sort(key=lambda u: u[0] - u[1])  # Sort by left endpoint
        maxi = 0
        result = lights[0][0]  # After sorting, but not used correctly either
        heap = []

        for cent, dist in lights:
            left = cent - dist
            right = cent + dist

            # ✓ CORRECT: Remove intervals that end before current left
            while len(heap) > 0 and heap[0] < left:
                heapq.heappop(heap)
            heapq.heappush(heap, right)

            if maxi < len(heap):
                maxi = len(heap)
                result = left  # ✓ CORRECT: Use computed left, not original value

        return result


def explain_differences():
    """Detailed comparison"""
    print("="*70)
    print("KEY DIFFERENCES BETWEEN THE TWO IMPLEMENTATIONS")
    print("="*70)
    print()

    print("1. CRITICAL BUG - Heap Pop Condition")
    print("-" * 70)
    print("Code 1: while heap and heap[0] > s:")
    print("        ❌ WRONG! Pops when end > start")
    print()
    print("Code 2: while heap and heap[0] < left:")
    print("        ✓ CORRECT! Pops when end < start")
    print()
    print("Why this matters:")
    print("  We want to remove intervals that have ENDED before current start")
    print("  If heap[0] (earliest end point) < current start:")
    print("    → That interval doesn't overlap, remove it")
    print()
    print("  Code 1's condition heap[0] > s removes intervals that:")
    print("    - End AFTER current start (these SHOULD stay!)")
    print("    - This is completely backwards!")
    print()

    print("2. Data Structure Organization")
    print("-" * 70)
    print("Code 1:")
    print("  - Pre-processes into intervals: [[start, end], ...]")
    print("  - Sorts intervals (by start point)")
    print("  - Iterates over intervals")
    print()
    print("Code 2:")
    print("  - Keeps original format: [[position, range], ...]")
    print("  - Sorts by position - range (left endpoint)")
    print("  - Computes left/right in loop")
    print()
    print("Both approaches are valid in concept, but Code 1 has the bug.")
    print()

    print("3. Result Initialization")
    print("-" * 70)
    print("Code 1:")
    print("  point = lights[0][0]")
    print("  → Uses ORIGINAL lights array (before sorting intervals)")
    print("  → This could be wrong if the first light isn't leftmost!")
    print()
    print("Code 2:")
    print("  result = lights[0][0]")
    print("  → Uses lights AFTER sorting")
    print("  → Still just initialization, gets overwritten correctly")
    print()

    print("4. Variable Naming")
    print("-" * 70)
    print("Code 1: s, e (start, end) - but extracted from pre-made intervals")
    print("Code 2: cent, dist (center, distance) - clearer intent")
    print("        left, right - explicit computation")
    print()


def demonstrate_bug():
    """Show concrete example where Code 1 fails"""
    print("="*70)
    print("CONCRETE EXAMPLE SHOWING THE BUG")
    print("="*70)
    print()

    lights = [[1, 2], [4, 1]]
    # Light at position 1 with range 2: covers [-1, 3]
    # Light at position 4 with range 1: covers [3, 5]

    print(f"Lights: {lights}")
    print("Light 1: position=1, range=2 → covers [-1, 3]")
    print("Light 2: position=4, range=1 → covers [3, 5]")
    print()
    print("Overlapping at position 3, max brightness = 2")
    print("Should return: -1 or 3 (positions with max brightness)")
    print()

    print("What Code 1 does (BUGGY):")
    print("-" * 70)
    intervals = [[l[0]-l[1], l[0]+l[1]] for l in lights]
    print(f"Intervals: {intervals}")  # [[-1, 3], [3, 5]]
    intervals_sorted = sorted(intervals)
    print(f"Sorted: {intervals_sorted}")  # [[-1, 3], [3, 5]]
    print()

    print("Iteration 1: s=-1, e=3")
    print("  heap is empty, so while loop skips")
    print("  Push 3 to heap → heap=[3]")
    print("  ans=1, point=-1")
    print()

    print("Iteration 2: s=3, e=5")
    print("  while heap[0] > s: while 3 > 3? NO (3 is not > 3)")
    print("  Push 5 to heap → heap=[3, 5]")
    print("  ans=2, point=3")
    print()
    print("Returns: 3")
    print()

    print("What Code 2 does (CORRECT):")
    print("-" * 70)
    lights_sorted = sorted(lights, key=lambda u: u[0] - u[1])
    print(f"Sorted by left endpoint: {lights_sorted}")
    print()

    print("Iteration 1: cent=1, dist=2 → left=-1, right=3")
    print("  heap is empty, so while loop skips")
    print("  Push 3 to heap → heap=[3]")
    print("  maxi=1, result=-1")
    print()

    print("Iteration 2: cent=4, dist=1 → left=3, right=5")
    print("  while heap[0] < left: while 3 < 3? NO")
    print("  Push 5 to heap → heap=[3, 5]")
    print("  maxi=2, result=3")
    print()
    print("Returns: 3")
    print()


def demonstrate_bug_worse():
    """Example where Code 1 really breaks"""
    print("="*70)
    print("EXAMPLE WHERE CODE 1 REALLY FAILS")
    print("="*70)
    print()

    lights = [[2, 3], [6, 2]]
    # Light at position 2 with range 3: covers [-1, 5]
    # Light at position 6 with range 2: covers [4, 8]

    print(f"Lights: {lights}")
    print("Light 1: position=2, range=3 → covers [-1, 5]")
    print("Light 2: position=6, range=2 → covers [4, 8]")
    print()
    print("They overlap at [4, 5], max brightness = 2")
    print("Should return: -1 or 4 (leftmost position with max brightness)")
    print()

    print("What Code 1 does (BUGGY):")
    print("-" * 70)
    intervals = [[l[0]-l[1], l[0]+l[1]] for l in lights]
    print(f"Intervals: {intervals}")  # [[-1, 5], [4, 8]]
    intervals_sorted = sorted(intervals)
    print(f"Sorted: {intervals_sorted}")  # [[-1, 5], [4, 8]]
    print()

    print("Iteration 1: s=-1, e=5")
    print("  heap is empty")
    print("  Push 5 to heap → heap=[5]")
    print("  ans=1, point=-1")
    print()

    print("Iteration 2: s=4, e=8")
    print("  while heap[0] > s: while 5 > 4? YES!")
    print("  ❌ BUG: Pops 5 from heap (but interval ending at 5 DOES overlap!)")
    print("  heap=[]")
    print("  Push 8 to heap → heap=[8]")
    print("  ans stays 1 (len(heap)=1, not > ans)")
    print("  point=-1")
    print()
    print("Returns: -1 ❌ MISSED the overlap!")
    print()

    print("What Code 2 does (CORRECT):")
    print("-" * 70)
    lights_sorted = sorted(lights, key=lambda u: u[0] - u[1])
    print(f"Sorted by left endpoint: {lights_sorted}")
    print()

    print("Iteration 1: cent=2, dist=3 → left=-1, right=5")
    print("  heap is empty")
    print("  Push 5 to heap → heap=[5]")
    print("  maxi=1, result=-1")
    print()

    print("Iteration 2: cent=6, dist=2 → left=4, right=8")
    print("  while heap[0] < left: while 5 < 4? NO (5 is not < 4)")
    print("  ✓ CORRECT: Keep 5 in heap (interval still overlaps!)")
    print("  Push 8 to heap → heap=[5, 8]")
    print("  maxi=2, result=4")
    print()
    print("Returns: 4 ✓ CORRECT!")
    print()


if __name__ == "__main__":
    explain_differences()
    print()
    demonstrate_bug()
    print()
    demonstrate_bug_worse()

    print("="*70)
    print("SUMMARY")
    print("="*70)
    print()
    print("Code 1 has a CRITICAL BUG:")
    print("  while heap and heap[0] > s:  ❌ BACKWARDS!")
    print()
    print("Should be:")
    print("  while heap and heap[0] < s:  ✓ CORRECT")
    print()
    print("This bug causes Code 1 to:")
    print("  - Remove overlapping intervals from the heap")
    print("  - Miss counting overlaps")
    print("  - Give wrong answer")
    print()
    print("Code 2 is CORRECT with proper condition: heap[0] < left")
    print("="*70)
