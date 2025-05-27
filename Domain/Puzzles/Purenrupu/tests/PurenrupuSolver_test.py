from unittest import TestCase

from Domain.Board.Grid import Grid
from Puzzles.Purenrupu.PurenrupuSolver import PurenrupuSolver

_ = 0


class PurenrupuSolverTests(TestCase):
    def test_solution_5x5(self):
        grid = Grid([
            [_, _, _, _, 1],
            [_, _, _, _, _],
            [1, _, _, 1, _],
            [_, _, 1, 1, _],
            [_, _, _, _, _],
        ])

        game_solver = PurenrupuSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌────────┐    \n'
            ' └─────┐  └──┐ \n'
            '    ┌──┘     │ \n'
            ' ┌──┘        │ \n'
            ' └───────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
