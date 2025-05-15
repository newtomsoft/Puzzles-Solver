import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Sudoku.Sudoku.SudokuSolver import SudokuSolver

_ = -1


class SudokuSolverTests(TestCase):


    def test_solution_grid_square(self):
        grid = Grid([
            [0, 1, 1],
            [0, 2, 2],
        ])
        with self.assertRaises(ValueError) as context:
            SudokuSolver(grid)

        self.assertEqual("Sudoku grid must be square", str(context.exception))

    def test_solution_subgrid(self):
        grid = Grid([
            [_, _, _, _, 1],
            [_, _, _, _, 2],
            [_, _, _, _, 3],
            [_, _, _, _, 4],
            [_, _, _, _, 5],
        ])
        with self.assertRaises(ValueError) as context:
            SudokuSolver(grid)

        self.assertEqual("Sudoku subgrid must have size n x n or 3x2 or 4x3", str(context.exception))

    def test_solution_initial_number_different_in_row(self):
        grid = Grid([
            [_, _, 1, 1],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        with self.assertRaises(ValueError) as context:
            SudokuSolver(grid)

        self.assertEqual("Initial numbers must be different in rows and columns", str(context.exception))

    def test_solution_initial_number_different_in_column(self):
        grid = Grid([
            [_, _, 1, _],
            [_, _, 1, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        with self.assertRaises(ValueError) as context:
            SudokuSolver(grid)

        self.assertEqual("Initial numbers must be different in rows and columns", str(context.exception))

    def test_solution_initial_number_different_in_sub_square(self):
        grid = Grid([
            [1, _, _, _],
            [_, 1, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        with self.assertRaises(ValueError) as context:
            SudokuSolver(grid)

        self.assertEqual("initial numbers must be different in sub squares", str(context.exception))

    def test_solution_initial_number_greater_than_1(self):
        grid = Grid([
            [0, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        with self.assertRaises(ValueError) as context:
            SudokuSolver(grid)

        self.assertEqual("initial numbers must be between 1 and n x n", str(context.exception))

    def test_solution_initial_number_less_than_n(self):
        grid = Grid([
            [5, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        with self.assertRaises(ValueError) as context:
            SudokuSolver(grid)

        self.assertEqual("initial numbers must be between 1 and n x n", str(context.exception))

    def test_solution_4x4(self):
        grid = Grid([
            [1, 2, 3, _],
            [3, 4, _, _],
            [2, 1, _, _],
            [_, _, 1, 2],
        ])
        expected_solution = Grid([
            [1, 2, 3, 4],
            [3, 4, 2, 1],
            [2, 1, 4, 3],
            [4, 3, 1, 2],
        ])
        sudoku_game = SudokuSolver(grid)

        solution = sudoku_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = sudoku_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6(self):
        grid = Grid([
            [6, _, 3, _, _, _],
            [_, 5, _, _, _, 2],
            [2, _, _, _, 6, 3],
            [_, _, _, _, 1, _],
            [1, _, 6, _, _, 5],
            [5, _, _, _, _, _]
        ])
        expected_solution = Grid([
            [6, 2, 3, 4, 5, 1],
            [4, 5, 1, 6, 3, 2],
            [2, 1, 4, 5, 6, 3],
            [3, 6, 5, 2, 1, 4],
            [1, 4, 6, 3, 2, 5],
            [5, 3, 2, 1, 4, 6]
        ])
        sudoku_game = SudokuSolver(grid)

        solution = sudoku_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = sudoku_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_9x9(self):
        grid = Grid([
            [_, 5, _, _, _, _, _, _, _],
            [_, _, 2, 4, _, 3, 8, 7, 1],
            [1, 7, _, 2, 9, 6, 5, 3, _],
            [6, _, _, _, _, _, 7, _, _],
            [_, _, _, _, 1, 4, 9, _, 3],
            [5, _, _, _, 8, 9, 1, 6, _],
            [_, 8, _, 3, 6, _, 4, _, _],
            [_, 4, 5, _, 2, _, _, 8, _],
            [2, 9, _, _, 4, _, _, _, _]
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
        sudoku_game = SudokuSolver(grid)

        solution = sudoku_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = sudoku_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_9x9_2(self):
        grid = Grid([
            [7, 1, _, _, 8, 3, _, 4, _],
            [9, _, _, _, _, _, _, 5, 8],
            [4, _, _, _, 1, _, _, _, _],
            [_, 8, _, _, _, 9, _, _, 5],
            [_, _, _, _, _, _, _, _, _],
            [5, _, _, 4, _, _, _, 2, _],
            [_, _, _, _, 7, _, _, _, 4],
            [3, 2, _, _, _, _, _, _, 9],
            [_, 4, _, 5, 9, _, _, 7, 2]
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
        sudoku_game = SudokuSolver(grid)

        solution = sudoku_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = sudoku_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_9x9_evil(self):
        grid = Grid([
            [_, _, _, _, _, 8, _, 7, _],
            [_, _, _, _, 5, _, _, _, 9],
            [_, _, _, 2, _, 4, 3, _, _],
            [_, 8, _, _, 4, _, _, 6, _],
            [5, _, _, _, _, 3, _, _, _],
            [_, _, 2, 7, _, _, _, _, 1],
            [9, _, _, _, _, 6, _, _, 5],
            [_, _, 7, _, 1, _, _, 8, _],
            [_, 3, _, _, _, _, 4, _, _],
        ])
        expected_solution = Grid([
            [2, 9, 5, 3, 6, 8, 1, 7, 4],
            [3, 4, 8, 1, 5, 7, 6, 2, 9],
            [1, 7, 6, 2, 9, 4, 3, 5, 8],
            [7, 8, 3, 9, 4, 1, 5, 6, 2],
            [5, 1, 9, 6, 2, 3, 8, 4, 7],
            [4, 6, 2, 7, 8, 5, 9, 3, 1],
            [9, 2, 4, 8, 3, 6, 7, 1, 5],
            [6, 5, 7, 4, 1, 9, 2, 8, 3],
            [8, 3, 1, 5, 7, 2, 4, 9, 6],
        ])
        sudoku_game = SudokuSolver(grid)

        solution = sudoku_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = sudoku_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
