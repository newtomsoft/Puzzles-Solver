import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.Renzoku.RenzokuSolver import RenzokuSolver


class RenzokuSolverTests(TestCase):
    def test_grid_must_be_square_raises_value_error(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1],
        ])
        consecutive_positions = [(Position(0, 0), Position(0, 1))]
        with self.assertRaises(ValueError) as context:
            RenzokuSolver(grid, consecutive_positions)
        self.assertEqual(str(context.exception), "The grid must be square")

    def test_solution_grid_too_small(self):
        grid = Grid([
            [-1, -1, -1],
            [-1, -1, 0],
            [1, -1, -1],
        ])
        consecutive_positions = [(Position(0, 0), Position(0, 1))]
        with self.assertRaises(ValueError) as context:
            RenzokuSolver(grid, consecutive_positions)
        self.assertEqual("The grid must be at least 4x4", str(context.exception))

    def test_solution_4x4(self):
        grid = Grid([
            [-1, -1, -1, -1],
            [-1, -1, -1, -1],
            [+4, -1, -1, -1],
            [-1, -1, -1, -1],
        ])
        consecutive_positions = [(Position(0, 0), Position(0, 1)), (Position(0, 0), Position(1, 0)), (Position(0, 1), Position(1, 1)), (Position(0, 2), Position(1, 2)), (Position(0, 3), Position(1, 3)), (Position(1, 2), Position(1, 3)), (Position(1, 2), Position(2, 2)),
                                 (Position(2, 1), Position(2, 2)), (Position(2, 0), Position(3, 0)), (Position(2, 1), Position(3, 1)), (Position(2, 2), Position(3, 2)), (Position(2, 3), Position(3, 3))]
        expected_grid = Grid([
            [2, 3, 1, 4],
            [1, 4, 2, 3],
            [4, 2, 3, 1],
            [3, 1, 4, 2],
        ])
        game_solver = RenzokuSolver(grid, consecutive_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5(self):
        grid = Grid([
            [-1, -1, -1, -1, -1],
            [-1, -1, 3, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, 5, -1, -1, -1],
        ])
        consecutive_positions = [
            (Position(0, 0), Position(0, 1)), (Position(0, 0), Position(1, 0)), (Position(0, 1), Position(1, 1)), (Position(0, 2), Position(0, 3)), (Position(0, 3), Position(1, 3)), (Position(0, 4), Position(1, 4)), (Position(1, 0), Position(2, 0)),
            (Position(1, 4), Position(2, 4)), (Position(2, 0), Position(2, 1)), (Position(2, 1), Position(3, 1)), (Position(2, 2), Position(2, 3)), (Position(2, 3), Position(2, 4)), (Position(2, 3), Position(3, 3)), (Position(3, 0), Position(3, 1)),
            (Position(3, 0), Position(4, 0)), (Position(3, 1), Position(3, 2)), (Position(3, 4), Position(4, 4)), (Position(4, 2), Position(4, 3)), (Position(4, 3), Position(4, 4))
        ]
        expected_grid = Grid([
            [3, 2, 5, 4, 1],
            [4, 1, 3, 5, 2],
            [5, 4, 1, 2, 3],
            [2, 3, 4, 1, 5],
            [1, 5, 2, 3, 4],
        ])
        game_solver = RenzokuSolver(grid, consecutive_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_7x7(self):
        grid = Grid([[-1, -1, -1, -1, -1, -1, -1], [1, -1, -1, -1, -1, 3, -1], [-1, -1, -1, -1, -1, 1, -1], [-1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, 4, -1], [-1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1]])
        consecutive_positions = [
            (Position(0, 3), Position(1, 3)), (Position(0, 4), Position(0, 5)), (Position(0, 4), Position(1, 4)), (Position(1, 1), Position(2, 1)), (Position(2, 0), Position(2, 1)), (Position(2, 2), Position(3, 2)), (Position(3, 0), Position(4, 0)),
            (Position(3, 1), Position(3, 2)), (Position(3, 3), Position(4, 3)), (Position(3, 5), Position(3, 6)), (Position(4, 2), Position(4, 3)), (Position(4, 3), Position(4, 4)), (Position(4, 6), Position(5, 6)), (Position(5, 0), Position(5, 1)),
            (Position(5, 0), Position(6, 0))
        ]
        expected_grid = Grid([[4, 2, 7, 3, 6, 5, 1], [1, 7, 4, 2, 5, 3, 6], [5, 6, 2, 7, 3, 1, 4], [2, 4, 3, 5, 1, 6, 7], [3, 1, 5, 6, 7, 4, 2], [6, 5, 1, 4, 2, 7, 3], [7, 3, 6, 1, 4, 2, 5]])
        game_solver = RenzokuSolver(grid, consecutive_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_9x9(self):
        grid = Grid([
            [9, -1, 7, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, 2, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, 6, -1, -1, 7, -1, -1, -1]
        ])
        consecutive_positions = [
            (Position(0, 0), Position(1, 0)), (Position(0, 1), Position(1, 1)), (Position(0, 3), Position(1, 3)), (Position(0, 4), Position(1, 4)), (Position(0, 6), Position(1, 6)), (Position(0, 7), Position(1, 7)), (Position(1, 2), Position(1, 3)),
            (Position(1, 5), Position(1, 6)), (Position(1, 7), Position(1, 8)), (Position(1, 8), Position(2, 8)), (Position(2, 0), Position(2, 1)), (Position(2, 0), Position(3, 0)), (Position(2, 1), Position(3, 1)), (Position(2, 3), Position(2, 4)),
            (Position(2, 6), Position(2, 7)), (Position(2, 6), Position(3, 6)), (Position(2, 8), Position(3, 8)), (Position(3, 0), Position(3, 1)), (Position(3, 2), Position(4, 2)), (Position(3, 5), Position(3, 6)), (Position(3, 5), Position(4, 5)),
            (Position(3, 7), Position(4, 7)), (Position(4, 0), Position(5, 0)), (Position(4, 1), Position(5, 1)), (Position(4, 3), Position(4, 4)), (Position(4, 3), Position(5, 3)), (Position(5, 0), Position(6, 0)), (Position(5, 1), Position(6, 1)),
            (Position(5, 2), Position(5, 3)), (Position(5, 5), Position(6, 5)), (Position(6, 0), Position(6, 1)), (Position(6, 1), Position(6, 2)), (Position(6, 7), Position(6, 8)), (Position(6, 7), Position(7, 7)), (Position(7, 0), Position(8, 0)),
            (Position(7, 4), Position(8, 4)), (Position(7, 6), Position(7, 7)), (Position(7, 6), Position(8, 6)), (Position(7, 7), Position(8, 7)), (Position(8, 0), Position(8, 1)), (Position(8, 5), Position(8, 6)), (Position(8, 6), Position(8, 7))
        ]
        expected_grid = Grid([
            [9, 2, 7, 4, 8, 6, 3, 5, 1], [8, 1, 4, 5, 9, 3, 2, 6, 7], [6, 7, 9, 2, 3, 1, 5, 4, 8], [7, 8, 3, 6, 1, 5, 4, 2, 9], [1, 6, 2, 8, 7, 4, 9, 3, 5], [2, 5, 8, 7, 4, 9, 6, 1, 3], [3, 4, 5, 9, 2, 8, 1, 7, 6], [5, 9, 1, 3, 6, 2, 7, 8, 4],
            [4, 3, 6, 1, 5, 7, 8, 9, 2]
        ])
        game_solver = RenzokuSolver(grid, consecutive_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_11x11(self):
        grid = Grid([[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1], [7, -1, -1, -1, -1, -1, -1, -1, -1, -1, 8], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 10], [-1, -1, -1, 5, 10, -1, 6, -1, -1, 9, 3],
                     [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, 6], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1], [10, -1, -1, -1, -1, -1, -1, 9, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1],
                     [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]])
        consecutive_positions = [
            (Position(0, 4), Position(0, 5)), (Position(0, 7), Position(1, 7)), (Position(1, 2), Position(1, 3)), (Position(1, 9), Position(1, 10)), (Position(2, 1), Position(3, 1)), (Position(2, 5), Position(3, 5)),
            (Position(2, 6), Position(2, 7)), (Position(2, 9), Position(3, 9)), (Position(3, 0), Position(4, 0)), (Position(3, 7), Position(3, 8)), (Position(4, 0), Position(4, 1)), (Position(4, 1), Position(5, 1)), (Position(4, 4), Position(4, 5)),
            (Position(4, 6), Position(5, 6)), (Position(5, 3), Position(5, 4)), (Position(5, 7), Position(5, 8)), (Position(5, 8), Position(6, 8)), (Position(6, 2), Position(6, 3)), (Position(6, 4), Position(7, 4)), (Position(6, 7), Position(7, 7)),
            (Position(6, 10), Position(7, 10)), (Position(7, 1), Position(7, 2)), (Position(7, 2), Position(7, 3)), (Position(7, 7), Position(7, 8)), (Position(7, 9), Position(8, 9)), (Position(8, 0), Position(8, 1)),
            (Position(8, 0), Position(9, 0)), (Position(8, 3), Position(8, 4)), (Position(8, 4), Position(9, 4)), (Position(8, 5), Position(8, 6)), (Position(8, 9), Position(8, 10)), (Position(9, 2), Position(9, 3)),
            (Position(9, 5), Position(9, 6)), (Position(9, 6), Position(10, 6)), (Position(9, 7), Position(9, 8)), (Position(9, 7), Position(10, 7)), (Position(9, 9), Position(10, 9)), (Position(10, 0), Position(10, 1)),
            (Position(10, 4), Position(10, 5)), (Position(10, 8), Position(10, 9))
        ]
        expected_grid = Grid([
            [3, 10, 1, 4, 8, 7, 9, 5, 11, 6, 2], [1, 5, 7, 8, 3, 9, 2, 4, 6, 10, 11], [7, 1, 4, 6, 9, 2, 10, 11, 3, 5, 8], [9, 2, 11, 1, 5, 3, 8, 6, 7, 4, 10], [8, 7, 2, 5, 10, 11, 6, 1, 4, 9, 3], [2, 8, 5, 3, 4, 1, 7, 10, 9, 11, 6], [6, 3, 8, 9, 7, 5, 11, 2, 10, 1, 4],
            [4, 9, 10, 11, 6, 8, 1, 3, 2, 7, 5], [10, 11, 6, 2, 1, 4, 3, 9, 5, 8, 7], [11, 4, 9, 10, 2, 6, 5, 7, 8, 3, 1], [5, 6, 3, 7, 11, 10, 4, 8, 1, 2, 9]
        ])
        game_solver = RenzokuSolver(grid, consecutive_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_13x13(self):
        grid = Grid([
            [3, -1, -1, -1, -1, -1, 13, -1, -1, -1, 11, -1, 6], [-1, -1, -1, -1, -1, -1, -1, -1, 10, 1, -1, 9, -1], [-1, -1, -1, -1, -1, -1, 6, -1, 2, -1, 5, 3, -1], [-1, -1, -1, -1, 6, -1, -1, -1, 8, 2, -1, 13, -1], [-1, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1, 3],
            [-1, -1, -1, -1, 4, -1, -1, -1, -1, -1, -1, -1, 13], [-1, -1, -1, -1, -1, -1, 9, -1, -1, -1, 12, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, 9, 7, -1, 12], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, 5, -1, 4, 6, -1, -1, 11], [-1, -1, -1, -1, -1, -1, 1, -1, 13, -1, -1, -1, -1]
        ])
        consecutive_positions = [
            (Position(0, 6), Position(1, 6)), (Position(0, 7), Position(0, 8)), (Position(1, 0), Position(2, 0)), (Position(1, 1), Position(1, 2)), (Position(1, 2), Position(2, 2)), (Position(1, 3), Position(1, 4)), (Position(1, 4), Position(2, 4)),
            (Position(1, 5), Position(1, 6)), (Position(1, 5), Position(2, 5)), (Position(2, 6), Position(3, 6)), (Position(2, 12), Position(3, 12)), (Position(3, 0), Position(4, 0)), (Position(3, 11), Position(4, 11)), (Position(4, 2), Position(5, 2)),
            (Position(4, 3), Position(5, 3)), (Position(4, 6), Position(4, 7)), (Position(4, 6), Position(5, 6)), (Position(4, 7), Position(4, 8)), (Position(4, 8), Position(4, 9)), (Position(5, 1), Position(5, 2)), (Position(5, 8), Position(6, 8)),
            (Position(5, 9), Position(5, 10)), (Position(6, 1), Position(6, 2)), (Position(6, 1), Position(7, 1)), (Position(6, 6), Position(6, 7)), (Position(7, 3), Position(7, 4)), (Position(7, 4), Position(7, 5)), (Position(7, 7), Position(8, 7)),
            (Position(7, 11), Position(7, 12)), (Position(8, 4), Position(9, 4)), (Position(8, 8), Position(8, 9)), (Position(8, 11), Position(8, 12)), (Position(8, 11), Position(9, 11)), (Position(9, 0), Position(9, 1)), (Position(9, 1), Position(10, 1)),
            (Position(9, 2), Position(10, 2)), (Position(9, 3), Position(10, 3)), (Position(9, 4), Position(10, 4)), (Position(9, 5), Position(9, 6)), (Position(9, 9), Position(10, 9)), (Position(9, 10), Position(10, 10)), (Position(10, 1), Position(11, 1)),
            (Position(10, 3), Position(11, 3)), (Position(10, 11), Position(10, 12)), (Position(11, 0), Position(12, 0)), (Position(12, 9), Position(12, 10))
        ]
        expected_grid = Grid([
            [3, 10, 12, 9, 7, 5, 13, 2, 1, 8, 11, 4, 6], [8, 6, 5, 3, 2, 11, 12, 7, 10, 1, 13, 9, 4], [7, 13, 4, 8, 1, 12, 6, 11, 2, 10, 5, 3, 9], [12, 5, 1, 11, 6, 4, 7, 3, 8, 2, 9, 13, 10], [13, 11, 9, 1, 8, 10, 4, 5, 6, 7, 2, 12, 3],
            [11, 9, 8, 2, 4, 7, 3, 1, 12, 5, 6, 10, 13], [4, 7, 6, 10, 13, 2, 9, 8, 11, 3, 12, 1, 5], [1, 8, 13, 4, 5, 6, 2, 10, 3, 9, 7, 11, 12], [6, 12, 2, 13, 10, 3, 11, 9, 5, 4, 1, 7, 8], [2, 3, 10, 5, 11, 9, 8, 13, 7, 12, 4, 6, 1],
            [5, 2, 11, 6, 12, 1, 10, 4, 9, 13, 3, 8, 7], [10, 1, 3, 7, 9, 13, 5, 12, 4, 6, 8, 2, 11], [9, 4, 7, 12, 3, 8, 1, 6, 13, 11, 10, 5, 2]
        ])
        game_solver = RenzokuSolver(grid, consecutive_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_15x15(self):
        grid = Grid([
            [-1, -1, -1, -1, 10, -1, -1, 2, -1, 1, -1, 6, -1, 15, -1], [-1, -1, 13, -1, -1, -1, -1, -1, -1, -1, -1, -1, 11, -1, 7], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3, -1, -1, -1, -1], [-1, -1, -1, -1, 12, -1, 1, 7, -1, 2, -1, 8, 13, -1, 3],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, 14, -1, -1, -1, -1, 4], [-1, -1, -1, -1, 3, 6, 14, -1, -1, 4, 12, -1, -1, 7, 11], [-1, -1, -1, -1, 8, -1, -1, 3, -1, -1, 2, -1, -1, -1, -1],
            [-1, -1, 11, -1, 1, -1, -1, -1, -1, -1, -1, 15, 6, 14, 9], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, 5, -1, -1, -1, -1, -1, 6, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, 13, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        ])
        consecutive_positions = [
            (Position(0, 0), Position(1, 0)), (Position(0, 2), Position(0, 3)), (Position(0, 4), Position(0, 5)), (Position(0, 4), Position(1, 4)), (Position(0, 5), Position(1, 5)), (Position(0, 7), Position(0, 8)), (Position(1, 2), Position(2, 2)),
            (Position(1, 5), Position(2, 5)), (Position(1, 8), Position(1, 9)), (Position(1, 9), Position(2, 9)), (Position(1, 11), Position(2, 11)), (Position(2, 4), Position(3, 4)), (Position(2, 5), Position(2, 6)), (Position(2, 14), Position(3, 14)),
            (Position(3, 2), Position(4, 2)), (Position(3, 3), Position(4, 3)), (Position(3, 5), Position(4, 5)), (Position(3, 11), Position(4, 11)), (Position(3, 12), Position(4, 12)), (Position(4, 0), Position(4, 1)), (Position(4, 1), Position(4, 2)),
            (Position(4, 4), Position(4, 5)), (Position(4, 7), Position(4, 8)), (Position(5, 0), Position(5, 1)), (Position(5, 2), Position(6, 2)), (Position(5, 3), Position(5, 4)), (Position(5, 10), Position(5, 11)), (Position(5, 10), Position(6, 10)),
            (Position(5, 12), Position(5, 13)), (Position(5, 12), Position(6, 12)), (Position(6, 1), Position(6, 2)), (Position(6, 2), Position(7, 2)), (Position(6, 6), Position(7, 6)), (Position(6, 9), Position(7, 9)), (Position(6, 10), Position(6, 11)),
            (Position(7, 1), Position(7, 2)), (Position(7, 3), Position(8, 3)), (Position(7, 5), Position(8, 5)), (Position(7, 10), Position(7, 11)), (Position(7, 12), Position(7, 13)), (Position(8, 0), Position(8, 1)), (Position(8, 6), Position(8, 7)),
            (Position(8, 10), Position(9, 10)), (Position(8, 11), Position(9, 11)), (Position(9, 1), Position(9, 2)), (Position(9, 1), Position(10, 1)), (Position(9, 8), Position(9, 9)), (Position(9, 9), Position(9, 10)), (Position(10, 0), Position(10, 1)),
            (Position(10, 4), Position(10, 5)), (Position(10, 5), Position(11, 5)), (Position(10, 6), Position(10, 7)), (Position(10, 8), Position(11, 8)), (Position(10, 9), Position(11, 9)), (Position(10, 12), Position(10, 13)), (Position(10, 12), Position(11, 12)),
            (Position(11, 2), Position(12, 2)), (Position(11, 6), Position(12, 6)), (Position(11, 13), Position(12, 13)), (Position(11, 14), Position(12, 14)), (Position(12, 2), Position(12, 3)), (Position(12, 4), Position(12, 5)), (Position(12, 5), Position(13, 5)),
            (Position(12, 11), Position(13, 11)), (Position(14, 10), Position(14, 11)), (Position(14, 11), Position(14, 12))
        ]
        expected_grid = Grid([
            [7, 14, 5, 4, 10, 11, 13, 2, 3, 1, 8, 6, 9, 15, 12], [8, 1, 13, 2, 9, 12, 10, 14, 5, 6, 15, 4, 11, 3, 7], [10, 8, 14, 9, 11, 13, 12, 4, 1, 7, 3, 5, 15, 6, 2], [14, 11, 4, 6, 12, 15, 1, 7, 9, 2, 5, 8, 13, 10, 3],
            [1, 2, 3, 5, 15, 14, 8, 10, 11, 9, 13, 7, 12, 4, 6], [13, 12, 9, 7, 6, 3, 5, 15, 8, 14, 11, 10, 1, 2, 4], [5, 9, 8, 10, 3, 6, 14, 1, 15, 4, 12, 13, 2, 7, 11], [11, 6, 7, 14, 8, 4, 15, 3, 12, 5, 2, 1, 10, 9, 13],
            [4, 3, 11, 13, 1, 5, 7, 8, 2, 12, 10, 15, 6, 14, 9], [15, 5, 6, 3, 13, 10, 2, 12, 7, 8, 9, 14, 4, 11, 1], [3, 4, 12, 15, 2, 1, 6, 5, 13, 11, 14, 9, 7, 8, 10], [12, 7, 1, 11, 5, 2, 4, 9, 14, 10, 6, 3, 8, 13, 15],
            [9, 15, 2, 1, 7, 8, 3, 6, 10, 13, 4, 11, 5, 12, 14], [2, 10, 15, 8, 4, 9, 11, 13, 6, 3, 7, 12, 14, 1, 5], [6, 13, 10, 12, 14, 7, 9, 11, 4, 15, 1, 2, 3, 5, 8]
        ])
        game_solver = RenzokuSolver(grid, consecutive_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
