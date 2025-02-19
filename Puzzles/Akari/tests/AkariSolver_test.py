import unittest
from unittest import TestCase

from Puzzles.Akari.AkariSolver import AkariSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine
from Utils.Grid import Grid


class AkariSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_grid_too_small_column(self):
        data_game = {
            'rows_number': 7,
            'columns_number': 6,
            'black_cells': {},
            'number_constraints': {}
        }

        with self.assertRaises(ValueError) as context:
            AkariSolver(data_game, self.get_solver_engine())
        self.assertEqual("Akari grid must be at least 7x7", str(context.exception))

    def test_solution_grid_too_small_row(self):
        data_game = {
            'rows_number': 6,
            'columns_number': 7,
            'black_cells': {},
            'number_constraints': {}
        }

        with self.assertRaises(ValueError) as context:
            AkariSolver(data_game, self.get_solver_engine())
        self.assertEqual("Akari grid must be at least 7x7", str(context.exception))

    def test_solution_7x7(self):
        data_game = {
            'rows_number': 7,
            'columns_number': 7,
            'black_cells': {(0, 4), (1, 1), (1, 5), (2, 0), (3, 3), (4, 6), (5, 1), (5, 5), (6, 2)},
            'number_constraints': {(0, 4): 1, (1, 1): 1, (1, 5): 3, (2, 0): 2, (3, 3): 2, (5, 5): 2},
        }
        expected_grid = Grid([
            [0, 0, 1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0],
            [1, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 1, 0],
        ])
        game_solver = AkariSolver(data_game, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)


if __name__ == '__main__':
    unittest.main()
