import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.TilePaint.TilePaintSolver import TilePaintSolver


class TilePaintSolverTests(TestCase):
    def test_solution_basic_grid(self):
        grid = Grid([
            [1, 2, 2, 2],
            [1, 1, 1, 2],
            [3, 1, 1, 1],
            [3, 3, 3, 3]
        ])
        row_sums = [3, -1, 1, 4]
        column_sums = [-1, 2, 2, 3]
        game_solver = TilePaintSolver(grid, row_sums, column_sums)
        solution, _ = game_solver.get_solution()
        expected_solution = Grid([
            [0, 1, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 0],
            [1, 1, 1, 1]
        ])
        self.assertEqual(expected_solution, solution)
        other_solution, _ = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_5jenr(self):
        #  https://gridpuzzle.com/tilepaint/5jenr
        grid = Grid([
            [1, 2, 3, 3, 4, 4, 5, 5],
            [1, 2, 6, 3, 3, 7, 5, 5],
            [2, 2, 6, 8, 8, 7, 9, 9],
            [10, 11, 12, 8, 8, 9, 9, 13],
            [10, 11, 12, 14, 15, 15, 16, 13],
            [10, 10, 12, 14, 14, 15, 16, 16],
            [17, 18, 12, 19, 20, 15, 21, 21],
            [17, 18, 19, 19, 20, 20, 21, 21]
        ])
        row_sums = [5, 4, -1, 4, -1, 4, -1, 5]
        column_sums = [-1, 3, 2, -1, 4, -1, -1, 7]
        game_solver = TilePaintSolver(grid, row_sums, column_sums)
        solution, _ = game_solver.get_solution()
        expected_solution = Grid([
            [1, 0, 0, 0, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1, 1],
            [0, 0, 1, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 0, 1],
            [1, 1, 0, 1, 1, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 1, 1],
            [0, 1, 0, 0, 1, 1, 1, 1]
        ])
        self.assertEqual(expected_solution, solution)
        other_solution, _ = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_16x16_050yg(self):
        #  https://gridpuzzle.com/tilepaint/050yg
        grid = Grid([
            [1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 5, 5, 5, 5, 6, 6],
            [7, 7, 1, 8, 8, 8, 3, 9, 9, 10, 10, 11, 12, 12, 13, 13],
            [7, 7, 14, 8, 15, 16, 17, 17, 9, 18, 18, 11, 11, 11, 19, 19],
            [20, 20, 14, 14, 15, 16, 21, 21, 22, 23, 23, 23, 24, 24, 25, 25],
            [26, 27, 27, 14, 28, 28, 21, 21, 22, 22, 22, 29, 24, 24, 30, 30],
            [26, 31, 32, 33, 33, 28, 28, 34, 34, 35, 35, 29, 36, 36, 37, 37],
            [26, 31, 32, 32, 32, 38, 39, 34, 34, 35, 40, 40, 41, 36, 42, 42],
            [43, 44, 44, 38, 38, 38, 39, 45, 45, 46, 47, 47, 41, 48, 48, 49],
            [43, 50, 50, 51, 51, 51, 39, 52, 52, 46, 46, 53, 53, 53, 48, 49],
            [54, 54, 50, 55, 55, 51, 56, 57, 58, 58, 59, 59, 60, 60, 61, 49],
            [62, 63, 63, 55, 56, 56, 56, 57, 58, 64, 59, 65, 65, 65, 61, 61],
            [62, 62, 63, 63, 66, 67, 68, 68, 64, 64, 69, 70, 70, 70, 71, 71],
            [72, 73, 74, 74, 66, 67, 68, 75, 75, 76, 69, 77, 78, 79, 79, 80],
            [72, 73, 74, 74, 66, 81, 81, 82, 82, 76, 83, 77, 78, 84, 79, 80],
            [72, 73, 73, 85, 85, 85, 81, 86, 86, 76, 83, 77, 84, 84, 84, 87],
            [88, 88, 88, 89, 89, 85, 86, 86, 90, 90, 90, 91, 91, 92, 92, 87]
        ])
        row_sums = [12, 3, -1, 6, 12, 5, 9, 8, 9, 9, 4, 10, 5, 7, 13, 11]
        column_sums = [9, -1, 9, -1, 11, -1, 11, 8, 7, 8, -1, 9, 4, -1, 8, 7]
        game_solver = TilePaintSolver(grid, row_sums, column_sums)
        solution, _ = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
            [0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
            [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1],
            [1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1],
            [0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
            [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
            [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0]
        ])
        self.assertEqual(expected_solution, solution)
        other_solution, _ = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
