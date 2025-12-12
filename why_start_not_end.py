"""
Why Can't the Brightest Position Be at an END point?

Key insight: Brightness INCREASES at START points and DECREASES at END points.
Therefore, maximum brightness occurs at START points, not END points.
"""

def visualize_brightness_changes():
    print("="*70)
    print("WHY WE CHECK START POINTS, NOT END POINTS")
    print("="*70)
    print()

    print("Example: lights = [[2, 3], [6, 2], [5, 1]]")
    print()
    print("Light coverage:")
    print("  Light 1: position=2, range=3 → covers [-1, 5]")
    print("  Light 2: position=6, range=2 → covers [4, 8]")
    print("  Light 3: position=5, range=1 → covers [4, 6]")
    print()

    print("Visual representation:")
    print()
    print("Position: -1  0  1  2  3  4  5  6  7  8")
    print("          |---|---|---|---|---|---|---|---|")
    print("Light 1:  [=================]")
    print("Light 2:              [=================]")
    print("Light 3:              [=======]")
    print()

    print("Brightness at each position:")
    print("Position  -1  0  1  2  3  4  5  6  7  8")
    print("Bright     1  1  1  1  1  3  2  1  1  0")
    print("           ↑           ↑  ↑  ↑  ↑")
    print("        start       start start end end")
    print()

    print("KEY OBSERVATIONS:")
    print("-" * 70)
    print("At START points (interval begins):")
    print("  - Brightness INCREASES by 1")
    print("  - Position 4: brightness jumps from 1 → 3 (TWO intervals start)")
    print("  - This is where we find MAXIMUM brightness!")
    print()
    print("At END points (interval ends):")
    print("  - Brightness DECREASES by 1")
    print("  - Position 5: brightness drops from 3 → 2 (one interval ends)")
    print("  - Position 6: brightness drops from 2 → 1 (one interval ends)")
    print("  - Can't be a new maximum here!")
    print()

    print("ANSWER: Maximum brightness = 3 at position 4")
    print("        This is a START point (where intervals 2 and 3 begin)")
    print()


def demonstrate_why_not_end():
    print("="*70)
    print("WHY END POINTS CAN'T BE THE ANSWER")
    print("="*70)
    print()

    print("Think about what happens at each type of position:")
    print()

    print("AT A START POINT:")
    print("-" * 70)
    print("  - A new interval begins")
    print("  - Brightness increases: brightness = previous + 1")
    print("  - Could be a NEW MAXIMUM ✓")
    print()
    print("Example: Position 4 in diagram above")
    print("  Before: brightness = 1 (only Light 1)")
    print("  At 4:   brightness = 3 (Light 1, 2, and 3 all overlap)")
    print("  → This IS the maximum!")
    print()

    print("AT AN END POINT:")
    print("-" * 70)
    print("  - An interval is ending")
    print("  - Brightness decreases: brightness = previous - 1")
    print("  - Can NEVER be a new maximum ✗")
    print()
    print("Example: Position 5 in diagram above")
    print("  Before: brightness = 3")
    print("  At 5:   brightness = 2 (Light 1 just ended)")
    print("  → Going DOWN, not a maximum")
    print()
    print("Example: Position 6 in diagram above")
    print("  Before: brightness = 2")
    print("  At 6:   brightness = 1 (Light 3 just ended)")
    print("  → Still going DOWN")
    print()


def edge_case_explanation():
    print("="*70)
    print("EDGE CASE: What if intervals touch exactly?")
    print("="*70)
    print()

    print("Example: [[1, 1], [2, 1]]")
    print("  Interval 1: [0, 2]")
    print("  Interval 2: [1, 3]")
    print()
    print("Position:  0  1  2  3")
    print("Interval1: [=====]")
    print("Interval2:    [=====]")
    print()
    print("Brightness: 1  2  2  1")
    print()
    print("The overlap is [1, 2] with brightness = 2")
    print()
    print("At position 1 (START of interval 2):")
    print("  - Brightness increases to 2")
    print("  - This is where maximum is detected ✓")
    print()
    print("At position 2 (END of interval 1):")
    print("  - Brightness is still 2, but about to decrease")
    print("  - We already found the maximum at position 1")
    print("  - No need to check here")
    print()


def algorithm_correctness():
    print("="*70)
    print("ALGORITHM CORRECTNESS")
    print("="*70)
    print()

    print("The sweep line algorithm:")
    print("1. Sorts intervals by START point")
    print("2. Processes intervals left to right")
    print("3. At each START point:")
    print("   - Removes intervals that ended before this start")
    print("   - Adds current interval")
    print("   - Checks if brightness is now maximum")
    print()

    print("Why this works:")
    print("-" * 70)
    print("✓ Every position with maximum brightness has at least one")
    print("  interval STARTING there (or to its left)")
    print()
    print("✓ When we process that interval's start, we count ALL")
    print("  intervals currently overlapping at that position")
    print()
    print("✓ If maximum brightness occurs at position X, we will")
    print("  detect it when processing the leftmost interval that")
    print("  covers X")
    print()

    print("Why we don't need to check END points:")
    print("-" * 70)
    print("✗ At an end point, brightness is DECREASING")
    print()
    print("✗ Any maximum that existed just before an end point")
    print("  would have been detected at some interval's start point")
    print()
    print("✗ Checking end points is redundant and gives wrong answers")
    print("  (we'd return a position where brightness is DROPPING,")
    print("  not where it's at maximum)")
    print()


def code_comparison():
    print("="*70)
    print("WHAT IF WE USED END POINTS? (WRONG)")
    print("="*70)
    print()

    print("WRONG approach:")
    print("-" * 70)
    print("""
for start, end in intervals:
    # ... remove expired intervals ...
    heap.push(end)
    if len(heap) > max_brightness:
        max_brightness = len(heap)
        result = end  # ❌ WRONG! Brightness is about to DECREASE here!
    """)
    print()

    print("Example: [[2, 3], [6, 2]]")
    print("  Intervals: [-1, 5], [4, 8]")
    print("  Maximum brightness = 2 at positions [4, 5]")
    print()
    print("If we returned END points:")
    print("  - At interval [-1, 5]: return 5")
    print("  - At interval [4, 8]: return 8")
    print()
    print("But brightness at position 5: about to drop from 2 to 1")
    print("And brightness at position 8: is 1 (only one interval)")
    print()
    print("Both WRONG! Should return 4 (START of second interval)")
    print()

    print("CORRECT approach:")
    print("-" * 70)
    print("""
for start, end in intervals:
    # ... remove expired intervals ...
    heap.push(end)
    if len(heap) > max_brightness:
        max_brightness = len(heap)
        result = start  # ✓ CORRECT! This is where brightness INCREASED
    """)
    print()


if __name__ == "__main__":
    visualize_brightness_changes()
    print()
    demonstrate_why_not_end()
    print()
    edge_case_explanation()
    print()
    algorithm_correctness()
    print()
    code_comparison()

    print("="*70)
    print("SUMMARY")
    print("="*70)
    print()
    print("The brightest position MUST be at a START point because:")
    print()
    print("1. Brightness INCREASES at start points → potential maximum")
    print("2. Brightness DECREASES at end points → can't be maximum")
    print("3. We want the leftmost position with max brightness")
    print("4. That position is where some interval(s) start, causing")
    print("   brightness to reach its maximum value")
    print()
    print("Using END points would give positions where brightness")
    print("is DROPPING, not where it's at its peak!")
    print("="*70)
