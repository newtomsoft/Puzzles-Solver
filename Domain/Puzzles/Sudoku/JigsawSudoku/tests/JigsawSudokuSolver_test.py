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
        regions = [
            [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 1)],
            [Position(0, 2), Position(0, 3), Position(0, 4), Position(1, 3), Position(1, 4)],
            [Position(1, 2), Position(2, 2), Position(2, 3), Position(3, 1), Position(3, 2)],
            [Position(2, 0), Position(3, 0), Position(4, 0), Position(4, 1), Position(4, 2)],
        ]
        with self.assertRaises(ValueError) as context:
            JigsawSudokuSolver(grid, regions)

        self.assertEqual("The grid must have the same number of regions as rows/column", str(context.exception))

    def test_solution_regions_cell_count_compliant(self):
        grid = Grid([
            [2, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
        ])
        regions = [
            [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 1)],
            [Position(0, 2), Position(0, 3), Position(0, 4), Position(1, 3), Position(1, 4)],
            [Position(1, 2), Position(2, 2), Position(2, 3), Position(3, 1)],
            [Position(2, 0), Position(3, 0), Position(4, 0), Position(4, 1), Position(4, 2)],
            [Position(2, 4), Position(3, 3), Position(3, 4), Position(4, 3), Position(4, 4)],
        ]

        with self.assertRaises(ValueError) as context:
            JigsawSudokuSolver(grid, regions)

        self.assertEqual("The regions must have the same number of cells", str(context.exception))

    def test_solution_initial_number_different_in_regions(self):
        grid = Grid([
            [2, _, _, _, _],
            [_, _, _, _, _],
            [_, 2, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
        ])
        regions = [
            [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 1)],
            [Position(0, 2), Position(0, 3), Position(0, 4), Position(1, 3), Position(1, 4)],
            [Position(1, 2), Position(2, 2), Position(2, 3), Position(3, 1), Position(3, 2)],
            [Position(2, 0), Position(3, 0), Position(4, 0), Position(4, 1), Position(4, 2)],
            [Position(2, 4), Position(3, 3), Position(3, 4), Position(4, 3), Position(4, 4)],
        ]

        with self.assertRaises(ValueError) as context:
            JigsawSudokuSolver(grid, regions)

        self.assertEqual("Initial numbers must be different in regions", str(context.exception))

    def test_solution_5x5_easy(self):
        grid = Grid([
            [2, _, _, _, _],
            [_, _, 3, _, 5],
            [_, _, _, _, _],
            [3, _, 4, _, _],
            [_, _, _, _, 3],
        ])
        regions = [
            [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 1)],
            [Position(0, 2), Position(0, 3), Position(0, 4), Position(1, 3), Position(1, 4)],
            [Position(1, 2), Position(2, 2), Position(2, 3), Position(3, 1), Position(3, 2)],
            [Position(2, 0), Position(3, 0), Position(4, 0), Position(4, 1), Position(4, 2)],
            [Position(2, 4), Position(3, 3), Position(3, 4), Position(4, 3), Position(4, 4)],
        ]

        expected_solution = Grid([
            [2, 5, 1, 3, 4],
            [1, 4, 3, 2, 5],
            [4, 3, 5, 1, 2],
            [3, 2, 4, 5, 1],
            [5, 1, 2, 4, 3],
        ])
        game = JigsawSudokuSolver(grid, regions)

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
        regions = [
            [Position(0, 0), Position(0, 1), Position(0, 2), Position(0, 3), Position(1, 3)],
            [Position(0, 4), Position(1, 4), Position(2, 3), Position(2, 4), Position(3, 4)],
            [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1), Position(2, 2)],
            [Position(2, 0), Position(3, 0), Position(3, 1), Position(4, 0), Position(4, 1)],
            [Position(3, 2), Position(3, 3), Position(4, 2), Position(4, 3), Position(4, 4)],
        ]

        expected_solution = Grid([
            [4, 3, 5, 2, 1],
            [2, 5, 4, 1, 3],
            [5, 1, 3, 4, 2],
            [1, 4, 2, 3, 5],
            [3, 2, 1, 5, 4],
        ])
        game = JigsawSudokuSolver(grid, regions)

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
        regions = [
            [Position(0, 1), Position(0, 2), Position(0, 0), Position(1, 0), Position(1, 1), Position(2, 0), Position(3, 0)],
            [Position(1, 2), Position(0, 4), Position(2, 1), Position(2, 2), Position(0, 3), Position(1, 3), Position(1, 4)],
            [Position(2, 3), Position(2, 4), Position(3, 4), Position(0, 5), Position(1, 5), Position(2, 5), Position(0, 6)],
            [Position(4, 5), Position(2, 6), Position(5, 6), Position(3, 6), Position(1, 6), Position(4, 6), Position(3, 5)],
            [Position(3, 3), Position(4, 3), Position(3, 1), Position(5, 3), Position(3, 2), Position(4, 2), Position(5, 2)],
            [Position(6, 2), Position(4, 0), Position(5, 0), Position(6, 0), Position(6, 1), Position(4, 1), Position(5, 1)],
            [Position(4, 4), Position(5, 5), Position(6, 5), Position(6, 6), Position(5, 4), Position(6, 3), Position(6, 4)]
        ]
        expected_solution = Grid([
            [4, 1, 2, 3, 6, 5, 7],
            [6, 3, 7, 2, 5, 1, 4],
            [7, 4, 1, 6, 2, 3, 5],
            [5, 2, 3, 7, 4, 6, 1],
            [1, 6, 5, 4, 3, 7, 2],
            [2, 5, 6, 1, 7, 4, 3],
            [3, 7, 4, 5, 1, 2, 6],
        ])
        game = JigsawSudokuSolver(grid, regions)

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
        regions = [
            [Position(0, 1), Position(1, 2), Position(0, 0), Position(1, 1), Position(0, 3), Position(2, 3), Position(0, 2), Position(3, 3), Position(1, 3)],
            [Position(0, 4), Position(2, 7), Position(4, 6), Position(0, 6), Position(2, 6), Position(0, 5), Position(3, 6), Position(1, 6), Position(3, 5)],
            [Position(0, 7), Position(3, 8), Position(3, 7), Position(1, 8), Position(1, 7), Position(4, 8), Position(0, 8), Position(4, 7), Position(2, 8)],
            [Position(2, 1), Position(3, 1), Position(2, 0), Position(5, 1), Position(3, 0), Position(2, 2), Position(1, 0), Position(3, 2), Position(4, 1)],
            [Position(4, 4), Position(2, 4), Position(3, 4), Position(1, 5), Position(4, 3), Position(5, 4), Position(1, 4), Position(4, 5), Position(2, 5)],
            [Position(4, 0), Position(7, 1), Position(8, 1), Position(6, 1), Position(7, 0), Position(8, 0), Position(5, 0), Position(6, 0), Position(8, 2)],
            [Position(5, 5), Position(6, 5), Position(6, 4), Position(4, 2), Position(5, 7), Position(5, 6), Position(5, 3), Position(6, 3), Position(5, 2)],
            [Position(8, 8), Position(7, 7), Position(5, 8), Position(8, 7), Position(6, 8), Position(6, 7), Position(8, 6), Position(8, 5), Position(7, 8)],
            [Position(7, 4), Position(6, 2), Position(8, 4), Position(7, 3), Position(8, 3), Position(7, 6), Position(7, 2), Position(6, 6), Position(7, 5)]
        ]
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
        game = JigsawSudokuSolver(grid, regions)

        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)


if __name__ == '__main__':
    unittest.main()
