import unittest
from unittest import TestCase

from PuzzleSolver.Board import RegionsGrid
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Heki.HekiSolver import HekiSolver

_ = HekiSolver.cell_empty


class HekiSolverTests(TestCase):
    def test_unique_solution(self):
        grid = Grid([
            [1, _, 2, _, _, _],
            [2, _, 1, _, 3, _],
            [_, 3, _, _, _, _],
        ])
        expected_str = (
            '┌───────────┐\n'
            '├───┬───────┤\n'
            '│   └───┐   │\n'
            '└───────┴───┘\n'
        )
        solver = HekiSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_str, str(solution))
        other = solver.get_other_solution()
        self.assertTrue(other.is_empty())

    def test_solution_6x7(self):
        grid = Grid([
            [_, 1, _, 2, _, _, _],
            [_, 2, _, _, _, 2, 1],
            [_, _, _, 1, 2, _, _],
            [_, 3, _, 1, _, 1, _],
            [2, _, _, _, _, _, _],
            [1, _, _, 2, 2, _, _],
        ])
        expected_str = (
            '┌─┬───────────┐\n'
            '│ └─┬───────┬─┤\n'
            '├─┐ └───┐   │ │\n'
            '│ └───┬─┴─┬─┘ │\n'
            '│   ┌─┴─┐ └─┐ │\n'
            '├───┘   │   │ │\n'
            '└───────┴───┴─┘\n'
        )

        solver = HekiSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_str, str(solution))
        other = solver.get_other_solution()
        self.assertTrue(other.is_empty())

    def test_solution_6x8(self):
        grid = Grid([
                [_, _, 3, _, _, 2, _, _],
                [_, _, 2, _, _, _, _, 2],
                [_, 2, 1, 2, _, _, _, _],
                [2, _, _, 1, _, 3, 3, _],
                [_, _, _, 2, 2, _, _, _],
                [_, _, 1, _, 2, _, _, 2],
        ])
        expected_str = (
            '┌───────┬───────┐\n'
            '├───┐   ├─────┐ │\n'
            '├─┐ ├───┘ ┌───┤ │\n'
            '│ │ └───┬─┘   └─┤\n'
            '│ ├─────┴─────┬─┤\n'
            '│ └───┬───────┘ │\n'
            '└─────┴─────────┘\n'
        )

        solver = HekiSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_str, str(solution))
        other = solver.get_other_solution()
        self.assertTrue(other.is_empty())


if __name__ == '__main__':
    unittest.main()
