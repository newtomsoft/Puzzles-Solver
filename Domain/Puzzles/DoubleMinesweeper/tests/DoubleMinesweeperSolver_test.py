import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.DoubleMinesweeper.DoubleMinesweeperSolver import DoubleMinesweeperSolver

_ = DoubleMinesweeperSolver.empty


class DoubleMinesweeperSolverTests(TestCase):
    def test_solution_basic_grid(self):
        grid = Grid([
            [_, _, _],
            [0, 3, 3],
            [_, 2, _]
        ])
        game_solver = DoubleMinesweeperSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [0, 0, 1],
            [0, 0, 0],
            [0, 0, 2]
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_easy_l9gqx(self):
        """https://gridpuzzle.com/minesweeper-double/l9gqx"""
        grid = Grid([
            [_, 2, 1, 2, _],
            [1, _, _, _, _],
            [2, _, 6, _, 4],
            [_, _, _, _, 3],
            [_, 4, 4, 2, _],
        ])
        game_solver = DoubleMinesweeperSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 0, 0, 0, 0],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 1, 0],
            [0, 2, 0, 2, 0],
            [2, 0, 0, 0, 0],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12_evil_j18g1(self):
        """https://gridpuzzle.com/minesweeper-double/j18g1"""
        grid = Grid([
            [_, 2, _, _, 3, 4, _, _, 2, _, _, 1],
            [_, _, 3, 6, _, _, 4, 5, _, 3, 2, _],
            [4, 5, _, _, _, 6, _, _, 6, 4, 2, _],
            [_, _, _, _, 7, _, 4, 4, _, _, _, 2],
            [_, 7, _, _, 5, _, _, _, _, _, _, _],
            [_, 2, 4, _, _, 2, _, _, 6, 4, _, _],
            [4, _, 4, _, 6, _, 4, _, _, _, 3, _],
            [_, _, _, _, _, 3, 6, 3, _, 4, _, 2],
            [_, _, _, _, 4, _, _, _, 2, _, _, _],
            [1, _, 3, _, _, _, 2, _, _, _, 4, 4],
            [5, _, 6, 3, _, _, _, 2, 3, 2, _, _],
            [_, _, 3, _, _, _, 2, _, _, _, 3, _],
        ])
        game_solver = DoubleMinesweeperSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 2, 1, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 2, 1, 0, 0, 2, 0, 0, 0, 1],
            [2, 2, 1, 1, 0, 2, 0, 0, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1],
            [2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 2, 0, 2, 0, 2, 0, 2, 0, 0],
            [2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 2, 0],
            [0, 1, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 2, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
