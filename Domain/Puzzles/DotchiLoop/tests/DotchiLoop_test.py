import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.DotchiLoop.DotchiLoopSolver import DotchiLoopSolver

_ = 0
B = 1
W = 2


class DotchiLoopSolverTests(TestCase):
    def test_solution_5x5_easy_37pm1(self):
        """https://gridpuzzle.com/dotchiloop/37pm1"""
        region_grid = Grid([
            [1, 1, 1, 2, 3],
            [4, 4, 1, 2, 3],
            [4, 4, 5, 6, 6],
            [4, 5, 5, 6, 6],
            [7, 7, 7, 7, 6]
        ])
        value_grid = Grid([
            [W, _, B, W, W],
            [_, _, W, _, _],
            [W, B, W, W, W],
            [_, _, _, _, _],
            [B, _, W, _, _]
        ])
        expected_solution_str = (
            ' ┌──┐  ·  ┌──┐ \n'
            ' │  └──┐  │  │ \n'
            ' │  ·  │  │  │ \n'
            ' └──┐  └──┘  │ \n'
            ' ·  └────────┘ '
        )
        game_solver = DotchiLoopSolver(region_grid, value_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_evil_0x2zw(self):
        """https://gridpuzzle.com/dotchiloop/0x2zw"""
        region_grid = Grid([
            [1, 1, 1, 1, 2],
            [1, 1, 1, 1, 2],
            [1, 1, 1, 1, 1],
            [3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3]
        ])
        value_grid = Grid([
            [_, W, _, _, B],
            [B, _, _, _, W],
            [W, _, W, _, W],
            [_, W, _, _, W],
            [_, _, W, _, _]
        ])
        expected_solution_str = (
            ' ·  ┌─────┐  · \n'
            ' ·  └──┐  └──┐ \n'
            ' ┌─────┘  ┌──┘ \n'
            ' │  ┌──┐  └──┐ \n'
            ' └──┘  └─────┘ '
        )
        game_solver = DotchiLoopSolver(region_grid, value_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
