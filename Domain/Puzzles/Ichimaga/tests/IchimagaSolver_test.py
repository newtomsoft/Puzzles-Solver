import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Puzzles.Ichimaga.IchimagaSolver import IchimagaSolver

_ = IchimagaSolver.Empty


class IchimagaSolverTests(TestCase):
    # region no turn
    def test_wrong_bridges(self):
        grid = Grid([
            [1, 2]
        ])
        game_solver = IchimagaSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(IslandGrid.empty(), solution)

    def test_2x2_square(self):
        grid = Grid([
            [2, 2],
            [2, 2]
        ])
        game_solver = IchimagaSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_repr = (
            ' ┌──┐ \n'
            ' └──┘ '
        )
        self.assertEqual(expected_solution_repr, repr(solution))

    def test_3x2_square(self):
        grid = Grid([
            [2, 2],
            [2, 2],
            [_, _]
        ])
        game_solver = IchimagaSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_repr = (
            ' ┌──┐ \n'
            ' └──┘ \n'
            ' ·  · '
        )
        self.assertEqual(expected_solution_repr, repr(solution))

    def test_3x2_rectangle(self):
        grid = Grid([
            [2, 2],
            [_, _],
            [2, 2]
        ])
        game_solver = IchimagaSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_repr = (
            ' ┌──┐ \n'
            ' │  │ \n'
            ' └──┘ '
        )
        self.assertEqual(expected_solution_repr, repr(solution))

    def test_solution_with_possible_isolated_islands(self):
        grid = Grid([
            [1, 2],
            [1, 2]
        ])
        game_solver = IchimagaSolver(grid)

        expected_solution_repr = (
            ' ╶──┐ \n'
            ' ╶──┘ '
        )

        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_repr, repr(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    # endregion

    def test_5x5_3n82k(self):
        """https://gridpuzzle.com/ichimaga/3n82k"""
        grid = Grid([
            [_, _, _, _, 1],
            [1, 1, _, _, _],
            [_, _, _, _, _],
            [3, 3, _, 4, 2],
            [_, _, _, 3, 2],
        ])

        expected_solution_repr = (
            ' ·  ·  ·  ┌──╴ \n'
            ' ╷  ╷  ·  │  · \n'
            ' │  │  ·  │  · \n'
            ' ├──┴─────┼──┐ \n'
            ' └────────┴──┘ '
        )

        game_solver = IchimagaSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_repr, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_7x7_0x8y1(self):
        """https://gridpuzzle.com/ichimaga/0x8y1"""
        grid = Grid([
            [_, _, _, _, _, 1, _],
            [1, 1, 1, 2, _, 1, _],
            [_, _, _, 4, _, _, 2],
            [3, _, _, 3, _, _, 2],
            [3, _, _, 3, _, _, _],
            [_, 4, _, 2, 2, 4, 1],
            [_, 2, _, _, _, _, _],
        ])

        expected_solution_str = (
            ' ·  ·  ·  ·  ·  ╶──┐ \n'
            ' ╷  ╷  ╶──┐  ·  ╷  │ \n'
            ' │  └─────┼─────┘  │ \n'
            ' ├────────┤  ·  ┌──┘ \n'
            ' ├──┐  ·  ├──┐  │  · \n'
            ' └──┼─────┘  └──┼──╴ \n'
            ' ·  └───────────┘  · '
        )

        game_solver = IchimagaSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_10x10_0xkp2(self):
        """https://gridpuzzle.com/ichimaga/0xkp2"""
        grid = Grid([
            [_, 3, 2, _, _, 3, _, _, _, 1],
            [2, _, _, _, _, _, _, _, _, 3],
            [2, _, 3, _, _, 2, _, _, _, 2],
            [2, _, _, 4, 4, _, _, 1, _, 2],
            [_, _, 2, 2, _, 1, _, _, _, _],
            [_, _, _, _, 4, _, 2, 3, _, _],
            [2, _, 1, _, _, 4, 3, _, _, 2],
            [2, _, _, _, 3, _, _, 1, _, 2],
            [1, _, _, _, _, _, _, _, _, 1],
            [1, _, _, _, 1, _, _, 2, 2, _],
        ])

        expected_solution_str = (
            ' ┌──┬──┐  ·  ┌──┬─────┐  ·  ╷ \n'
            ' │  │  │  ·  │  │  ·  │  ┌──┤ \n'
            ' │  │  ├──┐  │  │  ·  │  │  │ \n'
            ' │  │  └──┼──┼──┘  ·  ╵  │  │ \n'
            ' │  │  ┌──┘  │  ╶─────┐  │  │ \n'
            ' │  │  └─────┼──┐  ┌──┤  │  │ \n'
            ' │  │  ╷  ·  └──┼──┤  │  │  │ \n'
            ' │  │  └─────┬──┘  │  ╵  │  │ \n'
            ' ╵  │  ·  ·  │  ·  │  ·  │  ╵ \n'
            ' ╶──┘  ·  ·  ╵  ·  └─────┘  · '
        )

        game_solver = IchimagaSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
