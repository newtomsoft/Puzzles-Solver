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

    def test_get_solution_5x5_evil_ywr76(self):
        """https://gridpuzzle.com/from1tox/ywr76"""
        grid = Grid([
            [_, _, 5, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
        ])
        region_grid = Grid([
            [1, 2, 2, 2, 3],
            [1, 4, 2, 5, 3],
            [6, 4, 2, 5, 5],
            [6, 7, 7, 7, 7],
            [6, 6, 8, 8, 7]
        ])
        row_clues = [_, _, 11, _, 7]
        column_clues = [_, 14, 15, _, _]

        expected_grid = Grid([
            [2, 4, 5, 1, 2],
            [1, 2, 3, 2, 1],
            [4, 1, 2, 1, 3],
            [3, 5, 4, 3, 2],
            [1, 2, 1, 2, 1]
        ])
        game_solver = From1ToXSolver(grid, region_grid, row_clues, column_clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_6x6_evil_kqz21(self):
        """https://gridpuzzle.com/from1tox/kqz21"""
        grid = Grid([
            [_, _, _, _, _, 2],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, 3]
        ])
        region_grid = Grid([
            [1, 1, 2, 3, 3, 3],
            [1, 2, 2, 2, 4, 3],
            [1, 2, 2, 5, 4, 6],
            [1, 7, 2, 5, 6, 6],
            [1, 7, 8, 5, 6, 5],
            [8, 8, 8, 5, 5, 5]
        ])
        row_clues = [_, 22, 22, 17, 18, 13]
        column_clues = [_, 21, 17, 25, 15, 14]

        expected_grid = Grid([
            [6, 1, 5, 4, 3, 2],
            [5, 7, 4, 3, 2, 1],
            [4, 6, 2, 7, 1, 2],
            [3, 2, 1, 6, 4, 1],
            [2, 1, 3, 4, 3, 5],
            [1, 4, 2, 1, 2, 3]
        ])
        game_solver = From1ToXSolver(grid, region_grid, row_clues, column_clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
