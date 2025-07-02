import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Puzzles.Wamuzu.WamazuSolver import WamazuSolver

_ = 0


class WamazuSolverTests(TestCase):
    def test_solution_basic_2x2(self):
        grid = Grid([
            [1, 1],
            [_, _]
        ])
        expected_solution_str = (
            ' ╷  ╷ \n'
            ' └──┘ '
        )

        game_solver = WamazuSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_4x4(self):
        grid = Grid([
            [1, 1, _, 1],
            [_, _, _, _],
            [1, 1, _, _],
            [_, 1, 1, 1]
        ])
        expected_solution_str = (
            ' ╷  ╶──┐  ╷ \n'
            ' └──┐  └──┘ \n'
            ' ╷  ╵  ┌──┐ \n'
            ' └──╴  ╵  ╵ '
        )

        game_solver = WamazuSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_5x5_3w0yo(self):
        # https://fr.gridpuzzle.com/wamuzu/3w0yo
        grid = Grid([
            [1, _, _, 1, 1],
            [_, _, _, _, 1],
            [_, 1, 1, _, 1],
            [1, _, _, _, _],
            [1, _, _, _, 1],
        ])
        expected_solution_str = (
            ' ╷  ┌──┐  ╶──╴ \n'
            ' └──┘  └──┐  ╷ \n'
            ' ┌──╴  ╶──┘  ╵ \n'
            ' ╵  ┌──┐  ┌──┐ \n'
            ' ╶──┘  └──┘  ╵ '
        )

        game_solver = WamazuSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_8x8_1ny7k(self):
        # https://fr.gridpuzzle.com/wamuzu/1ny7k
        grid = Grid([
            [_, _, 1, _, _, _, _, _],
            [1, _, _, _, _, _, _, 1],
            [1, 1, _, _, _, _, 1, 1],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, 1, 1, 1, 1, _, _],
            [_, _, _, _, _, _, _, _],
            [_, 1, 1, _, 1, 1, 1, _],
        ])
        expected_solution_str = (
            ' ┌──┐  ╶──┐  ┌──┐  ┌──┐ \n'
            ' ╵  └──┐  └──┘  └──┘  ╵ \n'
            ' ╷  ╶──┘  ┌──┐  ┌──╴  ╷ \n'
            ' └──┐  ┌──┘  └──┘  ┌──┘ \n'
            ' ┌──┘  └──┐  ┌──┐  └──┐ \n'
            ' └──┐  ╷  ╵  ╵  ╵  ┌──┘ \n'
            ' ┌──┘  └──┐  ┌──┐  └──┐ \n'
            ' └──╴  ╶──┘  ╵  ╵  ╶──┘ '
        )

        game_solver = WamazuSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_12x12_0yeg8(self):
        # https://fr.gridpuzzle.com/wamuzu/0yeg8
        grid = Grid([
            [_, _, 1, 1, _, _, 1, _, _, _, 1, _],
            [1, _, _, 1, 1, _, _, _, _, _, 1, 1],
            [1, _, _, _, _, _, 1, 1, _, _, 1, 1],
            [_, _, 1, _, _, 1, _, 1, 1, 1, _, _],
            [1, _, _, 1, 1, 1, _, _, 1, _, _, 1],
            [1, _, _, 1, 1, _, _, _, 1, _, 1, 1],
            [_, 1, _, _, 1, _, 1, 1, _, 1, _, _],
            [_, _, _, 1, _, _, _, 1, _, _, _, _],
            [1, _, _, 1, _, _, _, _, _, 1, _, _],
            [_, _, 1, 1, _, _, _, _, _, _, 1, 1],
            [1, 1, 1, _, _, 1, 1, 1, _, _, 1, _],
            [1, 1, _, _, 1, 1, 1, _, 1, _, 1, 1]
        ])
        expected_solution_str = (
            ' ┌──┐  ╶──╴  ┌──┐  ╶──┐  ┌──┐  ╶──┐ \n'
            ' ╵  └──┐  ╷  ╵  └──┐  └──┘  └──╴  ╵ \n'
            ' ╶──┐  └──┘  ┌──┐  ╵  ╶──┐  ┌──╴  ╷ \n'
            ' ┌──┘  ╷  ┌──┘  ╵  ┌──╴  ╵  ╵  ┌──┘ \n'
            ' ╵  ┌──┘  ╵  ╶──╴  └──┐  ╶──┐  └──╴ \n'
            ' ╷  └──┐  ╷  ╶──┐  ┌──┘  ╷  └──╴  ╷ \n'
            ' └──╴  └──┘  ╶──┘  ╵  ╶──┘  ╷  ┌──┘ \n'
            ' ┌──┐  ┌──╴  ┌──┐  ┌──╴  ┌──┘  └──┐ \n'
            ' ╵  └──┘  ╶──┘  └──┘  ┌──┘  ╷  ┌──┘ \n'
            ' ┌──┐  ╶──╴  ┌──┐  ┌──┘  ┌──┘  ╵  ╷ \n'
            ' ╵  ╵  ╷  ┌──┘  ╵  ╵  ╷  └──┐  ╶──┘ \n'
            ' ╶──╴  └──┘  ╶──╴  ╶──┘  ╶──┘  ╶──╴ '
        )

        game_solver = WamazuSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
