import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine
from Domain.Puzzles.Vectors.VectorsSolver import VectorsSolver

_ = ''


class VectorsSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_basic_grid(self):
        grid = Grid([
            [_, 4, _],
            [_, _, 1],
            [1, _, _]
        ])
        game_solver = VectorsSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1],
            [3, 1, 2],
            [3, 1, 2]
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8(self):
        grid = Grid([
            [_, _, _, _, _, 5, _, _],
            [_, _, _, _, _, _, 8, _],
            [_, 6, _, _, _, _, _, _],
            [_, _, _, _, 1, _, _, 9],
            [_, _, 6, _, _, _, _, _],
            [9, _, _, _, _, _, _, _],
            [_, _, _, 5, _, _, _, _],
            [_, _, _, _, 6, _, _, _],
        ])
        game_solver = VectorsSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1, 1, 1, 1, 2, 5],
            [2, 2, 2, 2, 2, 2, 2, 5],
            [3, 3, 3, 3, 3, 3, 2, 5],
            [7, 3, 6, 4, 4, 5, 5, 5],
            [7, 6, 6, 6, 6, 6, 6, 5],
            [7, 7, 7, 7, 7, 7, 7, 5],
            [7, 8, 8, 8, 8, 8, 8, 5],
            [9, 9, 9, 9, 9, 9, 9, 5],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_9x9(self):
        grid = Grid([
            [_, _, _, 4, _, _, _, _, _],
            [_, _, _, _, _, 5, _, _, _],
            [_, 1, _, _, _, _, 2, _, _],
            [_, _, _, _, _, _, _, _, 6],
            [5, _, _, _, _, 2, _, _, _],
            [_, _, 4, _, _, _, 4, _, _],
            [1, _, _, _, 5, _, _, _, _],
            [_, _, _, 9, _, _, _, 9, _],
            [_, 5, _, _, 4, _, _, _, _],
        ])
        game_solver = VectorsSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1, 1, 1, 2, 4, 13, 5],
            [6, 2, 2, 2, 2, 2, 4, 13, 5],
            [6, 3, 8, 12, 11, 7, 4, 13, 5],
            [6, 3, 8, 12, 11, 7, 9, 13, 5],
            [6, 6, 8, 12, 11, 7, 9, 13, 5],
            [6, 14, 8, 12, 11, 9, 9, 13, 5],
            [10, 14, 8, 12, 11, 11, 9, 13, 5],
            [10, 14, 12, 12, 12, 12, 13, 13, 13],
            [14, 14, 14, 12, 15, 15, 15, 15, 15],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10(self):
        grid = Grid([
            [_, _, _, 4, _, _, 5, _, 1, _],
            [_, 9, _, _, 1, _, _, _, _, _],
            [2, _, _, 3, _, _, _, _, _, 3],
            [_, _, _, _, 3, _, 0, _, _, _],
            [_, _, _, 5, _, _, _, _, 1, _],
            [2, _, _, _, _, _, _, 9, _, 2],
            [_, _, 5, _, _, 1, _, _, _, _],
            [_, _, _, 4, _, _, _, 1, _, 2],
            [0, _, _, _, _, 1, _, _, _, _],
            [_, _, _, _, _, _, 7, _, 5, _],
        ])
        game_solver = VectorsSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1, 1, 2, 2, 2, 2, 3, 8],
            [4, 4, 4, 1, 5, 5, 2, 14, 3, 8],
            [6, 4, 7, 7, 7, 7, 2, 14, 8, 8],
            [6, 4, 9, 9, 9, 9, 10, 14, 12, 15],
            [6, 4, 11, 11, 11, 11, 11, 14, 12, 15],
            [13, 4, 16, 11, 14, 14, 14, 14, 14, 15],
            [13, 4, 16, 16, 16, 17, 17, 14, 24, 20],
            [13, 4, 16, 18, 18, 18, 18, 19, 24, 20],
            [21, 4, 16, 18, 22, 22, 23, 19, 24, 20],
            [23, 23, 23, 23, 23, 23, 23, 24, 24, 24],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_11x11(self):
        grid = Grid([
            [_, _, _, _, _, 8, _, _, _, 2, _],
            [_, 4, _, _, _, _, _, 1, _, _, 4],
            [_, _, 4, _, _, _, _, _, _, 3, _],
            [_, 7, _, _, 1, _, 1, _, 1, _, _],
            [_, _, _, _, _, _, _, 8, _, _, _],
            [_, _, 1, _, _, _, _, _, _, _, 8],
            [5, _, _, _, 7, _, _, _, _, _, _],
            [_, _, _, 3, _, _, _, _, _, 5, _],
            [_, _, _, _, 3, _, 2, _, _, _, _],
            [_, 2, _, _, _, _, _, _, 5, _, 1],
            [_, _, _, _, 6, _, 4, _, _, _, _],
        ])
        game_solver = VectorsSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 5],
            [3, 3, 3, 3, 3, 1, 4, 4, 5, 5, 5],
            [6, 6, 6, 6, 6, 1, 7, 7, 7, 7, 5],
            [8, 8, 8, 9, 9, 10, 10, 12, 11, 11, 14],
            [15, 8, 12, 12, 12, 12, 12, 12, 12, 12, 14],
            [15, 8, 13, 13, 16, 14, 14, 14, 14, 14, 14],
            [15, 8, 16, 16, 16, 16, 16, 16, 16, 18, 14],
            [15, 8, 17, 17, 17, 17, 20, 18, 18, 18, 18],
            [15, 8, 19, 19, 19, 19, 20, 20, 22, 18, 23],
            [15, 21, 21, 21, 24, 22, 22, 22, 22, 22, 23],
            [24, 24, 24, 24, 24, 24, 25, 25, 25, 25, 25],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_15x15(self):
        grid = Grid([
            [2, _, _, _, 1, _, _, 3, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, 11, _, _, _, 13, _],
            [4, _, _, _, 1, _, 2, _, _, _, _, _, 13, _, _],
            [_, _, _, _, _, _, _, _, _, 13, _, _, _, _, _],
            [2, _, _, _, _, _, 7, _, _, _, _, _, _, _, _],
            [_, 15, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, 6, _, _, _, _, _, _, _, _, 6],
            [5, _, 5, _, _, _, _, _, 4, _, _, 10, _, _, _],
            [_, _, _, _, _, _, 1, _, _, _, _, _, _, _, 1],
            [_, _, _, _, 2, _, _, 4, _, _, _, _, _, _, _],
            [_, _, _, 11, _, _, _, _, _, _, _, _, _, _, 1],
            [_, _, _, _, _, _, _, 4, _, _, 15, _, _, _, _],
            [_, _, _, _, _, 2, _, _, _, 1, _, 1, _, _, _],
            [1, _, 11, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, 8, _, _, _, _, _, _, 5],
        ])
        game_solver = VectorsSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 27, 19, 9, 5, 15],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 27, 19, 9, 5, 15],
            [6, 6, 6, 6, 7, 7, 8, 8, 8, 4, 27, 19, 9, 5, 15],
            [6, 10, 10, 10, 10, 10, 10, 10, 10, 10, 27, 19, 9, 5, 15],
            [11, 12, 12, 12, 12, 12, 12, 12, 12, 10, 27, 19, 9, 5, 15],
            [11, 13, 13, 13, 13, 13, 13, 13, 18, 10, 27, 19, 9, 5, 15],
            [11, 13, 17, 14, 14, 14, 14, 14, 18, 10, 27, 19, 9, 5, 15],
            [16, 13, 17, 17, 17, 14, 20, 18, 18, 10, 27, 19, 9, 5, 21],
            [16, 13, 17, 24, 22, 14, 20, 23, 18, 10, 27, 19, 9, 5, 21],
            [16, 13, 17, 24, 22, 22, 23, 23, 23, 23, 27, 19, 9, 5, 25],
            [16, 13, 24, 24, 24, 24, 24, 24, 24, 24, 27, 19, 9, 5, 25],
            [16, 13, 32, 24, 26, 26, 26, 26, 27, 27, 27, 27, 9, 5, 34],
            [16, 13, 32, 24, 28, 28, 28, 26, 29, 29, 27, 30, 9, 5, 34],
            [31, 13, 32, 32, 32, 32, 32, 32, 32, 32, 32, 30, 9, 5, 34],
            [31, 13, 32, 33, 33, 33, 33, 33, 33, 33, 33, 33, 34, 34, 34],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
