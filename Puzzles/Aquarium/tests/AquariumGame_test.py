import unittest
from unittest import TestCase

from Puzzles.Aquarium.AquariumGame import AquariumGame
from Utils.Grid import Grid


class AquariumGameTests(TestCase):
    def test_grid_must_be_square_raises_value_error(self):
        grid = Grid([
            [1, 1, 1, 2, 2, 2, 2],
            [1, 3, 1, 1, 1, 1, 1],
            [1, 3, 1, 4, 4, 4, 4],
            [1, 3, 1, 4, 4, 4, 4],
            [1, 3, 3, 4, 5, 4, 4],
            [3, 3, 6, 6, 5, 4, 4],
        ])
        numbers = [5, 2, 3, 5, 5, 5, 3, 5, 4, 5, 4, 4]
        with self.assertRaises(ValueError) as context:
            AquariumGame(grid, numbers)
        self.assertEqual(str(context.exception), "The grid must be square")

    def test_grid_must_be_at_least_6x6_raises_value_error(self):
        grid = Grid([
            [1, 1, 1, 2, 2],
            [1, 3, 1, 1, 1],
            [1, 3, 3, 4, 4],
            [1, 1, 3, 4, 4],
            [1, 3, 3, 4, 5],
        ])
        numbers = [5, 2, 3, 5, 5, 5, 3, 5, 4, 5]
        with self.assertRaises(ValueError) as context:
            AquariumGame(grid, numbers)
        self.assertEqual(str(context.exception), "The grid must be at least 6x6")

    def test_grid_must_have_at_least_2_regions_raises_value_error(self):
        grid = Grid([
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
        ])
        numbers = [5, 2, 3, 5, 5, 5, 3, 5, 4, 5, 4, 4]
        with self.assertRaises(ValueError) as context:
            AquariumGame(grid, numbers)
        self.assertEqual(str(context.exception), "The grid must have at least 2 regions")

    def test_get_solution_all_empty(self):
        grid = Grid([
            [1, 1, 1, 2, 2, 2],
            [1, 3, 1, 1, 1, 2],
            [1, 3, 3, 4, 4, 2],
            [1, 1, 3, 4, 4, 2],
            [1, 3, 3, 4, 5, 2],
            [3, 3, 6, 6, 5, 2],
        ])
        numbers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        expected_grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        game = AquariumGame(grid, numbers)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_get_solution_1_cell_full(self):
        grid = Grid([
            [1, 1, 1, 2, 2, 2],
            [1, 6, 1, 1, 1, 2],
            [1, 6, 6, 4, 4, 2],
            [1, 1, 6, 4, 4, 2],
            [1, 6, 6, 4, 5, 2],
            [3, 6, 6, 6, 5, 2],
        ])
        numbers = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        expected_grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
        ])
        game = AquariumGame(grid, numbers)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_get_solution_6x6(self):
        grid = Grid([
            [1, 1, 1, 2, 2, 2],
            [1, 3, 1, 1, 1, 2],
            [1, 3, 3, 4, 4, 2],
            [1, 1, 3, 4, 4, 2],
            [1, 3, 3, 4, 5, 2],
            [3, 3, 6, 6, 5, 2],
        ])
        numbers = [5, 2, 3, 5, 5, 5, 3, 5, 4, 5, 4, 4]
        expected_grid = Grid([
            [1, 1, 1, 0, 0, 0],
            [1, 0, 1, 1, 1, 1],
            [1, 0, 0, 1, 1, 1],
            [1, 1, 0, 1, 1, 1],
            [1, 0, 0, 1, 1, 1],
            [0, 0, 1, 1, 1, 1]
        ])
        game = AquariumGame(grid, numbers)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_get_solution_10x10(self):
        grid = Grid([
            [1, 1, 2, 3, 4, 5, 6, 6, 6, 7],
            [8, 9, 4, 4, 4, 5, 5, 5, 5, 7],
            [8, 9, 4, 10, 10, 11, 11, 11, 11, 7],
            [12, 13, 14, 14, 10, 10, 11, 11, 11, 15],
            [12, 13, 16, 16, 17, 11, 11, 15, 15, 15],
            [18, 18, 19, 19, 20, 20, 11, 21, 22, 22],
            [23, 24, 25, 25, 25, 25, 26, 21, 21, 22],
            [23, 24, 25, 26, 25, 26, 26, 26, 27, 27],
            [28, 28, 25, 26, 26, 26, 29, 29, 29, 30],
            [31, 31, 31, 32, 32, 26, 33, 33, 33, 30]
        ])
        numbers = [1, 3, 2, 3, 4, 2, 3, 3, 4, 3, 4, 7, 2, 2, 1, 1, 3, 3, 3, 2]
        expected_grid = Grid([
            [1, 1, 0, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
            [0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
        ])
        game = AquariumGame(grid, numbers)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_get_solution_15x15(self):
        grid = Grid([
            [1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6],
            [7, 1, 2, 3, 3, 3, 8, 8, 4, 9, 9, 10, 5, 5, 6],
            [7, 1, 2, 2, 2, 2, 2, 8, 8, 11, 11, 10, 5, 5, 6],
            [12, 12, 12, 2, 2, 2, 8, 8, 13, 11, 11, 6, 6, 6, 6],
            [14, 14, 12, 12, 12, 2, 15, 15, 13, 13, 16, 16, 16, 16, 17],
            [14, 12, 12, 18, 18, 2, 19, 20, 20, 13, 13, 16, 21, 22, 17],
            [23, 23, 24, 24, 25, 19, 19, 26, 20, 13, 13, 21, 21, 22, 27],
            [23, 23, 26, 25, 25, 26, 26, 26, 20, 20, 20, 22, 22, 22, 27],
            [23, 23, 26, 26, 26, 26, 26, 26, 28, 29, 20, 27, 22, 22, 27],
            [30, 23, 23, 23, 26, 31, 26, 32, 28, 29, 29, 27, 27, 27, 27],
            [30, 30, 30, 30, 33, 31, 31, 32, 34, 34, 35, 27, 27, 27, 36],
            [30, 37, 38, 30, 39, 39, 39, 40, 41, 41, 35, 35, 42, 36, 36],
            [30, 37, 38, 38, 43, 43, 43, 40, 35, 35, 35, 42, 42, 42, 36],
            [30, 37, 38, 43, 43, 43, 43, 40, 40, 40, 40, 42, 44, 42, 36],
            [37, 37, 38, 43, 43, 43, 43, 43, 40, 45, 45, 44, 44, 44, 36],
        ])
        numbers = [7, 7, 7, 7, 9, 11, 11, 8, 8, 7, 6, 8, 11, 10, 5, 7, 10, 7, 6, 6, 4, 8, 12, 13, 13, 9, 5, 5, 3, 14]
        expected_grid = Grid([
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0],
            [1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0],
            [1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        ])
        game = AquariumGame(grid, numbers)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)


if __name__ == '__main__':
    unittest.main()
