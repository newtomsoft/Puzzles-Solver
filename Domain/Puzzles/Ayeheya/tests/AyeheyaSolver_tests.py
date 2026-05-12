import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Ayeheya.AyeheyaSolver import AyeheyaSolver

_ = -1


class AyeheyaSolverTests(TestCase):
    def test_integration_puzzlink_11x11(self):
        """https://puzz.link/p?ayeheya/11/11/j7j1j1h1hi0i0i0i0papap0v003o03vvs000003vu000g3q3g3j"""
        grid = Grid([
            [_, 3, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, 3, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, 3, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _],
        ])
        region_grid = Grid([
            [0, 1, 1, 1, 2, 3, 3, 3, 4, 5, 6],
            [0, 1, 1, 1, 2, 7, 7, 7, 7, 7, 6],
            [0, 1, 1, 1, 2, 7, 7, 7, 7, 7, 6],
            [0, 8, 8, 8, 8, 7, 7, 7, 7, 7, 6],
            [0, 8, 8, 8, 8, 9, 10, 10, 10, 11, 11],
            [12, 12, 12, 12, 12, 12, 13, 13, 13, 11, 11],
            [12, 12, 12, 12, 12, 12, 13, 13, 13, 11, 11],
            [12, 12, 12, 12, 12, 12, 13, 13, 13, 11, 11],
            [12, 12, 12, 12, 12, 12, 14, 15, 15, 15, 16],
            [17, 17, 18, 18, 19, 19, 14, 15, 15, 15, 16],
            [17, 17, 18, 18, 19, 19, 14, 15, 15, 15, 16],
        ])

        expected_solution = Grid([
            [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1],
            [0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0],
            [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1],
            [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
        ])

        solver = AyeheyaSolver(grid, region_grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())


if __name__ == '__main__':
    unittest.main()
