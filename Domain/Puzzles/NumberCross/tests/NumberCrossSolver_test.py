import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.NumberCross.NumberCrossSolver import NumberCrossSolver

_ = NumberCrossSolver.empty
B = NumberCrossSolver.black_value

class NumberCrossSolverTests(TestCase):
    def test_get_solution_5x5_easy_l4j0e(self):
        """https://gridpuzzle.com/number-cross/l4j0e"""
        grid = Grid([
            [7, B, 9, 6, B],
            [1, 7, 1, 4, 2],
            [1, 5, 2, 7, 7],
            [1, B, B, 5, 2],
            [8, 3, 3, 8, 9],
        ])
        row_sums_clues = [9, 7, 15, 2, 14]
        column_sums_clues = [9, 8, 15, 4, 11]

        expected_grid = Grid([
            [B, B, 9, B, B],
            [B, B, 1, 4, 2],
            [1, 5, 2, B, 7],
            [B, B, B, B, 2],
            [8, 3, 3, B, B],
        ])
        game_solver = NumberCrossSolver(grid, row_sums_clues, column_sums_clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_5x5_evil_dn72v(self):
        """https://gridpuzzle.com/number-cross/dn72v"""
        grid = Grid([
            [3, 7, 4, 3, 4],
            [7, 3, 7, 6, 4],
            [3, 9, 6, 1, 4],
            [1, 3, 7, 8, 7],
            [6, 6, 8, 3, 8],
        ])
        row_sums_clues = [11, _, _, 18, 3]
        column_sums_clues = [10, 19, 13, 18, 4]

        expected_grid = Grid([
            [B, 7, B, B, 4],
            [7, B, B, 6, B],
            [3, 9, 6, 1, B],
            [B, 3, 7, 8, B],
            [B, B, B, 3, B],
        ])
        game_solver = NumberCrossSolver(grid, row_sums_clues, column_sums_clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_6x6_evil_n5k2w(self):
        """https://gridpuzzle.com/number-cross/n5k2w"""
        grid = Grid([
            [3, 4, 6, 6, 6, 3],
            [9, 1, 8, 7, 8, 2],
            [5, 8, 6, 2, 5, 2],
            [1, 6, 9, 1, 2, 5],
            [6, 2, 7, 4, 6, 7],
            [6, 3, 1, 4, 1, 2]
        ])
        row_sums_clues = [6, 15, 15, 8, 25, 8]
        column_sums_clues = [18, 10, _, _, 23, 14]

        expected_grid = Grid([
            [B, B, B, B, 6, B],
            [B, B, B, 7, 8, B],
            [5, 8, B, B, B, 2],
            [1, B, B, B, 2, 5],
            [6, 2, B, 4, 6, 7],
            [6, B, 1, B, 1, B],
        ])
        game_solver = NumberCrossSolver(grid, row_sums_clues, column_sums_clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_10x10_evil_5jyy9(self):
        """https://gridpuzzle.com/number-cross/5jyy9"""
        grid = Grid([
            [3, 3, 1, 8, 9, 9, 7, 5, 6, 4],
            [3, 6, 1, 2, 9, 3, 2, 4, 9, 3],
            [7, 9, 7, 2, 7, 9, 2, 8, 4, 4],
            [5, 3, 8, 8, 9, 1, 4, 9, 7, 2],
            [9, 4, 1, 4, 3, 1, 6, 7, 3, 6],
            [6, 8, 6, 5, 9, 4, 8, 4, 1, 1],
            [9, 5, 4, 5, 2, 5, 4, 6, 2, 3],
            [9, 3, 6, 4, 6, 4, 9, 9, 6, 5],
            [5, 9, 4, 2, 3, 6, 6, 1, 6, 9],
            [4, 5, 3, 7, 5, 9, 4, 5, 6, 3],
        ])
        row_sums_clues = [_, 25, 19, 52, 24, 25, 11, 32, 29, 37]
        column_sums_clues = [29, 19, 34, 36, 37, 35, 17, 39, 19, 9]

        expected_grid = Grid([
            [B, 3, B, 8, B, 9, B, B, B, B],
            [B, B, 1, B, 9, B, 2, 4, 9, B],
            [B, B, 7, 2, B, B, 2, 8, B, B],
            [5, 3, 8, 8, 9, 1, B, 9, 7, 2],
            [9, 4, 1, B, B, 1, B, B, 3, 6],
            [6, B, B, 5, 9, B, B, 4, B, 1],
            [B, B, 4, B, 2, 5, B, B, B, B],
            [B, B, 6, 4, B, 4, 9, 9, B, B],
            [5, 9, 4, 2, 3, 6, B, B, B, B],
            [4, B, 3, 7, 5, 9, 4, 5, B, B],
        ])
        game_solver = NumberCrossSolver(grid, row_sums_clues, column_sums_clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
