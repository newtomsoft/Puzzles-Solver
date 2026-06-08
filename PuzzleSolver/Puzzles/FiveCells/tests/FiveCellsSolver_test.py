import unittest
from unittest import TestCase

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.FiveCells.FiveCellsSolver import FiveCellsSolver

_ = FiveCellsSolver.cell_empty
X = FiveCellsSolver.cell_blocked

class FiveCellsSolverTests(TestCase):
    def test_5x5_multiple(self):
        grid = Grid([
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
        ])

        game_solver = FiveCellsSolver(grid)
        solution = game_solver.get_solution()
        self.assertFalse(solution.is_empty())
        other_solution = game_solver.get_other_solution()
        self.assertFalse(other_solution.is_empty())
        self.assertNotEqual(solution, other_solution)

    def test_5x5_unique(self):
        grid = Grid([
            [_, _, 2, _, 3],
            [_, _, _, 1, 2],
            [_, 0, _, _, _],
            [_, _, 3, _, 1],
            [_, _, 2, _, 2],
        ])

        expected_solution_str = (
            '┌───────┬─┐\n'
            '│ ┌─┬───┘ │\n'
            '├─┘ └─┐ ┌─┤\n'
            '├─┐ ┌─┼─┘ │\n'
            '│ └─┘ │   │\n'
            '└─────┴───┘\n'
        )

        game_solver = FiveCellsSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        self.assertTrue(game_solver.get_other_solution().is_empty())


    def test_5x6_unique(self):
        grid = Grid([
            [_, _, _, _, 1, _],
            [_, 3, 0, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, 3, 2, _],
            [_, 3, _, _, _, _],
        ])

        expected_solution_str = (
            '┌───┬─┬─────┐\n'
            '│ ┌─┘ └─┐   │\n'
            '│ └─┐ ┌─┴───┤\n'
            '├───┴─┴─┐   │\n'
            '│ ┌─────┴───┤\n'
            '└─┴─────────┘\n'
        )

        game_solver = FiveCellsSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_5x5_with_blocked_cells_multiple(self):
        grid = Grid([
            [X, _, _, _, X],
            [_, _, _, _, _],
            [_, _, X, _, _],
            [_, _, _, _, _],
            [X, _, _, _, X],
        ])

        game_solver = FiveCellsSolver(grid)
        solution = game_solver.get_solution()
        self.assertFalse(solution.is_empty())
        other_solution = game_solver.get_other_solution()
        self.assertFalse(other_solution.is_empty())
        self.assertNotEqual(solution, other_solution)

    def test_5x5_with_blocked_cells_unique(self):
        grid = Grid([
            [X, 2, 2, 3, X],
            [3, 1, 2, 2, 2],
            [2, 2, X, 3, 2],
            [2, 1, 2, 1, 3],
            [X, 3, 2, 2, X],
        ])

        expected_solution_str = (
            '┌─┬───┬─┬─┐\n'
            '├─┘   │ └─┤\n'
            '├───┬─┼─┐ │\n'
            '│   ├─┘ │ │\n'
            '├─┐ │   ├─┤\n'
            '└─┴─┴───┴─┘\n'
        )

        game_solver = FiveCellsSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        self.assertTrue(game_solver.get_other_solution().is_empty())

    def test_7x7_corners_blocked(self):
        grid = Grid([
            [X, _, _, _, _, _, X],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
            [X, _, _, _, _, _, X],
        ])

        game_solver = FiveCellsSolver(grid)
        solution = game_solver.get_solution()
        self.assertFalse(solution.is_empty())
        other_solution = game_solver.get_other_solution()
        self.assertFalse(other_solution.is_empty())
        self.assertNotEqual(solution, other_solution)

    def test_8x8_corners_blocked(self):
        grid = Grid([
            [X, _, _, _, _, _, _, X],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [X, _, _, _, _, _, _, X],
        ])

        game_solver = FiveCellsSolver(grid)
        solution = game_solver.get_solution()
        self.assertFalse(solution.is_empty())
        other_solution = game_solver.get_other_solution()
        self.assertFalse(other_solution.is_empty())
        self.assertNotEqual(solution, other_solution)

    def test_8x8_unique_solution(self):
        grid = Grid([
            [X, 3, _, 2, _, 2, 3, X],
            [_, 1, 3, 1, _, _, 1, _],
            [_, 3, 2, _, 3, 2, 2, 2],
            [_, 2, 2, _, 2, _, 3, 3],
            [_, _, 3, 3, _, 2, 3, _],
            [_, 3, 2, 2, _, _, _, 2],
            [2, 2, 2, _, 3, 2, _, 2],
            [X, 3, _, _, 2, _, _, X],
        ])

        expected_solution_str = (
            '┌─┬─┬───┬───┬─┬─┐\n'
            '├─┘ └─┐ └─┐ │ └─┤\n'
            '│ ┌───┤ ┌─┘ │   │\n'
            '├─┴─┐ └─┼───┴─┬─┤\n'
            '├─┐ └─┐ │   ┌─┤ │\n'
            '│ │ ┌─┴─┴─┬─┘ │ │\n'
            '│ └─┤ ┌─┬─┘ ┌─┘ │\n'
            '├─┐ │ │ └───┴─┬─┤\n'
            '└─┴─┴─┴───────┴─┘\n'
        )

        game_solver = FiveCellsSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_9x9_center_blocked(self):
        grid = Grid([
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, X, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
        ])

        game_solver = FiveCellsSolver(grid)
        solution = game_solver.get_solution()
        self.assertFalse(solution.is_empty())
        other_solution = game_solver.get_other_solution()
        self.assertFalse(other_solution.is_empty())
        self.assertNotEqual(solution, other_solution)


if __name__ == '__main__':
    unittest.main()
