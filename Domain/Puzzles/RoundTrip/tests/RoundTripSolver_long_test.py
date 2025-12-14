import unittest

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Puzzles.RoundTrip.RoundTripSolver import RoundTripSolver


class RoundTripSolverLongTests(unittest.TestCase):
    def test_solution_12x12_evil_2kv1d(self):
        """https://gridpuzzle.com/round-trip/2kv1d"""
        grid_str = (
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  │  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  · ─── ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  · '
        )
        clues = {
            Direction.down(): [6, 5, 3, 3, 3, 2, _, 2, 2, _, 3, 6],
            Direction.left(): [2, 3, 2, 6, 2, 2, _, 3, 7, 6, 5, 2],
            Direction.up(): [3, _, _, 2, 2, 2, 9, 2, 2, 6, 5, _],
            Direction.right(): [8, 3, 5, _, _, _, 4, 7, 4, 3, 2, 6],
        }

        expected_solution_string = (
            ' ┌────────────────────┐  ·  ·  ┌──┐ \n'
            ' │  ·  ·  ·  ┌─────┐  └─────┐  │  │ \n'
            ' │  ·  ·  ┌──┼─────┼──┐  ·  └──┘  │ \n'
            ' │  ┌──┐  │  └─────┼──┼─────┐  ·  │ \n'
            ' │  │  │  └──┐  ·  │  │  ·  └──┐  │ \n'
            ' └──┼──┘  ┌──┘  ┌──┼──┘  ·  ·  └──┘ \n'
            ' ·  │  ┌──┼─────┘  │  ┌──┐  ┌─────┐ \n'
            ' ·  └──┼──┼────────┼──┘  └──┼──┐  │ \n'
            ' ┌─────┼──┘  ·  ┌──┼────────┼──┼──┘ \n'
            ' │  ┌──┼──┐  ┌──┘  └────────┼──┼──┐ \n'
            ' └──┘  │  └──┘  ·  ·  ┌─────┼──┼──┘ \n'
            ' ·  ·  └──────────────┘  ·  └──┘  · '
        )

        game_solver = RoundTripSolver(Grid.from_str(grid_str, type(Island)), clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
