import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Puzzles.DosunFuwari.DosunFuwariSolver import DosunFuwariSolver

_ = DosunFuwariSolver.empty
B = DosunFuwariSolver.black
W = DosunFuwariSolver.white


class DosunFuwariSolverTests(TestCase):
    def test_get_solution_5x5_3n8qr(self):
        """https://gridpuzzle.com/dosun-fuwari/3n8qr"""
        region_grid = Grid([
            [1, 1, 1, 2, 2],
            [3, 3, 4, 4, 5],
            [_, 3, 4, _, 5],
            [3, 3, 3, 6, 6],
            [3, 3, 3, 6, _]
        ])
        expected_grid = Grid([
            [B, _, W, B, W],
            [B, _, W, B, W],
            [_, _, _, _, B],
            [W, _, _, W, B],
            [_, _, _, _, _]
        ])
        game_solver = DosunFuwariSolver(region_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_8x8_l0ee1(self):
        """https://gridpuzzle.com/dosun-fuwari/l0ee1"""
        region_grid = Grid([
            [1, 1, 1, 2, 2, 3, 3, 3],
            [1, 1, 4, 2, 5, 5, 6, 6],
            [1, 4, 4, 4, _, 8, 8, 6],
            [1, 4, 9, 9, 9, _, 11, 11],
            [_, 4, _, 14, 14, 15, 15, _],
            [17, 17, 18, _, 14, 20, 15, 21],
            [22, 22, 18, 23, 23, 20, 21, 21],
            [22, _, 25, 25, 23, 20, 20, 21]
        ])
        expected_grid = Grid([
            [_, _, W, _, W, B, W, _],
            [_, _, W, B, W, B, W, _],
            [_, _, _, B, _, B, W, B],
            [B, _, _, B, W, _, W, B],
            [_, _, _, B, W, W, _, _],
            [W, B, W, _, _, W, B, W],
            [W, B, B, W, _, _, B, _],
            [_, _, B, W, B, _, B, _]
        ])
        game_solver = DosunFuwariSolver(region_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
