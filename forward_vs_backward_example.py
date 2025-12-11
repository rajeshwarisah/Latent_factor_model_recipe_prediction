"""
1D Example: Why Forward DP Doesn't Work Well

Consider a simple 1D dungeon: [10, -15, 10]
"""

def forward_dp_attempt(dungeon):
    """
    Forward DP: Try to track minimum initial health needed.
    The problem: we can't make optimal decisions without knowing what's ahead.
    """
    print("=== Forward DP Attempt ===")
    print(f"Dungeon: {dungeon}\n")

    # Let's try to track: what's the minimum health needed to get HERE?
    # But this doesn't tell us if we'll survive the rest of the journey!

    n = len(dungeon)
    # Track (min_initial_health_needed, current_health)
    dp = [None] * n

    # Cell 0: Need enough to not die
    if dungeon[0] >= 0:
        dp[0] = (1, 1 + dungeon[0])  # Start with 1, gain health
    else:
        dp[0] = (1 - dungeon[0], 1)  # Need enough to survive, end with 1

    print(f"Cell 0 (value={dungeon[0]}): {dp[0]}")
    print(f"  → Start with {dp[0][0]} health, end with {dp[0][1]} health")

    for i in range(1, n):
        prev_min_initial, prev_current = dp[i-1]
        new_health = prev_current + dungeon[i]

        print(f"\nCell {i} (value={dungeon[i]}):")
        print(f"  → Coming from cell {i-1} with {prev_current} health")
        print(f"  → After this cell: {prev_current} + {dungeon[i]} = {new_health}")

        if new_health >= 1:
            # We survive with current initial health
            dp[i] = (prev_min_initial, new_health)
            print(f"  → Still need initial health: {prev_min_initial}, current: {new_health}")
        else:
            # We'd die! Need to increase initial health
            # But by how much? This is where it gets complicated!
            deficit = 1 - new_health
            new_initial = prev_min_initial + deficit
            dp[i] = (new_initial, 1)
            print(f"  → WOULD DIE! Need {deficit} more initial health")
            print(f"  → New minimum initial: {new_initial}")

    print(f"\n❌ Forward DP result: {dp[-1][0]}")
    print("Problem: We had to BACKTRACK and adjust when we discovered we'd die!")
    return dp[-1][0]


def backward_dp_correct(dungeon):
    """
    Backward DP: Work from destination to start.
    At each cell, we know exactly how much health we need to survive the rest.
    """
    print("\n=== Backward DP (Correct) ===")
    print(f"Dungeon: {dungeon}\n")

    n = len(dungeon)
    # dp[i] = minimum health needed when ENTERING cell i
    dp = [0] * n

    # Last cell: need at least 1 after taking the hit/gain
    dp[n-1] = max(1, 1 - dungeon[n-1])
    print(f"Cell {n-1} (value={dungeon[n-1]}): need {dp[n-1]} health before entering")
    print(f"  → {dp[n-1]} + {dungeon[n-1]} = {dp[n-1] + dungeon[n-1]} after (must be ≥1)")

    # Work backwards
    for i in range(n-2, -1, -1):
        # We need enough health to have dp[i+1] AFTER this cell
        dp[i] = max(1, dp[i+1] - dungeon[i])
        print(f"\nCell {i} (value={dungeon[i]}): need {dp[i]} health before entering")
        print(f"  → {dp[i]} + {dungeon[i]} = {dp[i] + dungeon[i]} after")
        print(f"  → This gives us {dp[i] + dungeon[i]} for next cell (need {dp[i+1]})")

    print(f"\n✓ Backward DP result: {dp[0]}")
    print("Advantage: No backtracking! We know exactly what's needed at each step.")
    return dp[0]


def verify_solution(dungeon, initial_health):
    """Verify that the initial health works"""
    print(f"\n=== Verification with initial health = {initial_health} ===")
    health = initial_health
    for i, value in enumerate(dungeon):
        print(f"Cell {i}: health {health} + {value} = {health + value}", end="")
        health += value
        if health < 1:
            print(f" ❌ DIED!")
            return False
        print(f" ✓")
    print(f"Final health: {health} ✓✓")
    return True


if __name__ == "__main__":
    # Example: [10, -15, 10]
    # - Cell 0: +10 health (gain)
    # - Cell 1: -15 health (demon!)
    # - Cell 2: +10 health (gain)

    dungeon = [10, -15, 10]

    forward_result = forward_dp_attempt(dungeon)
    backward_result = backward_dp_correct(dungeon)

    print("\n" + "="*60)
    print(f"Forward DP: {forward_result}")
    print(f"Backward DP: {backward_result}")
    print("="*60)

    verify_solution(dungeon, backward_result)

    print("\n" + "="*60)
    print("KEY INSIGHT:")
    print("Forward DP requires complex state tracking and backtracking")
    print("because we don't know future requirements when making decisions.")
    print("\nBackward DP is simpler: at each cell we know EXACTLY how much")
    print("health we need because we've already computed what's ahead!")
    print("="*60)
