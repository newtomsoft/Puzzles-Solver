from unittest import TestCase

from Domain.Board.Grid import Grid
from Map.MapSolver import MapSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine


class MapSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_white_0(self):
        grid = Grid([
            []
        ])

        game_solver = MapSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)