from unittest import TestCase

from Domain.Grid.Grid import Grid
from NumberLink.NumberLinkSolver import NumberLinkSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine

_ = -1

class NUmberLinkSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_basic_grid(self):
        grid = Grid([
            [1, 2, _],
            [_, 3, 2],
            [1, _, 3]
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
            [1, _, 2, _, 5],
            [_, _, 3, _, 4],
            [_, _, _, _, _],
            [_, 2, _, 5, _],
            [_, 1, 3, 4, _],
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

    def test_solution_9x9(self):
        grid = Grid([
            [_, _, _, _, _, _, _, _, _],
            [_, 1, _, _, 6, _, _, _, _],
            [_, _, 4, _, 4, _, _, _, _],
            [_, _, 5, _, _, _, _, _, _],
            [_, _, _, _, 2, _, _, _, _],
            [_, 2, 5, 1, _, _, _, _, _],
            [_, 3, _, _, _, _, _, _, _],
            [_, _, 3, _, _, 6, _, _, _],
            [_, _, _, _, _, _, _, _, _],
        ])
        game_solver = NumberLinkSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 1, 1, 1, 6, 6, 6, 6, 4],
            [4, 4, 4, 1, 4, 4, 4, 6, 4],
            [5, 5, 5, 1, 1, 1, 4, 6, 4],
            [5, 2, 2, 2, 2, 1, 4, 6, 4],
            [5, 2, 5, 1, 1, 1, 4, 6, 4],
            [5, 3, 5, 5, 4, 4, 4, 6, 4],
            [5, 3, 3, 5, 4, 6, 6, 6, 4],
            [5, 5, 5, 5, 4, 4, 4, 4, 4],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_15x15(self):
        grid = Grid([
            [_, _, _, _, _, _, _, _, 3, 4, 9, _, _, _, _],
            [_, _, _, _, 3, _, 5, 6, _, _, _, _, 7, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, 6, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, 9, _, _],
            [_, _, _, _, 4, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, 7, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, 0, _, 8, _, _],
            [_, _, _, 1, 2, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, 5, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, 8, _, _, _, _, _, _],
            [_, _, _, 2, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, 1, _, _, _, _, _, _, _, 0, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
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
            [6, 3, 5, 1, 1, 1, 1, 3, 3, 3, 0, 0, 8, 3, 6],
            [6, 3, 5, 1, 2, 2, 1, 1, 1, 1, 1, 0, 8, 3, 6],
            [6, 3, 5, 5, 5, 2, 2, 2, 2, 2, 1, 0, 8, 3, 6],
            [6, 3, 8, 8, 8, 8, 8, 8, 8, 2, 1, 0, 8, 3, 6],
            [6, 3, 8, 2, 2, 2, 2, 2, 2, 2, 1, 0, 8, 3, 6],
            [6, 3, 8, 1, 1, 1, 1, 1, 1, 1, 1, 0, 8, 3, 6],
            [6, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 3, 6],
            [6, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 6],
            [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
