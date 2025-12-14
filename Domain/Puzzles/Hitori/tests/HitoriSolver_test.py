import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Hitori.HitoriSolver import HitoriSolver

_ = False


class HitoriSolverTests(TestCase):


    def test_solution_not_exist_2_black_adjacent(self):
        grid = Grid([
            [1, 1, 1],
            [2, 2, 2],
            [3, 4, 5]
        ])
        game_solver = HitoriSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_not_exist_corner_isolated(self):
        grid = Grid([
            [1, 2, 4, 5],
            [3, 6, 3, 3],
            [7, 2, 8, 9],
            [4, 2, 3, 6]
        ])
        game_solver = HitoriSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_unique_numbers(self):
        grid = Grid([
            [1, 2, 3],
            [2, 3, 1],
            [3, 1, 2]
        ])
        expected_solution = Grid(grid.matrix.copy())
        game_solver = HitoriSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_simple_duplicate_numbers(self):
        grid = Grid([
            [1, 2, 3],
            [3, 2, 2],
            [2, 3, 1]
        ])
        expected_solution = Grid([
            [1, 2, 3],
            [3, _, 2],
            [2, 3, 1]
        ])
        game_solver = HitoriSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_5x5(self):
        grid = Grid([
            [1, 1, 3, 3, 5],
            [4, 3, 5, 2, 1],
            [2, 3, 4, 1, 5],
            [2, 1, 4, 4, 3],
            [5, 2, 1, 3, 2]
        ])
        expected_solution = Grid([
            [1, _, 3, _, 5],
            [4, 3, 5, 2, 1],
            [2, _, 4, 1, _],
            [_, 1, _, 4, 3],
            [5, 2, 1, 3, _]
        ])
        game_solver = HitoriSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12(self):  # approx 1.5s
        grid = Grid([
            [6, 6, 5, 6, 11, 5, 3, 9, 6, 8, 3, 4],
            [7, 1, 8, 5, 10, 3, 11, 10, 2, 4, 6, 12],
            [6, 11, 5, 9, 2, 9, 6, 7, 2, 3, 9, 10],
            [10, 6, 2, 7, 10, 4, 3, 8, 12, 2, 9, 1],
            [8, 9, 9, 4, 1, 2, 7, 12, 11, 5, 8, 6],
            [5, 11, 10, 2, 11, 12, 9, 12, 8, 9, 1, 7],
            [8, 12, 11, 12, 3, 12, 10, 6, 1, 2, 12, 8],
            [11, 8, 4, 10, 6, 1, 9, 5, 7, 10, 3, 2],
            [10, 2, 2, 11, 8, 11, 4, 8, 10, 12, 4, 9],
            [3, 9, 1, 9, 5, 8, 12, 2, 5, 10, 4, 11],
            [9, 4, 6, 8, 10, 7, 2, 3, 5, 5, 10, 6],
            [12, 11, 3, 1, 7, 10, 3, 11, 2, 9, 2, 5]
        ])
        expected_solution = Grid([
            [6, _, 5, _, 11, _, 3, 9, _, 8, _, 4],
            [7, 1, 8, 5, 10, 3, 11, _, 2, 4, 6, 12],
            [_, 11, _, 9, 2, _, 6, 7, _, 3, _, 10],
            [10, 6, 2, 7, _, 4, _, 8, 12, _, 9, 1],
            [8, 9, _, 4, 1, 2, 7, 12, 11, 5, _, 6],
            [5, _, 10, 2, _, 12, 9, _, 8, _, 1, 7],
            [_, 12, 11, _, 3, _, 10, 6, 1, 2, _, 8],
            [11, 8, 4, 10, 6, 1, _, 5, 7, _, 3, 2],
            [_, 2, _, 11, 8, _, 4, _, 10, 12, _, 9],
            [3, _, 1, _, 5, 8, 12, 2, _, 10, 4, 11],
            [9, 4, 6, 8, _, 7, 2, 3, 5, _, 10, _],
            [12, _, 3, 1, 7, 10, _, 11, _, 9, 2, 5]
        ])
        game_solver = HitoriSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_15x15(self):  # approx 3s
        grid = Grid([
            [2, 11, 10, 11, 15, 11, 13, 3, 12, 14, 4, 11, 3, 1, 11],
            [8, 6, 8, 5, 8, 11, 10, 14, 8, 13, 12, 9, 1, 8, 2],
            [6, 13, 7, 4, 1, 13, 15, 4, 2, 11, 11, 10, 12, 9, 4],
            [5, 14, 13, 12, 5, 1, 9, 7, 9, 2, 10, 3, 9, 6, 9],
            [11, 4, 5, 14, 12, 4, 14, 2, 13, 7, 9, 7, 15, 7, 10],
            [5, 3, 5, 7, 5, 13, 4, 5, 1, 9, 5, 12, 6, 11, 5],
            [9, 10, 2, 10, 6, 10, 3, 13, 10, 12, 15, 10, 14, 10, 8],
            [14, 12, 1, 3, 5, 15, 7, 6, 8, 5, 1, 4, 11, 13, 11],
            [7, 1, 15, 6, 9, 7, 14, 7, 5, 7, 2, 7, 13, 6, 3],
            [15, 4, 12, 1, 4, 9, 6, 11, 7, 8, 4, 13, 4, 2, 7],
            [12, 2, 14, 4, 13, 2, 8, 4, 15, 4, 11, 7, 2, 3, 1],
            [11, 7, 2, 15, 11, 12, 2, 3, 11, 1, 6, 11, 10, 2, 5],
            [1, 11, 6, 15, 10, 8, 5, 15, 3, 15, 15, 2, 11, 14, 15],
            [4, 9, 11, 2, 14, 4, 12, 1, 11, 5, 8, 15, 9, 10, 13],
            [5, 15, 11, 4, 5, 2, 11, 5, 14, 6, 13, 11, 9, 5, 11]
        ])
        expected_solution = Grid([
            [2, 11, 10, _, 15, _, 13, _, 12, 14, 4, _, 3, 1, _],
            [_, 6, _, 5, 8, 11, 10, 14, _, 13, 12, 9, 1, _, 2],
            [6, 13, 7, _, 1, _, 15, _, 2, 11, _, 10, 12, 9, 4],
            [5, 14, 13, 12, _, 1, 9, 7, _, 2, 10, 3, _, 6, _],
            [11, _, 5, 14, 12, 4, _, 2, 13, _, 9, _, 15, 7, 10],
            [_, 3, _, 7, _, 13, 4, _, 1, 9, 5, 12, 6, 11, _],
            [9, 10, 2, _, 6, _, 3, 13, _, 12, 15, _, 14, _, 8],
            [14, 12, _, 3, 5, 15, 7, 6, 8, _, 1, 4, _, 13, 11],
            [_, 1, 15, 6, 9, _, 14, _, 5, 7, 2, _, 13, _, 3],
            [15, _, 12, 1, _, 9, 6, 11, _, 8, _, 13, 4, 2, 7],
            [12, 2, 14, _, 13, _, 8, _, 15, 4, 11, 7, _, 3, 1],
            [_, 7, _, 15, 11, 12, 2, 3, _, 1, 6, _, 10, _, 5],
            [1, _, 6, _, 10, 8, 5, _, 3, 15, _, 2, 11, 14, _],
            [4, 9, 11, 2, 14, _, 12, 1, _, 5, 8, 15, _, 10, 13],
            [_, 15, _, 4, _, 2, 11, _, 14, 6, 13, _, 9, 5, _]
        ])
        game_solver = HitoriSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
if __name__ == '__main__':
    unittest.main()
