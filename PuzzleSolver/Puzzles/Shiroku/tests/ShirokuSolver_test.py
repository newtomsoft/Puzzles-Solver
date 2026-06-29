import unittest
from unittest import TestCase

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.Shiroku.ShirokuSolver import ShirokuSolver

_ = ShirokuSolver.cell_empty


class ShirokuSolverTests(TestCase):
    def test_5x6_unique_solution(self):
        grid = Grid([
            [3, _, 3, _, _, _],
            [_, _, _, 1, _, _],
            [_, 1, _, _, _, _],
            [2, _, _, 2, _, 2],
            [_, _, _, 2, _, _],
            [_, 3, _, _, _, 3]
        ])
        expected_solution_str = (
            '┌───┬───────┐\n'
            '├─┐ ├─────┬─┤\n'
            '│ │ └─┐ ┌─┤ │\n'
            '│ │ ┌─┴─┘ │ │\n'
            '│ ├─┴─────┤ │\n'
            '│ └─┬─────┴─┤\n'
            '└───┴───────┘\n'
        )

        solver = ShirokuSolver(grid)
        solution = solver.get_solution()
        self.assertFalse(solution.is_empty())
        self.assertEqual(expected_solution_str, str(solution))

    def test_segment_clues_consistent_solution(self):
        grid = Grid([
            [3, _, 3, _, _, _],
            [_, _, _, 1, _, _],
            [_, 1, _, _, _, _],
            [2, _, _, 2, _, 2],
            [_, _, _, 2, _, _],
            [_, 3, _, _, _, 3]
        ])
        expected_solution_str = (
            '┌───┬───────┐\n'
            '├─┐ ├─────┬─┤\n'
            '│ │ └─┐ ┌─┤ │\n'
            '│ │ ┌─┴─┘ │ │\n'
            '│ ├─┴─────┤ │\n'
            '│ └─┬─────┴─┤\n'
            '└───┴───────┘\n'
        )
        segment_clues = [
            (Position(0, 1), ShirokuSolver.RIGHT_EDGE),
            (Position(0, 2), ShirokuSolver.BOTTOM_EDGE),
            (Position(2, 2), ShirokuSolver.RIGHT_EDGE),
            (Position(2, 2), ShirokuSolver.BOTTOM_EDGE),
        ]

        solver = ShirokuSolver(grid, segment_clues=segment_clues)
        solution = solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))


if __name__ == '__main__':
    unittest.main()