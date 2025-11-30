import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Tatamibari.TatamibariSolver import TatamibariSolver

_ = '.'
M = '-'
P = '+'
I = '|'


class TatamibariSolverTests(TestCase):
    def test_solution_4x4_easy_lge62(self):
        """https://gridpuzzle.com/tatamibari/lge62"""
        grid = Grid([
            [I, _, M, _],
            [_, P, _, I],
            [_, P, I, P],
            [M, _, _, _]
        ])
        game_solver = TatamibariSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 2, 2, 4],
            [1, 3, 6, 4],
            [1, 5, 6, 7],
            [8, 8, 8, 8]
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_evil_l4xjg(self):
        """https://gridpuzzle.com/tatamibari/l4xjg"""
        grid = Grid([
            [M, _, _, P],
            [_, _, M, _],
            [_, _, M, _],
            [_, _, _, I]
        ])
        game_solver = TatamibariSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1, 2],
            [3, 3, 3, 3],
            [4, 4, 4, 5],
            [4, 4, 4, 5]
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_evil_v8rq9(self):
        """https://gridpuzzle.com/tatamibari/v8rq9"""
        grid = Grid([
            [_, _, M, M, _, P],
            [_, _, M, _, _, _],
            [_, _, _, _, M, _],
            [_, _, _, _, _, I],
            [_, M, P, _, _, M],
            [P, _, _, M, _, M],
        ])
        game_solver = TatamibariSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1, 2, 2, 3],
            [4, 4, 4, 4, 4, 4],
            [5, 5, 5, 5, 5, 6],
            [5, 5, 5, 5, 5, 6],
            [7, 7, 8, 9, 9, 9],
            [10, 11, 11, 11, 12, 12],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_evil_095e1(self):
        """https://gridpuzzle.com/tatamibari/095e1"""
        grid = Grid([
            [_, M, _, P, _, _, _, M, _, I],
            [_, _, _, P, P, _, P, _, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, M, _, _, I, _, _, _, _],
            [_, _, M, _, _, _, _, _, _, _],
            [_, _, _, P, _, P, P, _, _, I],
            [I, _, _, _, _, _, _, _, M, _],
            [_, P, P, _, _, _, I, I, P, _],
            [M, _, _, _, M, _, _, _, I, _],
            [M, _, _, M, _, P, _, P, _, I],
        ])
        game_solver = TatamibariSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1, 2, 6, 6, 3, 3, 4, 4],
            [1, 1, 1, 5, 6, 6, 7, 7, 4, 4],
            [8, 8, 8, 8, 8, 9, 7, 7, 4, 4],
            [8, 8, 8, 8, 8, 9, 13, 13, 13, 14],
            [10, 10, 10, 11, 11, 9, 13, 13, 13, 14],
            [10, 10, 10, 11, 11, 12, 13, 13, 13, 14],
            [15, 16, 16, 16, 16, 16, 16, 16, 16, 16],
            [15, 17, 18, 23, 23, 23, 19, 20, 21, 29],
            [22, 22, 22, 23, 23, 23, 19, 20, 24, 29],
            [25, 25, 26, 26, 26, 27, 19, 28, 24, 29],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

        if __name__ == '__main__':
            unittest.main()
