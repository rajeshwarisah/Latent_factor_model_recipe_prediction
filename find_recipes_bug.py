"""
Find All Recipes - Bug Analysis

Problem: Given recipes, their ingredients, and available supplies,
find which recipes can be made.

This is a topological sort problem using Kahn's algorithm.
"""

from typing import List
from collections import defaultdict, deque

class BuggyVersion:
    """Original buggy code"""
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        graph = defaultdict(list)
        indegree = defaultdict(int)

        # Build graph: ingredient -> recipe that needs it
        for i, ingredient in enumerate(ingredients):
            for item in ingredient:
                graph[item].append(recipes[i])
                indegree[recipes[i]] += 1

        reachedDegree = defaultdict(int)
        queue = deque()
        for supply in supplies:
            queue.append(supply)
            reachedDegree[supply] += 1

        while queue:
            supply = queue.popleft()
            for neigh in graph[supply]:
                # ❌ BUG: Recipe added to queue BEFORE all ingredients available!
                if neigh not in reachedDegree:
                    queue.append(neigh)  # Added after seeing FIRST ingredient!
                reachedDegree[neigh] += 1

        ans = []
        for recipe in recipes:
            if reachedDegree[recipe] == indegree[recipe]:
                ans.append(recipe)
        return ans


class CorrectVersion:
    """Fixed version"""
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        graph = defaultdict(list)
        indegree = defaultdict(int)

        # Build graph: ingredient -> recipes that need it
        for i, ingredient_list in enumerate(ingredients):
            for item in ingredient_list:
                graph[item].append(recipes[i])
                indegree[recipes[i]] += 1

        # BFS with topological sort
        queue = deque(supplies)
        makeable = set(supplies)

        while queue:
            item = queue.popleft()
            for recipe in graph[item]:
                indegree[recipe] -= 1
                # ✓ CORRECT: Only add recipe when ALL ingredients available
                if indegree[recipe] == 0:
                    queue.append(recipe)
                    makeable.add(recipe)

        # Return recipes that can be made, in original order
        return [r for r in recipes if r in makeable]


class AlternativeCorrectVersion:
    """Using the reachedDegree approach, but fixed"""
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        graph = defaultdict(list)
        indegree = defaultdict(int)

        for i, ingredient_list in enumerate(ingredients):
            for item in ingredient_list:
                graph[item].append(recipes[i])
                indegree[recipes[i]] += 1

        reachedDegree = defaultdict(int)
        queue = deque(supplies)

        while queue:
            item = queue.popleft()
            for recipe in graph[item]:
                reachedDegree[recipe] += 1
                # ✓ CORRECT: Only add when ALL ingredients seen
                if reachedDegree[recipe] == indegree[recipe]:
                    queue.append(recipe)

        return [r for r in recipes if reachedDegree[r] == indegree[r]]


def explain_bug():
    """Detailed explanation"""
    print("="*70)
    print("BUG ANALYSIS: Find All Recipes")
    print("="*70)
    print()

    print("THE BUG:")
    print("-" * 70)
    print("❌ WRONG:")
    print("    for neigh in graph[supply]:")
    print("        if neigh not in reachedDegree:")
    print("            queue.append(neigh)  # Add after seeing FIRST ingredient!")
    print("        reachedDegree[neigh] += 1")
    print()
    print("Why this is wrong:")
    print("  - A recipe gets added to the queue the FIRST time we see it")
    print("  - But a recipe might need MULTIPLE ingredients!")
    print("  - We should only process a recipe when ALL ingredients are available")
    print()

    print("✓ CORRECT (Standard topological sort):")
    print("    for recipe in graph[item]:")
    print("        indegree[recipe] -= 1")
    print("        if indegree[recipe] == 0:")
    print("            queue.append(recipe)  # Add only when ALL ingredients ready!")
    print()

    print("Or with reachedDegree:")
    print("    for recipe in graph[item]:")
    print("        reachedDegree[recipe] += 1")
    print("        if reachedDegree[recipe] == indegree[recipe]:")
    print("            queue.append(recipe)  # Same idea!")
    print()


