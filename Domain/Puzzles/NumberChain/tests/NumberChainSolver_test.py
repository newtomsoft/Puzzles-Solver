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

    def test_solution_5x5_31zxk(self):
        # https://gridpuzzle.com/number-chain/31zxk
        grid = Grid([
            [1, 11, 5, 14, 3],
            [3, 13, 2, 8, 10],
            [13, 4, 6, 5, 4],
            [7, 12, 7, 6, 9],
            [10, 2, 14, 5, 15],
        ])

        game_solver = NumberChainSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╶───────────┐ \n'
            '    ┌────────┘ \n'
            '    │          \n'
            '    └────────┐ \n'
            '             ↓ '
        )
        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_35ev9(self):
        # https://gridpuzzle.com/number-chain/35ev9
        grid = Grid([
            [1, 2, 13, 6, 13],
            [11, 5, 11, 8, 12],
            [13, 10, 14, 7, 2],
            [4, 9, 3, 8, 4],
            [5, 4, 1, 3, 15],
        ])

        game_solver = NumberChainSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╷        ┌──┐ \n'
            ' └──┐     │  │ \n'
            '    │  ┌──┘  │ \n'
            '    └──┘     │ \n'
            '             ↓ '
        )
        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_pnn4r(self):
        # https://gridpuzzle.com/number-chain/pnn4r
        grid = Grid([
            [1, 3, 2, 6, 16, 13],
            [9, 10, 12, 8, 7, 14],
            [4, 7, 5, 3, 16, 4],
            [16, 9, 13, 9, 4, 11],
            [13, 15, 16, 15, 13, 14],
            [3, 7, 10, 13, 12, 17]
        ])

        game_solver = NumberChainSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╶────────┐       \n'
            '    ┌─────┘       \n'
            '    └──┐          \n'
            '       │  ┌─────┐ \n'
            '       └──┘     │ \n'
            '                ↓ '
        )
        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_3wv0y(self):
        # https://gridpuzzle.com/number-chain/3wv0y
        grid = Grid([
            [1, 9, 14, 16, 4, 15],
            [3, 4, 11, 7, 12, 8],
            [10, 2, 10, 13, 15, 3],
            [15, 14, 6, 2, 12, 8],
            [8, 6, 14, 8, 4, 14],
            [15, 4, 15, 14, 5, 17]
        ])

        game_solver = NumberChainSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╶────────┐       \n'
            '       ┌──┘       \n'
            '       │  ┌─────┐ \n'
            '       └──┘  ┌──┘ \n'
            '             │    \n'
            '             └─→  '
        )
        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_7x7_0xj8r(self):
        # https://gridpuzzle.com/number-chain/0xj8r
        grid = Grid([
            [1, 10, 7, 11, 15, 8, 5],
            [5, 9, 18, 20, 14, 9, 16],
            [17, 3, 8, 9, 19, 12, 11],
            [10, 2, 17, 3, 13, 14, 8],
            [16, 12, 5, 15, 4, 16, 6],
            [6, 9, 12, 16, 7, 4, 16],
            [15, 6, 16, 9, 2, 20, 21]
        ])

        game_solver = NumberChainSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╶────────┐          \n'
            '    ┌─────┘          \n'
            '    │        ┌──┐    \n'
            '    └──┐     │  └──┐ \n'
            '       └─────┘     │ \n'
            '                   │ \n'
            '                   ↓ '
        )
        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
