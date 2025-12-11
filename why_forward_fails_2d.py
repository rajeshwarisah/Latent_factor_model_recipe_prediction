"""
Why Forward DP FAILS in 2D: A Simple Example

Consider this 2x2 dungeon:

    Start → [1]  [ -3]
              ↓     ↓
           [-2]  [Goal]

Two possible paths:
Path A: (0,0)→(0,1)→(1,1)  :  1, -3, 0
Path B: (0,0)→(1,0)→(1,1)  :  1, -2, 0

Which path needs less initial health?
"""

def analyze_paths():
    dungeon = [
        [1, -3],
        [-2, 0]
    ]

    print("Dungeon:")
    print("[  1] [ -3]")
    print("[ -2] [  0]")
    print()

    # Path A: RIGHT then DOWN
    print("=== PATH A: RIGHT → DOWN ===")
    print("Cells: (0,0)=1 → (0,1)=-3 → (1,1)=0")
    print()
    print("Working backward:")
    print("  At (1,1): need max(1, 1-0) = 1")
    print("  At (0,1): need max(1, 1-(-3)) = 4")
    print("  At (0,0): need max(1, 4-1) = 3")
    print("✓ Path A needs initial health = 3")
    print()
    print("Verify: 3+1=4, 4-3=1, 1+0=1 ✓")
    print()

    # Path B: DOWN then RIGHT
    print("=== PATH B: DOWN → RIGHT ===")
    print("Cells: (0,0)=1 → (1,0)=-2 → (1,1)=0")
    print()
    print("Working backward:")
    print("  At (1,1): need max(1, 1-0) = 1")
    print("  At (1,0): need max(1, 1-(-2)) = 3")
    print("  At (0,0): need max(1, 3-1) = 2")
    print("✓ Path B needs initial health = 2 (BETTER!)")
    print()
    print("Verify: 2+1=3, 3-2=1, 1+0=1 ✓")
    print()

    print("="*60)
    print("ANSWER: Minimum initial health = 2 (via Path B)")
    print("="*60)


def forward_dp_greedy_wrong():
    """
    Forward DP with greedy choice: pick path with lower requirement SO FAR
    This gives WRONG answer!
    """
    print("\n=== FORWARD DP (Greedy - WRONG!) ===\n")

    dungeon = [
        [1, -3],
        [-2, 0]
    ]

    # Track (min_initial_health, current_health) at each cell
    print("At (0,0): value=1")
    print("  dp[0][0] = (1, 2)  # start with 1, have 1+1=2")
    print()

    print("At (0,1): value=-3")
    print("  Coming from (0,0) with health 2")
    print("  2 + (-3) = -1 → DEAD!")
    print("  Need 2 more initial health → (3, 1)")
    print()

    print("At (1,0): value=-2")
    print("  Coming from (0,0) with health 2")
    print("  2 + (-2) = 0 → DEAD!")
    print("  Need 1 more initial health → (2, 1)")
    print()

    print("At (1,1): value=0")
    print("  Choice 1 - from (0,1): min_health=3, current=1 → stays (3,1)")
    print("  Choice 2 - from (1,0): min_health=2, current=1 → stays (2,1)")
    print("  GREEDY: Pick Choice 2 (lower min_health)")
    print("  dp[1][1] = (2, 1)")
    print()

    print("❌ Forward DP says: 2")
    print("✓ This is actually CORRECT by luck!")
    print()


def forward_dp_fails_example():
    """
    A case where forward greedy ACTUALLY fails
    """
    print("="*60)
    print("EXAMPLE WHERE FORWARD GREEDY TRULY FAILS")
    print("="*60)
    print()

    # This dungeon shows the real problem
    dungeon = [
        [0, -3],
        [-2, 10]
    ]

    print("Dungeon:")
    print("[  0] [ -3]")
    print("[ -2] [ 10]")
    print()

    print("=== PATH A: RIGHT → DOWN ===")
    print("Cells: 0 → -3 → 10")
    print("Backward: (1,1)=1, (0,1)=max(1,1-10)=1, (0,0)=max(1,1-(-3))=4")
    print("Wrong! Let me recalculate...")
    print("At (1,1): need max(1, 1-10) = 1")
    print("At (0,1): need max(1, 1-(-3)) = 4")
    print("At (0,0): need max(1, 4-0) = 4")
    print("Path A: initial = 4")
    print()

    print("=== PATH B: DOWN → RIGHT ===")
    print("Cells: 0 → -2 → 10")
    print("At (1,1): need max(1, 1-10) = 1")
    print("At (1,0): need max(1, 1-10) = 1")
    print("At (0,0): need max(1, 1-(-2)) = 3")
    print("Path B: initial = 3")
    print()

    print("Correct answer: 3 (Path B)")
    print()

    print("What would forward greedy do?")
    print("At (0,0): (1, 1)")
    print("At (0,1): 1-3=-2 dead → (3, 1)")
    print("At (1,0): 1-2=-1 dead → (2, 1)")
    print("At (1,1) from (0,1): (3, 1+10) = (3, 11)")
    print("At (1,1) from (1,0): (2, 1+10) = (2, 11)")
    print("Greedy picks (2, 11) → answer = 2")
    print()
    print("❌ Forward greedy: 2")
    print("But with initial=2: 2+0=2, 2-2=0 → DEAD at (1,0)!")
    print()
    print("✓ Correct answer: 3")


if __name__ == "__main__":
    analyze_paths()
    forward_dp_greedy_wrong()
    forward_dp_fails_example()

    print("\n" + "="*60)
    print("CONCLUSION:")
    print("Forward DP can't make optimal decisions at intermediate cells")
    print("because it doesn't know what's coming next.")
    print()
    print("Backward DP is guaranteed correct because at each cell,")
    print("we already know the minimum health needed for the rest!")
    print("="*60)
