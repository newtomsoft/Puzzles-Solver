from unittest import TestCase

from Domain.Grid.Grid import Grid
from NumberLink.NumberLinkSolver import NumberLinkSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine


class NUmberLinkSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_basic_grid(self):
        grid = Grid([
            [1, 2, 0],
            [0, 3, 2],
            [1, 0, 3]
        ])
        game_solver = NumberLinkSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 2, 2],
            [1, 3, 2],
            [1, 3, 3],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5(self):
        grid = Grid([
            [1, 0, 2, 0, 5],
            [0, 0, 3, 0, 4],
            [0, 0, 0, 0, 0],
            [0, 2, 0, 5, 0],
            [0, 1, 3, 4, 0],
        ])
        game_solver = NumberLinkSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 2, 2, 5, 5],
            [1, 2, 3, 5, 4],
            [1, 2, 3, 5, 4],
            [1, 2, 3, 5, 4],
            [1, 1, 3, 4, 4],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_15x15(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 9, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0, 5, 6, 0, 0, 0, 0, 7, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0],
            [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 8, 0, 0],
            [0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])
        game_solver = NumberLinkSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [6, 6, 6, 6, 6, 6, 6, 6, 3, 4, 9, 6, 6, 6, 6],
            [6, 3, 3, 3, 3, 5, 5, 6, 3, 4, 9, 6, 7, 7, 6],
            [6, 3, 5, 5, 5, 5, 3, 3, 3, 4, 9, 6, 6, 7, 6],
            [6, 3, 5, 3, 3, 3, 3, 4, 4, 4, 9, 9, 9, 7, 6],
            [6, 3, 5, 3, 4, 4, 4, 4, 7, 7, 7, 7, 7, 7, 6],
            [6, 3, 5, 3, 3, 3, 3, 3, 7, 3, 3, 3, 3, 3, 6],
            [6, 3, 5, 1, 1, 1, 1, 3, 3, 3, 10, 10, 8, 3, 6],
            [6, 3, 5, 1, 2, 2, 1, 1, 1, 1, 1, 10, 8, 3, 6],
            [6, 3, 5, 5, 5, 2, 2, 2, 2, 2, 1, 10, 8, 3, 6],
            [6, 3, 8, 8, 8, 8, 8, 8, 8, 2, 1, 10, 8, 3, 6],
            [6, 3, 8, 2, 2, 2, 2, 2, 2, 2, 1, 10, 8, 3, 6],
            [6, 3, 8, 1, 1, 1, 1, 1, 1, 1, 1, 10, 8, 3, 6],
            [6, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 3, 6],
            [6, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 6],
            [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
