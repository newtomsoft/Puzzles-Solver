import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Hakoiri.HakoiriSolver import HakoiriSolver

_ = 0
C = 1
S = 2
T = 3


class HakoiriSolverTests(TestCase):
    def test_solution_4x4_easy_2164d(self):
        """https://gridpuzzle.com/hakoiri/2164d"""
        region_grid = Grid([
            [1, 1, 2, 2],
            [1, 1, 1, 2],
            [1, 1, 3, 2],
            [3, 3, 3, 2]

        ])
        value_grid = Grid([
            [_, S, C, _],
            [_, _, _, _],
            [_, _, _, _],
            [_, T, C, _]
        ])
        expected_solution = Grid([
            [C, S, C, S],
            [_, _, T, _],
            [_, _, S, _],
            [_, T, C, T]
        ])
        game_solver = HakoiriSolver(region_grid, value_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_evil_57008(self):
        """https://gridpuzzle.com/hakoiri/57008"""
        region_grid = Grid([
            [1, 1, 1, 1, 2, 2, 2, 3, 3, 3],
            [4, 4, 4, 5, 5, 2, 2, 6, 7, 7],
            [8, 4, 8, 5, 5, 9, 6, 6, 7, 7],
            [8, 8, 8, 9, 9, 9, 9, 10, 10, 10],
            [8, 8, 11, 12, 12, 12, 12, 10, 10, 10],
            [8, 11, 11, 12, 12, 13, 12, 14, 14, 14],
            [15, 15, 16, 16, 13, 13, 13, 14, 14, 14],
            [15, 15, 16, 17, 17, 17, 18, 18, 18, 14],
            [15, 19, 20, 20, 20, 17, 18, 20, 20, 21],
            [19, 19, 19, 19, 20, 20, 20, 20, 21, 21]
        ])
        value_grid = Grid([
            [_, _, _, _, C, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, T, _, _, _, _],
            [_, C, _, _, _, C, _, _, _, _],
            [_, _, _, _, _, _, _, _, C, _],
            [_, _, T, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, S],
            [_, _, _, _, _, _, _, _, _, _],
            [S, _, _, _, _, _, _, _, _, _],
            [_, C, _, T, _, _, _, _, _, _]
        ])
        expected_solution = Grid([
            [S, T, C, _, C, T, S, T, S, C],
            [C, _, S, T, S, _, _, C, _, T],
            [S, T, _, C, _, T, S, T, S, C],
            [_, C, _, _, S, C, _, _, _, T],
            [_, _, S, C, T, _, _, _, C, S],
            [T, C, T, _, S, C, _, _, _, T],
            [_, _, S, C, _, T, S, _, _, S],
            [T, C, T, _, S, C, _, C, T, C],
            [S, _, _, _, _, T, S, _, _, S],
            [_, C, S, T, S, C, _, T, C, T]
        ])
        game_solver = HakoiriSolver(region_grid, value_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
