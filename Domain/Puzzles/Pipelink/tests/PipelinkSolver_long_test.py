import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Puzzles.Pipelink.PipelinkSolver import PipelinkSolver


class PipelinkSolverTests(TestCase):
    def test_solution_12x12_evil_41d1p(self):
        """https://gridpuzzle.com/pipelink/41d1p"""
        grid_str = (
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  · ─┘  ·  └─ ·  · ─┘  · \n'
            ' · ─── ·  └─ ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  · ─── ·  └─ ·  │  · \n'
            ' ·  · ─── ·  │  ┌─ ·  │  ·  ·  ·  │ \n'
            ' ·  · ─── ·  ·  ·  │  ·  ·  ┌─ ·  · \n'
            ' └─ ·  ·  · ─┐  ·  ·  · ─┼─ ·  └─ · \n'
            ' ·  · ─┘  ·  ·  · ─── ·  │  ·  ·  · \n'
            ' · ─── ·  ·  ·  ·  ·  ·  ·  · ─── · \n'
            ' ·  ·  · ─┐  │  ·  ┌─ · ─┐  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  │  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  └─ ·  ·  └─ · '
        )
        game_solver = PipelinkSolver(Grid.from_str(grid_str, type(Island)))

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐  ┌────────┐  ┌──┐  ┌──┐  ┌──┐ \n'
            ' │  └──┘  ┌─────┘  │  └──┘  └──┘  │ \n'
            ' └─────┐  └─────┐  └─────┐  ┌──┐  │ \n'
            ' ┌─────┘  ┌──┐  └─────┐  └──┘  │  │ \n'
            ' │  ┌─────┘  │  ┌──┐  │  ┌─────┘  │ \n'
            ' │  └─────┐  └──┘  │  │  │  ┌──┐  │ \n'
            ' └─────┐  └──┐  ┌──┘  └──┼──┘  └──┘ \n'
            ' ┌─────┘  ┌──┘  └─────┐  │  ┌─────┐ \n'
            ' └─────┐  └──┐  ┌─────┘  └──┼─────┘ \n'
            ' ┌──┐  └──┐  │  │  ┌─────┐  └─────┐ \n'
            ' │  └─────┘  │  │  │  ┌──┘  ┌──┐  │ \n'
            ' └───────────┘  └──┘  └─────┘  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_15x15_evil_029dr(self):
        """https://gridpuzzle.com/pipelink/029dr"""
        grid_str = (
            ' ·  ·  ·  ·  ·  ·  ·  ┌─ ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  └─ ·  └─ ·  ·  ·  ·  ·  ·  ·  │  ·  · \n'
            ' │  · ─┐  ·  ·  ·  ┌─ ·  ┌──┼─ ·  │  │  · ─┐ \n'
            ' ·  ·  ·  ·  └─ ·  ·  ·  ·  ·  └─ ·  ·  ·  · \n'
            ' · ─┘  ·  ·  · ─┼──┐  └──┐  ·  ·  ·  ·  └─ · \n'
            ' ·  ·  ·  ┌─ ·  ·  ·  ·  └─ · ─┘  ┌─ ·  ┌─ · \n'
            ' ·  ·  ┌─ ·  · ─── ·  ·  ·  ·  ·  · ─┐  ·  · \n'
            ' · ─── · ─┐  ·  ·  └─ ·  └─ ·  ·  ┌─ ·  ┌─ · \n'
            ' ·  · ─┘  ·  ·  ·  ·  ·  ·  └─ ·  · ─┐  ·  · \n'
            ' ·  └─ ·  └──┼─ ·  └─ ·  ·  ·  · ─┐  ·  ·  · \n'
            ' ·  ┌─ ·  ·  ·  · ─┐  └─────── ·  ·  ·  ┌─ · \n'
            ' ·  ·  ·  · ─┐  ·  ·  ·  ·  ·  └─ ·  ·  ·  · \n'
            ' ┌─ ·  └──── ·  │  ┌─ · ─┘  ·  ·  · ─── ·  │ \n'
            ' ·  · ─┐  ·  ·  ·  ·  ·  ·  ·  │  · ─── ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  └─ ·  ·  ·  ·  ·  ·  · '
        )
        game_solver = PipelinkSolver(Grid.from_str(grid_str, type(Island)))

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐  ┌─────┐  ┌──┐  ┌─────┐  ┌──┐  ┌─────┐ \n'
            ' │  │  └──┐  └──┘  └──┼─────┼──┘  │  │  ┌──┘ \n'
            ' │  └──┐  │  ┌──┐  ┌──┘  ┌──┼──┐  │  │  └──┐ \n'
            ' └──┐  └──┘  └──┼──┘  ┌──┘  │  └──┼──┘  ┌──┘ \n'
            ' ┌──┘  ┌────────┼──┐  └──┐  └──┐  └──┐  └──┐ \n'
            ' │  ┌──┘  ┌─────┘  └──┐  └─────┘  ┌──┘  ┌──┘ \n'
            ' └──┘  ┌──┘  ┌─────┐  └──┐  ┌──┐  └──┐  └──┐ \n'
            ' ┌─────┼──┐  └──┐  └──┐  └──┼──┘  ┌──┘  ┌──┘ \n'
            ' │  ┌──┘  │  ┌──┼──┐  └──┐  └──┐  └──┐  └──┐ \n'
            ' │  └──┐  └──┼──┘  └──┐  └─────┼──┐  └─────┘ \n'
            ' │  ┌──┘  ┌──┘  ┌──┐  └────────┼──┼──┐  ┌──┐ \n'
            ' └──┼──┐  └──┐  │  └──┐  ┌──┐  └──┘  └──┘  │ \n'
            ' ┌──┘  └─────┘  │  ┌──┼──┘  │  ┌────────┐  │ \n'
            ' │  ┌──┐  ┌──┐  └──┼──┼─────┘  │  ┌─────┘  │ \n'
            ' └──┘  └──┘  └─────┘  └────────┘  └────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
