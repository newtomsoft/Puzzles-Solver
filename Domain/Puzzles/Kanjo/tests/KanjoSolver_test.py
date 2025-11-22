import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Puzzles.Kanjo.KanjoSolver import KanjoSolver

_ = KanjoSolver.empty


class KanjoSolverTest(TestCase):
    def test_6x6_easy_5665w(self):
        """https://gridpuzzle.com/kanjo/5665w"""
        grid_str = (
            ' ·  ·  1  ·  2  · \n'
            ' ·  ┌─ ·  ·  ┌─ · \n'
            ' │  ·  ·  2  ·  2 \n'
            ' 1  ·  2  ·  · ─┘ \n'
            ' ·  │  ·  · ─── · \n'
            ' ·  1  ·  3  ·  · '
        )

        expected_solution_str = (
            ' ┌─────┐  ┌─────┐ \n'
            ' │  ┌──┘  │  ┌──┘ \n'
            ' │  │  ┌──┘  └──┐ \n'
            ' │  │  └────────┘ \n'
            ' │  │  ┌────────┐ \n'
            ' └──┘  └────────┘ '
        )

        game_solver = KanjoSolver(Grid.from_str(grid_str, type(Island)))
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_6x6_easy_g448m(self):
        """https://gridpuzzle.com/kanjo/g448m"""
        grid_str = (
            ' 4  ·  ·  · ─── · \n'
            ' │  ┌─ ·  · ─── 2 \n'
            ' 4  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  1 \n'
            ' 3  └─ ·  · ─┘  │ \n'
            ' · ─── ·  ·  ·  1 '
        )

        expected_solution_str = (
            ' ┌─────┐  ┌─────┐ \n'
            ' │  ┌──┘  └─────┘ \n'
            ' └──┘  ┌────────┐ \n'
            ' ┌──┐  └─────┐  │ \n'
            ' │  └──┐  ┌──┘  │ \n'
            ' └─────┘  └─────┘ '
        )

        game_solver = KanjoSolver(Grid.from_str(grid_str, type(Island)))
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_6x6_medium_lqpx9(self):
        """https://gridpuzzle.com/kanjo/lqpx9"""
        grid_str = (
            ' ·  ·  ·  ·  2  · \n'
            ' ·  ┌─ 3  ·  ·  · \n'
            ' ·  3  ·  ·  ·  4 \n'
            ' ·  ·  ·  3  ·  · \n'
            ' ·  └─ · ─── ·  1 \n'
            ' ·  · ─── ·  ·  · '
        )

        expected_solution_str = (
            ' ┌────────┐  ┌──┐ \n'
            ' │  ┌──┐  │  └──┘ \n'
            ' └──┘  │  │  ┌──┐ \n'
            ' ┌──┐  └──┘  └──┘ \n'
            ' │  └───────────┐ \n'
            ' └──────────────┘ '
        )

        game_solver = KanjoSolver(Grid.from_str(grid_str, type(Island)))
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_7x7_medium_16ekd(self):
        """https://gridpuzzle.com/kanjo/16ekd"""
        grid_str = (
            ' 3  ·  3  ·  · ─── · \n'
            ' ·  · ─┐  ·  ·  5  · \n'
            ' ┌─ ·  ·  ·  ·  ·  · \n'
            ' ·  1  ·  ·  5  ·  · \n'
            ' 1  ·  │  ┌─ ·  ·  · \n'
            ' ·  ·  1  ·  ·  · ─┐ \n'
            ' └─ ·  ·  4  ·  2  · '
        )

        expected_solution_str = (
            ' ┌─────────────────┐ \n'
            ' └─────┐  ┌─────┐  │ \n'
            ' ┌──┐  └──┼─────┼──┘ \n'
            ' │  └──┐  └─────┼──┐ \n'
            ' └──┐  │  ┌──┐  └──┘ \n'
            ' ┌──┘  │  │  │  ┌──┐ \n'
            ' └─────┘  └──┘  └──┘ '
        )

        game_solver = KanjoSolver(Grid.from_str(grid_str, type(Island)))
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_6x6_hard_21xk8(self):
        """https://gridpuzzle.com/kanjo/21xk8"""
        grid_str = (
            ' ·  ·  ·  ·  ·  · \n'
            ' 1  ·  1  │  ·  2 \n'
            ' ·  · ─┼─ ·  ·  · \n'
            ' ·  │  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  │ \n'
            ' ·  3  · ─── ·  · '
        )

        expected_solution_str = (
            ' ┌─────┐  ┌─────┐ \n'
            ' └──┐  │  │  ┌──┘ \n'
            ' ┌──┼──┼──┼──┼──┐ \n'
            ' │  │  │  │  │  │ \n'
            ' │  └──┘  └──┘  │ \n'
            ' └──────────────┘ '
        )

        game_solver = KanjoSolver(Grid.from_str(grid_str, type(Island)))
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_6x6_evil_4njq4(self):
        """https://gridpuzzle.com/kanjo/4njq4"""
        grid_str = (
            ' ·  ·  ·  ·  ·  · \n'
            ' ·  3  ·  2  ·  · \n'
            ' · ─┼─ ·  ·  ┌─ 1 \n'
            ' ·  ·  ·  ·  ·  · \n'
            ' ·  ·  1  · ─┼─ · \n'
            ' ·  3  ·  ·  1  · '
        )

        expected_solution_str = (
            ' ┌──────────────┐ \n'
            ' │  ┌──┐  ┌─────┘ \n'
            ' └──┼──┼──┘  ┌──┐ \n'
            ' ┌──┼──┘  ┌──┼──┘ \n'
            ' │  │  ┌──┼──┼──┐ \n'
            ' └──┘  └──┘  └──┘ '
        )

        game_solver = KanjoSolver(Grid.from_str(grid_str, type(Island)))
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_7x7_evil_16q2d(self):
        """https://gridpuzzle.com/kanjo/16q2d"""
        grid_str = (
            ' 2  ·  ·  3  ·  ·  3 \n'
            ' · ─┐  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  2  · \n'
            ' ·  ·  · ─┼─ ·  ·  · \n'
            ' ·  2  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  · ─┼─ · \n'
            ' 1  ·  ·  2  ·  ·  1 '
        )

        expected_solution_str = (
            ' ┌─────┐  ┌────────┐ \n'
            ' └──┐  └──┼─────┐  │ \n'
            ' ┌──┼──┐  │  ┌──┘  │ \n'
            ' │  │  └──┼──┼──┐  │ \n'
            ' │  └──┐  └──┼──┼──┘ \n'
            ' │  ┌──┼─────┼──┼──┐ \n'
            ' └──┘  └─────┘  └──┘ '
        )

        game_solver = KanjoSolver(Grid.from_str(grid_str, type(Island)))
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_10x10_evil_pg7qg(self):
        """https://gridpuzzle.com/kanjo/pg7qg"""
        grid_str = (
            ' ·  ·  ·  ·  ·  ·  1  ·  ·  -1\n'
            ' ·  ·  ·  4 ─┐  ·  └─ ·  -1 · \n'
            ' · ─── ·  ·  ·  ·  4  ·  ·  │ \n'
            ' ·  ·  ·  └──── · ─┼──┘  ·  · \n'
            ' ·  ·  ┌─ ·  ·  ·  ·  ·  -2─┐ \n'
            ' ┌─ 3  ·  ·  ·  ·  · ─── ·  · \n'
            ' ·  · ─┼──┘  ·  └──┘  ·  ·  · \n'
            ' ┌─ ·  ·  -2 ·  ·  ·  · ─┐  · \n'
            ' ·  -2 · ─┘  · ─┼─ 2  ·  ·  · \n'
            ' -2 ·  ·  -2 ·  ·  ·  ·  ·  · '
        )

        expected_solution_str = (
            ' ┌──────────────┐  ┌──┐  ┌──┐ \n'
            ' └─────┐  ┌──┐  │  └──┘  │  │ \n'
            ' ┌─────┼──┼──┘  │  ┌──┐  │  │ \n'
            ' │  ┌──┘  └─────┼──┼──┘  └──┘ \n'
            ' └──┘  ┌────────┼──┼────────┐ \n'
            ' ┌─────┼──┐  ┌──┼──┼─────┐  │ \n'
            ' └─────┼──┘  │  └──┘  ┌──┘  │ \n'
            ' ┌──┐  └──┐  │  ┌─────┼──┐  │ \n'
            ' │  └─────┘  └──┼──┐  │  │  │ \n'
            ' └──────────────┘  └──┘  └──┘ '
        )

        game_solver = KanjoSolver(Grid.from_str(grid_str, type(Island)))
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_10x10_evil_47nge(self):
        """https://gridpuzzle.com/kanjo/47nge"""
        grid_str = (
           ' ·  ·  ·  ·  2  ·  ·  ·  ·  3 \n'
           ' ·  2  └─ ·  ┌─ ·  ·  · ─┼─ · \n'
           ' ·  ·  · ─┘  ·  ·  ·  2  ·  · \n'
           ' ·  ·  1  ·  │  ·  ·  · ─┐  · \n'
           ' ·  ·  ·  ·  2  ·  ·  ·  ·  · \n'
           ' · ─┐  1  · ─── ·  ·  ·  └─ · \n'
           ' ·  ·  ·  ·  ·  2  ·  ·  ·  1 \n'
           ' · ─┘  1  ·  │  ·  ·  └─ ·  · \n'
           ' ·  ·  ·  ·  ·  1  ·  ·  ·  · \n'
           ' ·  4  ·  └─ · ─── ·  ·  ·  · '
        )

        expected_solution_str = (
            ' ┌──┐  ┌──────────────┐  ┌──┐ \n'
            ' │  │  └──┐  ┌──┐  ┌──┼──┼──┘ \n'
            ' └──┼─────┘  │  │  │  │  └──┐ \n'
            ' ┌──┼─────┐  │  │  └──┼──┐  │ \n'
            ' │  └─────┼──┘  │  ┌──┘  │  │ \n'
            ' └──┐  ┌──┼─────┼──┼──┐  └──┘ \n'
            ' ┌──┼──┼──┼──┐  └──┘  │  ┌──┐ \n'
            ' └──┘  └──┘  │  ┌──┐  └──┼──┘ \n'
            ' ┌─────┐  ┌──┘  └──┼──┐  └──┐ \n'
            ' └─────┘  └────────┘  └─────┘ '
        )

        game_solver = KanjoSolver(Grid.from_str(grid_str, type(Island)))
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
