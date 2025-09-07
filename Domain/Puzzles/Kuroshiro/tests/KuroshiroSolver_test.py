import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Puzzles.Kuroshiro.KuroshiroSolver import KuroshiroSolver

_ = ''
B = '■'
W = '□'


class KuroshiroSolverTests(TestCase):
    def test_solution_3x3_black_neighbors(self):
        grid = Grid([
            [B, _, B],
            [_, _, _],
            [B, _, B],
        ])
        expected_solution_str = (
            ' ┌─────┐ \n'
            ' │  ·  │ \n'
            ' └─────┘ '
        )
        game_solver = KuroshiroSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_5x5_black_neighbors(self):
        grid = Grid([
            [B, _, _, B, _],
            [_, _, _, B, B],
            [_, _, _, B, B],
            [B, B, _, _, _],
            [_, B, _, B, _],
        ])
        expected_solution_str = (
            ' ┌────────┐  · \n'
            ' │  ·  ·  └──┐ \n'
            ' │  ·  ·  ┌──┘ \n'
            ' └──┐  ·  │  · \n'
            ' ·  └─────┘  · '
        )
        game_solver = KuroshiroSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_5x5_white_neighbors(self):
        grid = Grid([
            [W, _, _, W, _],
            [_, _, _, W, W],
            [_, _, _, W, W],
            [W, W, _, _, _],
            [_, W, _, W, _],
        ])
        expected_solution_str = (
            ' ┌────────┐  · \n'
            ' │  ·  ·  └──┐ \n'
            ' │  ·  ·  ┌──┘ \n'
            ' └──┐  ·  │  · \n'
            ' ·  └─────┘  · '
        )
        game_solver = KuroshiroSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_10x10_black_neighbors(self):
        grid = Grid([
            [_, B, B, _, _, B, _, B, _, _],
            [_, B, B, _, B, _, _, B, _, B],
            [_, _, _, _, _, _, _, _, _, _],
            [_, B, _, B, B, B, _, B, _, B],
            [_, _, _, _, _, _, _, _, _, _],
            [B, _, _, B, _, _, _, _, B, B],
            [_, _, _, _, _, _, _, B, B, _],
            [B, _, B, _, _, B, _, B, _, _],
            [_, B, B, _, _, _, _, B, _, B],
            [_, B, _, _, _, B, _, _, _, _],
        ])
        expected_solution_str = (
            ' ·  ┌──┐  ·  ·  ┌─────┐  ·  · \n'
            ' ·  │  └─────┐  │  ·  └─────┐ \n'
            ' ·  │  ·  ·  │  │  ·  ·  ·  │ \n'
            ' ·  └─────┐  └──┘  ·  ┌─────┘ \n'
            ' ·  ·  ·  │  ·  ·  ·  │  ·  · \n'
            ' ┌────────┘  ·  ·  ·  │  ┌──┐ \n'
            ' │  ·  ·  ·  ·  ·  ·  └──┘  │ \n'
            ' └─────┐  ·  ·  ┌─────┐  ·  │ \n'
            ' ·  ┌──┘  ·  ·  │  ·  └─────┘ \n'
            ' ·  └───────────┘  ·  ·  ·  · '
        )
        game_solver = KuroshiroSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_5x5_292p8(self):
        # https://gridpuzzle.com/kuroshiro/l2x85
        grid = Grid([
            [B, B, B, _, B],
            [_, W, _, B, B],
            [_, W, W, B, B],
            [_, _, W, W, W],
            [B, B, _, _, _],
        ])
        expected_solution_str = (
            ' ┌───────────┐ \n'
            ' └──┐  ┌──┐  │ \n'
            ' ┌──┘  │  └──┘ \n'
            ' │  ·  └─────┐ \n'
            ' └───────────┘ '
        )
        game_solver = KuroshiroSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
