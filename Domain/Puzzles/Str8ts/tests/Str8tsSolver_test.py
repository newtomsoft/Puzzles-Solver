from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Str8ts.Str8tsSolver import Str8tsSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine

_ = 0
x = True
o = False

class Str8tsSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_initial_constraints(self):
        numbers_grid = Grid([
            [2, 1, _],
            [1, 2, 3],
            [3, _, 2],
        ])
        blacks_grid = Grid([
            [o, o, x],
            [x, o, o],
            [o, x, o],
        ])

        game_solver = Str8tsSolver(numbers_grid, blacks_grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [2, 1, _],
            [1, 2, 3],
            [3, _, 2],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_distinct_constraints(self):
        numbers_grid = Grid([
            [1, _, 3],
            [_, _, _],
            [3, _, _],
        ])
        blacks_grid = Grid([
            [o, o, o],
            [o, x, o],
            [o, o, o],
        ])

        game_solver = Str8tsSolver(numbers_grid, blacks_grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 2, 3],
            [2, _, 1],
            [3, 1, 2],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_adjacent_constraints(self):
        numbers_grid = Grid([
            [2, 1, _],
            [1, 2, 3],
            [3, _, _],
        ])
        blacks_grid = Grid([
            [o, o, x],
            [x, o, o],
            [o, x, o],
        ])

        game_solver = Str8tsSolver(numbers_grid, blacks_grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [2, 1, _],
            [1, 2, 3],
            [3, _, 2],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
