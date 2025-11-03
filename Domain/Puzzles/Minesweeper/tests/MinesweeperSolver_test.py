import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Minesweeper.MinesweeperSolver import MinesweeperSolver

_ = MinesweeperSolver.empty


class MinesweeperSolverTests(TestCase):
    def test_solution_basic_grid(self):
        grid = Grid([
            [_, _, _],
            [_, 1, 1],
            [_, 1, _]
        ])
        game_solver = MinesweeperSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 1]
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10(self):
        grid = Grid([
            [_, 1, _, _, _, _, 2, _, _, _],
            [1, 2, _, 2, _, 2, _, 1, 1, 1],
            [0, _, _, _, _, _, 1, _, _, _],
            [1, _, 1, _, 1, 1, _, _, 2, _],
            [_, _, _, _, 2, _, _, _, 4, _],
            [_, _, _, _, 4, _, _, _, _, 2],
            [2, _, 4, 4, _, _, _, 4, 4, _],
            [1, _, 3, _, _, _, _, _, _, _],
            [_, _, 3, _, 3, _, _, 1, 2, 2],
            [_, 0, _, _, _, 1, 1, _, _, 1]
        ])
        game_solver = MinesweeperSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 0, 0, 1, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0],
            [1, 0, 1, 1, 0, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
            [0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
