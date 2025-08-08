import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Trilogy.TrilogySolver import TrilogySolver

_ = 0
C = 1
S = 2
T = 3

class TrilogySolverTests(TestCase):
    def test_solution_4x4_easy_7pp4k(self):
        """https://gridpuzzle.com/trilogy/7pp4k"""
        grid = Grid([
            [C, _, _, C],
            [S, _, _, T],
            [C, _, _, C],
            [C, T, C, C]
        ])
        expected_solution = Grid([
            [C, S, C, C],
            [S, T, S, T],
            [C, S, C, C],
            [C, T, C, C]
        ])
        game_solver = TrilogySolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_evil_29qx8(self):
        """https://gridpuzzle.com/trilogy/29qx8"""
        grid = Grid([
            [_, _, _, _, _],
            [C, _, C, _, C],
            [_, _, _, _, _],
            [T, T, _, T, T],
            [_, _, S, _, _]
        ])
        expected_solution = Grid([
            [T, T, S, T, T],
            [C, S, C, S, C],
            [T, T, S, T, T],
            [T, T, C, T, T],
            [S, C, S, C, S]
        ])
        game_solver = TrilogySolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_evil_1q840(self):
        """https://gridpuzzle.com/trilogy/1q840"""
        grid = Grid([
            [_, _, _, _, _, _, _, C, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, T, _, _, _, _, _, _, _],
            [T, _, _, _, _, _, _, T, _, _],
            [_, _, _, _, _, _, S, _, _, _],
            [_, _, _, _, S, _, _, _, _, _],
            [S, _, _, _, T, _, _, _, _, S],
            [_, _, _, _, _, _, _, _, C, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _]
        ])
        expected_solution = Grid([
            [S, T, S, T, T, C, T, C, C, S],
            [S, T, T, C, T, C, C, S, C, S],
            [T, C, T, C, C, S, C, S, S, T],
            [T, C, C, S, C, S, S, T, S, T],
            [C, S, C, S, S, T, S, T, T, C],
            [C, S, S, T, S, T, T, C, T, C],
            [S, T, S, T, T, C, T, C, C, S],
            [S, T, T, C, T, C, C, S, C, S],
            [T, C, T, C, C, S, C, S, S, T],
            [T, C, C, S, C, S, S, T, S, T]
        ])
        game_solver = TrilogySolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

if __name__ == '__main__':
    unittest.main()
