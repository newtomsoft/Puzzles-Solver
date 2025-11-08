import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Tasukuea.TasukueaSolver import TasukueaSolver

_ = TasukueaSolver.empty
T = True
F = False
U = TasukueaSolver.unknown


class TasukueaSolverTests(TestCase):
    def test_solution_basic_3x3(self):
        grid = Grid([
            [1, _, _],
            [_, _, _],
            [_, _, _],
            [_, _, 4],
        ])
        expected_solution = Grid([
            [F, T, F],
            [F, F, F],
            [T, T, F],
            [T, T, F],
        ])

        game_solver = TasukueaSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_basic_4x4(self):
        grid = Grid([
            [_, _, _, 4],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        expected_solution1 = Grid([
            [F, T, T, F],
            [F, T, T, F],
            [F, F, F, F],
            [F, F, F, F],
        ])
        expected_solution2 = Grid([
            [F, F, F, F],
            [F, F, T, T],
            [F, F, T, T],
            [F, F, F, F],
        ])
        expected_solutions = {expected_solution1, expected_solution2}

        game_solver = TasukueaSolver(grid)
        solution1 = game_solver.get_solution()
        solution2 = game_solver.get_other_solution()
        solutions = {solution1, solution2}
        self.assertEqual(expected_solutions, solutions)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_without_continue_white_way_constraint(self):
        grid = Grid([
            [_, _, 2, _],
            [_, _, _, 5],
            [_, _, _, _],
            [1, _, _, _],
        ])
        expected_solution = Grid([
            [0, 1, 0, 1],
            [0, 0, 0, 0],
            [1, 0, 1, 1],
            [0, 0, 1, 1],
        ])

        game_solver = TasukueaSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_with_continue_white_way(self):
        grid = Grid([
            [_, 2, _, _],
            [_, _, _, 4],
            [_, _, _, _],
            [1, _, _, _],
        ])
        expected_solution = Grid([
            [1, 0, 1, 0],
            [0, 0, 0, 0],
            [1, 0, 1, 1],
            [0, 0, 1, 1],
        ])

        game_solver = TasukueaSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_evil_l4w53(self):
        """https://gridpuzzle.com/tasukuea/l4w53"""
        grid = Grid([
            [_, _, 1, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, 5, _],
            [_, 2, _, _, _],
        ])
        expected_solution = Grid([
            [0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 1, 1],
            [0, 1, 0, 0, 0],
            [1, 0, 0, 1, 0],
        ])

        game_solver = TasukueaSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_evil_3n8wx(self):
        """https://gridpuzzle.com/tasukuea/3n8wx"""
        grid = Grid([
            [_, _, _, 2, _],
            [U, _, _, _, _],
            [_, _, 2, _, _],
            [U, _, _, _, _],
            [_, _, _, U, U],
        ])
        expected_solution = Grid([
            [1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0],
        ])

        game_solver = TasukueaSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_evil_22025(self):
        """https://gridpuzzle.com/tasukuea/22025"""
        grid = Grid([
            [_, _, _, _, _, U, U, _],
            [_, _, _, _, _, _, _, 1],
            [_, _, _, _, _, _, _, _],
            [9, _, _, _, 13, _, _, _],
            [_, _, _, 13, _, _, _, 9],
            [_, _, _, _, _, _, _, _],
            [U, _, _, _, _, _, _, _],
            [_, U, 1, _, _, _, _, _],
        ])
        expected_solution = Grid([
            [1, 1, 1, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 0, 0],
            [1, 1, 1, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 1, 1, 0],
            [0, 1, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 1, 1, 0],
            [1, 0, 0, 1, 0, 0, 0, 0],
        ])

        game_solver = TasukueaSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12_evil_v95zk(self):
        """https://gridpuzzle.com/tasukuea/v95zk"""
        grid = Grid([
            [_, _, _, U, _, _, _, 2, _, _, _, _],
            [U, _, _, _, _, _, _, _, _, _, _, _],
            [5, _, _, _, _, _, _, _, _, _, _, 10],
            [_, _, _, _, 6, _, _, _, _, _, _, _],
            [2, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, 13, _, _, _],
            [_, _, _, _, _, _, _, _, _, 4, _, _],
            [_, _, 13, _, _, _, _, _, _, _, _, _],
            [2, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, 10, _, _],
            [_, 10, _, _, _, _, _, _, _, _, _, U],
            [_, _, _, _, _, _, _, _, 10, _, _, _],
        ])
        expected_solution = Grid([
            [0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0],
            [1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0],
            [1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
            [0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        ])

        game_solver = TasukueaSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
