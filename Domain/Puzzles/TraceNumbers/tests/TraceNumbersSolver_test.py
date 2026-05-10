import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.TraceNumbers.TraceNumbersSolver import TraceNumbersSolver

_ = 0


class TraceNumbersSolverTests(TestCase):
    def test_solution_7x7_3ne1r(self):
        # https://gridpuzzle.com/trace-numbers/3ne1r
        grid = Grid([
            [6, 5, 1, 1, 2, 0, 1],
            [4, 0, 2, 0, 0, 3, 0],
            [0, 0, 3, 2, 0, 0, 4],
            [3, 2, 0, 0, 1, 0, 5],
            [0, 5, 0, 4, 0, 3, 6],
            [0, 6, 0, 4, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 5],
        ])

        game_solver = TraceNumbersSolver(grid)
        solution = game_solver.get_solution()

        # Verify solution is not empty
        self.assertNotEqual(Grid.empty(), solution)

        # Verify each path contains numbers 1-6
        for path_idx in range(4):
            path_values = [grid[r][c] for r in range(7) for c in range(7) if solution[r][c] == path_idx and grid[r][c] > 0]
            self.assertEqual(sorted(path_values), [1, 2, 3, 4, 5, 6], f"Path {path_idx} should contain values 1-6")

        # Verify all cells are assigned
        for r in range(7):
            for c in range(7):
                self.assertNotEqual(-1, solution[r][c], f"Cell ({r},{c}) should be assigned to a path")

        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
