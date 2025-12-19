from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Hidoku.HidokuSolver import HidokuSolver

_ = HidokuSolver.empty


class HidokuSolverTest(TestCase):
    def test_solution_3x3_full(self):
        grid = Grid(
            [
                [1, 2, 3],
                [8, 9, 4],
                [7, 6, 5],
            ]
        )
        expected_grid = Grid(
            [
                [1, 2, 3],
                [8, 9, 4],
                [7, 6, 5],
            ]
        )
        game_solver = HidokuSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_3x3_easy(self):
        grid = Grid(
            [
                [1, _, 3],
                [_, 9, _],
                [7, _, 5],
            ]
        )
        expected_grid = Grid(
            [
                [1, 2, 3],
                [8, 9, 4],
                [7, 6, 5],
            ]
        )
        game_solver = HidokuSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_easy(self):
        grid = Grid(
            [
                [10, _, _, _, 25],
                [20, _, _, _, _],
                [_, _, _, _, 6],
                [_, 15, _, 1, _],
                [16, _, _, 2, _],
            ]
        )
        expected_grid = Grid(
            [
                [10, 9, 8, 23, 25],
                [20, 11, 22, 7, 24],
                [19, 21, 12, 5, 6],
                [18, 15, 13, 1, 4],
                [16, 17, 14, 2, 3],
            ]
        )
        game_solver = HidokuSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_medium(self):
        grid = Grid(
            [
                [23, _, _, 20, _, 16],
                [_, 26, _, 14, 19, _],
                [_, 9, _, 12, _, 1],
                [_, 28, _, _, 4, _],
                [_, _, _, _, _, 36],
                [_, _, 32, _, _, _],
            ]
        )
        expected_grid = Grid(
            [
                [23, 22, 21, 20, 15, 16],
                [24, 26, 13, 14, 19, 17],
                [25, 9, 27, 12, 18, 1],
                [8, 28, 10, 11, 4, 2],
                [29, 7, 6, 5, 3, 36],
                [30, 31, 32, 33, 34, 35],
            ]
        )
        game_solver = HidokuSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_7x7_hard(self):
        grid = Grid(
            [
                [37, _, 31, _, _, _, _],
                [_, _, _, 28, 27, 24, _],
                [33, _, _, _, _, _, _],
                [_, _, 10, _, _, 18, 21],
                [_, 7, _, _, _, _, 19],
                [6, _, _, _, _, 49, _],
                [_, _, 1, 14, _, _, 48],
            ]
        )
        expected_grid = Grid(
            [
                [37, 38, 31, 30, 29, 26, 25],
                [36, 32, 39, 28, 27, 24, 23],
                [33, 35, 9, 40, 41, 42, 22],
                [34, 8, 10, 11, 43, 18, 21],
                [5, 7, 12, 44, 17, 20, 19],
                [6, 4, 13, 16, 45, 49, 47],
                [3, 2, 1, 14, 15, 46, 48],
            ]
        )
        game_solver = HidokuSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_extreme(self):
        grid = Grid(
            [
                [_, _, _, _, 17, _, _, _],
                [_, 49, 56, _, _, 20, 19, _],
                [_, 48, 13, _, _, _, _, _],
                [47, _, _, _, _, _, 27, _],
                [46, _, 59, _, _, 8, _, _],
                [61, _, _, _, 9, _, 6, _],
                [_, 41, _, _, 1, 35, _, _],
                [64, _, _, 38, _, _, 32, _],
            ]
        )
        expected_grid = Grid(
            [
                [52, 53, 54, 55, 17, 18, 21, 22],
                [51, 49, 56, 14, 16, 20, 19, 23],
                [50, 48, 13, 57, 15, 26, 25, 24],
                [47, 45, 58, 12, 11, 4, 27, 28],
                [46, 44, 59, 10, 3, 8, 5, 29],
                [61, 60, 43, 2, 9, 7, 6, 30],
                [62, 41, 42, 39, 1, 35, 34, 31],
                [64, 63, 40, 38, 37, 36, 32, 33],
            ]
        )
        game_solver = HidokuSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
