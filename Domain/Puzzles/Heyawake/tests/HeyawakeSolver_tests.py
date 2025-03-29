import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Heyawake.HeyawakeSolver import HeyawakeSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine


class HeyawakeSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

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

        heyawake_solver = HeyawakeSolver(grid, region_grid, self.get_solver_engine())
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

        heyawake_solver = HeyawakeSolver(grid, region_grid, self.get_solver_engine())
        solution = heyawake_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = heyawake_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_no_black_cells_adjacent_grid_3x3(self):
        grid = Grid([
            [1, 1, ''],
            ['', 0, 1],
            [1, 0, ''],
        ])
        region_grid = Grid([
            [1, 2, 2],
            [1, 3, 4],
            [5, 6, 4],
        ])
        expected_solution = Grid([
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ])

        heyawake_solver = HeyawakeSolver(grid, region_grid, self.get_solver_engine())
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

        heyawake_solver = HeyawakeSolver(grid, region_grid, self.get_solver_engine())
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

        heyawake_solver = HeyawakeSolver(grid, region_grid, self.get_solver_engine())
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

        heyawake_solver = HeyawakeSolver(grid, region_grid, self.get_solver_engine())
        solution = heyawake_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = heyawake_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