def demonstrate_bug():
    """Show where the bug causes issues"""
    print("="*70)
    print("EXAMPLE WHERE BUG MANIFESTS")
    print("="*70)
    print()

    recipes = ["bread", "sandwich", "burger"]
    ingredients = [["yeast", "flour"], ["bread", "meat"], ["sandwich"]]
    supplies = ["yeast", "meat"]  # Missing flour!

    print(f"Recipes: {recipes}")
    print(f"Ingredients: {ingredients}")
    print(f"Supplies: {supplies}")
    print()
    print("Dependencies:")
    print("  bread needs: yeast, flour")
    print("  sandwich needs: bread, meat")
    print("  burger needs: sandwich")
    print()
    print("We have yeast and meat, but NO flour")
    print("Expected: Can't make any recipes")
    print()

    print("BUGGY EXECUTION:")
    print("-" * 70)
    print("Graph:")
    print("  yeast -> [bread]")
    print("  flour -> [bread]")
    print("  bread -> [sandwich]")
    print("  meat -> [sandwich]")
    print("  sandwich -> [burger]")
    print()
    print("Indegree:")
    print("  bread: 2, sandwich: 2, burger: 1")
    print()

    print("BFS Trace:")
    print("1. Start: queue = [yeast, meat]")
    print()
    print("2. Process yeast:")
    print("   - For neighbor 'bread':")
    print("     - bread not in reachedDegree, so ADD to queue ❌")
    print("     - reachedDegree[bread] = 1")
    print("   - queue = [meat, bread]")
    print()
    print("3. Process meat:")
    print("   - For neighbor 'sandwich':")
    print("     - sandwich not in reachedDegree, so ADD to queue ❌")
    print("     - reachedDegree[sandwich] = 1")
    print("   - queue = [bread, sandwich]")
    print()
    print("4. Process bread:")
    print("   - ⚠️  Processing bread even though we can't make it!")
    print("   - For neighbor 'sandwich':")
    print("     - sandwich IS in reachedDegree, don't add")
    print("     - reachedDegree[sandwich] = 2")
    print("   - queue = [sandwich]")
    print()
    print("5. Process sandwich:")
    print("   - ⚠️  Processing sandwich even though we can't make it!")
    print("   - For neighbor 'burger':")
    print("     - burger not in reachedDegree, so ADD to queue ❌")
    print("     - reachedDegree[burger] = 1")
    print("   - queue = [burger]")
    print()
    print("6. Process burger:")
    print("   - queue = []")
    print()

    print("Final check:")
    print("  bread: reachedDegree=1, indegree=2 → Can't make ✓")
    print("  sandwich: reachedDegree=2, indegree=2 → Can make ❌ WRONG!")
    print("  burger: reachedDegree=1, indegree=1 → Can make ❌ WRONG!")
    print()
    print("❌ BUGGY RESULT: [sandwich, burger]")
    print("✓ CORRECT RESULT: []")
    print()
    print("The bug: sandwich and burger get added to queue and processed")
    print("even though their dependencies (bread) can't be satisfied!")
    print()


def correct_execution():
    """Show correct execution"""
    print("="*70)
    print("CORRECT EXECUTION (Same Example)")
    print("="*70)
    print()

    print("BFS Trace (with fix):")
    print("1. Start: queue = [yeast, meat]")
    print()
    print("2. Process yeast:")
    print("   - For neighbor 'bread':")
    print("     - reachedDegree[bread] = 1")
    print("     - Is 1 == 2? NO, don't add to queue ✓")
    print("   - queue = [meat]")
    print()
    print("3. Process meat:")
    print("   - For neighbor 'sandwich':")
    print("     - reachedDegree[sandwich] = 1")
    print("     - Is 1 == 2? NO, don't add to queue ✓")
    print("   - queue = []")
    print()
    print("4. Queue empty, done")
    print()

    print("Final check:")
    print("  bread: reachedDegree=1, indegree=2 → Can't make")
    print("  sandwich: reachedDegree=1, indegree=2 → Can't make")
    print("  burger: reachedDegree=0, indegree=1 → Can't make")
    print()
    print("✓ CORRECT RESULT: []")
    print()


def test_both():
    """Test both versions"""
    print("="*70)
    print("TESTING BOTH VERSIONS")
    print("="*70)
    print()

    recipes = ["bread", "sandwich"]
    ingredients = [["yeast", "flour"], ["bread", "meat"]]
    supplies = ["yeast", "meat"]  # Missing flour

    print(f"Test case:")
    print(f"  Recipes: {recipes}")
    print(f"  Ingredients: {ingredients}")
    print(f"  Supplies: {supplies}")
    print()

    buggy = BuggyVersion()
    correct = CorrectVersion()

    result_buggy = buggy.findAllRecipes(recipes, ingredients, supplies)
    result_correct = correct.findAllRecipes(recipes, ingredients, supplies)

    print(f"Buggy result: {result_buggy}")
    print(f"Correct result: {result_correct}")
    print(f"Expected: []")
    print()


if __name__ == "__main__":
    explain_bug()
    print()
    demonstrate_bug()
    print()
    correct_execution()
    print()
    test_both()

    print("="*70)
    print("SUMMARY")
    print("="*70)
    print()
    print("The bug: Recipe added to queue when FIRST ingredient seen,")
    print("         not when ALL ingredients available")
    print()
    print("Fix: Only add recipe to queue when")
    print("     reachedDegree[recipe] == indegree[recipe]")
    print()
    print("This ensures we only process recipes we can actually make!")
    print("="*70)
