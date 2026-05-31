from unittest import TestCase

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.IslandsGrid import IslandGrid
from PuzzleSolver.Puzzles.ArukoneNo2x2.ArukoneNo2x2Solver import ArukoneNo2x2Solver

_ = ArukoneNo2x2Solver.empty


class ArukoneNo2x2SolverTests(TestCase):
    def test_basic_solution_with_3_same_neighbours(self):
        grid = Grid([
            [_, _, _, 3],
            [_, 2, _, _],
            [_, 2, _, 3],
            [_, 1, _, 1]
        ])
        expected_solution = Grid([
            [1, 1, 1, 3],
            [1, 2, 1, 3],
            [1, 2, 1, 3],
            [1, 1, 1, 1]
        ])

        game_solver = ArukoneNo2x2Solver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_15x15_51670(self):
        """https://gridpuzzle.com/arukone-no-2x2/51670"""
        grid = Grid([
            [11, _, _, _, _, 28, 16, _, 24, _, 20, _, _, _, _],
            [_, _, _, 29, _, _, _, _, 3, _, _, _, _, 5, _],
            [_, _, 29, 13, _, _, _, _, _, _, _, 20, _, _, _],
            [_, _, _, _, 8, _, _, _, _, 24, 5, _, _, _, 16],
            [_, 11, _, 9, _, _, _, _, 3, _, _, _, _, _, 1],
            [_, _, _, 21, _, _, 28, _, _, _, 15, _, _, _, 22],
            [_, 21, _, _, 8, _, _, 14, _, 14, _, 1, 22, _, 25],
            [_, 18, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, 9, _, 6, _, _, _, _, _, _, _, _, 15, _],
            [27, _, _, _, 26, _, _, 26, _, 13, 31, 18, _, 25, _],
            [_, 19, _, _, _, _, _, _, _, _, _, _, _, 4, _],
            [_, 27, _, 6, _, _, 31, _, _, 10, _, _, _, 12, _],
            [_, 2, _, 32, _, _, 32, _, _, _, _, _, _, _, _],
            [19, 30, _, _, 23, _, _, _, 10, _, _, _, 4, _, _],
            [30, _, 2, 23, 7, _, 7, _, _, _, 12, 17, _, _, 17],
        ])
        expected_solution = Grid([
            [11, 13, 13, 13, 13, 28, 16, 16, 24, 24, 20, 20, 20, 20, 20],
            [11, 13, 29, 29, 13, 28, 28, 16, 3, 24, 5, 5, 5, 5, 20],
            [11, 13, 29, 13, 13, 13, 28, 16, 3, 24, 5, 20, 20, 20, 20],
            [11, 13, 13, 13, 8, 13, 28, 16, 3, 24, 5, 16, 16, 16, 16],
            [11, 11, 9, 9, 8, 13, 28, 16, 3, 16, 16, 16, 1, 1, 1],
            [9, 9, 9, 21, 8, 13, 28, 16, 16, 16, 15, 1, 1, 22, 22],
            [9, 21, 21, 21, 8, 13, 13, 14, 14, 14, 15, 1, 22, 22, 25],
            [9, 18, 18, 18, 18, 18, 13, 13, 13, 13, 15, 15, 15, 15, 25],
            [9, 9, 9, 6, 6, 18, 18, 18, 18, 13, 31, 31, 31, 15, 25],
            [27, 27, 27, 6, 26, 26, 26, 26, 18, 13, 31, 18, 31, 25, 25],
            [19, 19, 27, 6, 32, 32, 32, 32, 18, 18, 18, 18, 31, 4, 4],
            [19, 27, 27, 6, 32, 31, 31, 32, 10, 10, 31, 31, 31, 12, 4],
            [19, 2, 2, 32, 32, 31, 32, 32, 10, 31, 31, 12, 12, 12, 4],
            [19, 30, 2, 23, 23, 31, 31, 31, 10, 31, 12, 12, 4, 4, 4],
            [30, 30, 2, 23, 7, 7, 7, 31, 31, 31, 12, 17, 17, 17, 17]
        ])

        game_solver = ArukoneNo2x2Solver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)
