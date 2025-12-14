import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.SeeThrough.SeeThroughSolver import SeeThroughSolver

_ = 0


class SeeThroughSolverTests(TestCase):
    def test_solution_basic2x2_no_wall(self):
        grid = Grid([
            [2, 2],
            [2, 2],
        ])

        expected_solution_str = (
            ' ┌─────┐ \n'
            ' │  ·  │ \n'
            ' └─────┘ '
        )

        game_solver = SeeThroughSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(grid.empty(), other_solution)

    def test_solution_basic_2x2_1_wall(self):
        grid = Grid([
            [1, 2],
            [1, 2],
        ])

        expected_solution_str = (
            ' ┌─────┐ \n'
            ' ├──╴  │ \n'
            ' └─────┘ '
        )

        game_solver = SeeThroughSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(grid.empty(), other_solution)

    def test_solution_basic_3x3(self):
        grid = Grid([
            [4, 4, 2],
            [2, 2, 1],
            [2, 3, 2],
        ])

        expected_solution_str = (
            ' ┌────────┐ \n'
            ' │  ╷  ┌──┤ \n'
            ' │  │  ╵  │ \n'
            ' └──┴─────┘ '
        )

        game_solver = SeeThroughSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(grid.empty(), other_solution)

    def test_solution_basic_3x3_2(self):
        grid = Grid([
            [2, 2, _],
            [2, _, _],
            [3, 2, 4],
        ])

        expected_solution_str = (
            ' ┌────────┐ \n'
            ' ├─────┐  │ \n'
            ' │  ╶──┘  │ \n'
            ' └────────┘ '
        )

        game_solver = SeeThroughSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(grid.empty(), other_solution)

    def test_solution_basic_3x3_3(self):
        grid = Grid([
            [2, 4, 3],
            [1, 2, 1],
            [3, 4, 2],
        ])

        expected_solution_str = (
            ' ┌────────┐ \n'
            ' ├──┐  ╷  │ \n'
            ' │  ╵  └──┤ \n'
            ' └────────┘ '
        )

        game_solver = SeeThroughSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(grid.empty(), other_solution)

    def test_solution_4x4_1(self):
        grid = Grid([
            [3, 2, 2, 4],
            [5, 4, 2, 2],
            [3, 2, 2, 3],
            [3, 4, 3, 2],
        ])

        expected_solution_str = (
            ' ┌──┬────────┐ \n'
            ' │  └─────┐  │ \n'
            ' │  ╷  ┌──┘  │ \n'
            ' │  │  ╵  ╶──┤ \n'
            ' └──┴────────┘ '
        )

        game_solver = SeeThroughSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(grid.empty(), other_solution)

    def test_solution_4x4_2(self):
        grid = Grid([
            [3, 2, 2, 4],
            [5, 4, 2, 2],
            [4, 3, 2, 3],
            [3, 4, 3, 2],
        ])

        expected_solution_str = (
            ' ┌──┬────────┐ \n'
            ' │  └─────┐  │ \n'
            ' │  ·  ┌──┘  │ \n'
            ' │  ╷  ╵  ╶──┤ \n'
            ' └──┴────────┘ '
        )

        game_solver = SeeThroughSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(grid.empty(), other_solution)

    def test_solution_5x5(self):
        grid = Grid([
            [5, 7, 5, 4, 4],
            [1, 3, 3, 5, 2],
            [2, 4, 2, 4, 3],
            [4, 5, 3, 3, 2],
            [3, 1, 2, 5, 4],
        ])

        expected_solution_str = (
            ' ┌──────────────┐ \n'
            ' │  ╷  ╷  ╶─────┤ \n'
            ' ├──┤  └──┐  ╶──┤ \n'
            ' │  ╵  ·  │  ╷  │ \n'
            ' │  ╶──┬──┘  ╵  │ \n'
            ' └─────┴────────┘ '
        )

        game_solver = SeeThroughSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(grid.empty(), other_solution)

    def test_solution_5x5_l5mmd(self):
        # https://gridpuzzle.com/seethrough/l5mmd
        grid = Grid([
            [8, 8, 4, 5, 4],
            [7, 7, 4, 4, 1],
            [8, 8, 5, 5, 5],
            [8, 8, 4, 5, 5],
            [8, 8, 4, 4, 5]
        ])

        expected_solution_str = (
            ' ┌──────────────┐ \n'
            ' │  ·  ╶──╴  ┌──┤ \n'
            ' │  ·  ·  ╶──┘  │ \n'
            ' │  ·  ╶──╴  ╶──┤ \n'
            ' │  ·  ╶─────╴  │ \n'
            ' └──────────────┘ '
        )

        game_solver = SeeThroughSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(grid.empty(), other_solution)

    def test_solution_5x5_3jywe(self):
        # https://gridpuzzle.com/seethrough/3jywe
        grid = Grid([
            [6, 6, 6, 2, 1],
            [5, 5, 4, 2, 4],
            [8, 8, 8, 6, 7],
            [6, 6, 6, 3, 4],
            [6, 6, 6, 2, 3]
        ])

        expected_solution_str = (
            ' ┌────────┬─────┐ \n'
            ' │  ·  ╷  │  ╶──┤ \n'
            ' │  ·  ╵  └──╴  │ \n'
            ' │  ·  ·  ╷  ·  │ \n'
            ' │  ·  ·  │  ╷  │ \n'
            ' └────────┴──┴──┘ '
        )

        game_solver = SeeThroughSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(grid.empty(), other_solution)

    def test_solution_5x5_3ejxg(self):
        # https://gridpuzzle.com/seethrough/3ejxg
        grid = Grid([
            [4, 7, 8, 5, 4],
            [2, 6, 7, 4, 3],
            [6, 7, 8, 4, 6],
            [2, 6, 7, 4, 5],
            [4, 4, 8, 5, 6]
        ])

        expected_solution_str = (
            ' ┌──────────────┐ \n'
            ' ├──┐  ·  ·  ╶──┤ \n'
            ' │  ╵  ·  ╶─────┤ \n'
            ' │  ╷  ·  ╶──╴  │ \n'
            ' ├──┴──╴  ·  ·  │ \n'
            ' └──────────────┘ '
        )

        game_solver = SeeThroughSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(grid.empty(), other_solution)

    def test_solution_5x5_37069(self):
        # https://gridpuzzle.com/seethrough/37069
        grid = Grid([
            [1, _, 4, 2, 1],
            [3, 3, _, 3, _],
            [_, 3, _, 5, _],
            [_, 5, _, 4, 4],
            [2, 1, 6, _, 2],
        ])

        expected_solution_str = (
            ' ┌──┬──┬──┬──┬──┐ \n'
            ' │  ╵  ╵  │  ╵  │ \n'
            ' ├──┬──╴  ╵  ╶──┤ \n'
            ' │  └──╴  ╶─────┤ \n'
            ' │  ╷  ╷  ╶─────┤ \n'
            ' └──┴──┴────────┘ '
        )

        game_solver = SeeThroughSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(grid.empty(), other_solution)

    def test_solution_5x5_370zk(self):
        # https://gridpuzzle.com/seethrough/370zk
        grid = Grid([
            [1, 5, 3, 2, 2],
            [4, _, 4, _, _],
            [1, _, 4, _, 4],
            [_, _, 4, _, 2],
            [1, 4, 2, 3, 1],
        ])

        expected_solution_str = (
            ' ┌─────┬────────┐ \n'
            ' ├──╴  ╵  ╶──┬──┤ \n'
            ' │  ╷  ┌─────┘  │ \n'
            ' ├──┘  ╵  ╷  ╷  │ \n'
            ' │  ╷  ╷  │  └──┤ \n'
            ' └──┴──┴──┴─────┘ '
        )

        game_solver = SeeThroughSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(grid.empty(), other_solution)

    def test_solution_10x10_2djnz(self):
        # https://gridpuzzle.com/seethrough/2djnz
        grid = Grid([
            [_, _, 4, _, 1, _, _, 6, _, 5],
            [_, 7, 9, _, 7, _, 7, _, 2, 1],
            [_, 1, 2, _, _, 5, 1, 4, _, _],
            [4, 1, 2, 1, 3, 5, 3, 1, _, 2],
            [5, 2, _, 3, _, 4, _, 1, 1, _],
            [_, 3, 4, _, 3, _, 2, _, 2, 4],
            [3, _, 3, 7, 5, 2, 2, 3, 1, 4],
            [_, _, 2, 4, 1, _, _, 4, 1, _],
            [2, 2, _, 6, _, 3, _, 3, 3, _],
            [4, _, 6, _, _, 4, _, 3, _, _]
        ])

        expected_solution_str = (
            ' ┌────────┬─────┬──────────────┐ \n'
            ' ├─────╴  ╵  ╶──┴─────╴  ┌──┐  │ \n'
            ' │  ╶──┐  ╷  ╶──┐  ╶──┐  ╵  └──┤ \n'
            ' │  ┌──┼──┼──┬──┤  ╶──┼──╴  ╷  │ \n'
            ' │  ╵  │  ╵  ╵  │  ╷  └──┬──┤  │ \n'
            ' │  ╶──┘  ┌──┐  │  │  ┌──┘  ├──┤ \n'
            ' ├──╴  ╶──┘  │  └──┴──┤  ╶──┤  │ \n'
            ' ├─────┬──┐  ├──┬─────┘  ┌──┘  │ \n'
            ' │  ╶──┤  │  ╵  └──┐  ╶──┴──╴  │ \n'
            ' ├──╴  ╵  ╵  ╶──┐  ╵  ╶─────┐  │ \n'
            ' └──────────────┴───────────┴──┘ '
        )

        game_solver = SeeThroughSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
