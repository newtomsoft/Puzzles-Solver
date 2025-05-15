from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.NumberChain.NumberChainSolver import NumberChainSolver

_ = 0


class NumberChainSolverTests(TestCase):


    def test_solution_basic(self):
        grid = Grid([
            [1, 2, 1],
            [4, 3, 1],
            [5, 6, 7],
        ])

        game_solver = NumberChainSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╶──┐  · \n'
            ' ┌──┘  · \n'
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

        game_solver = NumberChainSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╶──┐  · \n'
            ' ┌──┘  · \n'
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

        game_solver = NumberChainSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╷  ┌─────┐ \n'
            ' └──┘  ┌──┘ \n'
            ' ·  ·  │  · \n'
            ' ·  ·  └─→  '
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

        game_solver = NumberChainSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╶───────────┐ \n'
            ' ·  ┌────────┘ \n'
            ' ·  │  ·  ·  · \n'
            ' ·  └────────┐ \n'
            ' ·  ·  ·  ·  ↓ '
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

        game_solver = NumberChainSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╷  ·  ·  ┌──┐ \n'
            ' └──┐  ·  │  │ \n'
            ' ·  │  ┌──┘  │ \n'
            ' ·  └──┘  ·  │ \n'
            ' ·  ·  ·  ·  ↓ '
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

        game_solver = NumberChainSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╶────────┐  ·  · \n'
            ' ·  ┌─────┘  ·  · \n'
            ' ·  └──┐  ·  ·  · \n'
            ' ·  ·  │  ┌─────┐ \n'
            ' ·  ·  └──┘  ·  │ \n'
            ' ·  ·  ·  ·  ·  ↓ '
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

        game_solver = NumberChainSolver(grid)
        solution = game_solver.get_solution()

        expected_solution = (
            ' ╶────────┐  ·  · \n'
            ' ·  ·  ┌──┘  ·  · \n'
            ' ·  ·  │  ┌─────┐ \n'
            ' ·  ·  └──┘  ┌──┘ \n'
            ' ·  ·  ·  ·  │  · \n'
            ' ·  ·  ·  ·  └─→  '
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

        game_solver = NumberChainSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╶────────┐  ·  ·  · \n'
            ' ·  ┌─────┘  ·  ·  · \n'
            ' ·  │  ·  ·  ┌──┐  · \n'
            ' ·  └──┐  ·  │  └──┐ \n'
            ' ·  ·  └─────┘  ·  │ \n'
            ' ·  ·  ·  ·  ·  ·  │ \n'
            ' ·  ·  ·  ·  ·  ·  ↓ '
        )
        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_4n0m4(self):
        # https://gridpuzzle.com/number-chain/4n0m4
        grid = Grid([
            [1, 20, 14, 20, 8, 14, 26, 7],
            [8, 3, 20, 13, 18, 19, 24, 4],
            [24, 6, 23, 14, 13, 12, 23, 26],
            [26, 17, 14, 16, 5, 22, 24, 7],
            [22, 21, 6, 17, 7, 21, 26, 9],
            [5, 23, 11, 21, 18, 25, 16, 2],
            [4, 22, 2, 15, 10, 11, 10, 14],
            [26, 2, 18, 2, 4, 24, 20, 27]
        ])

        game_solver = NumberChainSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╷  ·  ·  ·  ·  ·  ·  · \n'
            ' └──┐  ┌────────┐  ·  · \n'
            ' ·  └──┘  ·  ·  │  ·  · \n'
            ' ·  ·  ·  ·  ┌──┘  ·  · \n'
            ' ·  ·  ·  ┌──┘  ·  ┌──┐ \n'
            ' ·  ·  ·  │  ·  ┌──┘  │ \n'
            ' ·  ·  ·  └──┐  │  ·  │ \n'
            ' ·  ·  ·  ·  └──┘  ·  ↓ '
        )
        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_21wr8(self):
        # https://gridpuzzle.com/number-chain/21wr8
        grid = Grid([
            [1, 11, 18, 16, 21, 19, 17, 24],
            [7, 16, 10, 20, 3, 10, 13, 16],
            [10, 12, 25, 24, 9, 16, 5, 12],
            [14, 18, 21, 23, 8, 14, 21, 15],
            [13, 11, 9, 24, 13, 7, 6, 12],
            [22, 23, 14, 6, 17, 6, 8, 16],
            [25, 11, 17, 4, 3, 26, 25, 10],
            [16, 8, 16, 22, 2, 19, 3, 27]
        ])

        game_solver = NumberChainSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╶─────┐  ·  ·  ·  ·  · \n'
            ' ·  ·  └──┐  ·  ·  ·  · \n'
            ' ·  ·  ·  │  ┌────────┐ \n'
            ' ·  ·  ·  └──┘  ┌─────┘ \n'
            ' ·  ·  ·  ·  ┌──┘  ·  · \n'
            ' ·  ·  ·  ┌──┘  ·  ·  · \n'
            ' ·  ·  ·  │  ·  ┌──┐  · \n'
            ' ·  ·  ·  └─────┘  └─→  '
        )
        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_9x9_0y9p1(self):
        # https://gridpuzzle.com/number-chain/0y9p1
        grid = Grid([
            [1, 20, 19, 3, 15, 21, 29, 28, 22],
            [10, 24, 30, 26, 12, 10, 24, 18, 25],
            [22, 25, 12, 14, 19, 28, 17, 11, 7],
            [2, 4, 13, 24, 2, 14, 9, 7, 21],
            [16, 12, 7, 15, 5, 4, 6, 29, 8],
            [6, 30, 21, 16, 7, 5, 14, 23, 25],
            [2, 26, 15, 23, 24, 4, 29, 22, 8],
            [12, 6, 12, 7, 22, 10, 13, 5, 27],
            [23, 13, 11, 26, 24, 26, 17, 30, 31]
        ])

        game_solver = NumberChainSolver(grid)
        solution = game_solver.get_solution()

        expected_solution = (
            ' ╶────────┐  ·  ·  ·  ·  · \n'
            ' ·  ·  ┌──┘  ·  ┌─────┐  · \n'
            ' ·  ┌──┘  ·  ·  │  ┌──┘  · \n'
            ' ·  └──┐  ·  ┌──┘  │  ·  · \n'
            ' ·  ·  │  ┌──┘  ·  └──┐  · \n'
            ' ·  ·  └──┘  ·  ·  ·  │  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  └──┐ \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  │ \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ↓ '
        )

        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_7j9yj(self):
        # https://gridpuzzle.com/number-chain/7j9yj
        grid = Grid([
            [1, 13, 23, 26, 2, 12, 27, 31, 6, 22],
            [12, 20, 14, 4, 14, 27, 5, 32, 19, 27],
            [29, 21, 16, 7, 29, 2, 21, 24, 28, 32],
            [10, 32, 9, 31, 18, 11, 27, 18, 10, 13],
            [5, 12, 5, 22, 2, 3, 24, 8, 20, 21],
            [7, 31, 2, 10, 19, 24, 14, 17, 8, 4],
            [26, 23, 21, 29, 17, 21, 7, 32, 2, 30],
            [6, 4, 8, 28, 8, 25, 2, 15, 30, 7],
            [28, 22, 13, 22, 16, 30, 9, 16, 6, 3],
            [20, 2, 28, 8, 14, 24, 25, 8, 25, 33]
        ])

        game_solver = NumberChainSolver(grid)
        solution = game_solver.get_solution()

        expected_solution = (
            ' ╷  ┌─────┐  ·  ·  ·  ·  ·  · \n'
            ' └──┘  ┌──┘  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  │  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  │  ┌────────┐  ·  ·  · \n'
            ' ·  ·  └──┘  ┌─────┘  ·  ·  · \n'
            ' ·  ·  ·  ┌──┘  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  │  ┌────────┐  ·  · \n'
            ' ·  ·  ·  └──┘  ·  ·  └──┐  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  │  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  └─→  '
        )

        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_16rk0(self):
        # https://gridpuzzle.com/number-chain/16rk0
        grid = Grid([
            [1, 7, 26, 21, 20, 16, 13, 3, 15, 29],
            [17, 6, 22, 27, 18, 4, 26, 22, 9, 8],
            [14, 12, 8, 2, 14, 9, 2, 19, 28, 20],
            [24, 15, 9, 24, 23, 20, 13, 21, 9, 21],
            [29, 9, 21, 23, 16, 31, 22, 12, 25, 32],
            [18, 12, 27, 26, 25, 16, 30, 8, 19, 2],
            [13, 6, 5, 10, 31, 29, 18, 10, 28, 5],
            [15, 19, 14, 24, 28, 11, 19, 3, 24, 22],
            [13, 14, 23, 31, 16, 26, 22, 2, 15, 30],
            [31, 32, 16, 5, 29, 4, 26, 13, 19, 33]
        ])

        game_solver = NumberChainSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╷  ┌─────┐  ·  ·  ·  ·  ·  · \n'
            ' └──┘  ·  └─────┐  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ┌──┘  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  └─────┐  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ┌──┘  ┌─────┐ \n'
            ' ·  ·  ·  ·  ·  │  ·  │  ·  │ \n'
            ' ·  ·  ·  ·  ·  │  ·  │  ┌──┘ \n'
            ' ·  ·  ·  ·  ·  └─────┘  │  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  └──┐ \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  ↓ '
        )
        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12(self):
        grid = Grid([
            [1, 28, 2, 32, 39, 13, 7, 14, 36, 8, 20, 11],
            [29, 37, 11, 37, 26, 30, 14, 5, 25, 32, 22, 19],
            [21, 9, 34, 5, 22, 36, 12, 37, 26, 4, 38, 32],
            [19, 6, 10, 26, 17, 20, 20, 9, 4, 19, 35, 7],
            [27, 18, 12, 24, 7, 20, 30, 13, 37, 10, 6, 15],
            [16, 25, 3, 31, 33, 12, 6, 14, 39, 17, 7, 31],
            [35, 15, 8, 37, 13, 3, 18, 18, 24, 17, 33, 37],
            [11, 32, 33, 23, 5, 28, 40, 37, 30, 6, 36, 19],
            [29, 5, 35, 34, 12, 30, 25, 13, 20, 38, 12, 26],
            [20, 5, 38, 15, 4, 12, 32, 34, 19, 32, 22, 8],
            [16, 22, 22, 32, 7, 39, 39, 7, 25, 40, 4, 31],
            [5, 40, 9, 25, 17, 32, 13, 3, 40, 28, 23, 41],
        ])

        game_solver = NumberChainSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╶─────┐  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ┌─────┘  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' │  ·  ┌───────────┐  ·  ·  ·  ·  · \n'
            ' │  ·  └─────┐  ·  └──┐  ·  ·  ·  · \n'
            ' └──┐  ·  ·  │  ·  ·  │  ·  ·  ·  · \n'
            ' ┌──┘  ┌─────┘  ·  ·  └──┐  ·  ·  · \n'
            ' └─────┘  ·  ·  ·  ·  ·  │  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  └──┐  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  │  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  │  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  └──┐  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  └─→  '
        )
        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_13x13(self):
        grid = Grid([
            [1, 19, 16, 40, 2, 29, 9, 20, 21, 40, 15, 28, 15],
            [25, 42, 40, 36, 34, 22, 37, 30, 12, 17, 32, 16, 22],
            [37, 12, 7, 4, 14, 15, 31, 4, 38, 21, 19, 15, 35],
            [19, 21, 3, 24, 35, 6, 42, 7, 18, 21, 33, 29, 8],
            [37, 16, 15, 39, 39, 36, 20, 35, 26, 23, 27, 13, 11],
            [38, 36, 19, 11, 19, 4, 30, 22, 27, 3, 41, 20, 21],
            [23, 14, 10, 18, 16, 29, 9, 42, 7, 37, 20, 10, 15],
            [5, 2, 8, 6, 27, 21, 13, 26, 40, 32, 33, 30, 24],
            [25, 31, 35, 5, 41, 6, 20, 19, 40, 21, 34, 42, 2],
            [24, 8, 37, 42, 25, 20, 42, 29, 5, 17, 11, 10, 33],
            [28, 31, 23, 18, 42, 2, 6, 13, 28, 13, 41, 29, 7],
            [6, 30, 17, 10, 27, 4, 12, 35, 9, 15, 15, 18, 3],
            [39, 30, 17, 17, 16, 35, 15, 7, 14, 38, 32, 36, 43],
        ])

        game_solver = NumberChainSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╷  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' │  ┌──┐  ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' └──┘  └──┐  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  │  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  │  ·  ·  ·  ·  ┌──┐  ·  ·  · \n'
            ' ·  ·  ┌──┘  ·  ·  ┌─────┘  └──┐  ·  · \n'
            ' ·  ┌──┘  ┌────────┘  ·  ·  ·  │  ·  · \n'
            ' ·  │  ┌──┘  ·  ·  ·  ·  ·  ·  │  ·  · \n'
            ' ·  └──┘  ·  ·  ·  ·  ·  ·  ┌──┘  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ┌──┘  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  └──┐  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  │  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  └───────→  '
        )
        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_13x13_hard(self):
        grid = Grid([
            [1, 29, 39, 25, 38, 14, 19, 18, 28, 4, 2, 33, 6],
            [42, 29, 16, 3, 35, 16, 4, 17, 21, 2, 5, 27, 10],
            [4, 40, 29, 3, 37, 8, 2, 31, 33, 16, 32, 40, 12],
            [7, 6, 12, 13, 16, 36, 22, 23, 21, 17, 22, 31, 20],
            [21, 17, 18, 14, 26, 39, 37, 4, 14, 20, 25, 22, 16],
            [19, 15, 17, 28, 13, 17, 23, 23, 32, 9, 26, 41, 19],
            [2, 36, 7, 27, 41, 31, 16, 28, 35, 38, 40, 20, 8],
            [3, 19, 20, 5, 26, 9, 21, 27, 32, 13, 26, 33, 8],
            [28, 10, 27, 24, 30, 6, 30, 16, 11, 38, 10, 40, 8],
            [30, 13, 37, 9, 41, 42, 29, 26, 8, 38, 6, 8, 23],
            [42, 9, 42, 8, 11, 42, 20, 13, 2, 12, 33, 23, 30],
            [31, 19, 4, 22, 21, 38, 39, 38, 37, 41, 39, 25, 38],
            [8, 17, 21, 7, 34, 33, 40, 23, 5, 31, 32, 2, 43],
        ])

        game_solver = NumberChainSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╶───────────┐  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  │  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  │  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ┌──┐  ·  │  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  │  └─────┘  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  │  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  └──┐  ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ┌─────┘  ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' │  ┌─────┐  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' └──┘  ·  └──┐  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ┌─────┘  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  └─────┐  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  └──────────────────────→  '
        )
        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_15x15(self):
        grid = Grid([
            [1, 40, 4, 43, 27, 46, 20, 46, 29, 46, 35, 23, 30, 15, 27],
            [43, 9, 10, 39, 28, 44, 12, 20, 34, 7, 20, 29, 48, 43, 49],
            [5, 15, 48, 39, 26, 38, 46, 46, 25, 33, 32, 14, 46, 26, 48],
            [41, 17, 40, 32, 39, 40, 43, 24, 42, 34, 23, 22, 33, 39, 50],
            [14, 45, 21, 47, 36, 16, 34, 43, 46, 26, 27, 29, 36, 43, 28],
            [7, 24, 13, 19, 38, 17, 43, 19, 6, 23, 25, 6, 38, 24, 49],
            [49, 11, 32, 15, 8, 22, 30, 25, 44, 20, 49, 39, 40, 45, 15],
            [44, 33, 42, 11, 49, 21, 37, 13, 3, 29, 22, 18, 23, 22, 19],
            [37, 32, 47, 39, 28, 2, 25, 11, 33, 15, 38, 47, 36, 13, 4],
            [4, 36, 23, 45, 7, 45, 17, 3, 37, 3, 34, 33, 44, 19, 34],
            [14, 2, 38, 28, 10, 14, 35, 46, 12, 11, 25, 47, 42, 31, 19],
            [42, 6, 49, 16, 38, 4, 32, 19, 23, 45, 42, 33, 15, 29, 24],
            [47, 11, 7, 2, 29, 29, 18, 34, 9, 35, 18, 3, 10, 38, 40],
            [10, 40, 35, 16, 43, 27, 45, 39, 42, 22, 47, 3, 15, 24, 36],
            [41, 20, 41, 17, 8, 6, 43, 20, 36, 50, 2, 26, 31, 16, 51],
        ])

        game_solver = NumberChainSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╶───────────┐  ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ┌─────┘  ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ┌─────┘  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' └──┐  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ┌──┘  ┌──┐  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' │  ┌──┘  └──┐  ·  ·  ·  ┌──┐  ·  ·  ·  ·  · \n'
            ' └──┘  ·  ·  └───────────┘  │  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ┌──┘  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  │  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  │  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ┌─────┘  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  │  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  └─────┐  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  │  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  └────────────────→  '
        )
        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
