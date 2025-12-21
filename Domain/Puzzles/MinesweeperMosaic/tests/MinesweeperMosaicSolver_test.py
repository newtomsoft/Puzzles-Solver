import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.MinesweeperMosaic.MinesweeperMosaicSolver import MinesweeperMosaicSolver

_ = MinesweeperMosaicSolver.empty


class MinesweeperMosaicSolverTests(TestCase):
    def test_solution_not_exist_2_black_adjacent(self):
        grid = Grid([
            [0, 1, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
        game_solver = MinesweeperMosaicSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_basic_grid(self):
        grid = Grid([
            [0, 0, 0],
            [0, 1, 1],
            [0, 1, 1]
        ])
        game_solver = MinesweeperMosaicSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 1]
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12(self):
        grid = Grid([
            [3, 5, 4, 2, _],
            [_, _, _, 3, _],
            [_, 3, _, 3, _],
            [_, 3, 2, _, _],
            [3, _, 1, 1, _]
        ])
        game_solver = MinesweeperMosaicSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [1, 0, 0, 0, 1],
            [1, 1, 0, 0, 0]
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
