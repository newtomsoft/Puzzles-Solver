import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Akari.AkariSolver import AkariSolver


class AkariSolverTests(TestCase):
    def test_solution_grid_too_small_column(self):
        grid = Grid([[-1] * 6 for _ in range(7)])

        with self.assertRaises(ValueError) as context:
            AkariSolver(grid)
        self.assertEqual("Akari grid must be at least 7x7", str(context.exception))

    def test_solution_grid_too_small_row(self):
        grid = Grid([[-1] * 7 for _ in range(6)])

        with self.assertRaises(ValueError) as context:
            AkariSolver(grid)
        self.assertEqual("Akari grid must be at least 7x7", str(context.exception))

    def test_solution_7x7(self):
        # -1 = empty white
        # -2 = empty black
        # 0-4 = numbered black
        initial_grid = Grid([
            [-1, -1, -1, -1,  1, -1, -1],
            [-1,  1, -1, -1, -1,  3, -1],
            [ 2, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1,  2, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -2],
            [-1, -2, -1, -1, -1,  2, -1],
            [-1, -1, -2, -1, -1, -1, -1],
        ])
        expected_grid = Grid([
            [0, 0, 1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0],
            [1, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 1, 0],
        ])
        game_solver = AkariSolver(initial_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)


if __name__ == '__main__':
    unittest.main()
