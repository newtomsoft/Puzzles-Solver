import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.KakuteruAnpu.KakuteruAnpuSolver import KakuteruAnpuSolver

_ = None


class KakuteruAnpuSolverTest(TestCase):
    def test_basic_grid(self):
        regions_grid = Grid([
            [1, 2, 2],
            [1, 1, 2],
            [3, 3, 3],
        ])
        numbers_grid = Grid([
            [2, 2, _],
            [_, _, _],
            [1, _, _]
        ])
        expected_solution = Grid([
            [1, 0, 1],
            [1, 0, 1],
            [0, 1, 0]
        ])
        game_solver = KakuteruAnpuSolver(numbers_grid, regions_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_basic_with_empty_region(self):
        regions_grid = Grid([
            [1, 1, 2, 2],
            [1, 3, 4, 2],
            [1, 3, 4, 5],
            [6, 6, 5, 5],
        ])
        numbers_grid = Grid([
            [4, _, 1, _],
            [_, _, 2, _],
            [_, _, _, _],
            [1, _, 1, _]
        ])
        expected_solution = Grid([
            [1, 1, 0, 1],
            [1, 0, 1, 0],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
        ])
        game_solver = KakuteruAnpuSolver(numbers_grid, regions_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_evil_5x5_7px1k(self):
        """https://gridpuzzle.com/cocktail-lamp/7px1k"""
        regions_grid = Grid([
            [1, 1, 2, 2, 2],
            [3, 4, 5, 6, 2],
            [3, 4, 5, 6, 6],
            [4, 4, 7, 8, 8],
            [4, 7, 7, 7, 8],
        ])
        numbers_grid = Grid([
            [1, _, 3, _, _],
            [1, _, 1, 1, _],
            [_, _, _, _, _],
            [4, _, _, 1, _],
            [_, 2, _, _, _],
        ])
        expected_solution = Grid([
            [0, 1, 0, 1, 1],
            [1, 0, 1, 0, 1],
            [0, 1, 0, 1, 0],
            [1, 1, 0, 0, 1],
            [1, 0, 1, 1, 0],
        ])
        game_solver = KakuteruAnpuSolver(numbers_grid, regions_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_evil_5x5_kd1x5(self):
        """https://gridpuzzle.com/cocktail-lamp/kd1x5"""
        regions_grid = Grid([
            [1, 1, 2, 2, 2],
            [1, 1, 3, 3, 2],
            [3, 3, 3, 2, 2],
            [3, 4, 4, 5, 6],
            [4, 4, 4, 5, 6],
        ])
        numbers_grid = Grid([
            [2, _, 4, _, _],
            [_, _, _, _, _],
            [5, _, _, _, _],
            [_, _, _, _, 1],
            [2, _, _, _, _],
        ])
        expected_solution = Grid([
            [1, 1, 0, 1, 1],
            [0, 0, 1, 0, 1],
            [1, 1, 1, 0, 1],
            [1, 0, 0, 1, 0],
            [0, 1, 1, 0, 1],
        ])
        game_solver = KakuteruAnpuSolver(numbers_grid, regions_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_evil_5x5_56209(self):
        """https://gridpuzzle.com/cocktail-lamp/56209"""
        regions_grid = Grid([
            [1, 2, 3, 3, 3],
            [1, 2, 3, 3, 4],
            [5, 5, 6, 6, 4],
            [5, 6, 6, 7, 7],
            [5, 6, 7, 7, 7],
        ])
        numbers_grid = Grid([
            [1, _, 4, _, _],
            [_, _, _, _, 1],
            [3, _, _, _, _],
            [_, 2, _, _, _],
            [_, _, 2, _, _],
        ])
        expected_solution = Grid([
            [1, 0, 1, 1, 1],
            [0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0],
            [1, 0, 0, 1, 1],
        ])
        game_solver = KakuteruAnpuSolver(numbers_grid, regions_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_evil_6x6_7j2rk(self):
        """https://gridpuzzle.com/cocktail-lamp/7j2rk"""
        regions_grid = Grid([
            [1, 1, 1, 2, 3, 3],
            [4, 5, 1, 2, 6, 3],
            [4, 5, 5, 2, 6, 6],
            [4, 4, 4, 7, 8, 8],
            [9, 7, 7, 7, 7, 8],
            [9, 9, 9, 7, 8, 8],
        ])
        numbers_grid = Grid([
            [1, _, _, 1, 1, _],
            [3, 1, _, _, 2, _],
            [_, _, _, _, _, _],
            [_, _, _, _, 4, _],
            [1, 4, _, _, _, _],
            [_, _, _, _, _, _],
        ])
        expected_solution = Grid([
            [0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1, 0],
            [1, 0, 1, 0, 1, 0],
            [1, 0, 0, 1, 0, 1],
            [0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 1],
        ])
        game_solver = KakuteruAnpuSolver(numbers_grid, regions_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    @unittest.skip("temporarily disabled - takes too long")
    def test_solution_evil_15x15_mkkjw(self):
        """https://gridpuzzle.com/cocktail-lamp/mkkjw"""
        regions_grid = Grid([
            [1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 5, 6, 6, 6],
            [7, 1, 2, 2, 3, 3, 8, 3, 3, 4, 4, 5, 9, 6, 9],
            [7, 10, 10, 11, 8, 8, 8, 8, 3, 3, 4, 5, 9, 9, 9],
            [7, 12, 10, 11, 8, 8, 8, 8, 8, 8, 13, 13, 14, 14, 9],
            [12, 12, 11, 11, 8, 15, 15, 16, 16, 16, 13, 14, 14, 9, 9],
            [12, 12, 12, 11, 15, 15, 15, 17, 16, 16, 13, 13, 14, 18, 9],
            [19, 19, 20, 11, 15, 21, 15, 17, 13, 13, 13, 14, 14, 18, 18],
            [22, 20, 20, 11, 15, 21, 15, 17, 17, 13, 13, 18, 18, 18, 18],
            [22, 22, 20, 23, 23, 21, 21, 17, 17, 24, 24, 24, 24, 18, 18],
            [25, 23, 23, 23, 23, 21, 26, 27, 27, 27, 24, 24, 28, 28, 28],
            [25, 25, 23, 29, 23, 30, 26, 31, 31, 27, 24, 32, 28, 33, 33],
            [34, 34, 34, 29, 29, 30, 30, 30, 35, 27, 27, 32, 28, 28, 33],
            [36, 36, 29, 29, 30, 30, 37, 37, 35, 35, 27, 32, 32, 32, 33],
            [36, 36, 29, 29, 29, 30, 37, 37, 37, 38, 27, 39, 40, 40, 40],
            [29, 29, 29, 29, 37, 37, 37, 38, 38, 38, 27, 39, 40, 40, 40]
        ])
        numbers_grid = Grid([
            [2, _, _, _, _, _, _, _, 5, _, _, _, 1, _, _],
            [1, _, 3, _, 1, _, _, _, _, _, _, _, 7, _, _],
            [_, 1, _, _, 7, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [1, _, 2, _, _, _, _, 3, _, _, _, 2, _, _, _],
            [_, _, _, _, 7, _, _, 3, _, _, _, _, _, _, _],
            [1, _, _, _, _, 1, _, _, 5, _, _, _, _, _, _],
            [1, 3, _, _, _, _, _, _, _, _, _, 8, _, _, _],
            [_, _, _, _, _, _, _, _, _, 4, _, _, _, _, _],
            [1, 7, _, _, _, _, 1, _, _, _, _, _, 1, _, _],
            [_, _, _, _, _, _, _, 1, _, _, _, 4, _, 2, _],
            [1, _, _, _, _, _, _, _, 1, _, _, _, _, _, _],
            [3, _, _, _, 4, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, 1, 3, _, _],
            [7, _, _, _, 5, _, _, 1, _, _, _, _, _, _, _]
        ])
        expected_solution = Grid([
            [1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0],
            [0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1],
            [0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
            [0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1],
            [0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1],
            [0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1],
            [0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
            [0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0],
            [1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
            [0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1],
        ])
        game_solver = KakuteruAnpuSolver(numbers_grid, regions_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        # other_solution = game_solver.get_other_solution()
        # self.assertEqual(Grid.empty(), other_solution)

    @unittest.skip("temporarily disabled - takes too long")
    def test_solution_evil_15x15_v6kd4(self):
        """https://gridpuzzle.com/cocktail-lamp/v6kd4"""
        pass
        

if __name__ == '__main__':
    unittest.main()
