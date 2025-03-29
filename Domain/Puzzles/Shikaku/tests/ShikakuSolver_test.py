import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Shikaku.ShikakuSolver import ShikakuSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine


class ShikakuSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_grid_must_be_at_least_5x5_raises_value_error(self):
        grid = Grid([
            [1, 1, 1, 2],
            [1, 3, 1, 1],
            [1, 3, 3, 4],
            [1, 1, 3, 4],
            [1, 3, 3, 4],
        ])
        with self.assertRaises(ValueError) as context:
            ShikakuSolver(grid, self.get_solver_engine())

        self.assertEqual(str(context.exception), "The grid must be at least 5x5")

    def test_grid_numbers_sum_equal_cells_number(self):
        grid = Grid([
            [24, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
        ])
        with self.assertRaises(ValueError) as context:
            ShikakuSolver(grid, self.get_solver_engine())

        self.assertEqual(str(context.exception), "Sum of numbers must be equal to the number of cells")

    def test_get_solution_1_rectangle(self):
        grid = Grid([
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, 25, -1, -1, -1],
            [-1, -1, -1, -1, -1],
        ])
        expected_grid = Grid([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ])
        game_solver = ShikakuSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_get_solution_2_rectangles(self):
        grid = Grid([
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [15, -1, -1, -1, 10],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
        ])
        expected_grid = Grid([
            [0, 0, 0, 1, 1],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 1, 1],
        ])
        game_solver = ShikakuSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_get_solution_3_rectangles(self):
        grid = Grid([
            [-1, -1, -1, 4, -1],
            [-1, -1, -1, -1, -1],
            [15, -1, -1, -1, 6],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
        ])
        expected_grid = Grid([
            [1, 1, 1, 0, 0],
            [1, 1, 1, 0, 0],
            [1, 1, 1, 2, 2],
            [1, 1, 1, 2, 2],
            [1, 1, 1, 2, 2]
        ])
        game_solver = ShikakuSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_get_solution_5x5(self):
        grid = Grid([
            [-1, -1, 4, -1, -1],
            [-1, -1, 3, -1, -1],
            [3, 2, -1, -1, -1],
            [4, -1, 4, -1, 2],
            [-1, -1, 3, -1, -1]
        ])
        expected_grid = Grid([
            [2, 0, 0, 0, 0],
            [2, 3, 1, 1, 1],
            [2, 3, 5, 5, 6],
            [4, 4, 5, 5, 6],
            [4, 4, 7, 7, 7]
        ])
        game_solver = ShikakuSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_get_solution_7x7(self):
        grid = Grid([
            [-1, 4, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, 6, 2, -1],
            [-1, -1, -1, -1, -1, 6, 6],
            [-1, 2, -1, -1, 4, -1, -1],
            [-1, 6, -1, 3, -1, -1, -1],
            [3, -1, -1, 3, -1, -1, -1],
            [-1, -1, -1, 2, -1, 2, -1]
        ])
        expected_grid = Grid([
            [0, 0, 1, 1, 1, 2, 4],
            [0, 0, 1, 1, 1, 2, 4],
            [3, 3, 3, 3, 3, 3, 4],
            [5, 5, 6, 6, 6, 6, 4],
            [9, 7, 7, 8, 8, 8, 4],
            [9, 7, 7, 10, 10, 10, 4],
            [9, 7, 7, 11, 11, 12, 12]
        ])
        game_solver = ShikakuSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)


if __name__ == '__main__':
    unittest.main()
