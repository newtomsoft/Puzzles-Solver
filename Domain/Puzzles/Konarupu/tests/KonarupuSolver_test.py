import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.IslandsGrid import IslandGrid
from Puzzles.Konarupu.KonarupuSolver import KonarupuSolver

_ = ''


class KuroshiroSolverTests(TestCase):
    def test_solution_5x5_37rvk(self):
        grid = Grid([
            [_, 3, 3, _, _],
            [1, 3, 3, _, 4],
            [_, 3, 4, _, 3],
            [3, _, _, 2, 2],
            [3, _, 1, 1, _],
        ])
        expected_solution_str = (
            ' ┌─────┐  ┌─────┐ \n'
            ' │  ┌──┘  │  ┌──┘ \n'
            ' │  │  ┌──┘  └──┐ \n'
            ' │  └──┘  ┌─────┘ \n'
            ' └──┐  ·  └─────┐ \n'
            ' ·  └───────────┘ '
        )
        game_solver = KonarupuSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_5x5_37z54(self):
        grid = Grid([
            [2, 2, _, 1, 2],
            [1, _, _, 3, _],
            [_, 3, _, _, 3],
            [_, 3, _, 2, _],
            [3, _, _, _, 3],
        ])
        expected_solution_str = (
            ' ┌──┐  ┌────────┐ \n'
            ' │  │  │  ┌─────┘ \n'
            ' │  └──┘  └──┐  · \n'
            ' └──┐  ·  ·  └──┐ \n'
            ' ┌──┘  ┌─────┐  │ \n'
            ' └─────┘  ·  └──┘ '
        )
        game_solver = KonarupuSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_5x5_37n71(self):
        grid = Grid([
            [1, _, 4, _, 1],
            [_, 1, 3, 4, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [2, 1, _, 3, 2],
        ])
        expected_solution_str = (
            ' ·  ·  ┌──┐  ·  · \n'
            ' ┌─────┘  └──┐  · \n'
            ' │  ·  ·  ┌──┘  · \n'
            ' └─────┐  │  ·  · \n'
            ' ┌─────┘  └──┐  · \n'
            ' └───────────┘  · '
        )
        game_solver = KonarupuSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_8x8_09w01(self):
        grid = Grid([
            [1, _, 2, 4, 4, 2, _, 3],
            [_, 1, _, _, _, _, 3, _],
            [_, _, _, 3, 3, _, _, _],
            [0, 2, _, _, _, _, 1, 1],
            [0, 2, _, _, _, _, 2, 2],
            [_, _, _, _, _, _, _, _],
            [2, 0, 1, _, _, 3, 3, 2],
            [1, _, _, 4, 4, _, _, 2],
        ])
        expected_solution_str = (
            ' ·  ·  ·  ┌──┐  ┌────────┐ \n'
            ' ┌────────┘  └──┘  ·  ┌──┘ \n'
            ' └─────┐  ·  ┌─────┐  └──┐ \n'
            ' ·  ·  └──┐  └──┐  │  ·  │ \n'
            ' ·  ·  ┌──┘  ·  │  └─────┘ \n'
            ' ·  ·  └─────┐  └─────┐  · \n'
            ' ┌───────────┘  ·  ┌──┘  · \n'
            ' └────────┐  ┌──┐  └─────┐ \n'
            ' ·  ·  ·  └──┘  └────────┘ '
        )
        game_solver = KonarupuSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_12x12_evil_0gqj2(self):
        grid = Grid([
            [_, _, _, 2, _, _, _, _, 1, _, _, _],
            [_, 4, 4, _, 1, 3, 4, 3, _, 4, 2, _],
            [4, _, _, 3, _, _, _, _, 3, _, _, 3],
            [_, 4, _, _, _, 1, 0, _, _, _, 3, _],
            [_, _, _, _, 1, _, _, 2, _, _, _, _],
            [_, 3, _, _, 2, _, _, 1, _, _, 1, _],
            [3, _, _, 2, _, 3, 2, _, 1, _, _, 2],
            [_, 2, 3, 1, _, _, _, _, 0, 1, 3, _],
            [2, 2, _, 2, 2, _, _, 3, 2, _, 2, 2],
            [_, _, _, 1, _, _, _, _, 2, _, _, _],
            [_, _, _, _, 2, _, _, 1, _, _, _, _],
            [2, 1, 2, 3, _, _, _, _, 4, 3, 3, 3]
        ])
        expected_solution_str = (
            ' ·  ┌──┐  ·  ┌─────────────────┐  ·  · \n'
            ' ┌──┘  └──┐  │  ┌──┐  ┌─────┐  └─────┐ \n'
            ' └──┐  ┌──┘  │  │  └──┘  ┌──┘  ┌─────┘ \n'
            ' ┌──┘  └──┐  └──┘  ·  ·  │  ┌──┘  ┌──┐ \n'
            ' │  ┌──┐  └──────────────┘  └─────┘  │ \n'
            ' │  │  └─────┐  ·  ┌─────┐  ·  ·  ·  │ \n'
            ' └──┘  ┌──┐  └─────┘  ·  │  ┌──┐  ·  │ \n'
            ' ┌─────┘  │  ·  ┌──┐  ·  │  │  │  ┌──┘ \n'
            ' └─────┐  └─────┘  └──┐  │  │  └──┘  · \n'
            ' ┌─────┘  ┌─────┐  ·  └──┘  └────────┐ \n'
            ' └─────┐  │  ·  │  ┌───────────┐  ·  │ \n'
            ' ┌─────┘  │  ┌──┘  └─────┐  ┌──┘  ┌──┘ \n'
            ' └────────┘  └───────────┘  └─────┘  · '
        )
        game_solver = KonarupuSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_15x15_evil_pzj1j(self):
        grid = Grid([
            [_, 1, _, _, 4, 4, _, 2, _, 2, 3, _, _, 3, _],
            [2, _, _, _, 3, _, 3, 2, 2, _, 3, _, _, _, 1],
            [0, _, 3, 2, _, 2, _, _, _, 2, _, 2, 2, _, 0],
            [_, 3, _, _, _, _, 1, _, 2, _, _, _, _, 3, _],
            [_, _, _, 2, 0, _, _, _, _, _, 3, 3, _, _, _],
            [_, 2, 3, 2, 1, 0, _, 3, _, 3, 2, 2, 1, 1, _],
            [_, _, _, _, _, _, 3, _, 1, _, _, _, _, _, _],
            [_, _, 1, 2, _, _, _, _, _, _, _, 2, 4, _, _],
            [3, _, _, 3, 4, _, 3, _, 1, _, 2, 2, _, _, 1],
            [_, _, 3, _, _, 4, _, _, _, 4, _, _, 3, _, _],
            [_, 3, _, _, 2, _, 2, _, 2, _, 3, _, _, 2, _],
            [3, 2, _, _, _, _, _, 2, _, _, _, _, _, 3, 4],
            [_, _, _, 4, _, _, _, 3, _, _, _, 4, _, _, _],
            [2, _, 4, _, _, _, 2, _, 3, _, _, _, 2, _, 4],
            [_, 2, 4, 3, 2, 2, _, 3, _, 2, 1, 1, 2, 3, _]
        ])
        expected_solution_str = (
            ' ┌───────────┐  ┌──┐  ┌─────┐  ┌──┐  ┌─────┐  · \n'
            ' └──┐  ·  ·  └──┘  └──┘  ·  │  │  └──┘  ┌──┘  · \n'
            ' ·  │  ·  ┌─────┐  ┌─────┐  └──┘  ┌─────┘  ·  · \n'
            ' ·  │  ┌──┘  ·  │  │  ┌──┘  ·  ·  └─────┐  ·  · \n'
            ' ┌──┘  └──┐  ·  │  │  │  ┌─────┐  ┌──┐  └──┐  · \n'
            ' │  ·  ┌──┘  ·  │  │  └──┘  ┌──┘  │  └─────┘  · \n'
            ' │  ·  └─────┐  │  │  ┌─────┘  ·  └───────────┐ \n'
            ' │  ┌────────┘  └──┘  └──────────────┐  ┌──┐  │ \n'
            ' │  └──┐  ·  ┌──┐  ·  ┌────────┐  ·  └──┘  │  │ \n'
            ' └──┐  │  ┌──┘  └──┐  └─────┐  └─────┐  ┌──┘  │ \n'
            ' ·  └──┘  └──┐  ┌──┘  ┌──┐  └──┐  ┌──┘  │  ┌──┘ \n'
            ' ┌─────┐  ·  │  │  ·  │  │  ·  │  └──┐  │  └──┐ \n'
            ' └──┐  │  ┌──┘  └─────┘  └──┐  └──┐  └──┘  ┌──┘ \n'
            ' ┌──┘  └──┘  ┌──┐  ┌─────┐  │  ┌──┘  ┌──┐  └──┐ \n'
            ' │  ·  ┌──┐  │  │  │  ┌──┘  └──┘  ·  │  │  ┌──┘ \n'
            ' └─────┘  └──┘  └──┘  └──────────────┘  └──┘  · '
        )
        game_solver = KonarupuSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
