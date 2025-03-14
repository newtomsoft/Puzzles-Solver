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
            ([Position(0, 3), Position(1, 3)], '÷', 2),
            ([Position(1, 1), Position(1, 2)], 'x', 6),
            ([Position(2, 0), Position(2, 1)], '-', 1),
            ([Position(2, 2), Position(3, 2)], '+', 5),
            ([Position(2, 3), Position(3, 3)], '-', 1),
            ([Position(3, 0), Position(3, 1)], '÷', 2),
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
            ([Position(1, 1), Position(2, 1)], '÷', 2),
            ([Position(2, 0), Position(3, 0), Position(3, 1)], 'x', 6),
            ([Position(2, 2), Position(3, 2)], '-', 2),
            ([Position(2, 3), Position(3, 3)], '÷', 2),
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

    def test_solution_7x7_hard(self):
        regions_operators_results = [
            ([Position(0, 1), Position(0, 0)], '+', 5),
            ([Position(0, 2), Position(1, 2), Position(2, 2)], '+', 16),
            ([Position(0, 3), Position(0, 4), Position(0, 5)], 'x', 60),
            ([Position(1, 6), Position(0, 6)], '-', 1),
            ([Position(1, 0), Position(2, 0)], 'x', 21),
            ([Position(1, 1), Position(2, 1)], '-', 5),
            ([Position(1, 3), Position(1, 4)], '-', 3),
            ([Position(2, 5), Position(3, 5), Position(1, 5)], 'x', 84),
            ([Position(2, 3), Position(3, 3)], 'x', 6),
            ([Position(2, 4), Position(3, 4)], '÷', 3),
            ([Position(2, 6), Position(3, 6)], '+', 9),
            ([Position(4, 0), Position(3, 0)], '÷', 3),
            ([Position(3, 1), Position(4, 1)], '-', 2),
            ([Position(3, 2), Position(4, 2)], '+', 7),
            ([Position(4, 4), Position(4, 5), Position(4, 3)], 'x', 20),
            ([Position(6, 6), Position(4, 6), Position(5, 6), Position(5, 5)], '+', 15),
            ([Position(5, 0), Position(5, 1)], '÷', 2),
            ([Position(6, 2), Position(5, 2)], '-', 1),
            ([Position(5, 3), Position(6, 3)], '+', 9),
            ([Position(5, 4), Position(6, 4), Position(6, 5)], 'x', 126),
            ([Position(6, 1), Position(6, 0)], '-', 2)
        ]
        expected_solution = Grid([
            [1, 4, 7, 6, 2, 5, 3],
            [3, 1, 5, 7, 4, 6, 2],
            [7, 6, 4, 3, 1, 2, 5],
            [6, 5, 1, 2, 3, 7, 4],
            [2, 3, 6, 1, 5, 4, 7],
            [4, 2, 3, 5, 7, 1, 6],
            [5, 7, 2, 4, 6, 3, 1]
        ])
        kenken_game = KenKenSolver(regions_operators_results, self.get_solver_engine())

        solution = kenken_game.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_8x8_hard(self):
        regions_operators_results = [
            ([Position(1, 0), Position(0, 0)], '-', 2),
            ([Position(0, 1), Position(1, 1)], '+', 8),
            ([Position(0, 2), Position(1, 2)], '÷', 3),
            ([Position(0, 3), Position(0, 4), Position(0, 5)], '+', 11),
            ([Position(2, 3), Position(1, 3)], 'x', 6),
            ([Position(1, 4), Position(1, 5)], '-', 4),
            ([Position(2, 0), Position(3, 0)], '-', 4),
            ([Position(3, 1), Position(2, 1)], '÷', 3),
            ([Position(3, 2), Position(3, 3), Position(4, 2), Position(2, 2)], 'x', 120),
            ([Position(2, 4), Position(2, 5)], '+', 8),
            ([Position(3, 4), Position(3, 5)], '-', 3), ([Position(4, 0), Position(5, 0)], 'x', 6),
            ([Position(4, 1), Position(5, 1), Position(5, 2)], 'x', 24),
            ([Position(5, 3), Position(4, 3)], 'x', 10),
            ([Position(4, 4), Position(5, 4)], '-', 1), ([Position(4, 5), Position(5, 5)], '+', 7)
        ]
        expected_solution = Grid([
            [6, 3, 1, 4, 2, 5],
            [4, 5, 3, 1, 6, 2],
            [1, 2, 4, 6, 5, 3],
            [5, 6, 2, 3, 1, 4],
            [3, 1, 5, 2, 4, 6],
            [2, 4, 6, 5, 3, 1]
        ])
        kenken_game = KenKenSolver(regions_operators_results, self.get_solver_engine())

        solution = kenken_game.get_solution()
        self.assertEqual(expected_solution, solution)


if __name__ == '__main__':
    unittest.main()
