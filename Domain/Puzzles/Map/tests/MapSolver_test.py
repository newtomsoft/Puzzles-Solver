from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Map.MapSolver import MapSolver


class MapSolverTests(TestCase):


    def test_solution_white_0(self):
        grid = Grid([
            []
        ])

        game_solver = MapSolver(grid)

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)