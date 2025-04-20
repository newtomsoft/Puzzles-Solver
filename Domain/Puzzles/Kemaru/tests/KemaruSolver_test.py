import unittest
from unittest import TestCase

from Domain.Puzzles.Kemaru.KemaruSolver import KemaruSolver
from Domain.Board.Grid import Grid
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine

_ = 0


class KemaruSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_grid_must_have_at_least_2_regions_raises_value_error(self):
        grid = Grid([
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
        ])
        region_grid = Grid([
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
        ])
        with self.assertRaises(ValueError) as context:
            KemaruSolver(grid, region_grid, self.get_solver_engine())
        self.assertEqual(str(context.exception), "The grid must have at least 2 regions")

    def test_get_solution_4x4_easy(self):
        grid = Grid([
            [_, 4, _, 3],
            [_, _, _, _],
            [2, _, 4, 2],
            [_, 1, _, _],
        ])
        region_grid = Grid([
            [1, 2, 2, 2],
            [3, 4, 4, 2],
            [3, 3, 4, 4],
            [3, 3, 3, 4],
        ])
        expected_grid = Grid([
            [1, 4, 2, 3],
            [5, 3, 5, 1],
            [2, 6, 4, 2],
            [4, 1, 3, 1],
        ])
        game_solver = KemaruSolver(grid, region_grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_11x9_hard(self):
        grid = Grid([
            [4, _, _, _, 1, 2, _, _, 4],
            [_, _, 4, _, _, _, _, _, _],
            [3, _, 1, _, _, _, _, _, _],
            [_, 4, _, _, 1, _, _, _, 3],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, 3, _, _, 5, _],
            [_, 2, _, _, _, _, _, 2, _],
            [_, _, _, _, _, 5, _, _, _],
            [_, _, 5, _, _, _, _, 5, _],
            [_, _, _, _, 4, _, _, _, _],
            [2, _, _, _, _, _, _, _, 2],
        ])
        region_grid = Grid([
            [1, 1, 1, 1, 2, 2, 3, 3, 3],
            [4, 4, 4, 1, 2, 2, 2, 3, 3],
            [4, 4, 5, 6, 6, 7, 7, 7, 8],
            [9, 5, 5, 6, 6, 6, 7, 7, 8],
            [9, 5, 5, 10, 11, 11, 11, 12, 8],
            [9, 9, 10, 10, 11, 11, 12, 12, 12],
            [9, 13, 13, 10, 10, 14, 14, 22, 12],
            [13, 13, 15, 15, 15, 14, 14, 22, 22],
            [13, 16, 15, 15, 17, 14, 22, 22, 18],
            [16, 16, 19, 19, 19, 20, 21, 21, 18],
            [16, 16, 19, 19, 20, 20, 21, 21, 21]
        ])
        expected_grid = Grid([
            [4, 3, 1, 2, 1, 2, 1, 2, 4,],
            [1, 2, 4, 5, 4, 5, 3, 5, 3,],
            [3, 5, 1, 2, 3, 2, 1, 4, 2,],
            [2, 4, 3, 5, 1, 4, 3, 5, 3,],
            [3, 5, 2, 4, 2, 5, 1, 2, 1,],
            [4, 1, 3, 5, 3, 4, 3, 5, 4,],
            [5, 2, 4, 2, 1, 2, 1, 2, 1,],
            [1, 3, 1, 3, 4, 5, 4, 3, 4,],
            [5, 4, 5, 2, 1, 3, 1, 5, 2,],
            [1, 3, 1, 3, 4, 2, 4, 3, 1,],
            [2, 5, 2, 5, 1, 3, 1, 5, 2,],
        ])
        game_solver = KemaruSolver(grid, region_grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
