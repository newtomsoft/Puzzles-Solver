from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Snake.SnakeSolver import SnakeSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine

_ = 0


class SnakeSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_only_cells_sum_constraint(self):
        grid = Grid([
            [1, _, _],
            [_, _, _],
            [_, _, 1],
        ])
        row_numbers = [1, 1, 3]
        column_numbers = [3, 1, 1]

        game_solver = SnakeSolver(grid, row_numbers, column_numbers, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, _, _],
            [1, _, _],
            [1, 1, 1],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_only_cells_sum_constraint(self):
        # https://gridpuzzle.com/snake/3jzyo
        grid = Grid([
            [_, _, _, _, 1, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, 1],
        ])
        row_numbers = [5, 1, 1, 1, 4, 3]
        column_numbers = [5, 2, 2, 3, 2, 1]

        game_solver = SnakeSolver(grid, row_numbers, column_numbers, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1, 1, 1, _],
            [_, _, 1, _, _, _],
            [1, _, _, _, _, _],
            [1, _, _, _, _, _],
            [1, 1, _, 1, 1, _],
            [1, _, _, 1, _, 1],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
