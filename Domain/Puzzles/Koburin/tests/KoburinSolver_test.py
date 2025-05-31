from unittest import TestCase

from Domain.Board.Grid import Grid
from Puzzles.Koburin.KoburinSolver import KoburinSolver

_ = -1


class KoburinSolverTests(TestCase):
    def test_solution_3x3_digit_0(self):
        grid = Grid([
            [_, _, _],
            [_, 0, _],
            [_, _, _],
        ])

        game_solver = KoburinSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' │  0  │ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x3_digit_1(self):
        grid = Grid([
            [_, 1, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        game_solver = KoburinSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ■  1  ┌──┐ \n'
            ' ┌─────┘  │ \n'
            ' └────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5(self):
        grid = Grid([
            [_, _, 0, _, _],
            [_, _, _, _, _],
            [_, 1, _, 1, _],
            [_, _, _, _, _],
            [_, _, _, _, 0],
        ])

        game_solver = KoburinSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐  0  ┌──┐ \n'
            ' │  └─────┘  │ \n'
            ' │  1  ■  1  │ \n'
            ' │  ┌──┐  ┌──┘ \n'
            ' └──┘  └──┘  0 '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
