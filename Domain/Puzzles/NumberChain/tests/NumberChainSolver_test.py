from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.NumberChain.NumberChainSolver import NumberChainSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine

_ = 0


class SnakeSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_basic(self):
        grid = Grid([
            [1, 2, 1],
            [4, 3, 1],
            [5, 6, 7],
        ])

        game_solver = NumberChainSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╶──┐    \n'
            ' ┌──┘    \n'
            ' └────→  '
        )
        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_basic_random_sort_numbers(self):
        grid = Grid([
            [1, 4, 1],
            [6, 3, 1],
            [2, 5, 7],
        ])

        game_solver = NumberChainSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╶──┐    \n'
            ' ┌──┘    \n'
            ' └────→  '
        )
        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_370j9(self):
        # https://gridpuzzle.com/number-chain/370j9
        grid = Grid([
            [1, 3, 8, 4],
            [9, 10, 7, 2],
            [3, 2, 6, 10],
            [7, 1, 5, 11]
        ])

        game_solver = NumberChainSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╷  ┌─────┐ \n'
            ' └──┘  ┌──┘ \n'
            '       │    \n'
            '       └─→  '
        )
        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
