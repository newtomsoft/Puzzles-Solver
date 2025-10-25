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
            [_, B, _, B],
            [B, _, B, _],
            [_, B, _, B],
            [B, _, B, _],
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

if __name__ == '__main__':
    unittest.main()
