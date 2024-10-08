import unittest
from unittest import TestCase

from Grid import Grid
from Puzzles.Queens.QueensGame import QueensGame


class QueensGameTests(TestCase):
    def test_solution_grid_not_a_square(self):
        grid = Grid([
            [0, 1, 1],
            [0, 2, 2],
        ])
        with self.assertRaises(ValueError) as context:
            QueensGame(grid)
        self.assertEqual("The grid must be square", str(context.exception))

    def test_solution_grid_size_less_than_4(self):
        grid = Grid([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ])
        with self.assertRaises(ValueError) as context:
            QueensGame(grid)
        self.assertEqual("The grid must be at least 4x4", str(context.exception))

    def test_solution_color_less_than_columns_number(self):
        grid = Grid([
            [0, 1, 2, 2],
            [0, 1, 2, 2],
            [0, 1, 2, 2],
            [0, 1, 2, 2],
        ])
        with self.assertRaises(ValueError) as context:
            QueensGame(grid)
        self.assertEqual("The grid must have the same number of regions as rows/column", str(context.exception))

    def test_solution_1(self):
        grid = Grid([
            [0, 1, 2, 3],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        game = QueensGame(grid)
        solution = game.get_solution()
        self.assertIsNone(solution)

    def test_solution_grid_4x4(self):
        grid = Grid([
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [0, 2, 2, 3],
            [2, 2, 2, 3],
        ])
        expected_solution = Grid([
            [False, False, True, False],
            [True, False, False, False],
            [False, False, False, True],
            [False, True, False, False],
        ])
        game = QueensGame(grid)
        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_9x9(self):
        grid = Grid([
            ['p', 'p', 'p', 'p', 'p', 'o', 'b', 'b', 'b'],
            ['p', 'p', 'p', 'g', 'o', 'o', 'o', 'b', 'b'],
            ['p', 'p', 'g', 'g', 'g', 'o', 'r', 'b', 'b'],
            ['p', 'p', 'p', 'g', 'm', 'r', 'r', 'r', 'b'],
            ['p', 'p', 'y', 'm', 'm', 'm', 'r', 's', 'b'],
            ['p', 'y', 'y', 'y', 'm', 'w', 's', 's', 's'],
            ['p', 'p', 'y', 'p', 'w', 'w', 'w', 's', 'p'],
            ['p', 'p', 'p', 'p', 'p', 'w', 'p', 'p', 'p'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ])
        expected_solution = Grid([
            [False, False, False, False, False, False, False, False, True],
            [False, False, False, False, True, False, False, False, False],
            [False, False, True, False, False, False, False, False, False],
            [False, False, False, False, False, False, True, False, False],
            [False, False, False, True, False, False, False, False, False],
            [False, True, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, True, False],
            [False, False, False, False, False, True, False, False, False],
            [True, False, False, False, False, False, False, False, False]
        ])
        game = QueensGame(grid)
        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_9x9_2(self):
        grid = Grid([
            [0, 0, 0, 0, 8, 2, 2, 3, 4],
            [0, 6, 6, 8, 8, 8, 2, 3, 4],
            [0, 5, 6, 6, 8, 3, 3, 3, 4],
            [0, 5, 8, 8, 8, 8, 8, 7, 4],
            [0, 5, 5, 5, 8, 7, 7, 7, 4],
            [0, 8, 8, 8, 8, 8, 8, 8, 4],
            [1, 1, 4, 4, 8, 4, 4, 4, 4],
            [1, 1, 4, 8, 8, 8, 4, 4, 4],
            [1, 4, 4, 4, 4, 4, 4, 4, 4]
        ])
        expected_solution = Grid([
            [False, False, False, False, False, False, True, False, False],
            [False, False, True, False, False, False, False, False, False],
            [False, False, False, False, False, True, False, False, False],
            [False, False, False, False, False, False, False, True, False],
            [False, False, False, True, False, False, False, False, False],
            [True, False, False, False, False, False, False, False, False],
            [False, False, False, False, True, False, False, False, False],
            [False, True, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, True]
        ])
        game = QueensGame(grid)
        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)


if __name__ == '__main__':
    unittest.main()
