import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Puzzles.Hashi.HashiSolver import HashiSolver

_ = '_'


class HashiSolverTests(TestCase):
    def test_wrong_bridges(self):
        grid = Grid([
            [1, 2]
        ])
        game_solver = HashiSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(IslandGrid.empty(), solution)

    def test_2x2_square(self):
        grid = Grid([
            [2, 2],
            [2, 2]
        ])
        game_solver = HashiSolver(grid)
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
        game_solver = HashiSolver(grid)
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
        game_solver = HashiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_repr = (
            ' ┌──┐ \n'
            ' │  │ \n'
            ' └──┘ '
        )
        self.assertEqual(expected_solution_repr, repr(solution))

    def test_solution_without_crossover(self):
        grid = Grid([
            [1, 4, _, 3],
            [_, _, 2, _],
            [1, _, 4, 4],
            [_, 2, _, _],
            [_, _, 1, _],
            [2, _, _, 2]
        ])

        expected_solution_str = (
            ' ╶──╥─────╖ \n'
            ' ·  ║  ║  ║ \n'
            ' ╷  ║  ├──┤ \n'
            ' │  ║  │  │ \n'
            ' │  ·  ╵  │ \n'
            ' └────────┘ '
        )
        game_solver = HashiSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_with_possible_crossover(self):
        grid = Grid([
            [_, 1, 2],
            [3, _, 3],
            [3, 2, _]
        ])
        game_solver = HashiSolver(grid)

        expected_solution_str = (
            ' ·  ╶──┐ \n'
            ' ╒═════╛ \n'
            ' ╘═══  · '
        )

        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_with_possible_isolated_islands(self):
        grid = Grid([
            [1, 2],
            [1, 2]
        ])
        game_solver = HashiSolver(grid)

        expected_solution_repr = (
            ' ╶──┐ \n'
            ' ╶──┘ '
        )

        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_repr, repr(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_with_possible_isolated_islands_10x10(self):
        grid = Grid([
            [3, _, 4, _, _, 3, _, _, _, 3],
            [_, _, _, _, 2, _, 1, _, 2, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, 3, _, _, _, _, _, _, 3],
            [3, _, _, _, _, _, 1, _, 3, _],
            [_, _, _, _, _, _, _, _, _, _],
            [2, _, _, _, _, _, _, _, _, 2],
            [_, _, 4, _, 4, _, _, _, _, _],
            [2, _, _, _, _, 4, _, _, 2, _],
            [_, 2, _, _, _, _, _, _, _, 3]
        ])

        expected_solution_str = (
            ' ╒═════┬────────┬───────────╖ \n'
            ' │  ·  │  ·  ║  │  ╶─────┐  ║ \n'
            ' │  ·  │  ·  ║  │  ·  ·  │  ║ \n'
            ' │  ·  │  ·  ║  │  ·  ·  │  ║ \n'
            ' │  ·  ║  ·  ║  │  ╶─────┤  │ \n'
            ' ║  ·  ║  ·  ║  │  ·  ·  │  │ \n'
            ' ║  ·  ║  ·  ║  │  ·  ·  │  │ \n'
            ' ·  ·  ╚═════╝  │  ·  ·  │  │ \n'
            ' ═══════════════┴────────┘  │ \n'
            ' ·  ════════════════════════╛ '
        )

        game_solver = HashiSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_multiple_solutions(self):
        grid = Grid([
            [2, 3, 2],
            [3, 4, 3],
            [2, 3, 2]
        ])
        game_solver = HashiSolver(grid)
        solution = game_solver.get_solution()
        solution_count = 1
        while solution != IslandGrid.empty():
            solution = game_solver.get_other_solution()
            solution_count += 1

        self.assertEqual(32, solution_count)


if __name__ == '__main__':
    unittest.main()
