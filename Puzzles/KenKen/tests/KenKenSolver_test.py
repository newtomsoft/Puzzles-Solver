import unittest
from unittest import TestCase

from KenKen.KenKenSolver import KenKenSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine
from Utils.Grid import Grid
from Utils.Position import Position


class KenKenSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_grid_square(self):
        regions_operators_results = [
            ([Position(0, 0), Position(0, 1), Position(0, 2)], '+', 8),
            ([Position(1, 0), Position(1, 1), Position(1, 2)], 'x', 4),
        ]
        with self.assertRaises(ValueError) as context:
            KenKenSolver(regions_operators_results, self.get_solver_engine())

        self.assertEqual("KenKen grid must be square", str(context.exception))

    def test_solution_4x4(self):
        regions_operators_results = [
            ([Position(0, 0), Position(1, 0)], 'x', 4),
            ([Position(0, 1), Position(0, 2)], '+', 7),
            ([Position(0, 3), Position(1, 3)], '/', 2),
            ([Position(1, 1), Position(1, 2)], 'x', 6),
            ([Position(2, 0), Position(2, 1)], '-', 1),
            ([Position(2, 2), Position(3, 2)], '+', 5),
            ([Position(2, 3), Position(3, 3)], '-', 1),
            ([Position(3, 0), Position(3, 1)], '/', 2),
        ]
        expected_solution = Grid([
            [1, 4, 3, 2],
            [4, 3, 2, 1],
            [3, 2, 1, 4],
            [2, 1, 4, 3],
        ])
        kenken_game = KenKenSolver(regions_operators_results, self.get_solver_engine())

        solution = kenken_game.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_4x4_hard(self):
        regions_operators_results = [
            ([Position(0, 0), Position(1, 0)], '-', 1),
            ([Position(0, 1), Position(0, 2), Position(0, 3), Position(1, 2), Position(1, 3)], '+', 11),
            ([Position(1, 1), Position(2, 1)], '/', 2),
            ([Position(2, 0), Position(3, 0), Position(3, 1)], 'x', 6),
            ([Position(2, 2), Position(3, 2)], '-', 2),
            ([Position(2, 3), Position(3, 3)], '/', 2),
        ]
        expected_solution = Grid([
            [4, 1, 2, 3],
            [3, 2, 4, 1],
            [1, 4, 3, 2],
            [2, 3, 1, 4],
        ])
        kenken_game = KenKenSolver(regions_operators_results, self.get_solver_engine())

        solution = kenken_game.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_6x6(self):
        grid = Grid([
            [6, -1, 3, -1, -1, -1],
            [-1, 5, -1, -1, -1, 2],
            [2, -1, -1, -1, 6, 3],
            [-1, -1, -1, -1, 1, -1],
            [1, -1, 6, -1, -1, 5],
            [5, -1, -1, -1, -1, -1]
        ])
        expected_solution = Grid([
            [6, 2, 3, 4, 5, 1],
            [4, 5, 1, 6, 3, 2],
            [2, 1, 4, 5, 6, 3],
            [3, 6, 5, 2, 1, 4],
            [1, 4, 6, 3, 2, 5],
            [5, 3, 2, 1, 4, 6]
        ])
        kenken_game = KenKenSolver(grid, self.get_solver_engine())

        solution = kenken_game.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_9x9(self):
        grid = Grid([
            [-1, 5, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, 2, 4, -1, 3, 8, 7, 1],
            [1, 7, -1, 2, 9, 6, 5, 3, -1],
            [6, -1, -1, -1, -1, -1, 7, -1, -1],
            [-1, -1, -1, -1, 1, 4, 9, -1, 3],
            [5, -1, -1, -1, 8, 9, 1, 6, -1],
            [-1, 8, -1, 3, 6, -1, 4, -1, -1],
            [-1, 4, 5, -1, 2, -1, -1, 8, -1],
            [2, 9, -1, -1, 4, -1, -1, -1, -1]
        ])
        expected_solution = Grid([
            [4, 5, 3, 1, 7, 8, 2, 9, 6],
            [9, 6, 2, 4, 5, 3, 8, 7, 1],
            [1, 7, 8, 2, 9, 6, 5, 3, 4],
            [6, 1, 9, 5, 3, 2, 7, 4, 8],
            [8, 2, 7, 6, 1, 4, 9, 5, 3],
            [5, 3, 4, 7, 8, 9, 1, 6, 2],
            [7, 8, 1, 3, 6, 5, 4, 2, 9],
            [3, 4, 5, 9, 2, 1, 6, 8, 7],
            [2, 9, 6, 8, 4, 7, 3, 1, 5],
        ])
        kenken_game = KenKenSolver(grid, self.get_solver_engine())

        solution = kenken_game.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_9x9_2(self):
        grid = Grid([
            [7, 1, -1, -1, 8, 3, -1, 4, -1],
            [9, -1, -1, -1, -1, -1, -1, 5, 8],
            [4, -1, -1, -1, 1, -1, -1, -1, -1],
            [-1, 8, -1, -1, -1, 9, -1, -1, 5],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [5, -1, -1, 4, -1, -1, -1, 2, -1],
            [-1, -1, -1, -1, 7, -1, -1, -1, 4],
            [3, 2, -1, -1, -1, -1, -1, -1, 9],
            [-1, 4, -1, 5, 9, -1, -1, 7, 2]
        ])
        expected_solution = Grid([
            [7, 1, 5, 9, 8, 3, 2, 4, 6],
            [9, 3, 2, 6, 4, 7, 1, 5, 8],
            [4, 6, 8, 2, 1, 5, 7, 9, 3],
            [1, 8, 3, 7, 2, 9, 4, 6, 5],
            [2, 7, 4, 8, 5, 6, 9, 3, 1],
            [5, 9, 6, 4, 3, 1, 8, 2, 7],
            [8, 5, 9, 3, 7, 2, 6, 1, 4],
            [3, 2, 7, 1, 6, 4, 5, 8, 9],
            [6, 4, 1, 5, 9, 8, 3, 7, 2]
        ])
        kenken_game = KenKenSolver(grid, self.get_solver_engine())

        solution = kenken_game.get_solution()
        self.assertEqual(expected_solution, solution)


if __name__ == '__main__':
    unittest.main()
