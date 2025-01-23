import unittest
from unittest import TestCase

from Puzzles.TentaiShow.TentaiShowGame import TentaiShowGame
from Utils.Grid import Grid


class TentaiShowGameTests(TestCase):
    def test_solution_grid_square(self):
        grid = Grid([
            [0, 1, 1],
            [0, 2, 2],
        ])
        with self.assertRaises(ValueError) as context:
            TentaiShowGame(grid)
        self.assertEqual("Sudoku grid must be square", str(context.exception))


if __name__ == '__main__':
    unittest.main()
