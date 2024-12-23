import unittest
from unittest import TestCase

from Puzzles.Stitches.StitchesGame import StitchesGame
from Puzzles.Thermometers.ThermometersGame import ThermometersGame
from Utils.Direction import Direction
from Utils.Grid import Grid


class ThermometersGameTests(TestCase):
    def test_solution_grid_not_a_square(self):
        grid = Grid([
            [0, 1, 1, 1],
            [0, 2, 2, 1],
            [0, 2, 2, 1],
            [0, 2, 2, 1],
            [0, 2, 2, 1],
        ])
        full_by_column_row = {'column': [1, 1, 1, 1], 'row': [1, 1, 1, 1, 1]}
        with self.assertRaises(ValueError) as context:
            ThermometersGame(grid, full_by_column_row)
        self.assertEqual("The grid must be square", str(context.exception))

    def test_solution_grid_size_less_than_4(self):
        grid = Grid([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ])
        full_by_column_row = {'column': [1, 1, 1], 'row': [1, 1, 1]}
        with self.assertRaises(ValueError) as context:
            ThermometersGame(grid, full_by_column_row)
        self.assertEqual("The grid must be at least 4x4", str(context.exception))


if __name__ == '__main__':
    unittest.main()
