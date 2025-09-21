import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Puzzles.EverySecondTurn.EverySecondTurnSolver import EverySecondTurnSolver

_ = '.'
X = '*'


class EverySecondTurnSolverTests(TestCase):
    def test_solution_6_6_37g81(self):
        """https://gridpuzzle.com/every-second-turn/37g81"""

        grid = Grid([
            [_, _, _, _, _, X],
            [_, X, _, _, _, _],
            [_, _, _, _, X, _],
            [X, _, _, X, _, _],
            [_, _, X, _, _, X],
            [X, _, _, _, _, _],
        ])
        expected_solution_str = (
            ' ┌──────────────┐ \n'
            ' │  ┌────────┐  │ \n'
            ' │  │  ┌─────┘  │ \n'
            ' └──┘  │  ┌─────┘ \n'
            ' ┌─────┘  └─────┐ \n'
            ' └──────────────┘ '
        )

        game_solver = EverySecondTurnSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_6_6_3e9k2(self):
        """https://gridpuzzle.com/every-second-turn/3e9k2"""

        grid = Grid([
            [X, _, _, _, _, _],
            [_, _, _, _, _, X],
            [_, _, X, _, _, _],
            [_, _, _, _, X, _],
            [_, X, _, _, _, _],
            [_, _, _, _, _, X]
        ])
        expected_solution_str = (
            ' ┌──────────────┐ \n'
            ' │  ┌───────────┘ \n'
            ' │  │  ┌────────┐ \n'
            ' │  │  └─────┐  │ \n'
            ' │  └────────┘  │ \n'
            ' └──────────────┘ '
        )

        game_solver = EverySecondTurnSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_10_10_0ygm8(self):
        """https://gridpuzzle.com/every-second-turn/0ygm8"""

        grid = Grid([
            [X, _, _, _, _, X, _, _, X, _],
            [_, _, _, X, _, _, _, X, _, _],
            [_, _, X, _, _, _, X, _, _, _],
            [_, X, _, _, X, _, _, _, X, _],
            [X, _, _, _, X, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, X, _],
            [_, X, _, X, _, _, X, _, _, _],
            [_, _, _, X, _, X, _, X, _, X],
            [_, X, _, _, X, _, _, _, X, _],
            [_, _, X, _, _, _, _, _, _, X]
        ])
        expected_solution_str = (
            ' ┌───────────┐  ┌─────┐  ┌──┐ \n'
            ' │  ┌─────┐  │  │  ┌──┘  │  │ \n'
            ' │  │  ┌──┘  │  │  └─────┘  │ \n'
            ' └──┘  │  ┌──┘  └────────┐  │ \n'
            ' ┌──┐  │  │  ┌───────────┘  │ \n'
            ' │  │  │  │  └───────────┐  │ \n'
            ' │  └──┘  └─────┐  ┌─────┘  │ \n'
            ' │  ┌─────┐  ┌──┘  └──┐  ┌──┘ \n'
            ' │  └──┐  │  └────────┘  └──┐ \n'
            ' └─────┘  └─────────────────┘ '
        )

        game_solver = EverySecondTurnSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_16_16_0zny2(self):
        """https://gridpuzzle.com/every-second-turn/0zny2"""

        grid = Grid([
            [X, _, X, _, X, _, X, _, _, _, _, _, _, _, X, _],
            [_, _, _, _, _, X, _, _, X, _, _, _, X, _, _, _],
            [_, _, _, X, _, _, _, X, _, X, _, _, _, X, _, _],
            [_, _, _, X, _, X, X, _, _, _, _, X, _, _, _, X],
            [_, X, _, _, X, _, _, _, X, _, X, _, X, _, X, _],
            [_, _, _, _, X, _, _, _, _, X, _, X, _, X, _, _],
            [X, _, _, _, _, X, _, _, _, _, _, X, _, _, X, _],
            [_, X, _, X, X, _, _, X, _, X, X, _, X, _, _, X],
            [X, _, X, _, _, X, _, _, _, X, _, _, X, X, _, _],
            [_, _, X, _, _, X, _, X, _, _, _, X, _, _, _, X],
            [X, _, _, _, X, _, _, _, X, _, _, X, _, X, _, _],
            [_, X, _, _, _, _, X, _, X, _, X, _, _, _, X, _],
            [_, _, X, X, _, _, _, X, _, _, X, _, _, X, _, _],
            [X, _, _, _, _, X, X, _, _, X, _, _, X, _, _, X],
            [_, X, _, _, X, _, _, X, X, _, _, X, _, _, _, _],
            [_, _, _, X, _, _, X, _, _, X, _, _, _, _, _, X]
        ])
        expected_solution_str = (
            ' ┌──┐  ┌──┐  ┌──┐  ┌────────────────────┐  ┌──┐ \n'
            ' │  │  │  │  │  └──┘  ┌──┐  ┌────────┐  │  │  │ \n'
            ' │  │  │  └──┘  ┌─────┘  │  └─────┐  │  └──┘  │ \n'
            ' │  │  └──┐  ┌──┘  ┌─────┘  ┌─────┘  └────────┘ \n'
            ' │  └─────┘  └──┐  │  ┌──┐  │  ┌──┐  ┌──┐  ┌──┐ \n'
            ' └───────────┐  │  │  │  │  └──┘  └──┘  └──┘  │ \n'
            ' ┌────────┐  └──┘  │  │  │  ┌─────┐  ┌─────┐  │ \n'
            ' └──┐  ┌──┘  ┌──┐  └──┘  └──┘  ┌──┘  └──┐  └──┘ \n'
            ' ┌──┘  └──┐  │  └────────┐  ┌──┘  ┌──┐  └─────┐ \n'
            ' └─────┐  │  └──┐  ┌──┐  │  │  ┌──┘  │  ┌─────┘ \n'
            ' ┌──┐  │  │  ┌──┘  │  │  └──┘  │  ┌──┘  └─────┐ \n'
            ' │  └──┘  │  └─────┘  └──┐  ┌──┘  │  ┌─────┐  │ \n'
            ' └─────┐  └────────┐  ┌──┘  │  ┌──┘  │  ┌──┘  │ \n'
            ' ┌──┐  │  ┌─────┐  └──┘  ┌──┘  │  ┌──┘  └─────┘ \n'
            ' │  └──┘  │  ┌──┘  ┌──┐  └──┐  │  └───────────┐ \n'
            ' └────────┘  └─────┘  └─────┘  └──────────────┘ '
        )

        game_solver = EverySecondTurnSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
