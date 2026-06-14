from unittest import TestCase

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles import GameSolver
from PuzzleSolver.Puzzles.Yakazu.YakazuSolver import YakazuSolver

_ = GameSolver.cell_empty
x = True
o = False


class YakazuSolverTests(TestCase):
    def test_5x5_evil_0x271(self):
        """https://gridpuzzle.com/yakazu/0x271"""
        clues_grid = Grid([
            [_, 3, _, 2, _],
            [4, _, 2, _, 2],
            [5, _, _, _, 3],
            [_, 3, _, 5, _],
            [3, _, 1, _, 5],
        ])
        blacks_grid = Grid([
            [o, o, o, o, o],
            [o, x, o, x, o],
            [o, x, o, x, o],
            [o, o, o, o, o],
            [o, x, o, x, o],
        ])

        expected_solution = Grid([
            [1, 3, 5, 2, 4],
            [4, 0, 2, 0, 2],
            [5, 0, 3, 0, 3],
            [2, 3, 4, 5, 1],
            [3, 0, 1, 0, 5],
        ])

        game_solver = YakazuSolver(clues_grid, blacks_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_12x12_evil_0d1gw(self):
        """https://gridpuzzle.com/yakazu/0d1gw"""
        clues_grid = Grid([
            [_, _, 1, _, _, _, _, _, _ ,2, _, _],
            [4, _, _, 4, _, 5, 6, _ ,2, _, _ ,5],
            [_, _, _, _, 1, _, _, 2, _, _, _, _],
            [_, _, _, _, _, 1, 2, _, _, _, _, _],
            [5, _, _, _, _, 4, 3, _, _, _, _ ,6],
            [3, _, _, _, _, _, _, _, _, _, _ ,1],
            [_, _, _, _, 2, _, _, 1, _, _, _, _],
            [1, _, 2, _, 1, _, _, 2, _ ,1, _, 3],
            [3, _, _, _, _, _, _, _, _, _, _, 4],
            [4, _, _, _, 7, _, _, 8, _, _, _, 2],
            [_, _, 7, _, _, 1, 3, _, _, 6, _, _],
            [_, 1, _, _, _, _, _, _, _, _, 3, _],
        ])
        blacks_grid = Grid([
            [o, o, o, x, o, x, x, o, x, o, o, o],
            [o, x, x, o, o, o, o, o, o, x, x, o],
            [o, x, o, o, o, x, x, o, o, o, x, o],
            [o, o, x, o, x, o, o, x, o, x, o, o],
            [o, x, o, o, o, o, o, o, o, o, x, o],
            [o, o, o, x, o, o, o, o, x, o, o, o],
            [x, x, o, x, o, o, o, o, x, o, x, x],
            [o, x, o, o, o, x, x, o, o, o, x, o],
            [o, x, o, o, o, o, o, o, o, o, x, o],
            [o, x, o, o, o, o, o, o, o, o, x, o],
            [o, x, o, o, o, o, o, o, o, o, x, o],
            [o, o, o, o, o, x, x, o, o, o, o, o],
        ])

        expected_solution = Grid([
            [2, 3, 1, 0, 2, 0, 0, 3, 0, 2, 1, 3],
            [4, 0, 0, 4, 3, 5, 6, 1, 2, 0, 0, 5],
            [6, 0, 2, 3, 1, 0, 0, 2, 3, 1, 0, 4],
            [1, 2, 0, 1, 0, 1, 2, 0, 4, 0, 1, 2],
            [5, 0, 8, 2, 5, 4, 3, 6, 1, 7, 0, 6],
            [3, 2, 1, 0, 4, 2, 1, 3, 0, 3, 2, 1],
            [0, 0, 5, 0, 2, 3, 4, 1, 0, 5, 0, 0],
            [1, 0, 2, 3, 1, 0, 0, 2, 3, 1, 0, 3],
            [3, 0, 3, 5, 6, 2, 1, 7, 4, 8, 0, 4],
            [4, 0, 6, 1, 7, 3, 2, 8, 5, 4, 0, 2],
            [2, 0, 7, 4, 8, 1, 3, 5, 2, 6, 0, 1],
            [5, 1, 4, 2, 3, 0, 0, 4, 1, 2, 3, 5],
        ])

        game_solver = YakazuSolver(clues_grid, blacks_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

if __name__ == '__main__':
    import unittest
    unittest.main()
