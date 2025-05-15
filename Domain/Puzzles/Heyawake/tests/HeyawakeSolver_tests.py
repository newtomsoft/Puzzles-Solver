import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Heyawake.HeyawakeSolver import HeyawakeSolver


class HeyawakeSolverTests(TestCase):


    def test_black_count_by_region_1(self):
        grid = Grid([
            [1, 0],
            [0, 0],
        ])
        region_grid = Grid([
            [1, 2],
            [3, 4],
        ])
        expected_solution = Grid([
            [0, 1],
            [1, 1],
        ])

        heyawake_solver = HeyawakeSolver(grid, region_grid)
        solution = heyawake_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = heyawake_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_no_black_cells_adjacent(self):
        grid = Grid([
            [1, 1, ''],
            [0, '', ''],
        ])
        region_grid = Grid([
            [1, 2, 2],
            [3, 3, 3],
        ])
        expected_solution = Grid([
            [0, 1, 0],
            [1, 1, 1],
        ])

        heyawake_solver = HeyawakeSolver(grid, region_grid)
        solution = heyawake_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = heyawake_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_basic(self):
        grid = Grid([
            [2, '', ''],
            [0, '', ''],
        ])
        region_grid = Grid([
            [1, 1, 1],
            [2, 2, 2],
        ])
        expected_solution = Grid([
            [0, 1, 0],
            [1, 1, 1],
        ])

        heyawake_solver = HeyawakeSolver(grid, region_grid)
        solution = heyawake_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = heyawake_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_with_adjacents_for_white_cells_constraint(self):
        grid = Grid([
            [2, '', ''],
            ['', '', ''],
        ])
        region_grid = Grid([
            [1, 1, 1],
            [2, 2, 2],
        ])
        expected_solution = Grid([
            [0, 1, 0],
            [1, 1, 1],
        ])

        heyawake_solver = HeyawakeSolver(grid, region_grid)
        solution = heyawake_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = heyawake_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_easy(self):
        grid = Grid([
            ['', '', '', '', '', 1],
            ['', '', 1, '', '', ''],
            [1, '', '', '', '', ''],
            [1, 0, '', '', '', ''],
            ['', '', 1, '', '', ''],
            ['', '', 1, '', '', ''],
        ])
        region_grid = Grid([
            [1, 2, 2, 2, 2, 3],
            [1, 4, 5, 5, 5, 3],
            [6, 4, 5, 5, 5, 3],
            [7, 8, 9, 9, 9, 3],
            [7, 10, 11, 11, 11, 3],
            [7, 10, 12, 12, 13, 13],

        ])
        expected_solution = Grid([
            [1, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1],
            [0, 1, 1, 0, 1, 0],
            [1, 1, 0, 1, 1, 1],
            [1, 0, 1, 1, 0, 1],
            [0, 1, 1, 0, 1, 1],
        ])

        heyawake_solver = HeyawakeSolver(grid, region_grid)
        solution = heyawake_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = heyawake_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_hard(self):
        grid = Grid([
            [-1, -1, 2, -1, -1, -1, -1, -1, -1, -1],
            [2, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, 1, -1, -1, -1, 3, -1, -1],
            [-1, 2, -1, -1, -1, -1, -1, -1, 2, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, 2, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, 0, -1],
            [-1, -1, -1, -1, -1, -1, 1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        ])
        region_grid = Grid([
            [1, 1, 2, 3, 4, 5, 5, 5, 5, 6],
            [7, 8, 2, 3, 4, 9, 9, 10, 10, 6],
            [7, 8, 2, 11, 11, 9, 9, 12, 13, 6],
            [7, 14, 14, 14, 15, 15, 15, 12, 16, 16],
            [7, 14, 14, 14, 15, 15, 15, 12, 16, 16],
            [7, 14, 14, 14, 17, 17, 18, 12, 19, 20],
            [7, 21, 22, 22, 23, 23, 18, 12, 19, 20],
            [7, 21, 24, 24, 23, 23, 18, 12, 25, 25],
            [7, 21, 24, 24, 23, 23, 26, 26, 25, 25],
            [7, 27, 27, 27, 27, 28, 28, 29, 29, 29]
        ])
        expected_solution = Grid([
            [1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
            [0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
            [1, 1, 0, 1, 0, 1, 1, 0, 1, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 0],
            [1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
            [0, 1, 1, 1, 1, 0, 1, 0, 1, 1],
            [1, 0, 1, 0, 1, 1, 0, 1, 1, 0],
            [1, 1, 0, 1, 0, 1, 1, 0, 1, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
        ])

        heyawake_solver = HeyawakeSolver(grid, region_grid)
        solution = heyawake_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = heyawake_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
