import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Minesweeper.MinesweeperSolver import MinesweeperSolver


class MinesweeperSolverTests(TestCase):
    def test_solution_basic_grid(self):
        grid = Grid([
            [-1, -1, -1],
            [-1, 1, 1],
            [-1, 1, -1]
        ])
        game_solver = MinesweeperSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [True, True, True],
            [True, True, True],
            [True, True, False]
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10(self):
        grid = Grid([
            [-1, 1, -1, -1, -1, -1, 2, -1, -1, -1],
            [1, 2, -1, 2, -1, 2, -1, 1, 1, 1],
            [0, -1, -1, -1, -1, -1, 1, -1, -1, -1],
            [1, -1, 1, -1, 1, 1, -1, -1, 2, -1],
            [-1, -1, -1, -1, 2, -1, -1, -1, 4, -1],
            [-1, -1, -1, -1, 4, -1, -1, -1, -1, 2],
            [2, -1, 4, 4, -1, -1, -1, 4, 4, -1],
            [1, -1, 3, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, 3, -1, 3, -1, -1, 1, 2, 2],
            [-1, 0, -1, -1, -1, 1, 1, -1, -1, 1]
        ])
        game_solver = MinesweeperSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [False, True, True, False, True, False, True, True, True, False],
            [True, True, True, True, True, True, False, True, True, True],
            [True, True, False, True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True, True, True, False],
            [False, True, True, True, True, False, True, False, True, True],
            [False, True, False, False, True, True, False, False, False, True],
            [True, True, True, True, False, False, False, True, True, False],
            [True, False, True, False, True, True, True, True, True, False],
            [True, True, True, False, True, False, True, True, True, True],
            [True, True, True, True, True, True, True, True, False, True]
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
