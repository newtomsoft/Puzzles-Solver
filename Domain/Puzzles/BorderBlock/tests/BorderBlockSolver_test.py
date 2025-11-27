import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.BorderBlock.BorderBlockSolver import BorderBlockSolver

_ = BorderBlockSolver.empty


class BorderBlockSolverTests(TestCase):
    def test_multiple_solution(self):
        grid = Grid([
            [1, _, _],
            [_, 2, _],
            [_, _, 3],
        ])
        dots_positions = [
            Position(-0.5, 0.5), Position(0.5, -0.5), Position(2.5, 0.5), Position(1.5, -0.5)
        ]

        game_solver = BorderBlockSolver(grid, dots_positions)
        self.assertNotEqual(Grid.empty(), game_solver.get_solution())
        self.assertNotEqual(Grid.empty(), game_solver.get_other_solution())

    # work when contigus cells
    def test_unique_solution(self):
        grid = Grid([
            [1, _, _],
            [_, 2, _],
            [_, _, 3],
        ])
        dots_positions = [
            Position(-0.5, 0.5), Position(0.5, -0.5), Position(2.5, 1.5), Position(1.5, 2.5)
        ]

        expected_grid = Grid([
            [1, 2, 2],
            [2, 2, 2],
            [2, 2, 3]
        ])
        game_solver = BorderBlockSolver(grid, dots_positions)
        self.assertEqual(expected_grid, game_solver.get_solution())
        self.assertNotEqual(Grid.empty(), game_solver.get_other_solution())

    def test_impossible_configuration(self):
        grid = Grid([
            [1, _, _],
            [1, 2, _],
            [_, _, _],
        ])
        dots_positions = [
            Position(-0.5, 0.5), Position(0.5, -0.5)
        ]

        game_solver = BorderBlockSolver(grid, dots_positions)
        self.assertEqual(Grid.empty(), game_solver.get_solution())

    def test_basic_numbers_constraints(self):
        grid = Grid([
            [1, _, _],
            [4, 2, 3],
            [_, _, _],
        ])
        dots_positions = [
            Position(-0.5, 0.5), Position(0.5, -0.5), Position(0.5, 0.5), Position(2.5, 0.5), Position(2.5, 1.5)
        ]

        expected_grid = Grid([
            [1, 3, 3],
            [4, 2, 3],
            [4, 2, 3]
        ])
        game_solver = BorderBlockSolver(grid, dots_positions)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
