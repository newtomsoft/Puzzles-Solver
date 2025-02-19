import unittest
from unittest import TestCase

from Puzzles.Norinori.NorinoriSolver import NorinoriSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine
from Utils.Grid import Grid


class NorinoriSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_grid_not_a_square(self):
        grid = Grid([
            [0, 1, 1, 1, 1, 1],
            [0, 2, 2, 1, 1, 1],
            [0, 2, 2, 1, 1, 1],
            [0, 2, 2, 1, 1, 1],
            [0, 2, 2, 1, 1, 1],
        ])
        with self.assertRaises(ValueError) as context:
            NorinoriSolver(grid, self.get_solver_engine())
        self.assertEqual("The grid must be square", str(context.exception))

    def test_solution_grid_size_less_than_4(self):
        grid = Grid([
            [0, 0, 0, 1, 1],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 1, 1],
        ])
        with self.assertRaises(ValueError) as context:
            NorinoriSolver(grid, self.get_solver_engine())
        self.assertEqual("The grid must be at least 6x6", str(context.exception))

    def test_solution_color_less_than_columns_number(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        with self.assertRaises(ValueError) as context:
            NorinoriSolver(grid, self.get_solver_engine())
        self.assertEqual("The grid must have at least 2 regions", str(context.exception))

    def test_solution_none_because_2_by_region(self):
        grid = Grid([
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        game_solver = NorinoriSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_none_because_1_isolated(self):
        grid = Grid([
            [1, 1, 3, 0, 0, 0],
            [1, 1, 3, 0, 0, 0],
            [2, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        game_solver = NorinoriSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution(self):
        grid = Grid([
            [0, 0, 1, 1, 2, 1],
            [3, 4, 1, 1, 2, 1],
            [3, 4, 4, 1, 1, 1],
            [3, 4, 4, 4, 7, 7],
            [4, 4, 6, 6, 7, 7],
            [4, 5, 5, 6, 6, 7],
        ])
        expected_solution = Grid([
            [1, 1, 0, 0, 1, 0],
            [0, 0, 1, 0, 1, 0],
            [1, 0, 1, 0, 0, 1],
            [1, 0, 0, 1, 0, 1],
            [0, 0, 0, 1, 0, 0],
            [0, 1, 1, 0, 1, 1]
        ])
        game_solver = NorinoriSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_10x10(self):
        grid = Grid([
            [0, 0, 1, 1, 1, 2, 2, 3, 4, 4],
            [5, 5, 1, 6, 6, 2, 3, 3, 3, 3],
            [5, 5, 7, 6, 6, 2, 2, 8, 8, 9],
            [5, 5, 7, 7, 6, 6, 2, 8, 8, 9],
            [10, 11, 11, 11, 11, 11, 2, 2, 2, 9],
            [10, 10, 10, 11, 11, 12, 12, 13, 13, 9],
            [14, 10, 10, 15, 15, 12, 12, 12, 13, 19],
            [14, 10, 16, 16, 12, 12, 20, 13, 13, 19],
            [14, 14, 16, 16, 12, 12, 20, 20, 20, 18],
            [17, 17, 17, 16, 18, 18, 18, 18, 18, 18],
        ])
        expected_solution = Grid([
            [1, 1, 0, 0, 1, 0, 0, 0, 1, 1],
            [0, 0, 1, 0, 1, 0, 1, 1, 0, 0],
            [1, 0, 1, 0, 0, 0, 0, 0, 1, 1],
            [1, 0, 0, 1, 1, 0, 1, 1, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 1, 1, 0, 0],
            [1, 0, 0, 1, 1, 0, 0, 0, 0, 1],
            [0, 1, 1, 0, 0, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
            [1, 0, 1, 1, 0, 1, 0, 0, 1, 0]
        ])
        game_solver = NorinoriSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)


if __name__ == '__main__':
    unittest.main()
