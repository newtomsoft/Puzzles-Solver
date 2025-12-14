import unittest

from Domain.Board.Grid import Grid
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Puzzles.EverySecondTurn.EverySecondTurnSolver import EverySecondTurnSolver

_ = '.'
X = '*'


class EverySecondTurnSolverLongTests(unittest.TestCase):
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
