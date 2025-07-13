import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Puzzles.Geradeweg.GeradewegSolver import GeradewegSolver

_ = 0


class GeradewegSolverTests(TestCase):
    def test_solution_4x4_31409(self):
        # https://gridpuzzle.com/straight-loop/31409
        grid = Grid([
            [_, _, _, _],
            [_, 1, 1, _],
            [2, _, _, 1],
            [_, 3, 3, _]
        ])
        expected_solution_str = (
            ' ·  ┌─────┐ \n'
            ' ┌──┘  ┌──┘ \n'
            ' │  ·  └──┐ \n'
            ' └────────┘ '
        )

        game_solver = GeradewegSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_4x4_314er(self):
        # https://gridpuzzle.com/straight-loop/314er
        grid = Grid([
            [_, _, _, _],
            [2, _, _, 3],
            [_, 1, 2, _],
            [_, _, _, _]
        ])
        expected_solution_str = (
            ' ┌────────┐ \n'
            ' │  ┌──┐  │ \n'
            ' └──┘  │  │ \n'
            ' ·  ·  └──┘ '
        )

        game_solver = GeradewegSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_8x8_0mmy1(self):
        # https://gridpuzzle.com/straight-loop/0mmy1
        grid = Grid([
            [_, 4, _, _, _, _, 1, _],
            [_, _, _, _, _, _, _, _],
            [_, _, 2, _, _, 3, _, _],
            [_, _, _, _, _, _, _, _],
            [_, 3, _, _, _, _, 4, _],
            [7, _, _, 3, 3, _, _, 7],
            [_, _, _, _, _, _, _, _],
            [_, 2, _, _, _, _, 3, _]
        ])
        expected_solution_str = (
            ' ┌───────────┐  ·  ┌──┐ \n'
            ' │  ┌──┐  ·  └─────┘  │ \n'
            ' │  │  │  ┌────────┐  │ \n'
            ' │  │  └──┘  ┌──┐  │  │ \n'
            ' │  └────────┘  │  │  │ \n'
            ' │  ·  ┌────────┘  │  │ \n'
            ' │  ·  │  ·  ┌─────┘  │ \n'
            ' └─────┘  ·  └────────┘ '
        )

        game_solver = GeradewegSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_12x12_020r8(self):
        # https://gridpuzzle.com/straight-loop/020r8
        grid = Grid([
            [_, _, 4, _, _, _, _, _, 4, _, _, _],
            [6, _, _, _, _, 2, 2, 1, _, _, _, _],
            [_, _, 2, _, _, _, _, 1, _, _, _, _],
            [_, _, _, 3, _, _, _, _, _, _, 5, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, 1, _, _, 1, _, _, 3, _, _],
            [_, _, _, _, _, _, _, 2, _, _, _, _],
            [_, _, 2, 2, _, _, _, _, _, 2, _, 5],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, 5, _, _, 3, _, _],
            [2, 1, _, 2, _, 4, _, _, 4, _, _, _],
            [_, _, 3, _, _, _, _, _, _, _, _, _]
        ])
        expected_solution_str = (
            ' ┌───────────┐  ┌──┐  ┌───────────┐ \n'
            ' │  ·  ·  ┌──┘  │  │  └──┐  ·  ┌──┘ \n'
            ' │  ┌─────┘  ┌──┘  └──┐  │  ·  │  · \n'
            ' │  └────────┘  ┌─────┘  └──┐  │  · \n'
            ' │  ┌─────┐  ·  │  ┌──┐  ·  │  │  · \n'
            ' │  │  ┌──┘  ·  └──┘  │  ·  │  │  · \n'
            ' └──┘  │  ┌────────┐  └─────┘  └──┐ \n'
            ' ┌─────┘  │  ┌──┐  │  ·  ┌─────┐  │ \n'
            ' └─────┐  └──┘  │  │  ·  │  ┌──┘  │ \n'
            ' ┌──┐  │  ┌──┐  │  │  ·  │  │  ·  │ \n'
            ' │  └──┘  │  │  │  │  ·  │  │  ·  │ \n'
            ' └────────┘  └──┘  └─────┘  └─────┘ '
        )

        game_solver = GeradewegSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
