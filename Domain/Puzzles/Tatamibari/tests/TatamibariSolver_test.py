import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Puzzles.Tatamibari.TatamibariSolver import TatamibariSolver

_ = ''
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


if __name__ == '__main__':
    unittest.main()
