import unittest
from unittest import TestCase

from Puzzles.Sumplete.SumpleteSolver import SumpleteSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine
from Utils.Grid import Grid


class SumpleteSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_grid_square(self):
        grid = Grid([
            [0, 1, 1],
            [0, 2, 2],
        ])
        with self.assertRaises(ValueError) as context:
            SumpleteSolver(grid, self.get_solver_engine())
        self.assertEqual("Sumplete grid must be square", str(context.exception))

    def test_solution_grid_size_less_than_2(self):
        grid = Grid([
            [0, 0],
            [0, 0],
        ])
        with self.assertRaises(ValueError) as context:
            SumpleteSolver(grid, self.get_solver_engine())
        self.assertEqual("Sumplete grid (without sums) must be at least 2x2", str(context.exception))

    def test_solution_3x3_without_solution(self):
        grid = Grid([
            [1, 2, 5],
            [3, 4, 6],
            [7, 8, 0],
        ])
        game_solver = SumpleteSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertIsNone(solution)

    def test_solution_3x3_basic(self):
        grid = Grid([
            [1, 2, 3],
            [3, 4, 7],
            [4, 6, 0],
        ])
        expected_solution = Grid([
            [True, True],
            [True, True]
        ])
        game_solver = SumpleteSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_3x3(self):
        grid = Grid([
            [1, 1, 1],
            [3, 3, 6],
            [4, 3, 0],
        ])
        expected_solution = Grid([
            [True, False],
            [True, True]
        ])
        game_solver = SumpleteSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_7x7(self):
        grid = Grid([
            [4, 2, 4, 6, 1, 7, 6, 15],
            [8, 8, 3, 5, 2, 1, 3, 14],
            [3, 2, 1, 1, 6, 8, 4, 18],
            [1, 2, 4, 5, 4, 4, 5, 9],
            [9, 5, 3, 5, 7, 3, 4, 10],
            [2, 5, 1, 5, 6, 6, 8, 6],
            [4, 8, 5, 2, 6, 5, 7, 13],
            [11, 10, 15, 13, 7, 15, 14, 0]
        ])
        expected_solution = Grid([
            [True, False, True, False, False, True, False],
            [False, True, True, False, False, False, True],
            [True, True, False, True, False, True, True],
            [False, False, True, True, False, False, False],
            [False, False, True, False, True, False, False],
            [False, False, True, True, False, False, False],
            [True, False, False, True, False, False, True],
        ])
        game_solver = SumpleteSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_9x9(self):
        grid = Grid([
            [-2, 13, 14, -14, -5, 1, 13, 4, 12, 39],
            [7, -15, 10, 2, 8, 12, -1, -18, -10, 23],
            [-5, 13, -2, -19, -16, 4, 1, 1, -11, -30],
            [10, 3, -9, 14, -14, -14, -16, -1, -5, -10],
            [-3, -18, 14, 9, -17, -15, 11, -10, 16, 10],
            [-15, -12, -8, 15, 3, -19, -16, -8, 3, -13],
            [4, -10, 11, -9, 9, -17, -5, -5, -9, -28],
            [-6, -17, -8, 12, 14, 15, 13, 15, 2, 23],
            [-10, -10, -13, -6, -1, 14, 19, 14, -10, -16],
            [-2, -34, 16, 15, 11, -37, 7, 18, 4, 0]
        ])
        expected_solution = Grid([
            [False, False, True, False, True, True, True, True, True],
            [True, True, True, True, True, True, True, False, False],
            [False, False, False, True, False, False, False, False, True],
            [True, True, True, True, True, True, False, False, False],
            [True, False, True, True, False, False, False, True, False],
            [False, True, False, True, False, True, False, False, True],
            [False, True, False, False, True, True, True, True, False],
            [True, False, False, False, True, False, False, True, False],
            [True, False, True, True, True, False, False, True, False]
        ])
        game_solver = SumpleteSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)


if __name__ == '__main__':
    unittest.main()
