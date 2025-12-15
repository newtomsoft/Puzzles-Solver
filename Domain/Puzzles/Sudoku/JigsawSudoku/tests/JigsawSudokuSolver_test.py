import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.Sudoku.JigsawSudoku.JigsawSudokuSolver import JigsawSudokuSolver

_ = -1


class JigsawSudokuSolverTests(TestCase):
    def test_solution_regions_numbers(self):
        grid = Grid([
            [2, _, _, _, _],
            [_, _, 3, _, 5],
            [_, _, _, _, _],
            [3, _, 4, _, _],
            [_, _, _, _, 3],
        ])
        regions_grid = Grid([
            [0, 0, 1, 1, 1],
            [0, 0, 2, 1, 1],
            [3, 0, 2, 2, 0],
            [3, 2, 2, 0, 0],
            [3, 3, 3, 0, 0],
        ])
        with self.assertRaises(ValueError) as context:
            JigsawSudokuSolver(grid, regions_grid)

        self.assertEqual("The grid must have the same number of regions as rows/column", str(context.exception))

    def test_solution_regions_cell_count_compliant(self):
        grid = Grid([
            [2, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
        ])
        regions_grid = Grid([
            [0, 0, 1, 1, 1],
            [0, 0, 2, 1, 1],
            [3, 0, 2, 2, 4],
            [3, 2, 0, 4, 4],
            [3, 3, 3, 4, 4],
        ])

        with self.assertRaises(ValueError) as context:
            JigsawSudokuSolver(grid, regions_grid)

        self.assertEqual("The regions must have the same number of cells", str(context.exception))

    def test_solution_initial_number_different_in_regions(self):
        grid = Grid([
            [2, _, _, _, _],
            [_, _, _, _, _],
            [_, 2, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
        ])
        regions_grid = Grid([
            [0, 0, 1, 1, 1],
            [0, 0, 2, 1, 1],
            [3, 0, 2, 2, 4],
            [3, 2, 2, 4, 4],
            [3, 3, 3, 4, 4],
        ])

        with self.assertRaises(ValueError) as context:
            JigsawSudokuSolver(grid, regions_grid)

        self.assertEqual("Initial numbers must be different in regions", str(context.exception))

    def test_solution_5x5_easy(self):
        grid = Grid([
            [2, _, _, _, _],
            [_, _, 3, _, 5],
            [_, _, _, _, _],
            [3, _, 4, _, _],
            [_, _, _, _, 3],
        ])
        regions_grid = Grid([
            [0, 0, 1, 1, 1],
            [0, 0, 2, 1, 1],
            [3, 0, 2, 2, 4],
            [3, 2, 2, 4, 4],
            [3, 3, 3, 4, 4],
        ])

        expected_solution = Grid([
            [2, 5, 1, 3, 4],
            [1, 4, 3, 2, 5],
            [4, 3, 5, 1, 2],
            [3, 2, 4, 5, 1],
            [5, 1, 2, 4, 3],
        ])
        game = JigsawSudokuSolver(grid, regions_grid)

        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_5x5_hard(self):
        grid = Grid([
            [4, _, 5, _, _],
            [_, _, _, _, 3],
            [_, _, _, _, _],
            [1, _, _, _, _],
            [_, _, 1, _, 4],
        ])
        regions_grid = Grid([
            [0, 0, 0, 0, 1],
            [2, 2, 2, 0, 1],
            [3, 2, 2, 1, 1],
            [3, 3, 4, 4, 1],
            [3, 3, 4, 4, 4],
        ])

        expected_solution = Grid([
            [4, 3, 5, 2, 1],
            [2, 5, 4, 1, 3],
            [5, 1, 3, 4, 2],
            [1, 4, 2, 3, 5],
            [3, 2, 1, 5, 4],
        ])
        game = JigsawSudokuSolver(grid, regions_grid)

        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_7x7_hard(self):
        grid = Grid([
            [4, 1, 2, 3, 6, 5, 7],
            [6, 3, 7, 2, 5, 1, 4],
            [7, 4, 1, 6, 2, 3, 5],
            [5, 2, 3, 7, 4, 6, 1],
            [1, 6, 5, 4, 3, 7, 2],
            [2, 5, 6, 1, 7, 4, 3],
            [3, 7, 4, 5, 1, 2, 6],
        ])
        regions_grid = Grid([
            [0, 0, 0, 1, 1, 2, 2],
            [0, 0, 1, 1, 1, 2, 3],
            [0, 1, 1, 2, 2, 2, 3],
            [0, 4, 4, 4, 2, 3, 3],
            [5, 5, 4, 4, 6, 3, 3],
            [5, 5, 4, 4, 6, 6, 3],
            [5, 5, 5, 6, 6, 6, 6],
        ])
        expected_solution = Grid([
            [4, 1, 2, 3, 6, 5, 7],
            [6, 3, 7, 2, 5, 1, 4],
            [7, 4, 1, 6, 2, 3, 5],
            [5, 2, 3, 7, 4, 6, 1],
            [1, 6, 5, 4, 3, 7, 2],
            [2, 5, 6, 1, 7, 4, 3],
            [3, 7, 4, 5, 1, 2, 6],
        ])
        game = JigsawSudokuSolver(grid, regions_grid)

        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_9x9_hard(self):
        grid = Grid([
            [9, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, 8],
            [_, _, _, 7, _, _, 9, 2, _],
            [_, 7, _, _, 1, 6, 8, _, _],
            [3, _, _, _, 7, _, _, _, 1],
            [_, _, 4, 1, 3, _, _, 7, _],
            [_, 2, 5, _, _, 3, _, _, _],
            [8, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, 6]
        ])
        regions_grid = Grid([
            [0, 0, 0, 0, 1, 1, 1, 2, 2],
            [3, 0, 0, 0, 4, 4, 1, 2, 2],
            [3, 3, 3, 0, 4, 4, 1, 1, 2],
            [3, 3, 3, 0, 4, 1, 1, 2, 2],
            [5, 3, 6, 4, 4, 4, 1, 2, 2],
            [5, 3, 6, 6, 4, 6, 6, 6, 7],
            [5, 5, 8, 6, 6, 6, 8, 7, 7],
            [5, 5, 8, 8, 8, 8, 8, 7, 7],
            [5, 5, 5, 8, 8, 7, 7, 7, 7],
        ])
        expected_solution = Grid([
            [9, 6, 2, 8, 5, 1, 3, 4, 7],
            [2, 3, 1, 4, 6, 9, 7, 5, 8],
            [1, 5, 6, 7, 4, 8, 9, 2, 3],
            [4, 7, 3, 5, 1, 6, 8, 9, 2],
            [3, 9, 8, 2, 7, 5, 4, 6, 1],
            [6, 8, 4, 1, 3, 2, 5, 7, 9],
            [7, 2, 5, 6, 9, 3, 1, 8, 4],
            [8, 1, 7, 9, 2, 4, 6, 3, 5],
            [5, 4, 9, 3, 8, 7, 2, 1, 6],
        ])
        game = JigsawSudokuSolver(grid, regions_grid)

        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)


if __name__ == '__main__':
    unittest.main()
