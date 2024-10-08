import unittest
from unittest import TestCase

from Grid import Grid
from Puzzles.Nonogram.NonogramGame import NonogramGame


class NonogramGameTests(TestCase):
    def test_solution_left_not_compliant(self):
        numbers_by_top_left = {
            'top': [[3], [3], [1], [3, 3], [4]],
            'left': [[4], [1], [5]],
        }
        with self.assertRaises(ValueError) as context:
            NonogramGame(numbers_by_top_left)
        self.assertEqual("Rows number must be divisible by 5", str(context.exception))

    def test_solution_top_not_compliant(self):
        numbers_by_top_left = {
            'top': [[4], [1], [5]],
            'left': [[3], [3], [1], [3, 3], [4]],
        }
        with self.assertRaises(ValueError) as context:
            NonogramGame(numbers_by_top_left)
        self.assertEqual("Columns number must be divisible by 5", str(context.exception))

    def test_solution_missing_number_left(self):
        numbers_by_top_left = {
            'top': [[3], [3], [1], [3, 3], [4]],
            'left': [[3], [], [1], [3, 3], [4]],
        }
        with self.assertRaises(ValueError) as context:
            NonogramGame(numbers_by_top_left)
        self.assertEqual("Missing number for row", str(context.exception))

    def test_solution_missing_number_top(self):
        numbers_by_top_left = {
            'top': [[3], [3], [1], [], [4]],
            'left': [[3], [3], [1], [3, 3], [4]],
        }
        with self.assertRaises(ValueError) as context:
            NonogramGame(numbers_by_top_left)
        self.assertEqual("Missing number for column", str(context.exception))

    def test_solution_number_too_big_(self):
        numbers_by_top_left = {
            'top': [[0], [6], [0], [0], [0]],
            'left': [[1], [1], [1], [1], [1]],
        }
        with self.assertRaises(ValueError) as context:
            game = NonogramGame(numbers_by_top_left)
            game.get_solution()
        self.assertEqual("Numbers for columns must be positive and less or equal than rows number", str(context.exception))

    def test_solution_number_too_small(self):
        numbers_by_top_left = {
            'top': [[1], [1], [1], [1], [1]],
            'left': [[0], [6], [0], [0], [0]],
        }
        with self.assertRaises(ValueError) as context:
            game = NonogramGame(numbers_by_top_left)
            game.get_solution()
        self.assertEqual("Numbers for rows must be positive and less or equal than columns number", str(context.exception))

    def test_solution_basic_1_cell(self):
        numbers_by_top_left = {
            'top': [[0], [0], [0], [1], [0]],
            'left': [[0], [1], [0], [0], [0]],
        }
        expected_grid = Grid([
            [False, False, False, False, False],
            [False, False, False, True, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False]
        ])
        game = NonogramGame(numbers_by_top_left)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_basic_1_full_column(self):
        numbers_by_top_left = {
            'top': [[0], [5], [0], [0], [0]],
            'left': [[1], [1], [1], [1], [1]],
        }
        expected_grid = Grid([
            [False, True, False, False, False],
            [False, True, False, False, False],
            [False, True, False, False, False],
            [False, True, False, False, False],
            [False, True, False, False, False]
        ])
        game = NonogramGame(numbers_by_top_left)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_basic_all_full_(self):
        numbers_by_top_left = {
            'top': [[5], [5], [5], [5], [5]],
            'left': [[5], [5], [5], [5], [5]],
        }
        expected_grid = Grid([
            [True, True, True, True, True],
            [True, True, True, True, True],
            [True, True, True, True, True],
            [True, True, True, True, True],
            [True, True, True, True, True]
        ])
        game = NonogramGame(numbers_by_top_left)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_basic_2_numbers_in_column(self):
        numbers_by_top_left = {
            'top': [[3, 1], [0], [0], [0], [0]],
            'left': [[1], [1], [1], [0], [1]],
        }
        expected_grid = Grid([
            [True, False, False, False, False],
            [True, False, False, False, False],
            [True, False, False, False, False],
            [False, False, False, False, False],
            [True, False, False, False, False]
        ])
        game = NonogramGame(numbers_by_top_left)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_basic_2_numbers_in_column_and_other_full(self):
        numbers_by_top_left = {
            'left': [[5], [5], [5], [4], [5]],
            'top': [[3, 1], [5], [5], [5], [5]],
        }
        expected_grid = Grid([
            [True, True, True, True, True],
            [True, True, True, True, True],
            [True, True, True, True, True],
            [False, True, True, True, True],
            [True, True, True, True, True]
        ])
        game = NonogramGame(numbers_by_top_left)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_5x5_1(self):
        numbers_by_top_left = {
            'left': [[4], [3], [3], [1, 1], [1]],
            'top': [[1], [3], [4], [3], [2]]
        }
        expected_grid = Grid([
            [True, True, True, True, False],
            [False, True, True, True, False],
            [False, True, True, True, False],
            [False, False, True, False, True],
            [False, False, False, False, True]
        ])
        game = NonogramGame(numbers_by_top_left)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_5x5_2(self):
        numbers_by_top_left = {
            'left': [[3], [3], [3, 1], [1], [1, 1]],
            'top': [[3], [1, 1], [3, 1], [2], [2]]
        }
        expected_grid = Grid([
            [False, True, True, True, False],
            [False, False, True, True, True],
            [True, True, True, False, True],
            [True, False, False, False, False],
            [True, False, True, False, False]
        ])
        game = NonogramGame(numbers_by_top_left)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_10x10(self):
        numbers_by_top_left = {
            'top': [[3, 1, 3], [2, 1], [2, 2], [1, 3], [2, 1, 3], [7], [6], [2, 4], [5], [2]],
            'left': [[2, 1, 1], [2, 3], [1, 3], [1, 5], [1, 1, 5], [6], [1, 4], [1, 3, 1], [5], [3]],
        }
        expected_grid = Grid([
            [True, True, False, True, False, False, False, True, False, False],
            [True, True, False, False, False, True, True, True, False, False],
            [True, False, False, False, True, True, True, False, False, False],
            [False, False, True, False, True, True, True, True, True, False],
            [True, False, True, False, False, True, True, True, True, True],
            [False, False, False, False, True, True, True, True, True, True],
            [True, False, False, False, False, True, True, True, True, False],
            [True, False, False, True, True, True, False, False, True, False],
            [True, True, True, True, True, False, False, False, False, False],
            [False, False, True, True, True, False, False, False, False, False]
        ])
        game = NonogramGame(numbers_by_top_left)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_15x15(self):
        numbers_by_top_left = {
            'top': [[10], [9, 2], [3, 5, 3], [3], [2], [2, 5], [1, 3], [2, 1, 1, 2], [2, 2, 2, 2], [3, 1, 1, 3], [3, 1, 6], [8, 3], [1, 9], [4, 1, 1], [1, 1, 2, 1, 1]],
            'left': [[3, 3], [3, 4, 1], [3, 1, 3], [2, 1], [6, 5], [9, 1, 2], [4, 3], [3, 4], [3, 2, 4], [1, 5], [1, 1, 1, 1], [1, 4], [2, 2, 5], [2, 8], [1, 4, 1, 3]],
        }
        expected_grid = Grid([
            [True, True, True, False, False, False, False, False, True, True, True, False, False, False, False],
            [True, True, True, False, False, False, False, True, True, True, True, False, False, False, True],
            [True, True, True, False, False, False, False, True, False, True, True, True, False, False, False],
            [True, True, False, False, False, False, False, False, False, False, False, True, False, False, False],
            [True, True, True, True, True, True, False, False, True, True, True, True, True, False, False],
            [True, True, True, True, True, True, True, True, True, False, False, True, False, True, True],
            [True, True, True, True, False, False, False, False, False, False, False, True, True, True, False],
            [True, True, True, False, False, False, False, False, False, False, False, True, True, True, True],
            [True, True, True, False, False, False, False, True, True, False, False, True, True, True, True],
            [True, False, False, False, False, False, False, False, True, True, True, True, True, False, False],
            [False, False, False, False, False, True, False, False, False, False, True, False, True, False, True],
            [False, False, False, False, False, True, False, False, False, True, True, True, True, False, False],
            [False, True, True, False, False, True, True, False, False, True, True, True, True, True, False],
            [False, True, True, False, False, True, True, True, True, True, True, True, True, False, False],
            [False, False, True, False, False, True, True, True, True, False, True, False, True, True, True],
        ])
        game = NonogramGame(numbers_by_top_left)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_20x20(self):
        numbers_by_top_left = {
            'top': [[2, 1, 3], [1, 4], [6], [1, 5], [1, 1, 5, 2], [4, 1, 2, 4], [7, 7], [9, 3], [10, 3], [6, 4, 1, 4], [13, 4], [5, 3], [2, 4, 1], [4, 4], [6, 1, 1], [6, 1, 1, 3], [7, 2, 7], [2, 4, 5], [4, 1, 3], [4, 1, 1, 3]],
            'left': [[1, 2, 2], [1, 2, 6], [4, 5], [7, 7], [6, 6], [2, 7, 7], [1, 9, 5], [3, 5], [9, 2, 1], [4, 7, 1], [5, 5, 1], [5, 3], [5, 1, 2], [5, 3, 2], [1, 1, 3, 5], [6, 4], [3, 4, 1, 4], [2, 3, 2], [3, 2, 2], [3, 2]],
        }
        expected_grid = Grid([
            [True, False, False, False, False, False, False, False, False, False, False, False, False, True, True, False, True, True, False, False],
            [True, False, False, False, False, False, False, False, False, True, True, False, True, True, True, True, True, True, False, False],
            [False, False, False, False, False, False, False, True, True, True, True, False, True, True, True, True, True, False, False, False],
            [False, False, False, False, True, True, True, True, True, True, True, False, False, True, True, True, True, True, True, True],
            [False, False, False, False, False, True, True, True, True, True, True, False, False, False, True, True, True, True, True, True],
            [True, True, False, False, True, True, True, True, True, True, True, False, False, True, True, True, True, True, True, True],
            [False, False, False, True, False, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True],
            [False, False, False, False, False, False, True, True, True, False, True, True, True, True, True, False, False, False, False, False],
            [False, False, False, False, False, True, True, True, True, True, True, True, True, True, False, True, True, False, False, True],
            [True, True, True, True, False, False, True, True, True, True, True, True, True, False, False, False, True, False, False, False],
            [True, True, True, True, True, False, False, True, True, True, True, True, False, False, False, False, False, False, False, True],
            [True, True, True, True, True, False, False, False, True, True, True, False, False, False, False, False, False, False, False, False],
            [False, True, True, True, True, True, False, False, False, False, True, False, False, False, False, False, False, True, True, False],
            [False, False, True, True, True, True, True, False, True, True, True, False, False, False, False, False, True, True, False, False],
            [False, False, True, False, True, False, True, True, True, False, False, False, False, False, False, True, True, True, True, True],
            [False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, True, True, True, True],
            [False, False, False, False, False, True, True, True, False, True, True, True, True, False, True, False, True, True, True, True],
            [False, False, False, False, False, True, True, False, False, True, True, True, False, False, False, True, True, False, False, False],
            [False, False, False, False, True, True, True, False, False, True, True, False, False, False, False, True, True, False, False, False],
            [False, False, False, False, True, True, True, False, False, False, False, False, False, False, False, True, True, False, False, False]
        ])
        game = NonogramGame(numbers_by_top_left)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_10x5(self):
        numbers_by_top_left = {
            'top': [[1, 1, 1], [1, 4, 1], [1, 1, 1, 1], [2, 1, 1, 2], [1, 1, 1, 1]],
            'left': [[2], [1, 1], [1, 1], [3], [1], [1, 2], [3], [2], [3], [1, 1]],
        }
        expected_grid = Grid([
            [False, False, True, True, False],
            [False, True, False, True, False],
            [True, False, False, False, True],
            [False, True, True, True, False],
            [False, True, False, False, False],
            [False, True, False, True, True],
            [True, True, True, False, False],
            [False, False, False, True, True],
            [False, True, True, True, False],
            [True, False, False, False, True]
        ])
        game = NonogramGame(numbers_by_top_left)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)


if __name__ == '__main__':
    unittest.main()
