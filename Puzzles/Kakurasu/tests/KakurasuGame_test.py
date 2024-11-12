import unittest
from unittest import TestCase

from Grid import Grid
from Puzzles.Kakurasu.KakurasuGame import KakurasuGame


class KakurasuGameTests(TestCase):
    def test_solution_side_not_compliant(self):
        numbers_by_side_top = {
            'side': [2, 7, 3],
            'top': [2, 7, 3, 2],
        }

        with self.assertRaises(ValueError) as context:
            KakurasuGame(numbers_by_side_top)
        self.assertEqual("Kakurasu grid must at least 4x4", str(context.exception))

    def test_solution_top_not_compliant(self):
        numbers_by_side_top = {
            'side': [2, 7, 3, 4],
            'top': [2, 7, 3],
        }
        with self.assertRaises(ValueError) as context:
            KakurasuGame(numbers_by_side_top)
        self.assertEqual("Kakurasu grid must at least 4x4", str(context.exception))

    def test_solution_basic_1(self):
        numbers_by_side_top = {
            'side': [0, 0, 0, 0],
            'top': [0, 0, 0, 0],
        }
        expected_grid = Grid([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        game = KakurasuGame(numbers_by_side_top)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_4x4(self):
        numbers_by_side_top = {
            'side': [2, 7, 3, 2],
            'top': [2, 7, 3, 2],
        }
        expected_grid = Grid([
            [0, 1, 0, 0],
            [1, 1, 0, 1],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
        ])
        game = KakurasuGame(numbers_by_side_top)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_basic_5x5(self):
        numbers_by_side_top = {
            'side': [3, 4, 3, 2, 5],
            'top': [1, 5, 3, 2, 5],
        }
        expected_grid = Grid([
            [1, 1, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1],
        ])
        game = KakurasuGame(numbers_by_side_top)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_basic_6x6(self):
        numbers_by_side_top = {
            'side': [3, 9, 4, 9, 6, 1],
            'top': [13, 2, 5, 3, 5, 6],
        }
        expected_grid = Grid([
            [0, 0, 1, 0, 0, 0],
            [1, 1, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 1, 0],
            [1, 0, 0, 0, 0, 0]
        ])
        game = KakurasuGame(numbers_by_side_top)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_basic_7x7(self):
        numbers_by_side_top = {
            'side': [15, 25, 21, 24, 21, 19, 20],
            'top': [26, 20, 21, 24, 21, 27, 13],
        }
        expected_grid = Grid([
            [1, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 0],
            [1, 0, 1, 1, 1, 1, 0],
            [1, 1, 0, 1, 0, 1, 1]
        ])
        game = KakurasuGame(numbers_by_side_top)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_basic_8x8(self):
        numbers_by_side_top = {
            'side': [23, 34, 32, 19, 27, 32, 30, 25],
            'top': [18, 34, 30, 21, 28, 32, 24, 30],
        }
        expected_grid = Grid([
            [1, 1, 1, 1, 0, 1, 1, 0],
            [1, 0, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 0, 0, 1],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 0, 1],
        ])
        game = KakurasuGame(numbers_by_side_top)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_basic_9x9(self):
        numbers_by_side_top = {
            'side': [2, 15, 8, 10, 1, 6, 18, 15, 15],
            'top': [12, 1, 4, 15, 8, 30, 13, 5, 9]
        }
        expected_grid = Grid([
            [0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0],
            [1, 0, 0, 1, 0, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 1]
        ])
        game = KakurasuGame(numbers_by_side_top)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_basic_10x10(self):
        numbers_by_side_top = {
            'side': [8, 51, 36, 18, 39, 23, 28, 28, 40, 39],
            'top': [29, 19, 35, 4, 39, 48, 29, 51, 9, 43],
        }
        expected_grid = Grid([
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 1, 1, 1, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
            [0, 1, 1, 0, 0, 1, 0, 1, 1, 0],
            [1, 0, 1, 0, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 1, 0, 0, 1, 1, 1, 1, 0, 1]
        ])
        game = KakurasuGame(numbers_by_side_top)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_basic_11x11(self):
        numbers_by_side_top = {
            'side': [43, 38, 39, 47, 37, 23, 26, 61, 65, 39, 19],
            'top': [41, 13, 36, 19, 42, 48, 18, 60, 50, 51, 26]
        }
        expected_grid = Grid([
            [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0],
            [1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1],
            [0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1],
            [1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0],
            [0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0],
            [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0]
        ])
        game = KakurasuGame(numbers_by_side_top)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_basic_12x12(self):
        numbers_by_side_top = {
            'side': [53, 55, 48, 59, 26, 71, 33, 70, 46, 66, 75, 49],
            'top': [72, 77, 62, 71, 55, 69, 50, 32, 63, 59, 43, 63]
        }
        expected_grid = Grid([
            [0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
            [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0],
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1],
            [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1]
        ])
        game = KakurasuGame(numbers_by_side_top)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)


if __name__ == '__main__':
    unittest.main()
