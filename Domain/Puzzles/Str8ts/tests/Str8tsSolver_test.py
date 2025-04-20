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

    def test_solution_grid_not_square(self):
        numbers_grid = Grid([
            [2, 1, _],
            [1, 2, 3],
        ])
        blacks_grid = Grid([
            [o, o, x],
            [x, o, o],
        ])
        with self.assertRaises(ValueError) as context:
            Str8tsSolver(numbers_grid, blacks_grid, self.get_solver_engine())
        self.assertEqual("Str8ts has to be a square", str(context.exception))

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
        solution, __ = game_solver.get_solution()
        expected_solution = Grid([
            [2, 1, _],
            [1, 2, 3],
            [3, _, 2],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution, __ = game_solver.get_other_solution()
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
        solution, __ = game_solver.get_solution()
        expected_solution = Grid([
            [1, 2, 3],
            [2, _, 1],
            [3, 1, 2],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution, __ = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_many_black_cell_distinct_constraints(self):
        numbers_grid = Grid([
            [1, _, 2],
            [_, _, _],
            [3, _, _],
        ])
        blacks_grid = Grid([
            [o, x, o],
            [o, x, x],
            [o, o, o],
        ])

        game_solver = Str8tsSolver(numbers_grid, blacks_grid, self.get_solver_engine())
        solution, __ = game_solver.get_solution()
        expected_solution = Grid([
            [1, _, 2],
            [2, _, _],
            [3, 2, 1],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution, __ = game_solver.get_other_solution()
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
        solution, __ = game_solver.get_solution()
        expected_solution = Grid([
            [2, 1, _],
            [1, 2, 3],
            [3, _, 2],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution, __ = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_easy(self):
        numbers_grid = Grid([
            [_, 3, 4, _, _],
            [3, _, _, 2, 4],
            [_, 2, 3, _, _],
            [_, _, _, 5, _],
            [5, _, 2, _, 1],
        ])
        blacks_grid = Grid([
            [x, o, o, x, x],
            [o, o, o, o, o],
            [o, o, o, o, o],
            [o, o, o, o, o],
            [x, x, o, o, x],
        ])

        game_solver = Str8tsSolver(numbers_grid, blacks_grid, self.get_solver_engine())
        solution, __ = game_solver.get_solution()
        expected_solution = Grid([
            [0, 3, 4, 0, 0],
            [3, 1, 5, 2, 4],
            [1, 2, 3, 4, 5],
            [2, 4, 1, 5, 3],
            [5, 0, 2, 3, 1],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution, __ = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_9x9_expert(self):
        # https://gridpuzzle.com/str8ts/0qq1g
        numbers_grid = Grid([
            [_, 4, _, _, _, 7, 6, _, _],
            [_, _, 2, _, 6, _, _, _, _],
            [_, _, _, _, _, _, _, 6, _],
            [_, _, _, _, _, _, _, 5, _],
            [_, _, _, _, _, _, _, _, _],
            [_, 6, _, _, _, 3, _, _, 9],
            [_, _, 5, _, _, _, _, _, _],
            [_, 8, _, _, 5, _, _, 9, _],
            [_, _, _, _, _, 5, _, _, _],
        ])
        blacks_grid = Grid([
            [x, o, o, o, o, o, o, o, o],
            [o, o, o, o, o, o, o, o, o],
            [o, o, x, o, o, o, x, o, o],
            [x, o, o, o, x, x, o, o, x],
            [o, o, o, o, o, o, o, o, o],
            [o, o, x, o, o, o, x, o, o],
            [o, o, x, x, x, x, o, o, x],
            [o, o, o, o, o, o, o, o, o],
            [x, o, o, o, o, o, x, o, o]
        ])

        game_solver = Str8tsSolver(numbers_grid, blacks_grid, self.get_solver_engine())
        solution, __ = game_solver.get_solution()
        expected_solution = Grid([
            [0, 4, 1, 5, 8, 7, 6, 2, 3],
            [1, 9, 2, 7, 6, 8, 5, 3, 4],
            [2, 1, 0, 8, 7, 9, 0, 6, 5],
            [0, 7, 8, 6, 0, 0, 4, 5, 0],
            [6, 5, 7, 9, 1, 2, 3, 4, 8],
            [5, 6, 0, 4, 2, 3, 0, 8, 9],
            [4, 3, 5, 0, 0, 0, 2, 1, 0],
            [3, 8, 4, 2, 5, 6, 1, 9, 7],
            [0, 2, 3, 1, 4, 5, 0, 7, 6],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution, __ = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_9x9_evil(self):
        # https://gridpuzzle.com/str8ts/5y1rd
        numbers_grid = Grid([
            [_, _, _, _, _, _, _, _, _],
            [_, _, 7, _, _, _, _, _, _],
            [_, 8, _, _, _, 5, _, _, 6],
            [_, _, _, _, _, _, _, 3, _],
            [_, 1, _, _, _, 7, _, _, _],
            [_, _, _, _, _, _, 9, 8, _],
            [5, _, _, 2, _, _, _, _, _],
            [_, _, _, _, 6, _, _, _, _],
            [_, _, 6, _, _, _, _, _, _]
        ])
        blacks_grid = Grid([
            [x, o, o, o, x, x, o, o, x],
            [o, o, o, o, o, o, o, o, x],
            [o, o, x, x, o, o, x, o, o],
            [x, o, o, x, o, o, x, o, o],
            [o, o, o, o, o, o, o, o, o],
            [o, o, x, o, o, x, o, o, x],
            [o, o, x, o, o, x, x, o, o],
            [x, o, o, o, o, o, o, o, o],
            [x, o, o, x, x, o, o, o, x]
        ])

        game_solver = Str8tsSolver(numbers_grid, blacks_grid, self.get_solver_engine())
        solution, __ = game_solver.get_solution()
        expected_solution = Grid([
            [0, 6, 8, 7, 0, 0, 4, 5, 0],
            [8, 9, 7, 6, 5, 4, 3, 2, 0],
            [9, 8, 0, 0, 4, 5, 0, 7, 6],
            [0, 2, 1, 0, 7, 6, 0, 3, 4],
            [6, 1, 2, 4, 3, 7, 8, 9, 5],
            [4, 3, 0, 1, 2, 0, 9, 8, 0],
            [5, 4, 0, 2, 1, 0, 0, 6, 7],
            [0, 7, 5, 3, 6, 2, 1, 4, 8],
            [0, 5, 6, 0, 0, 3, 2, 1, 0],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution, __ = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
