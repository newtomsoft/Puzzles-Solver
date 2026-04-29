import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.RegionsGrid import RegionsGrid
from Domain.Puzzles.Toichika.ToichikaSolver import ToichikaSolver


class ToichikaSolverTests(TestCase):
    def test_invalid_odd_regions(self):
        """Toichika requires an even number of regions (paired arrows)."""
        regions_grid = RegionsGrid([
            [1, 1, 2],
            [1, 2, 2],
            [3, 3, 3],
        ])

        given_arrows = Grid([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ])

        solver = ToichikaSolver(regions_grid, given_arrows)
        solution = solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_given_arrow_constraint_enforced(self):
        """A given arrow that breaks pairing rules should make puzzle unsolvable."""
        regions_grid = RegionsGrid([
            [1, 2],
            [3, 4],
        ])

        # All arrows point right, impossible to pair
        given_arrows = Grid([
            [3, 3],
            [3, 3],
        ])

        solver = ToichikaSolver(regions_grid, given_arrows)
        solution = solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_31xrr_solution(self):
        """https://gridpuzzle.com/toichika/31xrr"""
        regions_grid = RegionsGrid([
            [1, 1, 2, 3, 4],
            [5, 5, 2, 3, 3],
            [6, 5, 2, 3, 7],
            [6, 6, 2, 7, 7],
            [6, 8, 8, 8, 7],
        ])
        given_arrows = Grid([
            [0, 0, 0, 0, 0],
            [3, 0, 0, 0, 4],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 4, 0],
            [0, 0, 0, 0, 0],
        ])

        expected_solution = Grid([
            [0, 2, 3, 0, 4],
            [3, 0, 0, 0, 4],
            [0, 0, 0, 0, 0],
            [3, 0, 0, 4, 0],
            [0, 1, 0, 0, 0],
        ])

        solver = ToichikaSolver(regions_grid, given_arrows)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())

    def test_5x5_evil_0xw41(self):
        """https://gridpuzzle.com/toichika/0xw41"""
        regions_grid = RegionsGrid([
            [1, 1, 2, 3, 4],
            [2, 2, 2, 4, 4],
            [5, 5, 2, 4, 6],
            [5, 6, 6, 6, 6],
            [5, 5, 7, 7, 8],
        ])
        given_arrows = Grid([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2],
            [0, 1, 2, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [0, 2, 0, 2, 0],
            [0, 0, 0, 0, 2],
            [0, 1, 2, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 1],
        ])

        solver = ToichikaSolver(regions_grid, given_arrows)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())

    def test_7x7_evil_19jpd(self):
        """https://gridpuzzle.com/toichika/19jpd"""
        regions_grid = RegionsGrid([
            [1, 2, 3, 3, 4, 5, 5],
            [6, 2, 2, 3, 5, 5, 5],
            [6, 6, 6, 7, 7, 8, 5],
            [6, 6, 7, 7, 8, 8, 8],
            [9, 9, 7, 7, 10, 11, 8],
            [12, 13, 14, 14, 11, 11, 11],
            [13, 13, 13, 14, 14, 11, 11],
        ])
        given_arrows = Grid([
            [0, 0, 0, 4, 0, 2, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 4],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [3, 0, 0, 4, 2, 2, 0],
            [0, 2, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [3, 0, 0, 0, 0, 0, 4],
            [3, 0, 0, 0, 4, 1, 0],
            [3, 0, 4, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
        ])

        solver = ToichikaSolver(regions_grid, given_arrows)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())

    def test_9x9_evil_0d4jg(self):
        """https://gridpuzzle.com/toichika/0d4jg"""
        regions_grid = RegionsGrid([
            [1, 2, 2, 3, 4, 4, 5, 6, 6],
            [7, 8, 9, 4, 4, 4, 5, 10, 10],
            [7, 7, 9, 9, 9, 4, 5, 10, 11],
            [7, 7, 9, 12, 13, 14, 10, 10, 15],
            [7, 16, 9, 12, 12, 14, 17, 15, 15],
            [16, 16, 12, 12, 18, 19, 15, 15, 15],
            [16, 20, 20, 19, 19, 19, 21, 22, 23],
            [24, 24, 20, 20, 19, 21, 21, 21, 23],
            [24, 24, 24, 20, 19, 21, 21, 23, 23],
        ])
        given_arrows = Grid([
            [0, 0, 0, 0, 0, 0, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0],
            [1, 3, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [2, 0, 2, 2, 2, 0, 2, 0, 2],
            [0, 3, 0, 0, 0, 0, 0, 4, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 1],
            [0, 3, 0, 4, 1, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 3, 0, 0, 4, 0],
            [1, 3, 0, 0, 0, 0, 0, 4, 0],
            [0, 0, 0, 0, 3, 0, 0, 0, 4],
            [0, 0, 1, 0, 0, 1, 0, 0, 0],
        ])

        solver = ToichikaSolver(regions_grid, given_arrows)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())

    def test_12x12_evil_02ywg(self):
        """https://gridpuzzle.com/toichika/02ywg"""
        regions_grid = RegionsGrid([
            [1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4],
            [5, 2, 2, 6, 6, 6, 7, 7, 7, 7, 7, 7],
            [8, 2, 9, 6, 10, 6, 11, 11, 12, 7, 13, 13],
            [8, 14, 14, 6, 6, 6, 15, 11, 11, 11, 11, 11],
            [8, 14, 14, 14, 16, 17, 18, 19, 19, 20, 20, 20],
            [21, 21, 14, 22, 17, 17, 18, 18, 23, 20, 20, 24],
            [21, 25, 22, 22, 26, 18, 18, 18, 23, 20, 27, 27],
            [21, 25, 26, 26, 26, 26, 26, 23, 23, 27, 27, 28],
            [21, 25, 25, 26, 29, 29, 30, 30, 30, 30, 31, 28],
            [21, 25, 25, 26, 29, 29, 32, 33, 33, 33, 28, 28],
            [34, 34, 34, 34, 34, 35, 36, 37, 37, 33, 28, 28],
            [34, 36, 36, 36, 36, 36, 36, 37, 38, 33, 28, 28],
        ])
        given_arrows = Grid([
            [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0],
            [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 4, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        ])
        expected_solution = Grid([
            [3, 0, 0, 0, 0, 0, 0, 4, 0, 0, 2, 0],
            [3, 0, 0, 0, 4, 0, 0, 2, 0, 0, 0, 0],
            [0, 2, 2, 0, 3, 0, 0, 0, 4, 0, 0, 2],
            [3, 0, 0, 0, 0, 0, 4, 0, 0, 0, 1, 0],
            [0, 0, 0, 2, 2, 0, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 1],
            [0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0],
            [3, 0, 4, 0, 0, 0, 0, 1, 0, 2, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 3, 0, 0, 0, 0, 4, 0],
            [0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0],
        ])

        solver = ToichikaSolver(regions_grid, given_arrows)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())

    def test_15x15_evil_zrpkn(self):
        """https://gridpuzzle.com/toichika/zrpkn"""
        regions_grid = RegionsGrid([
            [1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4],
            [5, 5, 6, 6, 2, 2, 7, 8, 3, 9, 10, 10, 10, 11, 12],
            [5, 5, 5, 6, 13, 13, 8, 8, 3, 10, 10, 10, 11, 11, 12],
            [5, 14, 14, 6, 6, 8, 8, 8, 8, 8, 15, 15, 15, 11, 11],
            [16, 16, 17, 17, 18, 8, 19, 20, 20, 21, 22, 22, 15, 11, 23],
            [24, 25, 17, 17, 17, 19, 19, 19, 26, 21, 21, 15, 15, 23, 23],
            [25, 25, 25, 17, 17, 19, 19, 27, 26, 28, 21, 29, 29, 29, 23],
            [30, 25, 25, 31, 32, 19, 19, 27, 33, 28, 28, 29, 29, 29, 23],
            [30, 30, 30, 32, 32, 33, 33, 33, 33, 33, 28, 34, 35, 35, 36],
            [37, 37, 38, 32, 39, 39, 40, 40, 41, 28, 28, 42, 42, 35, 43],
            [44, 45, 32, 32, 39, 39, 46, 46, 41, 47, 47, 42, 42, 43, 43],
            [44, 48, 32, 49, 50, 39, 46, 51, 41, 41, 47, 42, 52, 53, 54],
            [44, 44, 44, 49, 49, 39, 51, 51, 41, 55, 55, 52, 52, 52, 54],
            [56, 57, 58, 58, 58, 59, 59, 51, 60, 60, 61, 61, 61, 62, 54],
            [56, 57, 58, 58, 58, 58, 59, 51, 60, 60, 63, 61, 62, 62, 64],
        ])
        given_arrows = Grid([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
            [0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 3, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0],
            [0, 0, 0, 0, 2, 0, 3, 0, 0, 4, 3, 0, 0, 0, 4],
            [0, 0, 3, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
            [1, 0, 2, 0, 1, 2, 0, 0, 3, 0, 0, 4, 0, 2, 0],
            [3, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2, 1, 3, 0, 0, 0, 0, 0, 4],
            [0, 1, 0, 2, 0, 0, 0, 0, 3, 0, 0, 4, 0, 0, 0],
            [0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 2, 2, 1, 0, 2],
            [2, 0, 2, 0, 0, 0, 1, 0, 3, 0, 0, 0, 4, 0, 0],
            [0, 3, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 1, 0],
            [0, 2, 0, 0, 1, 1, 3, 0, 0, 0, 0, 0, 0, 4, 0],
            [0, 0, 1, 1, 0, 0, 3, 0, 0, 4, 0, 1, 0, 0, 0],
            [1, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 4, 1],
            [0, 0, 0, 0, 3, 0, 0, 0, 4, 0, 1, 3, 0, 0, 4],
        ])

        solver = ToichikaSolver(regions_grid, given_arrows)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())


if __name__ == '__main__':
    unittest.main()
