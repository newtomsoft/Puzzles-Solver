import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.KinKonKan.KinKonKanSolver import KinKonKanSolver
from Domain.Board.RegionsGrid import RegionsGrid

_ = '.'
S = KinKonKanSolver.slash
B = KinKonKanSolver.backslash

class KinKonKanSolverTest(TestCase):
    def test_solve_4x4_evil_0x80w(self):
        """https://gridpuzzle.com/kin-kon-kan/0x80w"""
        regions_grid = RegionsGrid([
            [1, 1, 1, 1],
            [2, 1, 3, 4],
            [2, 5, 6, 7],
            [5, 5, 5, 7]
        ])
        clues = {
            'top': ['D3', 'B1', 'C2', 'C2'],
            'bottom': [_, _, _, 'A3'],
            'left': [_, _, 'D3', 'A3'],
            'right': ['B1', _, _, _]
        }
        expected_solution = Grid([
            [_, B, _, _],
            [B, _, B, S],
            [_, _, S, B],
            [_, _, S, _]
        ])

        solver = KinKonKanSolver(regions_grid, clues)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solve_5x5_evil_1yjmk(self):
        """https://gridpuzzle.com/kin-kon-kan/1yjmk"""
        regions_grid = RegionsGrid([
            [1, 2, 2, 3, 3],
            [2, 2, 4, 5, 5],
            [4, 4, 4, 6, 5],
            [4, 7, 8, 5, 5],
            [9, 10, 10, 10, 11]
        ])
        clues = {
            'top': ['C6', _, _, _, _],
            'bottom': ['B3', _, 'C6', 'A3', _],
            'left': [_, 'A3', 'D2', 'D2', _],
            'right': [_, _, _, 'B3', _]
        }
        
        expected_solution = Grid([
            [B, _, _, B, _],
            [_, B, _, _, _],
            [_, B, _, B, B],
            [_, S, S, _, _],
            [S, _, S, _, S]
        ])
        
        solver = KinKonKanSolver(regions_grid, clues)
        solution = solver.get_solution()
        self.assertEqual(expected_solution.matrix, solution.matrix)
        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solve_6x6_evil_0pg91(self):
        """https://gridpuzzle.com/kin-kon-kan/0pg91"""
        regions_grid = RegionsGrid([
            [1, 1, 2, 2, 3, 4],
            [1, 1, 5, 5, 3, 3],
            [6, 1, 5, 7, 7, 7],
            [6, 6, 8, 9, 9, 7],
            [10, 6, 8, 11, 11, 11],
            [12, 6, 8, 13, 13, 11]
        ])
        clues = {
            'top': ['', 'E3', '', 'A3', '', 'D4'],
            'bottom': ['', 'D4', '', '', '', 'B5'],
            'left': ['', 'C2', 'B5', '', '', ''],
            'right': ['E3', '', '', 'A3', '', 'C2']
        }

        expected_solution = Grid([
            [_, _, S, _, _, S],
            [_, _, _, B, B, _],
            [_, B, _, _, _, S],
            [_, _, _, _, B, _],
            [S, _, _, _, _, B],
            [B, S, S, B, _, _]
        ])

        solver = KinKonKanSolver(regions_grid, clues)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solve_8x8_evil_0vr8w(self):
        """https://gridpuzzle.com/kin-kon-kan/0vr8w"""
        regions_matrix = [
            [1, 1, 2, 2, 3, 3, 4, 5],
            [1, 6, 6, 7, 7, 8, 5, 5],
            [1, 6, 6, 9, 10, 11, 5, 5],
            [12, 9, 9, 9, 10, 11, 13, 13],
            [12, 14, 15, 16, 17, 17, 18, 18],
            [19, 19, 16, 16, 17, 18, 18, 18],
            [20, 21, 16, 16, 17, 17, 22, 23],
            [20, 21, 21, 24, 24, 22, 22, 23]
        ]
        regions_grid = RegionsGrid(regions_matrix)
        clues = {
            'top': ['G6', 'C9', _, 'E5', _, _, 'B3', 'A3'],
            'bottom': [_, _, 'D3', _, 'G6', _, 'F1', _],
            'left': [_, _, _, _, _, _, 'F1', 'D3'],
            'right': ['E5', _, 'B3', 'C9', 'A3', _, _, _]
        }

        expected_solution = Grid([
            [_, B, B, _, S, _, S, S],
            [_, _, _, B, _, B, _, _],
            [_, _, B, _, B, _, _, _],
            [B, _, B, _, _, B, _, S],
            [_, S, S, _, B, _, B, _],
            [S, _, B, _, _, _, _, _],
            [_, _, _, _, _, _, B, S],
            [S, B, _, _, B, _, _, _]
        ])

        solver = KinKonKanSolver(regions_grid, clues)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solve_9x9_evil_11516(self):
        """https://gridpuzzle.com/kin-kon-kan/11516"""
        regions_matrix = [
            [1, 2, 3, 4, 4, 4, 5, 6, 7],
            [1, 3, 3, 8, 8, 8, 5, 5, 7],
            [9, 9, 10, 8, 11, 8, 12, 13, 13],
            [14, 9, 15, 15, 11, 16, 16, 13, 17],
            [18, 19, 19, 19, 20, 21, 21, 21, 22],
            [18, 23, 19, 19, 20, 21, 21, 24, 22],
            [25, 26, 27, 20, 20, 20, 28, 29, 30],
            [31, 26, 32, 33, 33, 33, 34, 29, 35],
            [31, 31, 31, 33, 36, 33, 35, 35, 35]
        ]
        regions_grid = RegionsGrid(regions_matrix)
        clues = {
            'top': [_, _, 'G7', 'I6', 'I6', _, 'C9', 'H5', 'A5'],
            'bottom': ['E9', _, _, 'F3', _, _, _, 'B3', _],
            'left': [_, 'G7', _, _, 'F3', 'D6', 'C9', _, _],
            'right': [_, _, 'H5', 'D6', 'E9', _, 'B3', _, 'A5']
        }

        solver = KinKonKanSolver(regions_grid, clues)
        solution = solver.get_solution()

        expected_solution = Grid([
            [S, B, _, _, _, S, _, S, S],
            [_, B, _, _, _, _, S, _, _],
            [B, _, B, B, B, _, B, _, S],
            [S, _, _, B, _, B, _, _, S],
            [S, _, S, _, _, _, _, _, S],
            [_, B, _, _, _, S, _, S, _],
            [S, B, S, _, B, _, S, _, S],
            [_, _, B, _, _, _, S, S, S],
            [S, _, _, _, S, B, _, _, _]
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solve_10x10_evil_0eprg(self):
        """https://gridpuzzle.com/kin-kon-kan/0eprg"""
        regions_matrix = [
            [1, 1, 2, 3, 3, 4, 4, 5, 5, 6],
            [2, 2, 2, 3, 7, 7, 8, 5, 9, 6],
            [10, 11, 11, 12, 13, 14, 14, 15, 9, 6],
            [10, 16, 12, 12, 17, 15, 15, 15, 18, 6],
            [19, 16, 17, 17, 17, 17, 20, 20, 18, 6],
            [19, 16, 21, 22, 22, 20, 20, 23, 23, 23],
            [24, 24, 25, 25, 26, 26, 27, 23, 23, 28],
            [29, 24, 30, 31, 32, 27, 27, 27, 27, 28],
            [33, 33, 31, 31, 32, 32, 32, 34, 34, 35],
            [36, 36, 37, 37, 38, 32, 39, 39, 34, 35]
        ]
        regions_grid = RegionsGrid(regions_matrix)
        clues = {
            'top': ['H13', 'D3', _, _, 'J3', 'G8', _, 'I5', 'A3', _],
            'bottom': ['F6', _, 'E4', 'G8', 'E4', 'F6', _, 'K4', _, 'K4'],
            'left': ['I5', 'J3', _, 'C4', _, _, 'C4', 'D3', _, _],
            'right': [_, 'B6', _, _, 'H13', 'A3', _, _, _, 'B6']
        }

        solver = KinKonKanSolver(regions_grid, clues)
        solution = solver.get_solution()

        expected_solution = Grid([
            [B, _, B, S, _, _, B, _, B, B],
            [_, _, _, _, _, B, B, _, _, _],
            [B, _, B, _, B, S, _, _, B, _],
            [_, _, B, _, _, _, _, S, _, _],
            [S, S, _, B, _, _, _, _, B, _],
            [_, _, B, B, _, B, _, _, _, B],
            [_, _, _, S, S, _, S, _, _, _],
            [S, S, S, B, _, _, _, _, _, S],
            [_, S, _, _, S, _, _, _, _, B],
            [_, B, _, B, B, _, _, B, B, _]
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())


if __name__ == '__main__':
    unittest.main()
