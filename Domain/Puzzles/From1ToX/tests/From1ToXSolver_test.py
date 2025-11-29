import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.From1ToX.From1ToXSolver import From1ToXSolver

_ = From1ToXSolver.empty


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

    def test_get_solution_7x7_evil_nkwek(self):
        """https://gridpuzzle.com/from1tox/nkwek"""
        grid = Grid([
            [_, _, _, _, _, _, _],
            [_, _, _, _, 2, _, _],
            [_, _, _, 3, _, _, _],
            [_, 2, _, _, _, _, _],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _]
        ])
        region_grid = Grid([
            [1, 1, 1, 2, 2, 2, 3],
            [4, 1, 5, 5, 2, 3, 3],
            [4, 6, 5, 7, 7, 8, 3],
            [6, 6, 6, 7, 7, 8, 9],
            [10, 6, 11, 11, 12, 9, 9],
            [10, 10, 11, 12, 12, 12, 9],
            [10, 10, 11, 13, 13, 13, 9]
        ])
        row_clues = [_, 15, 18, _, 23, 17, 13]
        column_clues = [17, _, 17, 16, 18, 18, _]

        expected_grid = Grid([
            [4, 3, 2, 4, 3, 1, 3],
            [2, 1, 3, 1, 2, 4, 2],
            [1, 5, 2, 3, 4, 2, 1],
            [4, 2, 3, 1, 2, 1, 4],
            [3, 1, 4, 3, 4, 5, 3],
            [2, 5, 2, 1, 2, 3, 2],
            [1, 4, 1, 3, 1, 2, 1],
        ])
        game_solver = From1ToXSolver(grid, region_grid, row_clues, column_clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_8x8_evil_6qjr5(self):
        """https://gridpuzzle.com/from1tox/6qjr5"""
        grid = Grid([
            [_, _, _, _, _, _, _, 4],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, 2, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, 3, _, _, _, _],
            [_, _, _, _, _, _, _, _]
        ])
        region_grid = Grid([
            [1, 1, 2, 2, 3, 3, 3, 3],
            [1, 4, 4, 4, 4, 4, 4, 5],
            [1, 4, 6, 6, 4, 7, 7, 5],
            [8, 9, 9, 10, 10, 11, 11, 11],
            [8, 8, 9, 10, 10, 12, 12, 12],
            [8, 8, 9, 10, 13, 13, 14, 15],
            [16, 17, 17, 17, 13, 14, 14, 15],
            [16, 16, 16, 13, 13, 14, 14, 14]
        ])
        row_clues = [_, 30, 18, 23, _, 19, 24, 18]
        column_clues = [22, 29, 21, 16, 33, _, 16, 16]

        expected_grid = Grid([
            [3, 4, 2, 1, 3, 1, 2, 4],
            [2, 8, 5, 4, 6, 2, 1, 2],
            [1, 7, 2, 1, 3, 1, 2, 1],
            [4, 1, 4, 3, 5, 2, 1, 3],
            [3, 5, 3, 2, 4, 3, 2, 1],
            [2, 1, 2, 1, 5, 2, 4, 2],
            [4, 2, 1, 3, 4, 6, 3, 1],
            [3, 1, 2, 1, 3, 5, 1, 2],
        ])
        game_solver = From1ToXSolver(grid, region_grid, row_clues, column_clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_9x9_evil_6pqgq(self):
        """https://gridpuzzle.com/from1tox/6pqgq"""
        grid = Grid([
            [_, _, _, _, _, _, _, _, _],
            [7, 3, _, 1, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, 3, _, _, _],
            [_, _, _, 3, _, _, _, 5, _],
            [_, _, _, _, _, _, 2, _, _],
            [2, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, 1, _],
            [_, _, _, _, _, _, _, _, _]
        ])
        region_grid = Grid([
            [1, 1, 1, 2, 2, 2, 3, 4, 4],
            [5, 1, 6, 7, 7, 2, 3, 8, 8],
            [5, 1, 6, 6, 9, 8, 8, 8, 8],
            [5, 1, 6, 10, 9, 11, 8, 11, 8],
            [5, 5, 6, 10, 9, 11, 11, 11, 12],
            [13, 5, 5, 10, 10, 14, 14, 11, 12],
            [13, 13, 13, 15, 10, 14, 16, 12, 12],
            [17, 17, 15, 15, 16, 16, 16, 16, 12],
            [17, 17, 17, 15, 18, 18, 16, 12, 12]
        ])
        row_clues = [27, 34, 36, 26, 24, 31, _, 29, 19]
        column_clues = [32, 24, 32, _, 22, 25, 28, 40, _]

        expected_grid = Grid([
            [5, 4, 6, 2, 1, 4, 2, 1, 2],
            [7, 3, 4, 1, 2, 3, 1, 7, 6],
            [5, 2, 3, 5, 3, 2, 8, 5, 3],
            [3, 1, 2, 4, 2, 3, 4, 6, 1],
            [1, 4, 1, 3, 1, 2, 1, 5, 6],
            [3, 2, 6, 1, 5, 3, 2, 4, 5],
            [2, 4, 1, 3, 2, 1, 5, 7, 3],
            [4, 3, 4, 2, 4, 6, 3, 1, 2],
            [2, 1, 5, 1, 2, 1, 2, 4, 1],
        ])
        game_solver = From1ToXSolver(grid, region_grid, row_clues, column_clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_10x10_evil_xv6md(self):
        """https://gridpuzzle.com/from1tox/xv6md"""
        grid = Grid([
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, 2, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, 5, _, _, _, _, 2, _, _, _],
            [_, _, _, _, _, 3, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, _, 3, _, _, _, _, _, _]
        ])
        region_grid = Grid([
            [1, 2, 2, 3, 4, 4, 5, 5, 5, 6],
            [1, 3, 3, 3, 7, 4, 4, 5, 6, 6],
            [8, 8, 3, 7, 7, 9, 9, 9, 10, 6],
            [11, 11, 12, 7, 7, 13, 9, 10, 10, 10],
            [11, 11, 12, 12, 13, 13, 9, 10, 14, 15],
            [16, 11, 12, 17, 17, 13, 18, 14, 14, 15],
            [16, 16, 12, 17, 17, 19, 18, 18, 14, 14],
            [16, 16, 20, 20, 20, 19, 18, 21, 21, 22],
            [23, 23, 23, 20, 24, 19, 25, 25, 22, 22],
            [23, 23, 24, 24, 24, 19, 25, 25, 22, 22]
        ])
        row_clues = [24, _, 30, 32, 27, 23, 27, 23, 33, 18]
        column_clues = [26, 27, 28, _, 25, 25, 25, _, _, 23]

        expected_grid = Grid([
            [2, 1, 2, 3, 1, 3, 1, 4, 3, 4],
            [1, 4, 5, 1, 5, 2, 4, 2, 1, 3],
            [2, 1, 2, 4, 2, 3, 5, 4, 5, 2],
            [5, 4, 5, 3, 1, 4, 2, 3, 4, 1],
            [3, 2, 3, 4, 3, 2, 1, 2, 5, 2],
            [4, 1, 2, 3, 4, 1, 3, 1, 3, 1],
            [2, 5, 1, 2, 1, 4, 2, 4, 2, 4],
            [1, 3, 4, 3, 2, 3, 1, 2, 1, 3],
            [5, 4, 3, 1, 4, 2, 4, 3, 5, 2],
            [1, 2, 1, 3, 2, 1, 2, 1, 4, 1],
        ])
        game_solver = From1ToXSolver(grid, region_grid, row_clues, column_clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
