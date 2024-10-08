import unittest
from unittest import TestCase

from Grid import Grid
from Puzzles.Hitori.HitoriGame import HitoriGame


class HitoriGameTests(TestCase):
    def test_solution_not_exist_2_black_adjacent(self):
        grid = Grid([
            [1, 1, 1],
            [2, 2, 2],
            [3, 4, 5]
        ])
        game = HitoriGame(grid)
        solution, _ = game.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_not_exist_corner_isolated(self):
        grid = Grid([
            [1, 2, 4, 5],
            [3, 6, 3, 3],
            [7, 2, 8, 9],
            [4, 2, 3, 6]
        ])
        game = HitoriGame(grid)
        solution, _ = game.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_unique_numbers(self):
        grid = Grid([
            [1, 2, 3],
            [2, 3, 1],
            [3, 1, 2]
        ])
        expected_solution = Grid(grid.matrix.copy())
        game = HitoriGame(grid)

        solution, _ = game.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_simple_duplicate_numbers(self):
        grid = Grid([
            [1, 2, 3],
            [3, 2, 2],
            [2, 3, 1]
        ])
        expected_solution = Grid([
            [1, 2, 3],
            [3, False, 2],
            [2, 3, 1]
        ])
        game = HitoriGame(grid)
        solution, _ = game.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_12x12(self):
        grid = Grid([
            [6, 6, 5, 6, 11, 5, 3, 9, 6, 8, 3, 4],
            [7, 1, 8, 5, 10, 3, 11, 10, 2, 4, 6, 12],
            [6, 11, 5, 9, 2, 9, 6, 7, 2, 3, 9, 10],
            [10, 6, 2, 7, 10, 4, 3, 8, 12, 2, 9, 1],
            [8, 9, 9, 4, 1, 2, 7, 12, 11, 5, 8, 6],
            [5, 11, 10, 2, 11, 12, 9, 12, 8, 9, 1, 7],
            [8, 12, 11, 12, 3, 12, 10, 6, 1, 2, 12, 8],
            [11, 8, 4, 10, 6, 1, 9, 5, 7, 10, 3, 2],
            [10, 2, 2, 11, 8, 11, 4, 8, 10, 12, 4, 9],
            [3, 9, 1, 9, 5, 8, 12, 2, 5, 10, 4, 11],
            [9, 4, 6, 8, 10, 7, 2, 3, 5, 5, 10, 6],
            [12, 11, 3, 1, 7, 10, 3, 11, 2, 9, 2, 5]
        ])
        expected_solution = Grid([
            [6, False, 5, False, 11, False, 3, 9, False, 8, False, 4],
            [7, 1, 8, 5, 10, 3, 11, False, 2, 4, 6, 12],
            [False, 11, False, 9, 2, False, 6, 7, False, 3, False, 10],
            [10, 6, 2, 7, False, 4, False, 8, 12, False, 9, 1],
            [8, 9, False, 4, 1, 2, 7, 12, 11, 5, False, 6],
            [5, False, 10, 2, False, 12, 9, False, 8, False, 1, 7],
            [False, 12, 11, False, 3, False, 10, 6, 1, 2, False, 8],
            [11, 8, 4, 10, 6, 1, False, 5, 7, False, 3, 2],
            [False, 2, False, 11, 8, False, 4, False, 10, 12, False, 9],
            [3, False, 1, False, 5, 8, 12, 2, False, 10, 4, 11],
            [9, 4, 6, 8, False, 7, 2, 3, 5, False, 10, False],
            [12, False, 3, 1, 7, 10, False, 11, False, 9, 2, 5]
        ])
        game = HitoriGame(grid)
        solution, _ = game.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_many_games_solution_exist(self):
        grids5x5 = [
            Grid([[1, 1, 3, 3, 5], [4, 3, 5, 2, 1], [2, 3, 4, 1, 5], [2, 1, 4, 4, 3], [5, 2, 1, 3, 2]]),
            Grid([[3, 3, 5, 2, 3], [4, 5, 1, 2, 3], [3, 3, 3, 4, 1], [1, 2, 3, 5, 2], [3, 4, 4, 1, 5]]),
            Grid([[4, 5, 5, 2, 5], [4, 3, 2, 4, 1], [3, 3, 1, 3, 4], [1, 4, 5, 3, 3], [5, 4, 3, 1, 2]]),
            Grid([[3, 3, 1, 1, 4], [1, 3, 5, 4, 2], [3, 2, 3, 2, 5], [2, 4, 2, 1, 3], [5, 3, 2, 3, 4]]),
            Grid([[1, 4, 5, 1, 2], [3, 3, 4, 5, 1], [2, 3, 4, 4, 3], [2, 5, 2, 5, 4], [4, 1, 3, 2, 5]]),
            Grid([[4, 1, 5, 1, 3], [4, 3, 2, 1, 4], [5, 4, 1, 1, 2], [5, 2, 2, 3, 3], [3, 5, 4, 2, 1]]),
            Grid([[1, 1, 3, 4, 1], [2, 1, 1, 5, 4], [2, 3, 2, 2, 1], [5, 5, 1, 2, 3], [3, 4, 5, 3, 2]]),
            Grid([[3, 3, 5, 2, 3], [2, 1, 1, 4, 5], [3, 2, 1, 4, 4], [3, 5, 3, 1, 1], [1, 4, 4, 3, 2]]),
            Grid([[2, 2, 1, 5, 3], [2, 4, 4, 5, 1], [5, 1, 5, 1, 2], [3, 3, 4, 1, 5], [1, 3, 2, 3, 4]]),
            Grid([[3, 3, 5, 1, 2], [1, 3, 4, 3, 5], [3, 1, 4, 2, 5], [5, 4, 2, 3, 1], [1, 2, 3, 3, 4]]),
        ]

        for grid in grids5x5:
            game = HitoriGame(grid)
            solution, _ = game.get_solution()
            self.assertIsNotNone(solution)


if __name__ == '__main__':
    unittest.main()
