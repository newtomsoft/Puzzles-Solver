import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Akari.AkariSolver import AkariSolver


class AkariSolverTests(TestCase):
    def test_solution_grid_too_small_column(self):
        data_game = {
            'rows_number': 7,
            'columns_number': 6,
            'black_cells': {},
            'number_constraints': {}
        }

        with self.assertRaises(ValueError) as context:
            AkariSolver(data_game)
        self.assertEqual("Akari grid must be at least 7x7", str(context.exception))

    def test_solution_grid_too_small_row(self):
        data_game = {
            'rows_number': 6,
            'columns_number': 7,
            'black_cells': {},
            'number_constraints': {}
        }

        with self.assertRaises(ValueError) as context:
            AkariSolver(data_game)
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
        game_solver = AkariSolver(data_game)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)


if __name__ == '__main__':
    unittest.main()
