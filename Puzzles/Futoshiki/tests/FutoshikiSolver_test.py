import unittest
from unittest import TestCase

from Puzzles.Futoshiki.FutoshikiSolver import FutoshikiSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine
from Utils.Grid import Grid
from Utils.Position import Position


class FutoshikiSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_grid_must_be_square_raises_value_error(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1],
        ])
        higher_positions = [(Position(0, 0), Position(0, 1))]
        with self.assertRaises(ValueError) as context:
            FutoshikiSolver(grid, higher_positions, self.get_solver_engine())
        self.assertEqual(str(context.exception), "The grid must be square")

    def test_solution_grid_too_small(self):
        grid = Grid([
            [-1, -1, -1],
            [-1, -1, 0],
            [1, -1, -1],
        ])
        higher_positions = [(Position(0, 0), Position(0, 1))]
        with self.assertRaises(ValueError) as context:
            FutoshikiSolver(grid, higher_positions, self.get_solver_engine())
        self.assertEqual("The grid must be at least 4x4", str(context.exception))

    def test_solution_4x4(self):
        grid = Grid([
            [-1, -1, +3, -1],
            [-1, -1, -1, -1],
            [-1, -1, -1, -1],
            [-1, -1, -1, -1],
        ])
        higher_positions = [(Position(0, 3), Position(1, 3)), Position((1, 1), Position(1, 2)), Position((1, 3), Position(2, 3)), Position((2, 0), Position(3, 0)), Position((3, 1), Position(3, 2))]
        expected_grid = Grid([
            [2, 1, 3, 4],
            [4, 3, 1, 2],
            [3, 2, 4, 1],
            [1, 4, 2, 3],
        ])
        game_solver = FutoshikiSolver(grid, higher_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5(self):
        grid = Grid([
            [-1, -1, -1, -1, -1],
            [-1, +4, -1, -1, -1],
            [-1, -1, +4, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
        ])
        higher_positions = [
            (Position(0, 0), Position(0, 1)), Position((0, 3), Position(0, 2)), Position((0, 3), Position(1, 3)), Position((0, 4), Position(0, 3)), Position((2, 0), Position(2, 1)), Position((2, 2), Position(1, 2)), Position((2, 2), Position(3, 2)),
            Position((2, 4), Position(1, 4)), Position((3, 2), Position(3, 3)), Position((4, 3), Position(4, 4))
        ]
        expected_grid = Grid([
            [4, 2, 1, 3, 5],
            [5, 4, 3, 2, 1],
            [2, 1, 4, 5, 3],
            [3, 5, 2, 1, 4],
            [1, 3, 5, 4, 2],
        ])
        game_solver = FutoshikiSolver(grid, higher_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_7x7(self):
        grid = Grid([[-1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1], [6, 2, -1, -1, -1, -1, -1]])
        higher_positions = [
            (Position(0, 0), Position(1, 0)), Position((0, 1), Position(0, 0)), Position((0, 4), Position(0, 5)), Position((0, 5), Position(0, 6)), Position((1, 1), Position(1, 0)), Position((1, 4), Position(1, 5)), Position((1, 5), Position(1, 6)),
            Position((2, 0), Position(2, 1)), Position((2, 1), Position(1, 1)), Position((2, 3), Position(1, 3)), Position((2, 4), Position(2, 5)), Position((2, 6), Position(3, 6)), Position((3, 1), Position(3, 0)),
            (Position(3, 2), Position(2, 2)), Position((3, 3), Position(3, 2)), Position((3, 4), Position(3, 3)), Position((3, 6), Position(3, 5)), Position((4, 2), Position(4, 3)), Position((4, 3), Position(3, 3)), Position((5, 1), Position(6, 1)),
            Position((5, 2), Position(5, 1)), Position((5, 4), Position(5, 5)), Position((6, 0), Position(5, 0)), Position((6, 3), Position(6, 2)), Position((6, 3), Position(5, 3)), Position((6, 6), Position(5, 6))
        ]
        expected_grid = Grid([
            [2, 6, 5, 7, 4, 3, 1],
            [1, 3, 4, 2, 7, 6, 5],
            [5, 4, 1, 6, 3, 2, 7],
            [4, 7, 2, 3, 5, 1, 6],
            [7, 1, 6, 4, 2, 5, 3],
            [3, 5, 7, 1, 6, 4, 2],
            [6, 2, 3, 5, 1, 7, 4],
        ])
        game_solver = FutoshikiSolver(grid, higher_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_9x9(self):
        grid = Grid([
            [-1, 7, -1, -1, -1, 5, 3, 2, -1], [-1, -1, -1, -1, -1, -1, 7, -1, 2], [-1, -1, -1, -1, -1, -1, -1, -1, 5], [-1, -1, 3, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, 4, -1, -1, -1, -1], [-1, -1, -1, -1, -1, 8, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, 7, 2, -1, 5, 8]
        ])
        higher_positions = [
            (Position(0, 2), Position(0, 3)), Position((0, 3), Position(1, 3)), Position((0, 8), Position(1, 8)), Position((1, 0), Position(1, 1)), Position((1, 4), Position(0, 4)), Position((1, 7), Position(1, 6)), Position((2, 1), Position(2, 0)),
            Position((2, 2), Position(3, 2)), Position((2, 3), Position(2, 4)), Position((2, 5), Position(2, 4)), Position((2, 6), Position(3, 6)), Position((3, 1), Position(2, 1)), Position((3, 3), Position(3, 2)),
            (Position(3, 5), Position(3, 6)), Position((3, 6), Position(4, 6)), Position((3, 7), Position(3, 6)), Position((4, 2), Position(4, 1)), Position((4, 7), Position(3, 7)), Position((5, 0), Position(5, 1)), Position((5, 2), Position(4, 2)),
            Position((5, 5), Position(5, 4)), Position((5, 7), Position(5, 6)), Position((6, 7), Position(6, 8)), Position((7, 4), Position(7, 3)), Position((7, 4), Position(6, 4)), Position((7, 5), Position(7, 4)),
            (Position(7, 7), Position(8, 7)), Position((8, 3), Position(8, 4)), Position((8, 5), Position(8, 6))
        ]
        expected_grid = Grid([
            [1, 7, 9, 6, 8, 5, 3, 2, 4],
            [6, 3, 5, 4, 9, 1, 7, 8, 2],
            [2, 6, 8, 7, 3, 4, 9, 1, 5],
            [4, 8, 3, 5, 2, 9, 6, 7, 1],
            [7, 1, 2, 8, 4, 3, 5, 9, 6],
            [9, 5, 4, 1, 6, 8, 2, 3, 7],
            [5, 9, 7, 2, 1, 6, 8, 4, 3],
            [8, 2, 1, 3, 5, 7, 4, 6, 9],
            [3, 4, 6, 9, 7, 2, 1, 5, 8],
        ])
        game_solver = FutoshikiSolver(grid, higher_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_11x11(self):
        grid = Grid([
            [7, 4, 10, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 11], [-1, -1, 5, -1, -1, -1, 11, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, 7, -1, -1, -1],
            [-1, -1, -1, -1, 5, -1, -1, 9, -1, -1, 3], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, 3, -1, -1, -1, -1], [-1, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, 8, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 7]
        ])
        higher_positions = [
            (Position(0, 4), Position(1, 4)), Position((0, 5), Position(1, 5)), Position((0, 6), Position(0, 7)), Position((0, 7), Position(0, 8)), Position((0, 7), Position(1, 7)), Position((0, 9), Position(1, 9)), Position((1, 0), Position(1, 1)),
            Position((1, 3), Position(0, 3)), Position((1, 6), Position(0, 6)), Position((1, 7), Position(2, 7)), Position((1, 9), Position(2, 9)), Position((2, 0), Position(3, 0)), Position((2, 2), Position(2, 1)),
            (Position(2, 2), Position(1, 2)), Position((2, 4), Position(3, 4)), Position((2, 9), Position(2, 8)), Position((3, 3), Position(3, 2)), Position((3, 4), Position(3, 5)), Position((3, 5), Position(4, 5)), Position((3, 6), Position(3, 7)),
            Position((3, 9), Position(3, 10)), Position((4, 1), Position(5, 1)), Position((4, 2), Position(4, 1)), Position((4, 3), Position(3, 3)), Position((4, 3), Position(5, 3)), Position((4, 6), Position(5, 6)),
            (Position(5, 3), Position(5, 4)), Position((5, 4), Position(6, 4)), Position((5, 7), Position(5, 8)), Position((5, 8), Position(4, 8)), Position((5, 9), Position(5, 10)), Position((6, 0), Position(5, 0)), Position((6, 1), Position(7, 1)),
            Position((6, 3), Position(6, 2)), Position((6, 4), Position(6, 3)), Position((6, 6), Position(5, 6)), Position((6, 8), Position(6, 9)), Position((6, 9), Position(6, 10)), Position((6, 10), Position(5, 10)),
            (Position(7, 0), Position(6, 0)), Position((7, 1), Position(7, 0)), Position((7, 2), Position(8, 2)), Position((7, 6), Position(8, 6)), Position((7, 7), Position(7, 8)), Position((7, 7), Position(6, 7)), Position((7, 9), Position(7, 8)),
            Position((7, 10), Position(8, 10)), Position((8, 4), Position(9, 4)), Position((8, 6), Position(8, 5)), Position((8, 7), Position(7, 7)), Position((8, 9), Position(7, 9)), Position((8, 10), Position(8, 9)),
            (Position(9, 0), Position(8, 0)), Position((9, 1), Position(9, 0)), Position((9, 2), Position(10, 2)), Position((9, 3), Position(8, 3)), Position((9, 3), Position(10, 3)), Position((9, 4), Position(9, 3)), Position((9, 7), Position(10, 7)),
            Position((9, 9), Position(8, 9)), Position((9, 10), Position(10, 10)), Position((10, 0), Position(9, 0)), Position((10, 1), Position(10, 0))
        ]
        expected_grid = Grid([
            [7, 4, 10, 1, 8, 9, 6, 5, 3, 11, 2],
            [10, 1, 4, 8, 3, 5, 7, 2, 6, 9, 11],
            [9, 3, 5, 2, 10, 7, 11, 1, 4, 8, 6],
            [8, 10, 7, 9, 6, 4, 5, 3, 11, 2, 1],
            [11, 6, 8, 10, 2, 3, 9, 7, 5, 1, 4],
            [1, 2, 11, 7, 5, 10, 4, 9, 8, 6, 3],
            [2, 8, 1, 3, 4, 11, 10, 6, 9, 7, 5],
            [5, 7, 9, 11, 1, 6, 3, 8, 2, 4, 10],
            [3, 11, 6, 4, 9, 1, 2, 10, 7, 5, 8],
            [4, 5, 3, 6, 7, 2, 8, 11, 1, 10, 9],
            [6, 9, 2, 5, 11, 8, 1, 4, 10, 3, 7],
        ])
        game_solver = FutoshikiSolver(grid, higher_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    @unittest.skip("This grid is too slow or/and have no solution")
    def test_solution_13x13(self):
        grid = Grid([
            [-1, -1, 4, -1, -1, -1, -1, -1, 5, -1, -1, -1, -1, 2, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, 12, -1, -1, -1, -1, 1, -1, 14, -1, 8, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, 13, -1, -1, -1, -1, 7, -1, 4, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 8, -1, -1], [-1, -1, -1, -1, -1, -1, -1, 15, 3, -1, -1, -1, -1, -1, -1], [-1, -1, 12, -1, -1, -1, -1, -1, 6, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, 11, -1, -1, 10, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 9, -1, -1], [-1, 11, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 5],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 12, -1, -1, -1], [7, 13, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 8, -1], [-1, -1, -1, 11, 4, 3, 13, -1, -1, 9, 2, -1, -1, 10, 15]
        ])
        higher_positions = [
            (Position(0, 3), Position(0, 4)), Position((0, 8), Position(0, 7)), Position((0, 9), Position(0, 10)), Position((0, 10), Position(0, 11)), Position((1, 0), Position(1, 1)), Position((1, 1), Position(2, 1)), Position((1, 2), Position(1, 1)),
            Position((1, 3), Position(0, 3)), Position((1, 4), Position(2, 4)), Position((1, 5), Position(1, 4)), Position((1, 5), Position(0, 5)), Position((1, 7), Position(1, 8)), Position((1, 8), Position(0, 8)),
            (Position(1, 9), Position(1, 8)), Position((1, 10), Position(1, 11)), Position((1, 12), Position(1, 11)), Position((1, 13), Position(1, 14)), Position((1, 14), Position(2, 14)), Position((2, 0), Position(2, 1)), Position((2, 2), Position(2, 1)),
            Position((2, 3), Position(2, 4)), Position((2, 5), Position(2, 4)), Position((2, 8), Position(1, 8)), Position((2, 9), Position(1, 9)), Position((2, 9), Position(3, 9)),
            (Position(2, 10), Position(3, 10)), Position((2, 12), Position(2, 13)), Position((2, 13), Position(1, 13)), Position((2, 14), Position(3, 14)), Position((3, 3), Position(3, 2)), Position((3, 4), Position(3, 3)), Position((3, 4), Position(4, 4)),
            Position((3, 9), Position(4, 9)), Position((3, 11), Position(3, 12)), Position((3, 12), Position(4, 12)), Position((4, 0), Position(5, 0)), Position((4, 1), Position(3, 1)),
            (Position(4, 3), Position(4, 2)), Position((4, 4), Position(4, 3)), Position((4, 9), Position(4, 10)), Position((4, 11), Position(5, 11)), Position((4, 13), Position(4, 12)), Position((4, 14), Position(5, 14)), Position((5, 0), Position(5, 1)),
            Position((5, 2), Position(6, 2)), Position((5, 4), Position(5, 5)), Position((5, 5), Position(5, 6)), Position((5, 7), Position(4, 7)), Position((5, 8), Position(5, 7)), Position((5, 9), Position(6, 9)),
            (Position(5, 10), Position(6, 10)), Position((5, 11), Position(5, 12)), Position((5, 14), Position(5, 13)), Position((6, 1), Position(7, 1)), Position((6, 2), Position(6, 3)), Position((6, 3), Position(7, 3)), Position((6, 4), Position(6, 3)),
            Position((6, 6), Position(6, 5)), Position((6, 9), Position(6, 8)), Position((6, 10), Position(6, 9)), Position((6, 12), Position(6, 13)), Position((6, 13), Position(7, 13)),
            (Position(7, 1), Position(8, 1)), Position((7, 4), Position(8, 4)), Position((7, 5), Position(7, 4)), Position((7, 6), Position(7, 5)), Position((7, 11), Position(7, 12)), Position((8, 0), Position(7, 0)), Position((8, 2), Position(8, 1)),
            Position((8, 3), Position(8, 2)), Position((8, 4), Position(8, 3)), Position((8, 7), Position(7, 7)), Position((8, 8), Position(7, 8)), Position((8, 10), Position(7, 10)), Position((8, 11), Position(8, 12)),
            (Position(8, 12), Position(7, 12)), Position((8, 13), Position(7, 13)), Position((8, 14), Position(8, 13)), Position((9, 1), Position(9, 2)), Position((9, 1), Position(8, 1)), Position((9, 3), Position(8, 3)), Position((9, 6), Position(9, 5)),
            Position((9, 7), Position(10, 7)), Position((9, 8), Position(9, 7)), Position((9, 9), Position(9, 8)), Position((9, 10), Position(10, 10)), Position((9, 12), Position(8, 12)),
            (Position(9, 13), Position(9, 12)), Position((10, 1), Position(9, 1)), Position((10, 3), Position(9, 3)), Position((10, 5), Position(11, 5)), Position((10, 6), Position(9, 6)), Position((10, 8), Position(10, 7)), Position((10, 9), Position(11, 9)),
            Position((10, 10), Position(10, 9)), Position((10, 11), Position(10, 12)), Position((11, 0), Position(10, 0)), Position((11, 2), Position(11, 1)), Position((11, 6), Position(11, 5)),
            (Position(11, 11), Position(10, 11)), Position((11, 12), Position(12, 12)), Position((11, 13), Position(11, 12)), Position((11, 14), Position(11, 13)), Position((12, 0), Position(11, 0)), Position((12, 2), Position(12, 1)),
            Position((12, 4), Position(12, 3)), Position((12, 9), Position(12, 10)), Position((12, 10), Position(13, 10)), Position((12, 14), Position(13, 14)), Position((13, 0), Position(12, 0)),
            (Position(13, 3), Position(12, 3)), Position((13, 4), Position(13, 3)), Position((13, 5), Position(14, 5)), Position((13, 6), Position(13, 7)), Position((13, 7), Position(14, 7)), Position((13, 8), Position(13, 7)), Position((13, 10), Position(14, 10)),
            Position((13, 12), Position(13, 13)), Position((13, 13), Position(12, 13)), Position((13, 14), Position(13, 13)), Position((14, 2), Position(14, 3)),
            (Position(14, 3), Position(13, 3)), Position((14, 8), Position(14, 7)), Position((14, 9), Position(14, 8)), Position((14, 11), Position(14, 12))
        ]
        expected_grid = Grid([
            [0]
        ])
        game_solver = FutoshikiSolver(grid, higher_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    @unittest.skip("This grid is too slow or/and have no solution")
    def test_solution_13x13_2(self):
        grid = Grid([[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, 7, -1, -1, -1, -1, -1, -1, -1, 3, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                     [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, 3, -1, 11, -1, -1, -1, -1, 5, -1, -1, -1], [-1, -1, -1, -1, -1, -1, 5, -1, -1, -1, -1, -1, -1], [-1, 9, -1, -1, -1, -1, 3, -1, -1, -1, 5, -1, -1],
                     [-1, -1, -1, -1, -1, -1, -1, -1, 7, -1, -1, -1, -1], [-1, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, 6, -1, 12, -1, -1, -1, -1, 1, -1, -1], [-1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, 5],
                     [-1, 8, -1, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1]])
        higher_positions = [(Position(0, 1), Position(0, 0)), (Position(0, 2), Position(0, 3)), (Position(0, 4), Position(0, 3)), (Position(0, 6), Position(1, 6)), (Position(0, 7), Position(0, 6)), (Position(0, 8), Position(0, 7)), (Position(0, 10), Position(0, 11)),
                            (Position(0, 11), Position(0, 12)), (Position(1, 1), Position(1, 2)), (Position(1, 2), Position(0, 2)), (Position(1, 4), Position(0, 4)), (Position(1, 5), Position(2, 5)), (Position(1, 6), Position(1, 5)), (Position(1, 7), Position(1, 8)),
                            (Position(1, 8), Position(0, 8)), (Position(1, 9), Position(1, 10)), (Position(1, 11), Position(1, 10)), (Position(1, 12), Position(1, 11)), (Position(2, 0), Position(2, 1)), (Position(2, 2), Position(2, 3)), (Position(2, 3), Position(3, 3)),
                            (Position(2, 4), Position(3, 4)), (Position(2, 6), Position(2, 7)), (Position(2, 7), Position(3, 7)), (Position(2, 9), Position(3, 9)), (Position(2, 10), Position(1, 10)), (Position(2, 11), Position(2, 10)),
                            (Position(2, 11), Position(2, 12)),
                            (Position(2, 12), Position(3, 12)), (Position(3, 0), Position(2, 0)), (Position(3, 0), Position(4, 0)), (Position(3, 1), Position(4, 1)), (Position(3, 2), Position(2, 2)), (Position(3, 3), Position(4, 3)), (Position(3, 6), Position(3, 5)),
                            (Position(3, 6), Position(4, 6)), (Position(3, 9), Position(3, 8)), (Position(3, 10), Position(3, 11)), (Position(3, 11), Position(2, 11)), (Position(4, 0), Position(5, 0)), (Position(4, 2), Position(5, 2)), (Position(4, 4), Position(3, 4)),
                            (Position(4, 6), Position(4, 7)), (Position(4, 7), Position(3, 7)), (Position(4, 8), Position(5, 8)), (Position(4, 9), Position(4, 8)), (Position(4, 11), Position(3, 11)), (Position(5, 1), Position(5, 2)), (Position(5, 3), Position(6, 3)),
                            (Position(5, 4), Position(5, 3)), (Position(5, 4), Position(4, 4)), (Position(5, 6), Position(5, 7)), (Position(5, 8), Position(6, 8)), (Position(5, 10), Position(4, 10)), (Position(5, 12), Position(6, 12)), (Position(6, 0), Position(7, 0)),
                            (Position(6, 2), Position(6, 3)), (Position(6, 3), Position(6, 4)), (Position(6, 5), Position(7, 5)), (Position(6, 7), Position(6, 8)), (Position(6, 9), Position(7, 9)), (Position(6, 10), Position(5, 10)), (Position(6, 11), Position(5, 11)),
                            (Position(6, 12), Position(6, 11)), (Position(7, 2), Position(6, 2)), (Position(7, 6), Position(7, 7)), (Position(7, 6), Position(8, 6)), (Position(7, 9), Position(7, 10)), (Position(7, 11), Position(8, 11)),
                            (Position(7, 12), Position(6, 12)),
                            (Position(8, 2), Position(7, 2)), (Position(8, 2), Position(9, 2)), (Position(8, 4), Position(7, 4)), (Position(8, 6), Position(8, 5)), (Position(8, 7), Position(8, 8)), (Position(8, 9), Position(7, 9)), (Position(8, 12), Position(8, 11)),
                            (Position(9, 0), Position(8, 0)), (Position(9, 1), Position(9, 0)), (Position(9, 2), Position(10, 2)), (Position(9, 3), Position(9, 4)), (Position(9, 5), Position(9, 6)), (Position(9, 6), Position(9, 7)), (Position(9, 8), Position(9, 7)),
                            (Position(9, 9), Position(9, 8)), (Position(9, 10), Position(9, 9)), (Position(9, 11), Position(9, 10)), (Position(9, 12), Position(9, 11)), (Position(10, 1), Position(10, 0)), (Position(10, 3), Position(9, 3)),
                            (Position(10, 4), Position(10, 5)), (Position(10, 5), Position(9, 5)), (Position(10, 7), Position(10, 6)), (Position(10, 9), Position(10, 8)), (Position(10, 9), Position(11, 9)), (Position(11, 1), Position(11, 0)),
                            (Position(11, 2), Position(10, 2)), (Position(11, 3), Position(11, 2)), (Position(11, 9), Position(11, 8)), (Position(11, 9), Position(12, 9)), (Position(11, 12), Position(10, 12)), (Position(12, 1), Position(12, 0)),
                            (Position(12, 5), Position(11, 5)), (Position(12, 6), Position(12, 7)), (Position(12, 7), Position(11, 7)), (Position(12, 9), Position(12, 8)), (Position(12, 9), Position(12, 10))]
        expected_grid = Grid([
            [3, 6, 5, 4, 9, 13, 7, 8, 10, 1, 12, 11, 2],
            [2, 12, 7, 1, 10, 5, 6, 13, 11, 9, 3, 4, 8],
            [9, 1, 12, 11, 5, 4, 13, 10, 2, 3, 7, 8, 6],
            [12, 5, 13, 7, 3, 8, 11, 6, 1, 2, 10, 9, 4],
            [11, 2, 6, 5, 8, 3, 9, 7, 12, 13, 4, 10, 1],
            [7, 13, 3, 9, 11, 2, 10, 4, 8, 5, 6, 1, 12],
            [13, 3, 8, 2, 1, 10, 5, 12, 4, 11, 9, 6, 7],
            [1, 9, 10, 12, 4, 6, 3, 2, 13, 8, 5, 7, 11],
            [5, 4, 11, 13, 6, 1, 2, 9, 7, 12, 8, 3, 10],
            [8, 10, 9, 3, 2, 7, 4, 1, 5, 6, 11, 12, 13],
            [4, 7, 2, 6, 13, 12, 8, 11, 9, 10, 1, 5, 3],
            [10, 11, 4, 8, 12, 9, 1, 3, 6, 7, 13, 2, 5],
            [6, 8, 1, 10, 7, 11, 12, 5, 3, 4, 2, 13, 9],
        ])
        game_solver = FutoshikiSolver(grid, higher_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
