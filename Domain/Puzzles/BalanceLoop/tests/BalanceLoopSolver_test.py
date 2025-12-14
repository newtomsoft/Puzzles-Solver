import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.BalanceLoop.BalanceLoopSolver import BalanceLoopSolver

# region
__ = BalanceLoopSolver.empty
B0 = 'b0'
B2 = 'b2'
B3 = 'b3'
B4 = 'b4'
B5 = 'b5'
B6 = 'b6'
B7 = 'b7'
B8 = 'b8'
B9 = 'b9'
W0 = 'w0'
W2 = 'w2'
W4 = 'w4'
W6 = 'w6'
W8 = 'w8'


# endregion

class BalanceLoopSolverTest(TestCase):
    def test_5x5_medium_31846(self):
        """https://gridpuzzle.com/balance-loop/31846"""
        clues_grid = Grid([
            [B6, B4, W4, B4, B6],
            [__, __, B3, __, __],
            [B3, __, __, __, B3],
            [__, __, __, __, __],
            [__, B4, __, B3, __],
        ])

        expected_solution_str = (
            ' ┌───────────┐ \n'
            ' │  ┌──┐  ·  │ \n'
            ' └──┘  │  ┌──┘ \n'
            ' ·  ┌──┘  └──┐ \n'
            ' ·  └────────┘ '
        )

        game_solver = BalanceLoopSolver(clues_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_6x6_hard_0zppg(self):
        """https://gridpuzzle.com/balance-loop/0zppg"""
        clues_grid = Grid([
            [__, __, __, W2, W2, __],
            [B3, __, __, W2, __, W2],
            [__, __, B3, __, __, B3],
            [__, __, __, __, __, __],
            [B3, __, W4, W2, B3, __],
            [__, __, __, __, __, __],
        ])

        expected_solution_str = (
            ' ┌──┐  ┌──┐  ┌──┐ \n'
            ' │  └──┘  └──┘  │ \n'
            ' │  ┌──┐  ·  ┌──┘ \n'
            ' └──┘  │  ·  │  · \n'
            ' ┌─────┘  ┌──┘  · \n'
            ' └────────┘  ·  · '
        )

        game_solver = BalanceLoopSolver(clues_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_8x8_hard_4k65p(self):
        """https://gridpuzzle.com/balance-loop/4k65p"""
        clues_grid = Grid([
            [B3, __, __, __, __, __, __, B3],
            [__, B3, __, __, __, __, W2, __],
            [B3, __, __, __, __, __, __, W4],
            [__, __, __, B3, B3, __, __, __],
            [B3, __, __, __, __, __, __, W2],
            [__, __, __, W2, B5, __, __, __],
            [__, W2, __, __, __, __, B3, __],
            [B4, __, __, __, __, __, __, B3],
        ])

        expected_solution_str = (
            ' ┌──┐  ·  ┌─────┐  ┌──┐ \n'
            ' │  └─────┘  ·  └──┘  │ \n'
            ' └──┐  ·  ┌──┐  ┌─────┘ \n'
            ' ·  └─────┘  │  └─────┐ \n'
            ' ┌─────┐  ·  │  ·  ┌──┘ \n'
            ' └──┐  └─────┘  ·  │  · \n'
            ' ┌──┘  ·  ┌─────┐  └──┐ \n'
            ' └────────┘  ·  └─────┘ '
        )

        game_solver = BalanceLoopSolver(clues_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_10x10_hard_0dr7g(self):
        """https://gridpuzzle.com/balance-loop/0dr7g"""
        clues_grid = Grid([
            [__, B3, __, W2, __, __, B3, __, W2, __],
            [B3, __, __, __, __, __, __, __, __, B6],
            [__, __, __, __, __, __, __, __, __, __],
            [B4, __, B5, __, W4, B4, __, W4, __, W6],
            [B3, __, __, __, __, __, __, __, __, B6],
            [__, __, W4, __, __, __, __, B6, __, __],
            [__, __, __, W2, B3, W2, W2, __, __, __],
            [__, __, __, __, __, __, __, __, __, __],
            [__, B3, __, __, __, __, __, __, B3, __],
            [__, __, B6, __, __, __, __, W2, __, __]
        ])

        expected_solution_str = (
            ' ┌──┐  ┌──┐  ┌─────┐  ·  ┌──┐ \n'
            ' │  │  │  └──┘  ┌──┘  ┌──┘  │ \n'
            ' │  └──┘  ·  ·  └──┐  │  ·  │ \n'
            ' └──┐  ┌───────────┘  │  ·  │ \n'
            ' ┌──┘  └─────┐  ·  ·  │  ·  │ \n'
            ' │  ·  ┌─────┘  ┌─────┘  ·  │ \n'
            ' └──┐  │  ┌──┐  └──┐  ·  ┌──┘ \n'
            ' ·  │  └──┘  │  ┌──┘  ·  │  · \n'
            ' ┌──┘  ·  ·  └──┘  ┌──┐  │  · \n'
            ' └─────────────────┘  └──┘  · '
        )

        game_solver = BalanceLoopSolver(clues_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_12x12_hard_12g46(self):
        """https://gridpuzzle.com/balance-loop/12g46"""
        clues_grid = Grid([
            [__, __, B3, W2, __, __, __, __, W2, B3, __, __],
            [__, W2, W2, B3, __, __, __, __, W2, W2, W2, __],
            [__, __, B3, __, __, __, __, __, __, B3, __, __],
            [B4, B3, B4, __, __, B4, B3, __, __, W2, W2, B3],
            [__, __, __, B6, __, __, __, __, B3, __, __, __],
            [__, __, B3, __, __, __, __, __, __, W4, __, __],
            [__, __, __, __, B3, __, __, W2, __, __, __, __],
            [W2, __, __, __, B3, W2, B3, B5, __, __, __, B5],
            [B3, __, __, __, W2, W2, W2, W2, __, __, __, W2],
            [__, W2, __, __, __, __, __, __, __, __, W2, __],
            [W2, __, __, __, __, B5, B5, __, __, __, __, W2],
            [__, __, __, B3, __, __, __, __, W2, __, __, __]
        ])

        expected_solution_str = (
            ' ┌──┐  ┌──┐  ·  ·  ·  ┌──┐  ┌─────┐ \n'
            ' │  │  │  └─────┐  ·  │  └──┘  ┌──┘ \n'
            ' │  └──┘  ·  ·  └──┐  └─────┐  └──┐ \n'
            ' └──┐  ┌────────┐  └─────┐  └──┐  │ \n'
            ' ·  │  └──┐  ┌──┘  ·  ·  └─────┘  │ \n'
            ' ·  └──┐  │  │  ┌──┐  ┌───────────┘ \n'
            ' ┌──┐  │  │  └──┘  └──┘  ·  ·  ·  · \n'
            ' │  └──┘  │  ┌─────┐  ┌───────────┐ \n'
            ' └──┐  ·  │  └──┐  └──┘  ·  ·  ┌──┘ \n'
            ' ┌──┘  ·  └─────┘  ·  ·  ·  ·  └──┐ \n'
            ' └──┐  ·  ┌──────────────┐  ┌──┐  │ \n'
            ' ·  └─────┘  ·  ·  ·  ·  └──┘  └──┘ '
        )

        game_solver = BalanceLoopSolver(clues_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_4x4_with_black0_full(self):
        clues_grid = Grid([
            [B0, W2, W2, B0],
            [__, W2, W2, __],
            [__, W2, W2, __],
            [B0, W2, W2, B0],
        ])

        expected_solution_str = (
            ' ┌──┐  ┌──┐ \n'
            ' │  └──┘  │ \n'
            ' │  ┌──┐  │ \n'
            ' └──┘  └──┘ '
        )

        game_solver = BalanceLoopSolver(clues_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_4x4_with_withe0_full(self):
        clues_grid = Grid([
            [B4, W0, W0, B4],
            [__, W0, W0, __],
            [__, W0, W0, __],
            [B4, W0, W0, B4],
        ])

        expected_solution_str = (
            ' ┌──┐  ┌──┐ \n'
            ' │  └──┘  │ \n'
            ' │  ┌──┐  │ \n'
            ' └──┘  └──┘ '
        )

        game_solver = BalanceLoopSolver(clues_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_4x4_with_withe0(self):
        clues_grid = Grid([
            [B5, __, B3, __],
            [__, __, W0, W0],
            [__, B3, __, B3],
            [B4, W0, __, __],
        ])

        expected_solution_str = (
            ' ┌─────┐  · \n'
            ' │  ·  └──┐ \n'
            ' │  ┌─────┘ \n'
            ' └──┘  ·  · '
        )

        game_solver = BalanceLoopSolver(clues_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_4x4_with_black0(self):
        clues_grid = Grid([
            [B0, __, B0, __],
            [__, __, W2, W2],
            [__, B0, __, B0],
            [B0, W2, __, __],
        ])

        expected_solution_str = (
            ' ┌─────┐  · \n'
            ' │  ·  └──┐ \n'
            ' │  ┌─────┘ \n'
            ' └──┘  ·  · '
        )

        game_solver = BalanceLoopSolver(clues_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_4x4_with_black0_white0(self):
        clues_grid = Grid([
            [B0, __, B0, __],
            [__, __, W0, W0],
            [__, B0, __, B0],
            [B0, W0, __, __],
        ])

        expected_solution_str = (
            ' ┌─────┐  · \n'
            ' │  ·  └──┐ \n'
            ' │  ┌─────┘ \n'
            ' └──┘  ·  · '
        )

        game_solver = BalanceLoopSolver(clues_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    # test ko
    def test_4x4_with_white0_2_solutions(self):
        clues_grid = Grid([
            [W0, __, __, __],
            [__, __, __, __],
            [__, __, __, __],
            [__, __, __, W0],
        ])

        expected_solution_str = (
            ' ┌─────┐  · \n'
            ' │  ·  └──┐ \n'
            ' └──┐  ·  │ \n'
            ' ·  └─────┘ '
        )
        expected_solution2_str = (
            ' ┌────────┐ \n'
            ' │  ·  ·  │ \n'
            ' │  ·  ·  │ \n'
            ' └────────┘ '
        )
        expected_solutions_strs = {expected_solution_str, expected_solution2_str}

        game_solver = BalanceLoopSolver(clues_grid)
        solution = game_solver.get_solution()
        solution2 = game_solver.get_other_solution()
        solutions_str = {str(solution), str(solution2)}
        self.assertEqual(expected_solutions_strs, solutions_str)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_5x5_evil_0xpnr(self):
        """https://gridpuzzle.com/balance-loop/0xpnr"""
        clues_grid = Grid([
            [__, B3, __, B4, __],
            [__, __, __, __, __],
            [B0, __, __, __, B0],
            [__, __, __, __, __],
            [B5, __, W0, __, B6],
        ])

        expected_solution_str = (
            ' ┌────────┐  · \n'
            ' │  ·  ┌──┘  · \n'
            ' └──┐  │  ┌──┐ \n'
            ' ┌──┘  └──┘  │ \n'
            ' └───────────┘ '
        )

        game_solver = BalanceLoopSolver(clues_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_5x5_evil_1np7k(self):
        """https://gridpuzzle.com/balance-loop/1np7k"""
        clues_grid = Grid([
            [__, __, B0, __, __],
            [__, __, __, __, __],
            [B0, __, B0, __, B0],
            [__, __, __, __, __],
            [B0, __, B0, __, W0]
        ])

        expected_solution_str = (
            ' ·  ·  ┌──┐  · \n'
            ' ┌──┐  │  │  · \n'
            ' │  └──┘  └──┐ \n'
            ' │  ┌──┐  ·  │ \n'
            ' └──┘  └─────┘ '
        )

        game_solver = BalanceLoopSolver(clues_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    @unittest.skip("temporarily disabled - fails intermittently")  # todo reactive test
    def test_6x6_evil_1yew0(self):
        """https://gridpuzzle.com/balance-loop/1yew0"""
        clues_grid = Grid([
            [B5, __, __, __, __, __],
            [__, __, __, __, __, W0],
            [W0, __, __, __, __, __],
            [__, __, __, __, __, __],
            [__, __, __, __, __, __],
            [B3, __, __, W4, __, B0],
        ])

        expected_solution_str = (
            ' ┌───────────┐  · \n'
            ' └──┐  ·  ·  └──┐ \n'
            ' ┌──┘  ·  ·  ┌──┘ \n'
            ' └──┐  ┌──┐  │  · \n'
            ' ┌──┘  │  │  └──┐ \n'
            ' └─────┘  └─────┘ '
        )

        game_solver = BalanceLoopSolver(clues_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_6x6_evil_1y199(self):
        """https://gridpuzzle.com/balance-loop/1y199"""
        clues_grid = Grid([
            [__, __, B0, B4, __, __],
            [__, __, W0, W0, __, __],
            [__, __, __, __, __, __],
            [__, __, B0, B3, __, __],
            [W0, B3, __, __, W0, B5],
            [__, __, __, __, __, __],
        ])

        expected_solution_str = (
            ' ┌────────┐  ┌──┐ \n'
            ' │  ·  ┌──┘  │  │ \n'
            ' └──┐  └─────┘  │ \n'
            ' ·  │  ┌──┐  ·  │ \n'
            ' ┌──┘  │  │  ┌──┘ \n'
            ' └─────┘  └──┘  · '
        )

        game_solver = BalanceLoopSolver(clues_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_8x8_evil_01err(self):
        """https://gridpuzzle.com/balance-loop/01err"""
        clues_grid = Grid([
            [__, __, __, W2, B4, __, __, __],
            [__, __, B0, __, __, B6, __, __],
            [B6, __, __, W0, B0, __, __, B7],
            [__, __, __, __, __, __, __, __],
            [__, __, __, __, __, __, __, __],
            [__, __, B5, __, __, B6, __, __],
            [__, __, __, __, __, __, __, __],
            [__, __, B7, __, __, B0, __, __]
        ])

        expected_solution_str = (
            ' ·  ·  ·  ┌──┐  ┌─────┐ \n'
            ' ┌────────┘  │  │  ·  │ \n'
            ' │  ·  ┌──┐  │  │  ·  │ \n'
            ' │  ·  │  └──┘  │  ·  │ \n'
            ' │  ·  │  ·  ·  │  ·  │ \n'
            ' │  ·  └─────┐  │  ·  │ \n'
            ' │  ·  ·  ·  └──┘  ·  │ \n'
            ' └────────────────────┘ '
        )

        game_solver = BalanceLoopSolver(clues_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_10x10_evil_11qz6(self):
        """https://gridpuzzle.com/balance-loop/11qz6"""
        clues_grid = Grid([
            [__, __, __, B3, __, __, B5, __, __, __],
            [__, __, __, B0, __, __, W0, __, __, __],
            [B0, __, W6, __, __, __, __, W0, __, B0],
            [__, __, __, __, __, __, __, __, __, __],
            [B6, __, B0, __, __, __, __, B0, __, W0],
            [__, __, __, __, B0, B5, __, __, __, __],
            [B8, __, __, __, B0, B0, __, __, __, W0],
            [__, __, __, W0, __, __, W0, __, __, __],
            [B3, __, B0, __, B0, B0, __, W0, __, B0],
            [__, __, __, __, __, __, __, __, __, __]
        ])

        expected_solution_str = (
            ' ┌──┐  ·  ┌─────┐  ┌────────┐ \n'
            ' │  └─────┘  ·  │  │  ·  ·  │ \n'
            ' │  ·  ┌────────┘  └──┐  ┌──┘ \n'
            ' │  ·  │  ·  ·  ┌─────┘  └──┐ \n'
            ' │  ·  │  ·  ·  │  ·  ┌──┐  │ \n'
            ' │  ·  └────────┘  ·  │  └──┘ \n'
            ' └─────┐  ┌────────┐  └─────┐ \n'
            ' ┌─────┘  │  ·  ·  └──┐  ·  │ \n'
            ' └─────┐  └────────┐  │  ┌──┘ \n'
            ' ·  ·  └───────────┘  └──┘  · '
        )

        game_solver = BalanceLoopSolver(clues_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_12x12_evil_12zrr(self):
        """https://gridpuzzle.com/balance-loop/12zrr"""
        clues_grid = Grid([
            [__, B3, __, __, __, __, __, __, __, __, B4, __],
            [__, __, B0, __, __, __, __, __, __, B0, __, __],
            [__, B0, W2, __, W0, W4, W0, W0, __, W0, B3, __],
            [__, __, __, __, __, __, __, __, __, __, __, __],
            [__, B6, __, B4, __, __, __, __, B3, __, B3, __],
            [__, __, B7, __, W4, __, __, B0, __, B0, __, __],
            [__, __, __, __, __, B0, B4, __, __, __, __, __],
            [__, __, __, __, __, B4, W6, __, __, __, __, __],
            [__, B6, B0, __, __, __, __, __, __, B0, B3, __],
            [__, __, __, __, __, __, __, __, __, __, __, __],
            [W0, __, __, __, __, __, __, __, __, __, __, B0],
            [__, __, B3, __, __, B0, B0, __, __, W4, __, __]
        ])

        expected_solution_str = (
            ' ┌──┐  ·  ·  ┌──┐  ·  ┌───────────┐ \n'
            ' │  │  ┌─────┘  │  ┌──┘  ·  ┌─────┘ \n'
            ' │  └──┘  ┌─────┘  │  ┌──┐  └──┐  · \n'
            ' └──┐  ┌──┘  ·  ·  └──┘  │  ·  │  · \n'
            ' ·  │  └───────────┐  ┌──┘  ·  └──┐ \n'
            ' ·  │  ┌─────┐  ┌──┘  └─────┐  ·  │ \n'
            ' ·  │  │  ·  │  └───────────┘  ┌──┘ \n'
            ' ·  │  │  ·  └──┐  ┌────────┐  │  · \n'
            ' ·  │  │  ·  ·  │  │  ┌─────┘  └──┐ \n'
            ' ┌──┘  │  ·  ·  │  │  └─────┐  ·  │ \n'
            ' │  ·  └──┐  ┌──┘  └──┐  ·  │  ·  │ \n'
            ' └────────┘  └────────┘  ·  └─────┘ '
        )

        game_solver = BalanceLoopSolver(clues_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
