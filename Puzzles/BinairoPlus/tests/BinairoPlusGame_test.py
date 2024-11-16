import unittest
from unittest import TestCase

from Grid import Grid
from Puzzles.BinairoPlus.BinairoPlusGame import BinairoPlusGame


class BinairoGameTests(TestCase):
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
        game = BinairoPlusGame(grid, comparison_operators)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)


if __name__ == '__main__':
    unittest.main()
