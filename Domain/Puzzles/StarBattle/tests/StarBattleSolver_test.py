import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.StarBattle.StarBattleSolver import StarBattleSolver

_ = 0


class StarBattleSolverTests(TestCase):
    def test_solution_grid_not_a_square(self):
        grid = Grid([
            [3, 1, 1],
            [3, 2, 2],
        ])
        with self.assertRaises(ValueError) as context:
            StarBattleSolver(grid, 1)
        self.assertEqual("The grid must be square", str(context.exception))

    def test_solution_grid_size_less_than_4(self):
        grid = Grid([
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ])
        with self.assertRaises(ValueError) as context:
            StarBattleSolver(grid, 1)
        self.assertEqual("The grid must be at least 4x4", str(context.exception))

    def test_solution_color_less_than_columns_number(self):
        grid = Grid([
            [3, 1, 2, 2],
            [3, 1, 2, 2],
            [3, 1, 2, 2],
            [3, 1, 2, 2],
        ])
        with self.assertRaises(ValueError) as context:
            StarBattleSolver(grid, 1)
        self.assertEqual("The grid must have the same number of regions as rows/column", str(context.exception))

    def test_solution_1(self):
        grid = Grid([
            [4, 1, 2, 3],
            [4, 4, 4, 4],
            [4, 4, 4, 4],
            [4, 4, 4, 4],
        ])
        game_solver = StarBattleSolver(grid, 1)
        solution = game_solver.get_solution()
        self.assertIsNone(solution)

    def test_solution_grid_4x4(self):
        grid = Grid([
            [4, 4, 1, 1],
            [4, 4, 4, 1],
            [4, 2, 2, 3],
            [2, 2, 2, 3],
        ])
        expected_solution = Grid([
            [_, _, 1, _],
            [1, _, _, _],
            [_, _, _, 1],
            [_, 1, _, _],
        ])
        game_solver = StarBattleSolver(grid, 1)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_9x9(self):
        grid = Grid([
            [1, 1, 1, 1, 1, 2, 3, 3, 3],
            [1, 1, 1, 4, 2, 2, 2, 3, 3],
            [1, 1, 4, 4, 4, 2, 5, 3, 3],
            [1, 1, 1, 4, 6, 5, 5, 5, 3],
            [1, 1, 7, 6, 6, 6, 5, 8, 3],
            [1, 7, 7, 7, 6, 9, 8, 8, 8],
            [1, 1, 7, 1, 9, 9, 9, 8, 1],
            [1, 1, 1, 1, 1, 9, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
        ])
        expected_solution = Grid([
            [_, _, _, _, _, _, _, _, 1],
            [_, _, _, _, 1, _, _, _, _],
            [_, _, 1, _, _, _, _, _, _],
            [_, _, _, _, _, _, 1, _, _],
            [_, _, _, 1, _, _, _, _, _],
            [_, 1, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, 1, _],
            [_, _, _, _, _, 1, _, _, _],
            [1, _, _, _, _, _, _, _, _]
        ])
        game_solver = StarBattleSolver(grid, 1)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_9x9_2(self):
        grid = Grid([
            [9, 9, 9, 9, 8, 2, 2, 3, 4],
            [9, 6, 6, 8, 8, 8, 2, 3, 4],
            [9, 5, 6, 6, 8, 3, 3, 3, 4],
            [9, 5, 8, 8, 8, 8, 8, 7, 4],
            [9, 5, 5, 5, 8, 7, 7, 7, 4],
            [9, 8, 8, 8, 8, 8, 8, 8, 4],
            [1, 1, 4, 4, 8, 4, 4, 4, 4],
            [1, 1, 4, 8, 8, 8, 4, 4, 4],
            [1, 4, 4, 4, 4, 4, 4, 4, 4]
        ])
        expected_solution = Grid([
            [_, _, _, _, _, _, 1, _, _],
            [_, _, 1, _, _, _, _, _, _],
            [_, _, _, _, _, 1, _, _, _],
            [_, _, _, _, _, _, _, 1, _],
            [_, _, _, 1, _, _, _, _, _],
            [1, _, _, _, _, _, _, _, _],
            [_, _, _, _, 1, _, _, _, _],
            [_, 1, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, 1]
        ])
        game_solver = StarBattleSolver(grid, 1)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_when_stars_count_equal_0(self):
        grid = Grid([
            [9, 9, 9, 9, 8, 2, 2, 3, 4],
            [9, 6, 6, 8, 8, 8, 2, 3, 4],
            [9, 5, 6, 6, 8, 3, 3, 3, 4],
            [9, 5, 8, 8, 8, 8, 8, 7, 4],
            [9, 5, 5, 5, 8, 7, 7, 7, 4],
            [9, 8, 8, 8, 8, 8, 8, 8, 4],
            [1, 1, 4, 4, 8, 4, 4, 4, 4],
            [1, 1, 4, 8, 8, 8, 4, 4, 4],
            [1, 4, 4, 4, 4, 4, 4, 4, 4],
        ])
        stars_count_by_region_column_row = _
        with self.assertRaises(ValueError) as context:
            StarBattleSolver(grid, stars_count_by_region_column_row)
        self.assertEqual("The stars count by region/column/row must be at least 1", str(context.exception))

    def test_solution_when_stars_count_equal_2(self):
        grid = Grid([
            [1, 1, 1, 2, 2, 2, 2, 3, 3, 3],
            [4, 1, 1, 2, 2, 2, 3, 3, 3, 3],
            [4, 1, 1, 1, 1, 5, 5, 6, 7, 7],
            [4, 1, 1, 1, 5, 5, 6, 6, 7, 7],
            [4, 1, 1, 8, 5, 5, 6, 6, 7, 7],
            [4, 8, 8, 8, 8, 8, 6, 6, 7, 7],
            [4, 9, 9, 9, 9, 8, 6, 6, 7, 7],
            [4, 10, 9, 9, 9, 8, 6, 6, 6, 7],
            [4, 10, 10, 10, 10, 8, 6, 6, 7, 7],
            [4, 4, 10, 10, 10, 8, 8, 6, 7, 7]
        ])
        expected_solution = Grid([
            [_, _, _, _, _, 1, _, 1, _, _],
            [_, _, _, 1, _, _, _, _, _, 1],
            [_, 1, _, _, _, _, 1, _, _, _],
            [_, _, _, _, 1, _, _, _, 1, _],
            [1, _, 1, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, 1, _, 1],
            [_, 1, _, 1, _, _, _, _, _, _],
            [_, _, _, _, _, 1, _, _, 1, _],
            [1, _, 1, _, _, _, _, _, _, _],
            [_, _, _, _, 1, _, 1, _, _, _],
        ])
        stars_count_by_region_column_row = 2
        game_solver = StarBattleSolver(grid, stars_count_by_region_column_row)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_when_stars_count_equal_3(self):
        grid = Grid([
            [1, 1, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 4, 4, 4, 3],
            [1, 1, 2, 2, 1, 1, 2, 4, 4, 4, 4, 4, 5, 5],
            [6, 1, 2, 2, 1, 2, 2, 2, 2, 7, 7, 4, 4, 5],
            [6, 1, 1, 1, 1, 1, 2, 8, 8, 7, 4, 4, 4, 5],
            [6, 6, 6, 6, 2, 2, 2, 8, 7, 7, 4, 4, 4, 5],
            [6, 6, 6, 6, 9, 2, 8, 8, 8, 7, 7, 4, 4, 5],
            [6, 6, 9, 9, 9, 10, 8, 11, 8, 8, 7, 7, 12, 5],
            [6, 9, 9, 9, 10, 10, 10, 11, 8, 8, 7, 7, 12, 12],
            [6, 6, 9, 9, 10, 10, 10, 11, 8, 11, 11, 12, 12, 13],
            [6, 6, 9, 9, 9, 9, 10, 11, 11, 11, 12, 12, 13, 13],
            [14, 6, 14, 14, 14, 14, 10, 14, 11, 12, 12, 12, 12, 13],
            [14, 14, 14, 14, 10, 10, 10, 14, 11, 12, 12, 12, 13, 13],
            [14, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13]
        ])
        expected_solution = Grid([
            [_, _, _, _, 1, _, 1, _, 1, _, _, _, _, _],
            [1, _, 1, _, _, _, _, _, _, _, 1, _, _, _],
            [_, _, _, _, _, 1, _, 1, _, _, _, _, 1, _],
            [_, 1, _, 1, _, _, _, _, _, 1, _, _, _, _],
            [_, _, _, _, _, _, _, 1, _, _, _, 1, _, 1],
            [1, _, 1, _, 1, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, 1, _, _, 1, _, _, _, 1],
            [_, 1, _, 1, _, _, _, _, _, _, _, 1, _, _],
            [_, _, _, _, _, 1, _, 1, _, 1, _, _, _, _],
            [_, _, 1, _, _, _, _, _, _, _, _, 1, _, 1],
            [_, _, _, _, 1, _, 1, _, 1, _, _, _, _, _],
            [1, _, _, _, _, _, _, _, _, _, 1, _, 1, _],
            [_, _, _, 1, _, 1, _, _, 1, _, _, _, _, _],
            [_, 1, _, _, _, _, _, _, _, _, 1, _, 1, _],
        ])
        stars_count_by_region_column_row = 3
        game_solver = StarBattleSolver(grid, stars_count_by_region_column_row)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
