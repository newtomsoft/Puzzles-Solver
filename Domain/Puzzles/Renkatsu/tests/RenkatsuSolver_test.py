from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Renkatsu.RenkatsuSolver import RenkatsuSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine

_ = 0


class RenkatsuSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_2_regions(self):
        grid = Grid([
            [1, 2, 3],
            [1, 2, 4],
            [3, 5, 4],
        ])

        game_solver = RenkatsuSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [2, 2, 2],
            [1, 1, 2],
            [1, 1, 1],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_3_regions(self):
        grid = Grid([
            [2, 1, 1],
            [2, 3, 3],
            [4, 1, 2],
        ])

        game_solver = RenkatsuSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [3, 3, 2],
            [1, 1, 2],
            [1, 1, 2],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4(self):
        # https://gridpuzzle.com/renkatsu/3155d
        grid = Grid([
            [4, 5, 2, 2],
            [3, 1, 3, 4],
            [3, 1, 5, 1],
            [1, 4, 2, 2]
        ])

        game_solver = RenkatsuSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [2, 2, 2, 1],
            [2, 2, 1, 1],
            [3, 1, 1, 4],
            [3, 3, 3, 4],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
