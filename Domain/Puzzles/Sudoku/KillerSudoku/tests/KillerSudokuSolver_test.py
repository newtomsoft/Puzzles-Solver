import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.Sudoku.KillerSudoku.KillerSudokuSolver import KillerSudokuSolver

_ = -1


class KillerSudokuSolverTests(TestCase):
    def test_solution_cages_cover_grid(self):
        grid = Grid([
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        cages = {
            1: ([Position(0, 0), Position(0, 1)], 6),
            2: ([Position(1, 0), Position(1, 1), Position(1, 2)], 6),
            3: ([Position(0, 3), Position(1, 3)], 6),
            4: ([Position(2, 0), Position(2, 1)], 7),
            5: ([Position(2, 2), Position(2, 3)], 5),
            6: ([Position(3, 0)], 2),
            7: ([Position(3, 1), Position(3, 2), Position(3, 3)], 6),
        }

        with self.assertRaises(ValueError) as context:
            KillerSudokuSolver(grid, cages)

        self.assertEqual("The cages must cover the whole grid", str(context.exception))

    def test_solution_initial_number_different_in_cages(self):
        grid = Grid([
            [_, 2, _, _],
            [_, _, 2, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        cages = {
            1: ([Position(0, 0), Position(1, 0)], 6),
            2: ([Position(0, 2), Position(0, 3), Position(1, 3)], 6),
            3: ([Position(0, 1), Position(1, 1), Position(1, 2)], 6),
            4: ([Position(2, 0), Position(2, 1)], 7),
            5: ([Position(2, 2), Position(2, 3)], 5),
            6: ([Position(3, 0)], 2),
            7: ([Position(3, 1), Position(3, 2), Position(3, 3)], 6),
        }

        with self.assertRaises(ValueError) as context:
            KillerSudokuSolver(grid, cages)

        self.assertEqual("Initial numbers must be different in cages", str(context.exception))

    def test_solution_2x2x4_easy(self):
        grid = Grid([
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        cages = {
            1: ([Position(0, 0), Position(1, 0)], 7),
            2: ([Position(0, 1), Position(0, 2)], 4),
            3: ([Position(0, 3), Position(1, 3)], 3),
            4: ([Position(1, 1), Position(2, 1)], 6),
            5: ([Position(1, 2), Position(2, 2)], 5),
            6: ([Position(2, 3), Position(3, 2), Position(3, 3)], 9),
            7: ([Position(2, 0), Position(3, 0), Position(3, 1)], 6),
        }

        expected_solution = Grid([
            [4, 1, 3, 2],
            [3, 2, 4, 1],
            [2, 4, 1, 3],
            [1, 3, 2, 4],
        ])
        game = KillerSudokuSolver(grid, cages)
        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_2x3x4_hard(self):
        grid = Grid([
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
        ])
        cages = {
            1: ([Position(0, 0), Position(1, 0)], 10),
            2: ([Position(0, 1), Position(1, 1)], 5),
            3: ([Position(0, 2), Position(1, 2)], 6),
            4: ([Position(0, 3), Position(1, 3)], 7),
            5: ([Position(0, 4), Position(0, 5)], 8),
            6: ([Position(1, 4), Position(1, 5)], 6),
            7: ([Position(2, 0), Position(2, 1), Position(2, 2)], 12),
            8: ([Position(2, 3), Position(3, 3)], 6),
            9: ([Position(2, 4), Position(3, 4)], 6),
            10: ([Position(2, 5), Position(3, 5), Position(4, 4), Position(4, 5)], 14),
            11: ([Position(3, 0), Position(3, 1)], 7),
            12: ([Position(3, 2), Position(4, 2)], 8),
            13: ([Position(4, 0), Position(5, 0)], 5),
            14: ([Position(4, 1), Position(5, 1)], 6),
            15: ([Position(4, 3), Position(5, 2), Position(5, 3)], 12),
            16: ([Position(5, 4), Position(5, 5)], 8)
        }

        expected_solution = Grid([
            [4, 2, 1, 6, 3, 5],
            [6, 3, 5, 1, 2, 4],
            [5, 4, 3, 2, 1, 6],
            [1, 6, 2, 4, 5, 3],
            [2, 5, 6, 3, 4, 1],
            [3, 1, 4, 5, 6, 2],
        ])
        game = KillerSudokuSolver(grid, cages)
        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_3x3x4_easy(self):
        grid = Grid([
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
        ])
        cages = {
            1: ([Position(0, 0), Position(0, 1)], 11),
            2: ([Position(0, 2), Position(0, 3), Position(0, 4)], 16),
            3: ([Position(0, 5), Position(1, 5), Position(1, 6)], 6),
            4: ([Position(0, 6), Position(0, 7)], 11),
            5: ([Position(0, 8), Position(1, 8)], 7),
            6: ([Position(1, 0), Position(1, 1)], 10),
            7: ([Position(1, 2), Position(2, 2)], 7),
            8: ([Position(1, 3), Position(1, 4)], 15),
            9: ([Position(1, 7), Position(2, 6), Position(2, 7)], 20),
            10: ([Position(2, 0), Position(3, 0)], 6),
            11: ([Position(2, 1), Position(3, 1)], 9),
            12: ([Position(2, 3), Position(3, 2), Position(3, 3)], 13),
            13: ([Position(2, 4), Position(2, 5)], 14),
            14: ([Position(2, 8), Position(3, 8)], 7),
            15: ([Position(3, 4), Position(3, 5)], 13),
            16: ([Position(3, 6), Position(3, 7)], 15),
            17: ([Position(4, 0), Position(4, 1)], 12),
            18: ([Position(4, 2), Position(5, 2)], 13),
            19: ([Position(4, 3), Position(4, 4), Position(5, 3), Position(5, 4)], 18),
            20: ([Position(4, 5), Position(5, 5)], 8),
            21: ([Position(4, 6), Position(4, 7), Position(4, 8)], 18),
            22: ([Position(5, 0), Position(6, 0)], 12),
            23: ([Position(5, 1), Position(6, 1)], 7),
            24: ([Position(5, 6), Position(5, 7)], 7),
            25: ([Position(5, 8), Position(6, 8)], 12),
            26: ([Position(6, 2), Position(6, 3)], 10),
            27: ([Position(6, 4), Position(7, 2), Position(7, 3), Position(7, 4), Position(8, 4)], 21),
            28: ([Position(6, 5), Position(7, 5), Position(8, 5)], 18),
            29: ([Position(6, 6), Position(7, 6)], 14),
            30: ([Position(6, 7), Position(7, 7)], 6),
            31: ([Position(7, 0), Position(7, 1), Position(8, 0), Position(8, 1)], 23),
            32: ([Position(7, 8), Position(8, 8)], 10),
            33: ([Position(8, 2), Position(8, 3)], 9),
            34: ([Position(8, 6), Position(8, 7)], 7)
        }

        expected_solution = Grid([
            [8, 3, 9, 1, 6, 2, 4, 7, 5],
            [6, 4, 5, 7, 8, 3, 1, 9, 2],
            [1, 7, 2, 4, 9, 5, 8, 3, 6],
            [5, 2, 3, 6, 4, 9, 7, 8, 1],
            [4, 8, 7, 2, 5, 1, 3, 6, 9],
            [9, 1, 6, 8, 3, 7, 2, 5, 4],
            [3, 6, 1, 9, 7, 4, 5, 2, 8],
            [2, 5, 8, 3, 1, 6, 9, 4, 7],
            [7, 9, 4, 5, 2, 8, 6, 1, 3],
        ])
        game = KillerSudokuSolver(grid, cages)
        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_3x3x4_hard(self):
        grid = Grid([
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
        ])
        cages = {
            1: ([Position(0, 0), Position(1, 0)], 12),
            2: ([Position(0, 1), Position(1, 1)], 11),
            3: ([Position(0, 2), Position(0, 3), Position(1, 2), Position(1, 3)], 20),
            4: ([Position(0, 4), Position(1, 4), Position(2, 3), Position(2, 4)], 20),
            5: ([Position(0, 5), Position(0, 6)], 8),
            6: ([Position(0, 7), Position(0, 8)], 12),
            7: ([Position(1, 5), Position(2, 5)], 9),
            8: ([Position(1, 6), Position(2, 6)], 8),
            9: ([Position(1, 7), Position(1, 8)], 11),
            10: ([Position(2, 0), Position(3, 0)], 4),
            11: ([Position(2, 1), Position(2, 2)], 10),
            12: ([Position(2, 7), Position(3, 6), Position(3, 7)], 19),
            13: ([Position(2, 8), Position(3, 8)], 6),
            14: ([Position(3, 1), Position(3, 2)], 8),
            15: ([Position(3, 3), Position(3, 4)], 14),
            16: ([Position(3, 5), Position(4, 5)], 11),
            17: ([Position(4, 0), Position(4, 1)], 13),
            18: ([Position(4, 2), Position(4, 3)], 8),
            19: ([Position(4, 4), Position(5, 4), Position(6, 4)], 10),
            20: ([Position(4, 6), Position(4, 7)], 15),
            21: ([Position(4, 8), Position(5, 8)], 10),
            22: ([Position(5, 0), Position(5, 1)], 11),
            23: ([Position(5, 2), Position(5, 3)], 15),
            24: ([Position(5, 5), Position(5, 6)], 7),
            25: ([Position(5, 7), Position(6, 7)], 5),
            26: ([Position(6, 0), Position(6, 1), Position(7, 1)], 15),
            27: ([Position(6, 2), Position(6, 3)], 11),
            28: ([Position(6, 5), Position(6, 6), Position(7, 6)], 16),
            29: ([Position(6, 8), Position(7, 7), Position(7, 8), Position(8, 6), Position(8, 7), Position(8, 8)], 33),
            30: ([Position(7, 0), Position(8, 0)], 8),
            31: ([Position(7, 2), Position(8, 1), Position(8, 2)], 14),
            32: ([Position(7, 3), Position(8, 3)], 6),
            33: ([Position(7, 4), Position(8, 4)], 15),
            34: ([Position(7, 5), Position(8, 5)], 10)
        }

        expected_solution = Grid([
            [4, 2, 5, 8, 6, 7, 1, 9, 3],
            [8, 9, 6, 1, 3, 5, 2, 4, 7],
            [1, 7, 3, 9, 2, 4, 6, 8, 5],
            [3, 6, 2, 5, 9, 8, 4, 7, 1],
            [5, 8, 1, 7, 4, 3, 9, 6, 2],
            [7, 4, 9, 6, 1, 2, 5, 3, 8],
            [9, 1, 8, 3, 5, 6, 7, 2, 4],
            [2, 5, 7, 4, 8, 9, 3, 1, 6],
            [6, 3, 4, 2, 7, 1, 8, 5, 9],
        ])
        game = KillerSudokuSolver(grid, cages)
        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
