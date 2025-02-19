import unittest
from unittest import TestCase

from Puzzles.BinairoPlus.BinairoPlusSolver import BinairoPlusSolver
from SolverEngineAdapters.OrToolsSolverEngine import Z3SolverEngine
from Utils.Grid import Grid


class BinairoPlusSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_6x6(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, 1, 0, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [1, -1, -1, -1, -1, 0],
            [1, -1, 1, 0, -1, 1],
        ])
        comparison_operators = {
            'equal_on_columns': [(2, 0), (3, 4)],
            'equal_on_rows': [(1, 1), (1, 3)],
            'non_equal_on_columns': [(0, 2), (0, 3), (2, 5), (3, 1)],
            'non_equal_on_rows': []
        }
        expected_grid = Grid([
            [0, 1, 1, 0, 0, 1],
            [1, 0, 0, 1, 1, 0],
            [0, 1, 1, 0, 0, 1],
            [0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 1, 0],
            [1, 0, 1, 0, 0, 1]
        ])
        game_solver = BinairoPlusSolver(grid, comparison_operators, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)


if __name__ == '__main__':
    unittest.main()
