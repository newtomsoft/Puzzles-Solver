import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Fubuki.FubukiSolver import FubukiSolver

_ = -1


class FubukiSolverTests(TestCase):


    def test_solution_grid_square(self):
        grid = Grid([
            [0, 1, 1],
            [0, 2, 2],
        ])
        with self.assertRaises(ValueError) as context:
            FubukiSolver(grid, [], [])

        self.assertEqual("Fubuki grid must be a 3x3 square", str(context.exception))

    def test_solution_initial_number_different_in_row(self):
        grid = Grid([
            [_, 1, 1],
            [_, _, _],
            [_, _, _],
        ])
        with self.assertRaises(ValueError) as context:
            FubukiSolver(grid, [], [])

        self.assertEqual("Initial numbers must be different in rows and columns", str(context.exception))

    def test_solution_initial_number_different_in_column(self):
        grid = Grid([
            [_, 1, _],
            [_, 1, _],
            [_, _, _],
        ])
        with self.assertRaises(ValueError) as context:
            FubukiSolver(grid, [], [])

        self.assertEqual("Initial numbers must be different in rows and columns", str(context.exception))

    def test_solution_initial_number_greater_than_1(self):
        grid = Grid([
            [0, _, _],
            [_, _, _],
            [_, _, _],
        ])
        with self.assertRaises(ValueError) as context:
            FubukiSolver(grid, [], [])

        self.assertEqual("initial numbers must be between 1 and 9", str(context.exception))

    def test_solution_initial_number_less_than_n(self):
        grid = Grid([
            [10, _, _],
            [_, _, _],
            [_, _, _],
        ])
        with self.assertRaises(ValueError) as context:
            FubukiSolver(grid, [], [])

        self.assertEqual("initial numbers must be between 1 and 9", str(context.exception))

    def test_solution_easy(self):
        grid = Grid([
            [_, 6, _],
            [7, _, 4],
            [_, 1, _],
        ])
        row_sums = [16, 20, 9]
        column_sums = [20, 16, 9]
        expected_solution = Grid([
            [8, 6, 2],
            [7, 9, 4],
            [5, 1, 3],
        ])
        game = FubukiSolver(grid, row_sums, column_sums)

        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_hard(self):
        grid = Grid([
            [_, 8, _],
            [_, _, _],
            [_, _, _],
        ])
        row_sums = [17, 11, 17]
        column_sums = [17, 22, 6]

        expected_solution = Grid([
            [6, 8, 3],
            [4, 5, 2],
            [7, 9, 1],
        ])
        game = FubukiSolver(grid, row_sums, column_sums)
        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_evil(self):
        grid = Grid([
            [_, _, _],
            [_, _, _],
            [_, _, _],
        ])
        row_sums = [19, 10, 16]
        column_sums = [23, 15, 7]

        expected_solution = Grid([
            [8, 7, 4],
            [6, 3, 1],
            [9, 5, 2],
        ])
        game = FubukiSolver(grid, row_sums, column_sums)
        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
