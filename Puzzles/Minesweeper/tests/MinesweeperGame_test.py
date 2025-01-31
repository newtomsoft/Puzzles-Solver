import unittest
from unittest import TestCase

from Puzzles.Minesweeper.MinesweeperGame import MinesweeperGame
from Utils.Grid import Grid


class MinesweeperGameTests(TestCase):
    def test_solution_basic_grid(self):
        grid = Grid([
            [0, 0, 0],
            [0, 1, 1],
            [0, 1, -1]
        ])
        game = MinesweeperGame(grid)
        solution = game.get_solution()
        expected_solution = Grid([
            [True, True, True],
            [True, True, True],
            [True, True, False]
        ])
        self.assertEqual(expected_solution, solution)

    def test_solution_12x12(self):
        grid = Grid([
            [3, 5, 4, 2, -1],
            [-1, -1, -1, 3, -1],
            [-1, 3, -1, 3, -1],
            [-1, 3, 2, -1, -1],
            [3, -1, 1, 1, -1]
        ])
        game = MinesweeperGame(grid)
        solution = game.get_solution()
        expected_solution = Grid([
            [False, False, False, True, True],
            [True, False, False, True, True],
            [True, True, True, False, True],
            [False, True, True, True, False],
            [False, False, True, True, True]
        ])
        self.assertEqual(expected_solution, solution)


if __name__ == '__main__':
    unittest.main()
