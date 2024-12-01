import unittest
from unittest import TestCase

from Puzzles.Tents.TentsGame import TentsGame
from Utils.Grid import Grid


class TentsGameTests(TestCase):
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
        tents_numbers_by_column_row = {'column': [3, 0, 1, 1, 1, 1], 'row': [2, 0, 1, 1, 0, 3, 1]}
        with self.assertRaises(ValueError) as context:
            TentsGame((grid, tents_numbers_by_column_row))
        self.assertEqual(str(context.exception), "The grid must be square")

    def test_grid_must_be_at_least_6x6_raises_value_error(self):
        grid = Grid([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ])
        tents_numbers_by_column_row = {'column': [3, 0, 1, 1, 1], 'row': [2, 0, 1, 1, 0]}
        with self.assertRaises(ValueError) as context:
            TentsGame((grid, tents_numbers_by_column_row))
        self.assertEqual(str(context.exception), "The grid must be at least 6x6")

    def test_with_constraint_sum_in_row_column(self):
        grid = Grid([
            [0, 0, 0, -1, 0, 0],
            [0, -1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [-1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, -1, 0],
        ])
        tents_numbers_by_column_row = {'column': [2, 0, 0, 2, 0, 0], 'row': [0, 2, 0, 0, 0, 2]}
        expected_solution = Grid([
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 1, 0, 0],
        ])
        game = TentsGame((grid, tents_numbers_by_column_row))
        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)
        # other_solution = game.get_other_solution()

    def test_no_solution_with_constraint_no_adjacents_tents(self):
        grid = Grid([
            [0, -1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, -1],
            [-1, 0, -1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        tents_numbers_by_column_row = {'column': [1, 1, 1, 0, 1, 0], 'row': [0, 4, 0, 0, 0, 0]}

        game = TentsGame((grid, tents_numbers_by_column_row))
        solution = game.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_no_solution_with_no_tent_over_tree_constraint(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, -1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        tents_numbers_by_column_row = {'column': [0, 0, 1, 0, 0, 0], 'row': [0, 1, 0, 0, 0, 0]}
        game = TentsGame((grid, tents_numbers_by_column_row))
        solution = game.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_no_solution_with_one_tent_for_each_tree_constraint(self):
        grid = Grid([
            [0, -1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [-1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        tents_numbers_by_column_row = {'column': [1, 0, 0, 0, 0, 0], 'row': [0, 0, 0, 0, 1, 0]}
        game = TentsGame((grid, tents_numbers_by_column_row))
        solution = game.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_1(self):
        grid = Grid([
            [0, -1, 0, 0, 0, 0],
            [0, 0, 0, -1, 0, 0],
            [-1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, -1, 0],
            [-1, 0, 0, 0, 0, -1],
            [0, -1, 0, 0, 0, 0],
        ])
        tents_numbers_by_column_row = {'column': [3, 0, 1, 1, 1, 1], 'row': [2, 0, 1, 1, 0, 3]}
        expected_solution = Grid([
            [1, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 1],
        ])
        game = TentsGame((grid, tents_numbers_by_column_row))
        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_2(self):
        grid = Grid([
            [0, 0, 0, -1, 0, 0],
            [-1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, -1, 0],
            [0, -1, -1, 0, 0, 0],
            [0, 0, 0, 0, 0, -1],
            [0, -1, 0, 0, 0, 0]
        ])
        tents_numbers_by_column_row = {'column': [2, 1, 1, 1, 1, 1], 'row': [2, 1, 1, 1, 0, 2]}
        expected_solution = Grid([
            [1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1]
        ])
        game = TentsGame((grid, tents_numbers_by_column_row))
        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)


if __name__ == '__main__':
    unittest.main()
