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

    def test_solution_with_sum_thermometer_cells_constraint(self):
        grid = Grid([
            ['c1', 'sh', 'sh', 'e3'],
            ['s4', 'c1', 'c2', 's2'],
            ['s1', 'c3', 'e4', 'sv'],
            ['e1', 'sh', 'sh', 'c3'],
        ])
        full_by_column_row = {'column': [2, 0, 1, 3], 'row': [1, 2, 1, 2]}
        game = ThermometersGame(grid, full_by_column_row)
        solution = game.get_solution()
        self.assertTrue(all([full_by_column_row['row'][i] == sum(row) for i, row in enumerate(solution.matrix)]))
        self.assertTrue(all([full_by_column_row['column'][i] == sum(column) for i, column in enumerate(zip(*solution.matrix))]))

    def test_solution_empty(self):
        grid = Grid([
            ['c1', 'sh', 'sh', 'e3'],
            ['s4', 'c1', 'c2', 's2'],
            ['s1', 'c3', 'e4', 'sv'],
            ['e1', 'sh', 'sh', 'c3'],
        ])
        full_by_column_row = {'column': [1, 0, 0, 0], 'row': [1, 0, 0, 0]}
        game = ThermometersGame(grid, full_by_column_row)
        solution = game.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_self(self):
        grid = Grid([
            ['c1', 'sh', 'sh', 'e3'],
            ['s4', 'c1', 'c2', 's2'],
            ['s1', 'c3', 'e4', 'sv'],
            ['e1', 'sh', 'sh', 'c3'],
        ])
        expected_solution = Grid([
            [1, 0, 0, 0],
            [1, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 1, 1],
        ])
        full_by_column_row = {'column': [2, 0, 1, 3], 'row': [1, 2, 1, 2]}
        game = ThermometersGame(grid, full_by_column_row)
        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)

if __name__ == '__main__':
    unittest.main()
