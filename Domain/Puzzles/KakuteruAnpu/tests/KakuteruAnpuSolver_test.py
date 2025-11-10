import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Puzzles.KakuteruAnpu.KakuteruAnpuSolver import KakuteruAnpuSolver

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


if __name__ == '__main__':
    unittest.main()
