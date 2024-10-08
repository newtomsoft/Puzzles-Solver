import unittest
from unittest import TestCase

from Grid import Grid
from Puzzles.Nonogram.NonogramGame import NonogramGame


class NonogramGameTests(TestCase):
    def test_solution_30x25(self):
        numbers_by_top_left = {
            'top': [[3, 14, 3], [2, 4, 2, 8, 3], [2, 1, 1, 8], [3, 1, 7], [3, 1, 9, 6], [3, 12, 2, 6], [1, 7, 4, 2, 6], [1, 7, 4, 3, 3], [4, 1, 1, 3, 5, 2], [15, 10], [3, 9, 4], [2, 6, 4], [2, 1, 5, 2, 1], [1, 2, 3, 2, 3], [1, 1, 1, 6], [1, 3, 3], [2, 4, 1, 3],
                    [3, 4, 5, 2], [4, 6, 3, 2], [4, 6, 1, 3, 5], [4, 1, 1, 1, 6], [4, 3, 3, 6], [4, 2, 1, 1, 1, 1, 2], [3, 2, 5, 4], [6, 3, 4]],
            'left': [[1, 2, 9], [2, 2, 5], [2, 2, 6], [1, 3, 7], [4, 1, 5], [5, 1, 4], [2, 6, 1, 1], [2, 3, 1, 4, 1], [1, 3, 2, 6, 1], [3, 2, 5], [10, 1, 7], [7, 3, 2], [2, 3, 5, 5], [2, 4, 5, 3], [1, 10, 1], [2, 11], [3, 9, 2, 1, 1, 1], [1, 1, 1, 4], [5, 3, 1, 2],
                     [2, 3, 3, 2], [2, 3, 3, 5, 1], [2, 5, 1, 3], [3, 5, 3, 3], [4, 3, 3, 3], [7, 3, 9], [6, 2, 5], [5, 3, 1, 3], [8, 1, 3, 2], [10, 1, 1, 3], [10, 1, 1, 3]],
        }
        expected_grid = Grid([
            [False, False, False, False, True, False, True, True, False, False, False, True, True, True, True, True, True, True, True, True, False, False, False, False, False],
            [False, False, False, False, True, True, False, False, False, False, False, True, True, False, False, False, True, True, True, True, True, False, False, False, False],
            [False, False, False, False, True, True, False, False, False, True, True, False, False, False, False, False, False, True, True, True, True, True, True, False, False],
            [False, False, False, False, False, True, False, False, True, True, True, False, False, False, False, False, False, False, True, True, True, True, True, True, True],
            [False, False, False, False, False, False, False, True, True, True, True, False, False, True, False, False, False, False, False, False, True, True, True, True, True],
            [False, False, False, False, False, True, True, True, True, True, False, False, False, True, False, False, False, False, False, False, False, True, True, True, True],
            [True, True, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True],
            [True, True, False, False, False, True, True, True, False, True, False, False, False, False, False, False, True, True, True, True, False, False, False, False, True],
            [True, False, False, False, False, True, True, True, False, True, True, False, False, False, False, True, True, True, True, True, True, False, False, False, True],
            [False, False, False, False, False, True, True, True, False, True, True, False, False, False, False, True, True, True, True, True, False, False, False, False, False],
            [False, True, True, True, True, True, True, True, True, True, True, False, True, False, True, True, True, True, True, True, True, False, False, False, False],
            [True, True, True, True, True, True, True, False, False, True, True, True, False, False, False, False, False, False, True, True, False, False, False, False, False],
            [True, True, False, True, True, True, False, False, True, True, True, True, True, False, False, False, False, False, False, True, True, True, True, True, False],
            [True, True, False, False, True, True, True, True, False, True, True, True, True, True, False, False, False, False, False, False, False, True, True, True, False],
            [True, False, False, False, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, True, False, False, False],
            [True, True, False, False, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False],
            [True, True, True, False, True, True, True, True, True, True, True, True, True, False, False, False, True, True, False, True, False, True, False, True, False],
            [True, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, True, True, True, True],
            [True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, False, True, False, True, True],
            [True, True, False, False, False, False, False, False, False, False, False, False, True, True, True, False, False, True, True, True, False, False, False, True, True],
            [True, True, False, False, False, False, False, True, True, True, False, False, True, True, True, False, False, True, True, True, True, True, False, True, False],
            [True, True, False, False, False, True, True, True, True, True, False, False, False, False, True, False, False, False, False, False, True, True, True, False, False],
            [True, True, True, False, False, True, True, True, True, True, False, False, False, False, True, True, True, False, False, True, True, True, False, False, False],
            [True, True, True, True, False, False, False, False, True, True, True, False, False, False, True, True, True, False, False, True, True, True, False, False, False],
            [True, True, True, True, True, True, True, False, True, True, True, False, False, False, True, True, True, True, True, True, True, True, True, False, False],
            [False, True, True, True, True, True, True, False, False, True, True, False, False, False, False, False, False, True, True, True, True, True, False, False, False],
            [False, False, True, True, True, True, True, False, False, True, True, True, False, False, False, False, False, False, False, True, False, False, True, True, True],
            [True, True, True, True, True, True, True, True, False, True, False, True, True, True, False, False, False, False, False, False, False, False, False, True, True],
            [True, True, True, True, True, True, True, True, True, True, False, True, False, True, False, False, False, False, False, False, False, False, True, True, True],
            [True, True, True, True, True, True, True, True, True, True, False, True, False, True, False, False, False, False, False, False, False, False, True, True, True]])
        game = NonogramGame(numbers_by_top_left)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)


if __name__ == '__main__':
    unittest.main()
