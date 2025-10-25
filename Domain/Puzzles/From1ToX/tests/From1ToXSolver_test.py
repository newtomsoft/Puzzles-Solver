import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Puzzles.From1ToX.From1ToXSolver import From1ToXSolver

_ = 0


class From1ToXSolverTests(TestCase):
    def test_get_solution_4x4_evil_vrdjk(self):
        """https://gridpuzzle.com/from1tox/vrdjk"""
        grid = Grid([
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        region_grid = Grid([
            [1, 1, 1, 1],
            [2, 2, 1, 1],
            [3, 2, 2, 4],
            [3, 3, 3, 4]
        ])
        row_clues = [16, _, 8, 8]
        column_clues = [14, 11, 12, _]

        expected_grid = Grid([
            [6, 2, 5, 3],
            [4, 3, 4, 1],
            [3, 2, 1, 2],
            [1, 4, 2, 1],
        ])
        game_solver = From1ToXSolver(grid, region_grid, row_clues, column_clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
