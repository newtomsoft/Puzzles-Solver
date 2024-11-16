import unittest
from unittest import TestCase

from Grid import Grid
from Puzzles.Aquarium.AquariumGame import AquariumGame


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


if __name__ == '__main__':
    unittest.main()
