import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Fobidoshi.FobidoshiSolver import FobidoshiSolver

_ = -1


class FobidoshiSolverTests(TestCase):
    def test_initial_constraint(self):
        grid = Grid([
            [1, 1, 0, 1],
            [0, 1, 1, 1],
            [1, 1, 1, 0],
            [1, 0, 1, 1],
        ])
        expected_grid = Grid([
            [1, 1, 0, 1],
            [0, 1, 1, 1],
            [1, 1, 1, 0],
            [1, 0, 1, 1],
        ])
        game_solver = FobidoshiSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_horizontally_constraint(self):
        grid = Grid([
            [1, 1, 1, _],
            [_, 1, 1, 1],
            [0, 0, 0, 1],
            [_, 1, 1, 1]
        ])
        expected_grid = Grid([
            [1, 1, 1, 0],
            [0, 1, 1, 1],
            [0, 0, 0, 1],
            [0, 1, 1, 1]
        ])
        game_solver = FobidoshiSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_vertically_constraint(self):
        grid = Grid([
            [_, 0, _, 1],
            [1, 0, 1, 1],
            [1, 0, 1, 1],
            [1, 1, 1, _],
        ])
        expected_grid = Grid([
            [0, 0, 0, 1, ],
            [1, 0, 1, 1, ],
            [1, 0, 1, 1, ],
            [1, 1, 1, 0, ]
        ])
        game_solver = FobidoshiSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_connectivity_constraint(self):
        grid = Grid([
            [1, 1, 1, _],
            [_, 1, 1, 1],
            [0, 0, 0, _],
            [_, 1, _, 1]
        ])
        expected_grid = Grid([
            [1, 1, 1, 0],
            [0, 1, 1, 1],
            [0, 0, 0, 1],
            [0, 1, 1, 1]
        ])
        game_solver = FobidoshiSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_hard_31j59(self):
        """https://gridpuzzle.com/fobidoshi/31j59"""
        grid = Grid([
            [1, _, 1, 0],
            [_, 1, _, 1],
            [1, _, 1, _],
            [0, _, _, _]
        ])
        expected_grid = Grid([
            [1, 1, 1, 0],
            [0, 1, 1, 1],
            [1, 1, 1, 0],
            [0, 0, 0, 0]
        ])
        game_solver = FobidoshiSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_evil_088v2(self):
        """https://gridpuzzle.com/fobidoshi/088v2"""
        grid = Grid([
            [_, 1, _, _, _, 1],
            [_, 0, _, _, _, _],
            [_, 1, _, _, _, 1],
            [_, 1, _, _, _, _],
            [_, _, _, _, 0, 1],
            [_, 1, _, _, _, 1]
        ])
        expected_grid = Grid([
            [0, 1, 1, 1, 0, 1],
            [0, 0, 0, 1, 1, 1],
            [0, 1, 1, 1, 0, 1],
            [1, 1, 1, 0, 0, 0],
            [1, 0, 1, 1, 0, 1],
            [1, 1, 0, 1, 1, 1],
        ])
        game_solver = FobidoshiSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_evil_2pwe9(self):
        """https://gridpuzzle.com/fobidoshi/2pwe9"""
        grid = Grid([
            [_, 1, 1, 1, _, _, _, _],
            [1, 1, _, 1, 1, _, 0, 1],
            [1, _, _, _, 1, 1, 1, _],
            [1, 1, _, 1, 1, _, 1, 1],
            [_, _, 1, 1, _, 1, 1, _],
            [_, _, _, 1, 1, 1, _, 1],
            [_, 0, 1, _, _, _, _, _],
            [_, 1, _, _, 1, _, _, 1],
        ])
        expected_grid = Grid([
            [0, 1, 1, 1, 0, 1, 1, 1],
            [1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 1, 1, 0],
            [1, 1, 0, 1, 1, 0, 1, 1],
            [0, 1, 1, 1, 0, 1, 1, 1],
            [1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 0],
            [1, 1, 1, 0, 1, 0, 1, 1]
        ])
        game_solver = FobidoshiSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_evil_22wr9(self):
        """https://gridpuzzle.com/fobidoshi/22wr9"""
        grid = Grid([
            [1, _, _, 1, 1, 1, _, _, 1, _],
            [_, 1, _, _, _, _, 1, _, _, _],
            [1, _, 0, _, _, 1, _, 1, _, 1],
            [_, _, 1, _, _, 1, _, 1, 1, _],
            [_, 1, _, _, _, _, 0, _, _, _],
            [1, _, 1, 0, _, _, 1, _, _, _],
            [_, _, _, 1, _, 1, _, _, _, _],
            [_, _, _, _, _, 1, 1, 0, _, _],
            [_, 1, _, 1, 1, _, _, _, _, _],
            [1, _, _, _, 1, 1, 1, _, _, _]
        ])
        expected_grid = Grid([
            [1, 1, 0, 1, 1, 1, 0, 0, 1, 1],
            [0, 1, 1, 1, 0, 0, 1, 1, 0, 1],
            [1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 0, 1, 0, 1, 1, 0],
            [1, 1, 1, 0, 1, 1, 0, 0, 1, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
            [0, 1, 1, 1, 0, 1, 1, 0, 1, 0],
            [1, 1, 0, 1, 1, 0, 1, 1, 1, 0],
            [1, 0, 0, 0, 1, 1, 1, 0, 0, 0]
        ])
        game_solver = FobidoshiSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12_evil_2d0q8(self):
        """https://gridpuzzle.com/fobidoshi/2d0q8"""
        grid = Grid([
            [_, 1, 1, 1, _, _, 1, 1, 1, _, 1, _],
            [_, _, 1, _, _, 1, 1, _, _, 1, _, 1],
            [_, _, _, _, _, 1, _, 1, 1, _, 1, _],
            [_, _, _, _, 1, _, 1, _, _, 0, _, _],
            [1, _, 1, _, 1, 1, _, 1, 1, _, _, _],
            [_, 1, 1, 0, _, 1, 1, _, 1, 1, _, _],
            [_, _, 1, _, _, 1, 1, 1, 0, 1, _, _],
            [_, _, _, _, _, _, _, 1, 1, _, 1, _],
            [_, 1, 0, 1, _, 1, 1, _, 1, 1, 1, _],
            [_, _, _, _, _, _, _, _, _, _, _, 1],
            [_, _, _, 1, _, _, _, _, 1, _, _, _],
            [1, _, _, _, 1, _, 1, _, _, _, _, _],
        ])
        expected_grid = Grid([
            [0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1],
            [0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
            [1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1],
            [1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0],
            [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
            [0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1],
            [1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0],
            [1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
            [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1]
        ])
        game_solver = FobidoshiSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
