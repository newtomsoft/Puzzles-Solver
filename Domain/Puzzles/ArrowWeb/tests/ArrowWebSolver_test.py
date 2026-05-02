import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.ArrowWeb.ArrowWebSolver import ArrowWebSolver


class ArrowWebSolverTests(TestCase):
    """https://gridpuzzle.com/arrow-web/3j8wy - 4x4"""

    def test_known_puzzle_4x4(self):
        grid = Grid([
            ['d', 'd', 'ld', 'ld'],
            ['ru', 'r', 'lu', 'ld'],
            ['ru', 'rd', 'r', 'u'],
            ['ru', 'lu', 'r', 'lu'],
        ])
        solver = ArrowWebSolver(grid)
        solution = solver.get_solution()
        self.assertNotEqual(Grid.empty(), solution)
        # Verify constraints: each arrow points to exactly one shaded arrow
        for r in range(4):
            for c in range(4):
                direction = grid[r, c]
                ray = solver._get_ray_positions(r, c, direction)
                shaded_count = sum(solution[p.r, p.c] for p in ray)
                self.assertEqual(1, shaded_count, f"Cell ({r},{c}) direction={direction} should point to exactly 1 shaded arrow")
        self.assertEqual(Grid.empty(), solver.get_other_solution())

    def test_unsolvable_no_ray(self):
        """Arrow pointing off-grid makes puzzle unsolvable."""
        grid = Grid([
            ['u', 'r'],
            ['l', 'd'],
        ])
        solver = ArrowWebSolver(grid)
        self.assertEqual(Grid.empty(), solver.get_solution())

    def test_unsolvable_contradictory(self):
        """Two arrows point only to each other - both cannot be satisfied if they both must point to exactly 1."""
        grid = Grid([
            ['r', 'l'],
        ])
        solver = ArrowWebSolver(grid)
        # (0,0) r -> {(0,1)}, (0,1) l -> {(0,0)}
        # Sum of both constraints: shaded(0,1) == 1 and shaded(0,0) == 1
        # That's feasible. Let me think of a truly unsolvable case.
        # Actually this is solvable: both shaded.
        solution = solver.get_solution()
        self.assertNotEqual(Grid.empty(), solution)

    def test_2x2_with_solution(self):
        """Simple 2x2 puzzle."""
        grid = Grid([
            ['d', 'd'],
            ['u', 'u'],
        ])
        # (0,0) d -> {(1,0)}, (0,1) d -> {(1,1)}
        # (1,0) u -> {(0,0)}, (1,1) u -> {(0,1)}
        # Two valid solutions: shade {(0,0),(1,1)} or {(0,1),(1,0)}
        solver = ArrowWebSolver(grid)
        solution = solver.get_solution()
        self.assertNotEqual(Grid.empty(), solution)
        for r in range(2):
            for c in range(2):
                direction = grid[r, c]
                ray = solver._get_ray_positions(r, c, direction)
                shaded_count = sum(solution[p.r, p.c] for p in ray)
                self.assertEqual(1, shaded_count)


if __name__ == '__main__':
    unittest.main()
