import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Puzzles.Doppelblock.DoppelblockSolver import DoppelblockSolver

_ = DoppelblockSolver.empty
B = DoppelblockSolver.black_value


class DoppelblockSolverTests(TestCase):
    def test_get_solution_without_sums_clues(self):
        grid = Grid([
            [1, _, 2, _],
            [_, 2, _, _],
            [2, _, 1, _],
            [_, _, _, _],
        ])
        row_sums_clues = [_, _, _, _]
        column_sums_clues = [_, _, _, _]

        expected_grid = Grid([
            [1, 0, 2, 0],
            [0, 2, 0, 1],
            [2, 0, 1, 0],
            [0, 1, 0, 2],
        ])
        game_solver = DoppelblockSolver(grid, row_sums_clues, column_sums_clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_with_sums_clues(self):
        grid = Grid([
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        row_sums_clues = [2, 2, 1, 1]
        column_sums_clues = [2, 2, 1, 1]

        expected_grid = Grid([
            [1, 0, 2, 0],
            [0, 2, 0, 1],
            [2, 0, 1, 0],
            [0, 1, 0, 2],
        ])
        game_solver = DoppelblockSolver(grid, row_sums_clues, column_sums_clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_5x5_evil_mny1w(self):
        """https://gridpuzzle.com/doppelblock/mny1w"""
        grid = Grid([
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
        ])
        row_sums_clues = [1, _, 3, 0, 5]
        column_sums_clues = [0, 2, _, _, _]

        expected_grid = Grid([
            [B, 1, B, 2, 3],
            [B, 3, B, 1, 2],
            [2, B, 3, B, 1],
            [3, 2, 1, B, B],
            [1, B, 2, 3, B],
        ])
        game_solver = DoppelblockSolver(grid, row_sums_clues, column_sums_clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_6x6_evil_vwk4k(self):
        """https://gridpuzzle.com/doppelblock/vwk4k"""
        grid = Grid([
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
        ])
        row_sums_clues = [9, 0, 4, 3, 3, 5]
        column_sums_clues = [4, _, 0, 0, _, 0]

        expected_grid = Grid([
            [1, B, 2, 3, 4, B],
            [3, 2, 4, 1, B, B],
            [2, 1, B, 4, B, 3],
            [B, 3, B, 2, 1, 4],
            [4, B, 3, B, 2, 1],
            [B, 4, 1, B, 3, 2],
        ])
        game_solver = DoppelblockSolver(grid, row_sums_clues, column_sums_clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_7x7_evil_8d69k(self):
        """https://gridpuzzle.com/doppelblock/8d69k"""
        grid = Grid([
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
        ])
        row_sums_clues = [2, _, 15, _, _, 2, 10]
        column_sums_clues = [12, 3, 3, _, 2, 11, _]

        expected_grid = Grid([
            [1, B, 2, B, 4, 3, 5],
            [2, 1, B, 4, 5, B, 3],
            [B, 2, 3, 5, 1, 4, B],
            [4, B, B, 1, 3, 5, 2],
            [5, 4, 1, 3, B, 2, B],
            [3, 5, 4, B, 2, B, 1],
            [B, 3, 5, 2, B, 1, 4],
        ])
        game_solver = DoppelblockSolver(grid, row_sums_clues, column_sums_clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_8x8_evil_48w6p(self):
        """https://gridpuzzle.com/doppelblock/48w6p"""
        grid = Grid([
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
        ])
        row_sums_clues = [0, 6, 9, _, 9, 14, 15, 9]
        column_sums_clues = [7, 15, _, 3, 0, 18, 11, 16]

        expected_grid = Grid([
            [6, 4, 3, 1, 5, 2, B, B],
            [B, 2, 4, B, 6, 1, 5, 3],
            [5, B, 2, 3, 4, B, 1, 6],
            [2, 6, 5, B, B, 4, 3, 1],
            [B, 3, 1, 5, B, 6, 2, 4],
            [4, 1, B, 6, 3, 5, B, 2],
            [1, 5, B, 4, 2, 3, 6, B],
            [3, B, 6, 2, 1, B, 4, 5],
        ])
        game_solver = DoppelblockSolver(grid, row_sums_clues, column_sums_clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
