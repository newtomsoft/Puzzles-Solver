import unittest
from unittest import TestCase

from Puzzles.Queens.QueensSolver import QueensSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine
from Utils.Grid import Grid


class QueensSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_grid_not_a_square(self):
        grid = Grid([
            [0, 1, 1],
            [0, 2, 2],
        ])
        with self.assertRaises(ValueError) as context:
            QueensSolver(grid, 1, self.get_solver_engine())
        self.assertEqual("The grid must be square", str(context.exception))

    def test_solution_grid_size_less_than_4(self):
        grid = Grid([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ])
        with self.assertRaises(ValueError) as context:
            QueensSolver(grid, 1, self.get_solver_engine())
        self.assertEqual("The grid must be at least 4x4", str(context.exception))

    def test_solution_color_less_than_columns_number(self):
        grid = Grid([
            [0, 1, 2, 2],
            [0, 1, 2, 2],
            [0, 1, 2, 2],
            [0, 1, 2, 2],
        ])
        with self.assertRaises(ValueError) as context:
            QueensSolver(grid, 1, self.get_solver_engine())
        self.assertEqual("The grid must have the same number of regions as rows/column", str(context.exception))

    def test_solution_1(self):
        grid = Grid([
            [0, 1, 2, 3],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        game_solver = QueensSolver(grid, 1, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertIsNone(solution)

    def test_solution_grid_4x4(self):
        grid = Grid([
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [0, 2, 2, 3],
            [2, 2, 2, 3],
        ])
        expected_solution = Grid([
            [0, 0, 1, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 1, 0, 0],
        ])
        game_solver = QueensSolver(grid, 1, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_9x9(self):
        grid = Grid([
            ['p', 'p', 'p', 'p', 'p', 'o', 'b', 'b', 'b'],
            ['p', 'p', 'p', 'g', 'o', 'o', 'o', 'b', 'b'],
            ['p', 'p', 'g', 'g', 'g', 'o', 'r', 'b', 'b'],
            ['p', 'p', 'p', 'g', 'm', 'r', 'r', 'r', 'b'],
            ['p', 'p', 'y', 'm', 'm', 'm', 'r', 's', 'b'],
            ['p', 'y', 'y', 'y', 'm', 'w', 's', 's', 's'],
            ['p', 'p', 'y', 'p', 'w', 'w', 'w', 's', 'p'],
            ['p', 'p', 'p', 'p', 'p', 'w', 'p', 'p', 'p'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ])
        expected_solution = Grid([
            [0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        game_solver = QueensSolver(grid, 1, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_9x9_2(self):
        grid = Grid([
            [0, 0, 0, 0, 8, 2, 2, 3, 4],
            [0, 6, 6, 8, 8, 8, 2, 3, 4],
            [0, 5, 6, 6, 8, 3, 3, 3, 4],
            [0, 5, 8, 8, 8, 8, 8, 7, 4],
            [0, 5, 5, 5, 8, 7, 7, 7, 4],
            [0, 8, 8, 8, 8, 8, 8, 8, 4],
            [1, 1, 4, 4, 8, 4, 4, 4, 4],
            [1, 1, 4, 8, 8, 8, 4, 4, 4],
            [1, 4, 4, 4, 4, 4, 4, 4, 4]
        ])
        expected_solution = Grid([
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1]
        ])
        game_solver = QueensSolver(grid, 1, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_when_stars_count_equal_0(self):
        grid = Grid([
            [0, 0, 0, 0, 8, 2, 2, 3, 4],
            [0, 6, 6, 8, 8, 8, 2, 3, 4],
            [0, 5, 6, 6, 8, 3, 3, 3, 4],
            [0, 5, 8, 8, 8, 8, 8, 7, 4],
            [0, 5, 5, 5, 8, 7, 7, 7, 4],
            [0, 8, 8, 8, 8, 8, 8, 8, 4],
            [1, 1, 4, 4, 8, 4, 4, 4, 4],
            [1, 1, 4, 8, 8, 8, 4, 4, 4],
            [1, 4, 4, 4, 4, 4, 4, 4, 4],
        ])
        stars_count_by_region_column_row = 0
        with self.assertRaises(ValueError) as context:
            QueensSolver(grid, stars_count_by_region_column_row, self.get_solver_engine())
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
            [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
        ])
        stars_count_by_region_column_row = 2
        game_solver = QueensSolver(grid, stars_count_by_region_column_row, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)


if __name__ == '__main__':
    unittest.main()
