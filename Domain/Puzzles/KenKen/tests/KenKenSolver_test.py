import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.KenKen.KenKenSolver import KenKenSolver


class KenKenSolverTests(TestCase):


    def test_solution_grid_square(self):
        regions_operators_results = [
            ([Position(0, 0), Position(0, 1), Position(0, 2)], '+', 8),
            ([Position(1, 0), Position(1, 1), Position(1, 2)], 'x', 4),
        ]
        with self.assertRaises(ValueError) as context:
            KenKenSolver(regions_operators_results)

        self.assertEqual("KenKen grid must be square", str(context.exception))

    def test_solution_4x4(self):
        regions_operators_results = [
            ([Position(0, 0), Position(1, 0)], 'x', 4),
            ([Position(0, 1), Position(0, 2)], '+', 7),
            ([Position(0, 3), Position(1, 3)], '÷', 2),
            ([Position(1, 1), Position(1, 2)], 'x', 6),
            ([Position(2, 0), Position(2, 1)], '-', 1),
            ([Position(2, 2), Position(3, 2)], '+', 5),
            ([Position(2, 3), Position(3, 3)], '-', 1),
            ([Position(3, 0), Position(3, 1)], '÷', 2),
        ]
        expected_solution = Grid([
            [1, 4, 3, 2],
            [4, 3, 2, 1],
            [3, 2, 1, 4],
            [2, 1, 4, 3],
        ])
        kenken_game = KenKenSolver(regions_operators_results)

        solution = kenken_game.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_4x4_hard(self):
        regions_operators_results = [
            ([Position(0, 0), Position(1, 0)], '-', 1),
            ([Position(0, 1), Position(0, 2), Position(0, 3), Position(1, 2), Position(1, 3)], '+', 11),
            ([Position(1, 1), Position(2, 1)], '÷', 2),
            ([Position(2, 0), Position(3, 0), Position(3, 1)], 'x', 6),
            ([Position(2, 2), Position(3, 2)], '-', 2),
            ([Position(2, 3), Position(3, 3)], '÷', 2),
        ]
        expected_solution = Grid([
            [4, 1, 2, 3],
            [3, 2, 4, 1],
            [1, 4, 3, 2],
            [2, 3, 1, 4],
        ])
        kenken_game = KenKenSolver(regions_operators_results)

        solution = kenken_game.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_7x7_hard(self):
        regions_operators_results = [
            ([Position(0, 1), Position(0, 0)], '+', 5),
            ([Position(0, 2), Position(1, 2), Position(2, 2)], '+', 16),
            ([Position(0, 3), Position(0, 4), Position(0, 5)], 'x', 60),
            ([Position(1, 6), Position(0, 6)], '-', 1),
            ([Position(1, 0), Position(2, 0)], 'x', 21),
            ([Position(1, 1), Position(2, 1)], '-', 5),
            ([Position(1, 3), Position(1, 4)], '-', 3),
            ([Position(2, 5), Position(3, 5), Position(1, 5)], 'x', 84),
            ([Position(2, 3), Position(3, 3)], 'x', 6),
            ([Position(2, 4), Position(3, 4)], '÷', 3),
            ([Position(2, 6), Position(3, 6)], '+', 9),
            ([Position(4, 0), Position(3, 0)], '÷', 3),
            ([Position(3, 1), Position(4, 1)], '-', 2),
            ([Position(3, 2), Position(4, 2)], '+', 7),
            ([Position(4, 4), Position(4, 5), Position(4, 3)], 'x', 20),
            ([Position(6, 6), Position(4, 6), Position(5, 6), Position(5, 5)], '+', 15),
            ([Position(5, 0), Position(5, 1)], '÷', 2),
            ([Position(6, 2), Position(5, 2)], '-', 1),
            ([Position(5, 3), Position(6, 3)], '+', 9),
            ([Position(5, 4), Position(6, 4), Position(6, 5)], 'x', 126),
            ([Position(6, 1), Position(6, 0)], '-', 2)
        ]
        expected_solution = Grid([
            [1, 4, 7, 6, 2, 5, 3],
            [3, 1, 5, 7, 4, 6, 2],
            [7, 6, 4, 3, 1, 2, 5],
            [6, 5, 1, 2, 3, 7, 4],
            [2, 3, 6, 1, 5, 4, 7],
            [4, 2, 3, 5, 7, 1, 6],
            [5, 7, 2, 4, 6, 3, 1]
        ])
        kenken_game = KenKenSolver(regions_operators_results)

        solution = kenken_game.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_8x8_hard(self):
        regions_operators_results = [
            ([Position(1, 0), Position(0, 0)], '-', 2),
            ([Position(0, 1), Position(1, 1)], '+', 8),
            ([Position(0, 2), Position(1, 2)], '÷', 3),
            ([Position(0, 3), Position(0, 4), Position(0, 5)], '+', 11),
            ([Position(2, 3), Position(1, 3)], 'x', 6),
            ([Position(1, 4), Position(1, 5)], '-', 4),
            ([Position(2, 0), Position(3, 0)], '-', 4),
            ([Position(3, 1), Position(2, 1)], '÷', 3),
            ([Position(3, 2), Position(3, 3), Position(4, 2), Position(2, 2)], 'x', 120),
            ([Position(2, 4), Position(2, 5)], '+', 8),
            ([Position(3, 4), Position(3, 5)], '-', 3), ([Position(4, 0), Position(5, 0)], 'x', 6),
            ([Position(4, 1), Position(5, 1), Position(5, 2)], 'x', 24),
            ([Position(5, 3), Position(4, 3)], 'x', 10),
            ([Position(4, 4), Position(5, 4)], '-', 1), ([Position(4, 5), Position(5, 5)], '+', 7)
        ]
        expected_solution = Grid([
            [6, 3, 1, 4, 2, 5],
            [4, 5, 3, 1, 6, 2],
            [1, 2, 4, 6, 5, 3],
            [5, 6, 2, 3, 1, 4],
            [3, 1, 5, 2, 4, 6],
            [2, 4, 6, 5, 3, 1]
        ])
        kenken_game = KenKenSolver(regions_operators_results)

        solution = kenken_game.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_9x9_easy(self):
        regions_operators_results = [
            ([Position(1, 0), Position(2, 0), Position(0, 0)], 'x', 105),
            ([Position(0, 1), Position(1, 1)], '+', 13),
            ([Position(0, 2), Position(0, 3)], '-', 1),
            ([Position(0, 4), Position(1, 4)], '-', 3),
            ([Position(0, 5), Position(1, 5)], '÷', 4),
            ([Position(0, 7), Position(0, 6)], '-', 2),
            ([Position(0, 8), Position(1, 8), Position(2, 8)], 'x', 36),
            ([Position(1, 2), Position(1, 3)], '-', 1),
            ([Position(1, 6), Position(2, 6)], '-', 5),
            ([Position(1, 7), Position(2, 7)], 'x', 18),
            ([Position(2, 1), Position(2, 2)], '-', 7),
            ([Position(2, 3), Position(2, 4)], '÷', 3),
            ([Position(2, 5), Position(3, 5)], '÷', 3),
            ([Position(4, 0), Position(4, 1), Position(3, 0)], 'x', 64),
            ([Position(3, 1), Position(3, 2)], '+', 14),
            ([Position(3, 3), Position(3, 4)], '+', 15),
            ([Position(3, 7), Position(4, 6), Position(3, 6)], 'x', 20),
            ([Position(3, 8), Position(4, 7), Position(4, 8)], '+', 18),
            ([Position(4, 2), Position(5, 2)], '÷', 3),
            ([Position(4, 4), Position(4, 3)], 'x', 3),
            ([Position(4, 5), Position(5, 5)], '+', 12),
            ([Position(5, 0), Position(6, 0)], '-', 3),
            ([Position(6, 1), Position(5, 1)], '-', 1),
            ([Position(5, 3), Position(5, 4)], 'x', 7),
            ([Position(5, 6), Position(5, 7)], '+', 12),
            ([Position(6, 8), Position(5, 8)], '-', 3),
            ([Position(6, 2), Position(7, 2)], 'x', 21),
            ([Position(7, 5), Position(6, 3), Position(6, 4), Position(6, 5)], 'x', 2592),
            ([Position(6, 6), Position(6, 7)], 'x', 7),
            ([Position(7, 0), Position(8, 0)], '÷', 4),
            ([Position(7, 1), Position(8, 1)], '+', 6),
            ([Position(7, 4), Position(7, 3)], '+', 10),
            ([Position(7, 6), Position(8, 6)], '÷', 3),
            ([Position(7, 7), Position(7, 8)], '÷', 4),
            ([Position(8, 2), Position(8, 3)], '-', 6),
            ([Position(8, 4), Position(8, 5)], '÷', 2),
            ([Position(8, 7), Position(8, 8)], '+', 12)
        ]
        expected_solution = Grid([
            [3, 7, 4, 5, 2, 1, 6, 8, 9],
            [7, 6, 9, 8, 5, 4, 2, 3, 1],
            [5, 8, 1, 9, 3, 2, 7, 6, 4],
            [2, 9, 5, 7, 8, 6, 4, 1, 3],
            [8, 4, 2, 3, 1, 7, 5, 9, 6],
            [9, 3, 6, 1, 7, 5, 8, 4, 2],
            [6, 2, 3, 4, 9, 8, 1, 7, 5],
            [1, 5, 7, 6, 4, 9, 3, 2, 8],
            [4, 1, 8, 2, 6, 3, 9, 5, 7],
        ])
        kenken_game = KenKenSolver(regions_operators_results)

        solution = kenken_game.get_solution()
        self.assertEqual(expected_solution, solution)

    @unittest.skip("This test is too slow")
    def test_solution_9x9_hard(self):
        regions_operators_results = [
            ([Position(0, 1), Position(0, 0)], '-', 7),
            ([Position(1, 3), Position(0, 2), Position(0, 3), Position(0, 4)], 'x', 84),
            ([Position(0, 5), Position(0, 6)], '-', 1), ([Position(0, 7), Position(0, 8)], '÷', 3),
            ([Position(1, 0), Position(2, 0)], '÷', 2), ([Position(1, 1), Position(1, 2)], 'x', 24),
            ([Position(2, 4), Position(1, 4)], '+', 13), ([Position(2, 5), Position(1, 5)], '+', 13),
            ([Position(1, 6), Position(2, 6)], '÷', 2), ([Position(1, 7), Position(2, 7)], '-', 4),
            ([Position(3, 8), Position(1, 8), Position(2, 8)], 'x', 80), ([Position(3, 1), Position(2, 1)], '-', 2),
            ([Position(3, 2), Position(2, 2)], '-', 6), ([Position(2, 3), Position(3, 3)], '+', 13),
            ([Position(4, 0), Position(3, 0)], '÷', 2), ([Position(3, 4), Position(3, 5)], '-', 5),
            ([Position(3, 7), Position(3, 6)], '-', 3), ([Position(4, 1), Position(4, 2), Position(4, 3)], 'x', 80),
            ([Position(4, 4), Position(4, 5)], '÷', 2), ([Position(4, 6), Position(4, 7)], '+', 8),
            ([Position(4, 8), Position(5, 8)], '+', 13), ([Position(5, 0), Position(6, 0)], '+', 14),
            ([Position(5, 1), Position(5, 2)], '+', 10), ([Position(5, 3), Position(6, 2), Position(6, 3)], 'x', 105),
            ([Position(5, 4), Position(6, 4)], 'x', 12), ([Position(5, 5), Position(6, 5)], '÷', 2),
            ([Position(5, 6), Position(5, 7)], '-', 2), ([Position(6, 1), Position(7, 1)], '+', 13),
            ([Position(6, 6), Position(6, 7)], '÷', 4), ([Position(6, 8), Position(7, 8)], 'x', 6),
            ([Position(7, 0), Position(8, 0)], '+', 9), ([Position(7, 2), Position(7, 3)], 'x', 6),
            ([Position(7, 4), Position(7, 5)], '-', 1), ([Position(7, 6), Position(7, 7)], '-', 1),
            ([Position(8, 2), Position(8, 1)], '+', 13),
            ([Position(8, 3), Position(8, 4)], 'x', 8),
            ([Position(8, 5), Position(8, 6)], 'x', 18), ([Position(8, 7), Position(8, 8)], '-', 2)
        ]
        expected_solution = Grid([
            [1, 8, 2, 6, 7, 5, 4, 9, 3],
            [3, 4, 6, 1, 5, 9, 2, 7, 8],
            [6, 5, 7, 9, 8, 4, 1, 3, 2],
            [8, 3, 1, 4, 2, 7, 9, 6, 5],
            [4, 2, 8, 5, 6, 3, 7, 1, 9],
            [5, 1, 9, 7, 3, 2, 6, 8, 4],
            [9, 7, 5, 3, 4, 1, 8, 2, 6],
            [7, 6, 3, 2, 9, 8, 5, 4, 1],
            [2, 9, 4, 8, 1, 6, 3, 5, 7],
        ])
        kenken_game = KenKenSolver(regions_operators_results)

        solution = kenken_game.get_solution()
        self.assertEqual(expected_solution, solution)


if __name__ == '__main__':
    unittest.main()
