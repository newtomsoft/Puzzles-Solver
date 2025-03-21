from unittest import TestCase

from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine
from Utils.Grid import Grid
from Zip.ZipSolver import ZipSolver


class ZipSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_basic_grid(self):
        grid = Grid([
            [1, 0, 4],
            [0, 5, 0],
            [2, 0, 3]
        ])
        game_solver = ZipSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 4, 4],
            [1, 5, 3],
            [2, 2, 3],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6(self):
        grid = Grid([
            [0, 0, 0, 4, 7, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 8, 1, 0, 0],
            [5, 3, 0, 0, 2, 6],
            [0, 0, 0, 0, 0, 0],
        ])
        game_solver = ZipSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [4, 4, 4, 4, 7, 6],
            [4, 3, 3, 3, 7, 6],
            [4, 3, 7, 7, 7, 6],
            [4, 3, 8, 1, 1, 6],
            [5, 3, 2, 2, 2, 6],
            [5, 5, 5, 5, 5, 5],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_7x7(self):
        grid = Grid([
            [7, 0, 0, 0, 0, 0, 6],
            [0, 2, 0, 0, 0, 0, 0],
            [0, 0, 9, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 8, 0, 0],
            [0, 0, 0, 0, 0, 3, 0],
            [4, 0, 0, 0, 0, 0, 5],
        ])
        game_solver = ZipSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [7, 6, 6, 6, 6, 6, 6],
            [7, 2, 2, 2, 2, 2, 5],
            [7, 1, 9, 8, 8, 2, 5],
            [7, 1, 1, 1, 8, 2, 5],
            [7, 7, 7, 7, 8, 2, 5],
            [3, 3, 3, 3, 3, 3, 5],
            [4, 4, 4, 4, 4, 4, 5],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
