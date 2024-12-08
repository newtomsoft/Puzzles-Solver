import unittest
from unittest import TestCase

from Puzzles.Bimaru.BimaruGame import BimaruGame
from Utils.Grid import Grid


class BimaruGameTests(TestCase):
    def test_grid_must_be_square_raises_value_error(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        boats = {'column': [1, 0, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0, 0, 0]}
        boats_number_by_size = {1: 1}
        with self.assertRaises(ValueError) as context:
            BimaruGame((grid, boats, boats_number_by_size))
        self.assertEqual("The grid must be square", str(context.exception))

    def test_grid_must_be_at_least_4x4_raises_value_error(self):
        grid = Grid([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ])
        boats = {'column': [1, 0, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0, 0, 0]}
        boats_number_by_size = {1: 1}
        with self.assertRaises(ValueError) as context:
            BimaruGame((grid, boats, boats_number_by_size))
        self.assertEqual("The grid must be at least 6x6", str(context.exception))

    def test_boats_number_by_size_not_filled(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        boats = {'column': [1, 0, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0, 0]}
        boats_number_by_size = {}
        with self.assertRaises(ValueError) as context:
            BimaruGame((grid, boats, boats_number_by_size))
        self.assertEqual("At least one boat must be placed", str(context.exception))

    def test_boats_column_not_compliant(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        boats = {'column': [1, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0, 0]}
        boats_number_by_size = {1: 1}
        with self.assertRaises(ValueError) as context:
            BimaruGame((grid, boats, boats_number_by_size))
        self.assertEqual("Boat parts column must have the same length as the columns number", str(context.exception))

    def test_boats_row_not_compliant(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        boats = {'column': [1, 0, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0]}
        boats_number_by_size = {1: 1}
        with self.assertRaises(ValueError) as context:
            BimaruGame((grid, boats, boats_number_by_size))
        self.assertEqual("Boat parts row must have the same length as the rows number", str(context.exception))


if __name__ == '__main__':
    unittest.main()
