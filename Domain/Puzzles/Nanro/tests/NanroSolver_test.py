import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Nanro.NanroSolver import NanroSolver

_ = 0


class NanroSolverTests(TestCase):
    def test_solution_basic(self):
        values_grid = Grid([
            [1, _, 2],
            [_, _, _],
            [_, 3, _],
        ])
        regions_grid = Grid([
            [1, 2, 3],
            [1, 2, 3],
            [2, 2, 3],
        ])

        expected_solution = Grid([
            [1, 3, 2],
            [_, 3, _],
            [_, 3, 2]
        ])
        game = NanroSolver(values_grid, regions_grid)

        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_no_adjacent_constraint(self):
        values_grid = Grid([
            [3, _, _, 3],
            [_, _, _, 3],
            [_, 2, 1, _],
            [_, _, _, _],
        ])
        regions_grid = Grid([
            [1, 1, 2, 2],
            [1, 3, 2, 2],
            [3, 3, 4, 4],
            [3, 3, 4, 4],
        ])

        expected_solution = Grid([
            [3, 3, _, 3],
            [3, _, 3, 3],
            [2, 2, 1, _],
            [_, _, _, _]
        ])
        game = NanroSolver(values_grid, regions_grid)

        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_easy(self):
        values_grid = Grid([
            [2, _, 3, _, _],
            [2, _, _, 2, _],
            [_, 4, _, _, 3],
            [2, _, _, _, _],
            [2, 4, _, 2, _],
        ])
        regions_grid = Grid([
            [1, 2, 2, 2, 3],
            [1, 1, 3, 3, 3],
            [1, 4, 4, 5, 5],
            [6, 6, 4, 7, 5],
            [6, 4, 4, 7, 5]
        ])

        expected_solution = Grid([
            [2, 3, 3, 3, 2],
            [2, _, _, 2, _],
            [_, 4, 4, 3, 3],
            [2, _, _, 2, _],
            [2, 4, 4, 2, 3]
        ])
        game = NanroSolver(values_grid, regions_grid)

        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_easy_3jgny(self):
        """https://gridpuzzle.com/nanro/3jqny"""
        values_grid = Grid([
            [2, _, _, _, _],
            [2, _, _, 2, _],
            [_, 4, _, _, 3],
            [2, _, _, _, _],
            [2, 4, _, _, _],
        ])
        regions_grid = Grid([
            [1, 2, 2, 2, 3],
            [1, 1, 3, 3, 3],
            [1, 4, 4, 5, 5],
            [6, 6, 4, 7, 5],
            [6, 4, 4, 7, 5]
        ])

        expected_solution = Grid([
            [2, 3, 3, 3, 2],
            [2, _, _, 2, _],
            [_, 4, 4, 3, 3],
            [2, _, _, 2, _],
            [2, 4, 4, 2, 3]
        ])
        game = NanroSolver(values_grid, regions_grid)

        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_expert_1n61r(self):
        """https://gridpuzzle.com/nanro/1n61r"""
        values_grid = Grid([
            [_, _, _, _, 2],
            [_, 4, _, _, _],
            [_, 3, _, _, 3],
            [2, _, _, 1, _],
            [2, 4, _, _, _]
        ])
        regions_grid = Grid([
            [1, 2, 2, 3, 3],
            [1, 2, 2, 4, 3],
            [1, 1, 2, 4, 4],
            [5, 5, 6, 6, 6],
            [5, 7, 7, 7, 7]
        ])

        expected_solution = Grid([
            [3, 4, 4, 2, 2],
            [_, 4, _, 3, _],
            [3, 3, 4, 3, 3],
            [2, _, _, 1, _],
            [2, 4, 4, 4, 4]
        ])
        game = NanroSolver(values_grid, regions_grid)

        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_evil_21jy5(self):
        """https://gridpuzzle.com/nanro/21jy5"""
        values_grid = Grid([
            [0, 0, 3, 0, 0],
            [0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 2, 0, 3, 0],
            [4, 0, 0, 0, 0]
        ])
        regions_grid = Grid([
            [1, 1, 1, 1, 2],
            [3, 3, 3, 1, 2],
            [3, 4, 5, 6, 2],
            [4, 4, 5, 6, 6],
            [5, 5, 5, 6, 6]
        ])

        expected_solution = Grid([
            [0, 0, 3, 3, 0],
            [3, 3, 0, 3, 2],
            [3, 0, 4, 0, 2],
            [2, 2, 4, 3, 3],
            [4, 0, 4, 0, 3]
        ])
        game = NanroSolver(values_grid, regions_grid)

        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_7x7_hard_1502d(self):
        """https://gridpuzzle.com/nanro/1502d"""
        values_grid = Grid([
            [_, 3, _, 2, _, _, _],
            [_, _, 2, _, _, _, _],
            [3, _, _, _, _, _, 1],
            [3, 3, _, _, 3, _, _],
            [_, _, 2, _, _, _, 4],
            [4, _, _, _, 3, _, _],
            [4, _, _, _, _, 4, 4]
        ])
        regions_grid = Grid([
            [1, 1, 1, 2, 2, 2, 3],
            [4, 5, 5, 5, 6, 6, 3],
            [4, 4, 5, 6, 6, 7, 7],
            [4, 4, 8, 9, 9, 9, 7],
            [10, 10, 8, 11, 11, 9, 12],
            [10, 8, 8, 11, 11, 12, 12],
            [10, 10, 10, 13, 13, 12, 12]
        ])

        expected_solution = Grid([
            [3, 3, 3, 2, 2, _, 2],
            [_, _, 2, _, 4, 4, 2],
            [3, _, 2, 4, 4, _, 1],
            [3, 3, _, _, 3, 3, _],
            [_, 4, 2, 3, _, 3, 4],
            [4, 2, _, 3, 3, 4, _],
            [4, _, 4, 1, _, 4, 4]
        ])
        game = NanroSolver(values_grid, regions_grid)

        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    @unittest.skip("This test is too slow, needs to be fixed (49 seconds)")
    def test_solution_7x7_evil_yw0gp(self):
        """https://gridpuzzle.com/nanro/yw0gp"""
        values_grid = Grid([
            [_, _, _, 2, _, 3, _],
            [3, _, _, _, _, _, _],
            [_, 4, _, _, _, _, _],
            [_, _, _, 2, _, _, 4],
            [4, _, _, _, _, _, _],
            [_, _, _, _, _, _, 2],
            [4, 4, _, _, 2, _, _]
        ])
        regions_grid = Grid([
            [1, 1, 1, 2, 2, 3, 3],
            [4, 1, 5, 2, 3, 3, 6],
            [4, 1, 5, 7, 7, 7, 6],
            [4, 1, 5, 8, 8, 6, 6],
            [9, 10, 8, 8, 11, 6, 6],
            [9, 10, 10, 10, 11, 12, 12],
            [9, 9, 9, 9, 11, 11, 11]
        ])

        expected_solution = Grid([
            [4, 4, 4, 2, 2, 3, 3],
            [3, _, 3, _, 3, _, 4],
            [3, 4, 3, _, 2, 2, _],
            [3, _, 3, 2, _, 4, 4],
            [4, _, 2, _, 2, 4, _],
            [_, 3, 3, 3, _, 2, 2],
            [4, 4, _, 4, 2, _, _]
        ])
        game = NanroSolver(values_grid, regions_grid)

        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    @unittest.skip("This test is too slow, needs to be fixed (8 minutes)")
    def test_solution_7x7_evil_0py8g(self):
        """https://gridpuzzle.com/nanro/0py8g"""
        values_grid = Grid([
            [4, _, _, _, _, _, _],
            [_, 4, _, _, _, 3, _],
            [4, _, 2, _, _, _, 3],
            [_, 4, _, 2, _, 3, _],
            [_, _, 3, _, _, _, 2],
            [_, _, _, _, _, 3, _],
            [_, _, _, _, _, _, _]
        ])
        regions_grid = Grid([
            [1, 1, 1, 2, 2, 2, 2],
            [1, 1, 3, 4, 4, 5, 5],
            [1, 3, 3, 4, 4, 5, 5],
            [6, 6, 7, 7, 7, 5, 8],
            [6, 9, 9, 7, 10, 8, 8],
            [6, 11, 9, 12, 10, 13, 13],
            [6, 11, 11, 12, 10, 13, 13]
        ])

        expected_solution = Grid([
            [4, 4, _, 4, 4, 4, 4],
            [_, 4, _, 3, _, 3, _],
            [4, 2, 2, 3, 3, _, 3],
            [_, 4, _, 2, _, 3, 2],
            [4, 3, 3, 2, _, _, 2],
            [4, _, 3, _, 2, 3, 3],
            [4, 2, 2, 1, 2, _, 3]
        ])
        game = NanroSolver(values_grid, regions_grid)

        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12_hard_117q0(self):
        """https://gridpuzzle.com/nanro/117q0"""
        values_grid = Grid([
            [0, 0, 0, 2, 0, 6, 6, 0, 4, 0, 4, 0], [0, 6, 0, 0, 5, 0, 0, 0, 0, 0, 0, 6], [0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 5, 0, 0, 0, 0, 6, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 2, 4, 0, 3, 0, 5, 0, 5, 5], [0, 5, 0, 0, 4, 0, 0, 5, 0, 0, 2, 0],
             [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0], [0, 3, 0, 4, 0, 0, 0, 0, 3, 0, 0, 4], [2, 0, 0, 0, 0, 0, 0, 5, 0, 3, 0, 0], [2, 0, 0, 0, 0, 0, 3, 0, 0, 0, 2, 0]
        ])
        regions_grid = Grid([
            [1, 1, 1, 2, 3, 4, 4, 4, 5, 5, 5, 6], [1, 1, 2, 2, 3, 4, 4, 4, 7, 5, 5, 6], [1, 1, 8, 8, 3, 4, 4, 7, 7, 7, 6, 6], [9, 9, 8, 8, 3, 3, 3, 7, 7, 6, 6, 6],
             [9, 8, 8, 8, 3, 10, 7, 7, 11, 11, 11, 6], [9, 9, 12, 12, 12, 10, 10, 7, 11, 11, 11, 11], [9, 9, 13, 12, 14, 10, 10, 10, 15, 15, 11, 11],
             [16, 9, 13, 14, 14, 14, 14, 15, 15, 15, 17, 17], [16, 16, 13, 13, 18, 18, 18, 15, 19, 17, 17, 20], [16, 16, 21, 21, 22, 18, 22, 22, 19, 19, 20, 20],
             [23, 23, 24, 21, 22, 22, 22, 22, 19, 19, 20, 20], [23, 21, 21, 21, 25, 25, 25, 25, 26, 26, 26, 26]
        ])

        expected_solution = Grid([
            [6, 6, 6, 2, 0, 6, 6, 6, 4, 4, 4, 6],
            [0, 6, 0, 2, 5, 6, 0, 6, 0, 4, 0, 6],
            [6, 6, 5, 5, 0, 6, 0, 0, 6, 6, 0, 6],
            [5, 0, 5, 0, 5, 5, 5, 6, 6, 0, 6, 6],
            [0, 5, 5, 0, 5, 0, 0, 6, 0, 5, 0, 6],
            [5, 0, 0, 2, 0, 3, 3, 6, 0, 5, 5, 0],
            [5, 5, 3, 2, 4, 0, 3, 0, 5, 0, 5, 5],
            [0, 5, 0, 0, 4, 4, 4, 5, 5, 5, 2, 0],
            [3, 0, 3, 3, 0, 2, 0, 5, 0, 0, 2, 4],
            [3, 3, 0, 4, 5, 2, 5, 0, 3, 0, 0, 4],
            [2, 0, 1, 0, 5, 0, 5, 5, 3, 3, 4, 4],
            [2, 4, 4, 4, 3, 3, 3, 0, 2, 0, 2, 0]
        ])
        game = NanroSolver(values_grid, regions_grid)

        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12_hard_1181d(self):
        """https://gridpuzzle.com/nanro/1181d"""
        values_grid = Grid([
            [_, 5, _, _, _, _, _, _, 5, _, _, 5],
            [5, 5, _, _, _, 4, _, 4, _, _, _, _],
            [5, _, _, _, _, _, _, _, _, _, 5, _],
            [_, _, 5, _, 5, _, 5, _, _, _, 3, _],
            [2, _, _, _, _, _, _, 2, _, 3, _, _],
            [_, 4, _, _, _, _, 4, _, 5, _, _, 5],
            [_, _, _, _, _, _, _, _, _, 2, _, _],
            [2, _, _, _, 5, _, _, 2, _, _, _, 6],
            [_, _, 3, 3, _, 4, _, _, _, _, 6, _],
            [_, _, _, _, _, _, 3, _, _, 6, _, _],
            [2, _, _, _, _, 5, _, _, _, _, _, 2],
            [_, 6, _, _, _, _, _, _, _, 6, _, _]
        ])
        regions_grid = Grid([
            [1, 1, 2, 2, 2, 2, 2, 3, 4, 4, 4, 4],
            [1, 1, 2, 5, 5, 2, 3, 3, 3, 4, 4, 4],
            [1, 1, 5, 5, 5, 6, 3, 3, 7, 4, 8, 8],
            [1, 1, 5, 5, 6, 6, 6, 9, 7, 10, 10, 8],
            [11, 12, 12, 13, 6, 6, 9, 9, 7, 10, 10, 8],
            [11, 12, 12, 14, 15, 15, 15, 9, 7, 7, 8, 8],
            [16, 16, 12, 14, 14, 15, 15, 17, 7, 18, 8, 19],
            [16, 14, 14, 14, 14, 15, 17, 17, 17, 18, 18, 19],
            [16, 20, 20, 20, 20, 21, 21, 21, 21, 19, 19, 19],
            [22, 22, 22, 20, 23, 24, 24, 24, 19, 19, 19, 25],
            [26, 22, 22, 20, 23, 23, 24, 27, 27, 27, 27, 25],
            [26, 22, 22, 23, 23, 23, 24, 24, 27, 27, 27, 25]
        ])

        expected_solution = Grid([
            [_, 5, 4, 4, _, 4, _, 4, 5, 5, 5, 5],
            [5, 5, _, 5, 5, 4, _, 4, _, 5, _, _],
            [5, _, 5, 5, _, 5, 4, 4, 5, _, 5, 5],
            [5, _, 5, _, 5, _, 5, _, 5, _, 3, _],
            [2, _, 4, 1, 5, 5, 2, 2, 5, 3, 3, 5],
            [2, 4, 4, _, 4, _, 4, _, 5, _, _, 5],
            [_, _, 4, 5, 5, 4, 4, 2, 5, 2, 5, 6],
            [2, 5, 5, _, 5, _, _, 2, _, 2, _, 6],
            [2, _, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6],
            [6, 6, 6, _, 5, _, 3, _, _, 6, _, 2],
            [2, _, 6, _, 5, 5, 3, 6, 6, _, 6, 2],
            [2, 6, 6, 5, 5, _, 3, _, 6, 6, 6, _]
        ])
        game = NanroSolver(values_grid, regions_grid)

        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12_expert_12w6k(self):
        """https://gridpuzzle.com/nanro/12w6k"""
        values_grid = Grid([
            [_, _, _, _, _, _, 4, _, _, _, 6, _],
            [_, _, 2, _, 4, _, _, _, _, 3, 6, _],
            [2, _, _, _, _, _, _, 2, 3, _, _, _],
            [6, _, 2, _, _, 2, 2, _, 5, _, 5, _],
            [_, _, _, _, _, _, _, 5, _, _, _, 5],
            [_, _, _, _, _, _, _, _, _, 2, _, 5],
            [_, _, _, _, 4, _, _, 6, _, _, _, _],
            [6, _, 5, _, _, _, _, _, _, 5, _, _],
            [_, _, _, _, 5, _, 3, _, _, _, _, 6],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, 2, _, _, _, 2, _, _, _, _, _],
            [_, _, 4, _, _, 3, _, 2, _, _, 4, _]
        ])
        regions_grid = Grid([
            [1, 1, 2, 3, 4, 4, 4, 5, 6, 6, 6, 6],
            [1, 2, 2, 3, 3, 4, 4, 5, 7, 7, 6, 6],
            [8, 8, 8, 3, 3, 9, 4, 5, 7, 7, 6, 6],
            [10, 10, 11, 11, 11, 9, 9, 12, 12, 13, 13, 13],
            [10, 10, 10, 11, 12, 12, 12, 12, 12, 13, 13, 13],
            [14, 15, 10, 10, 16, 16, 16, 17, 17, 17, 13, 13],
            [14, 15, 15, 16, 16, 16, 18, 19, 19, 20, 13, 21],
            [14, 15, 15, 22, 22, 22, 18, 19, 19, 20, 20, 21],
            [14, 15, 15, 22, 22, 22, 18, 19, 19, 20, 20, 21],
            [14, 14, 23, 22, 22, 24, 24, 19, 20, 20, 25, 21],
            [14, 23, 23, 23, 23, 24, 26, 19, 25, 25, 25, 21],
            [14, 27, 27, 27, 27, 24, 26, 26, 25, 25, 25, 21]
        ])

        expected_solution = Grid([
            [3, 3, 2, 4, _, 4, 4, 2, 6, _, 6, 6],
            [3, _, 2, _, 4, _, 4, _, 3, 3, 6, _],
            [2, 2, _, 4, 4, _, 4, 2, 3, _, 6, 6],
            [6, _, 2, 2, _, 2, 2, _, 5, _, 5, _],
            [6, 6, 6, _, 5, _, 5, 5, 5, _, 5, 5],
            [_, _, 6, 6, 4, 4, 4, _, 2, 2, _, 5],
            [6, 5, 5, _, 4, _, 3, 6, 6, _, 5, 6],
            [6, _, 5, _, 5, 5, 3, _, 6, 5, _, 6],
            [6, 5, 5, _, 5, _, 3, 6, _, 5, 5, 6],
            [6, _, 2, 5, 5, 3, _, 6, 5, 5, _, 6],
            [6, _, 2, _, _, 3, 2, 6, _, 4, _, 6],
            [6, 4, 4, 4, 4, 3, _, 2, 4, 4, 4, 6]
        ])
        game = NanroSolver(values_grid, regions_grid)

        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12_evil_12xwd(self):
        """https://gridpuzzle.com/nanro/12xwd"""
        values_grid = Grid([
            [4, 4, _, _, _, _, 5, _, _, _, _, 3],
            [_, _, _, _, _, 6, _, _, _, _, _, _],
            [_, _, _, 2, _, _, _, 3, _, _, _, _],
            [4, _, _, 3, _, _, _, _, _, _, 3, _],
            [_, 4, _, _, 6, _, _, _, _, _, 3, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, 6, _, _, _, 5, _, _, 6],
            [_, _, _, _, _, _, _, _, _, _, 4, _],
            [_, _, _, 5, _, _, 3, _, _, 6, _, _],
            [_, _, _, _, _, _, _, 2, 2, _, _, _],
            [_, _, _, 4, _, 2, _, 6, _, _, _, _],
            [_, _, 2, _, _, _, _, _, 4, _, 2, _]
        ])
        regions_grid = Grid([
            [1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 4, 4],
            [1, 1, 2, 2, 2, 2, 3, 5, 5, 3, 4, 4],
            [6, 1, 7, 7, 7, 2, 5, 5, 5, 8, 9, 4],
            [6, 10, 10, 10, 10, 10, 11, 11, 12, 8, 9, 9],
            [6, 13, 13, 14, 11, 11, 11, 11, 12, 8, 9, 8],
            [6, 13, 13, 14, 14, 11, 11, 12, 12, 8, 8, 8],
            [6, 13, 13, 14, 14, 14, 15, 12, 12, 16, 16, 8],
            [6, 17, 14, 14, 15, 15, 15, 15, 16, 16, 16, 16],
            [6, 17, 17, 17, 17, 15, 15, 18, 19, 19, 19, 19],
            [6, 17, 17, 20, 20, 20, 20, 18, 18, 18, 18, 19],
            [6, 21, 21, 21, 22, 22, 20, 20, 23, 23, 24, 19],
            [6, 25, 25, 21, 21, 22, 20, 23, 23, 23, 24, 24]
        ])

        expected_solution = Grid([
            [4, 4, 0, 6, 6, 5, 5, 5, 0, 5, 3, 3],
            [0, 4, 6, 6, 0, 6, 0, 3, 3, 5, 0, 3],
            [0, 4, 0, 2, 2, 6, 0, 3, 0, 6, 3, 0],
            [4, 3, 3, 3, 0, 0, 6, 6, 5, 0, 3, 0],
            [0, 4, 0, 0, 6, 6, 6, 0, 5, 6, 3, 6],
            [0, 4, 4, 6, 0, 0, 6, 5, 0, 6, 0, 6],
            [0, 4, 0, 6, 6, 6, 0, 5, 5, 4, 4, 6],
            [4, 5, 6, 6, 0, 3, 3, 0, 4, 0, 4, 0],
            [0, 5, 0, 5, 0, 0, 3, 0, 6, 6, 6, 6],
            [4, 5, 5, 6, 6, 6, 6, 2, 2, 0, 0, 6],
            [0, 4, 0, 4, 0, 2, 0, 6, 0, 4, 0, 6],
            [4, 2, 2, 4, 4, 2, 6, 4, 4, 4, 2, 2]
        ])
        game = NanroSolver(values_grid, regions_grid)

        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12_evil_24xm8(self):
        """https://gridpuzzle.com/nanro/24xm8"""
        values_grid = Grid([
            [2, _, _, _, _, 5, _, _, _, _, _, _],
            [_, _, _, _, 4, _, _, _, 2, _, 2, _],
            [3, _, _, 2, 3, _, _, 5, _, _, _, _],
            [_, 4, _, _, 3, _, _, _, _, _, _, 5],
            [2, _, _, _, 6, _, 5, _, _, _, _, _],
            [_, _, 2, _, _, _, _, _, _, _, 2, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, 6, _],
            [_, 6, _, 2, 3, _, _, _, 3, 3, _, _],
            [2, _, _, _, 3, 6, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, 3],
            [_, _, _, _, 5, _, 5, 4, _, _, _, _]
        ])
        regions_grid = Grid([
            [1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 4, 5],
            [1, 6, 2, 2, 2, 7, 8, 4, 4, 4, 4, 5],
            [6, 6, 6, 9, 7, 7, 8, 8, 8, 8, 5, 5],
            [10, 10, 10, 9, 7, 7, 11, 11, 11, 5, 5, 5],
            [12, 13, 10, 9, 14, 7, 11, 11, 11, 11, 15, 15],
            [12, 13, 13, 13, 14, 14, 11, 16, 16, 16, 16, 15],
            [12, 12, 14, 14, 14, 14, 14, 17, 18, 18, 15, 15],
            [19, 19, 20, 20, 21, 17, 17, 17, 17, 18, 22, 22],
            [23, 19, 19, 20, 21, 17, 24, 24, 18, 18, 22, 22],
            [23, 19, 19, 21, 21, 17, 24, 24, 25, 22, 22, 22],
            [23, 19, 26, 21, 26, 24, 24, 25, 25, 25, 27, 27],
            [23, 26, 26, 26, 26, 26, 24, 25, 25, 27, 27, 27]
        ])

        expected_solution = Grid([
            [2, _, 4, 4, 5, 5, _, 5, 5, 5, _, 5],
            [2, 3, 4, _, 4, _, 5, _, 2, _, 2, 5],
            [3, _, 3, 2, 3, 3, 5, 5, 5, 5, _, 5],
            [4, 4, 4, _, 3, _, _, _, _, _, 5, 5],
            [2, _, 4, 2, 6, _, 5, 5, 5, 5, _, 3],
            [_, 2, 2, _, 6, 6, 5, _, _, 2, 2, 3],
            [2, _, 6, 6, 6, _, _, 6, _, 3, _, 3],
            [6, 6, 2, _, 3, 6, 6, 6, 6, _, 6, 6],
            [_, 6, _, 2, 3, _, 5, _, 3, 3, _, 6],
            [2, 6, 6, _, 3, 6, 5, 5, _, 6, 6, 6],
            [_, 6, _, _, 5, _, 5, _, 4, 4, _, 3],
            [2, 5, 5, 5, 5, _, 5, 4, 4, _, 3, 3]
        ])
        game = NanroSolver(values_grid, regions_grid)

        solution = game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
