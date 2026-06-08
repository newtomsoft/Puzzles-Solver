import unittest
from unittest import TestCase

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.RegionsGrid import RegionsGrid
from PuzzleSolver.Puzzles.Yonmasu.YonmasuSolver import YonmasuSolver

_ = YonmasuSolver.cell_empty
X = YonmasuSolver.forbidden
o = YonmasuSolver.circle


class YonmasuSolverTests(TestCase):
    def test_known_puzzle_5x5(self):
        """https://gridpuzzle.com/yonmasu/3jgpe"""
        grid = Grid([
            [_, X, _, _, X],
            [o, o, _, _, _],
            [_, _, X, _, _],
            [o, _, o, _, o],
            [X, _, _, X, _],
        ])
        expected_solution_str = (
            "┌─┬─┬───┬─┐\n"
            "│ ├─┘ ┌─┼─┤\n"
            "│ └─┬─┤ │ │\n"
            "├───┼─┘ │ │\n"
            "├─┐ └─┬─┤ │\n"
            "└─┴───┴─┴─┘\n"
        )
        solver = YonmasuSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(RegionsGrid.empty(), other_solution)

    def test_known_puzzle_8x8(self):
        """https://gridpuzzle.com/yonmasu/82765"""
        grid = Grid([
            [_, o, _, _, _, _, X, o],
            [o, X, _, o, _, X, _, _],
            [_, _, o, o, X, _, _, _],
            [_, _, X, _, _, o, _, X],
            [X, _, o, _, _, X, _, o],
            [_, _, _, X, _, _, _, o],
            [o, _, X, _, _, _, X, _],
            [_, X, _, _, o, o, _, _],
        ])
        expected_solution_str = (
            "┌─┬─────┬───┬─┬─┐\n"
            "│ ├─┐ ┌─┘ ┌─┼─┘ │\n"
            "│ ├─┴─┼─┬─┼─┴─┐ │\n"
            "│ │ ┌─┤ └─┤   ├─┤\n"
            "├─┤ ├─┴─┐ ├─┬─┴─┤\n"
            "├─┼─┘ ┌─┼─┼─┘ ┌─┤\n"
            "│ └─┬─┼─┤ └─┬─┤ │\n"
            "│ ┌─┼─┘ └─┐ ├─┘ │\n"
            "└─┴─┴─────┴─┴───┘\n"
        )
        solver = YonmasuSolver(grid)
        solver._solver.parameters.max_time_in_seconds = 60
        solution = solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(RegionsGrid.empty(), other_solution)

    def test_known_puzzle_9x9(self):
        """https://gridpuzzle.com/yonmasu/9w8rr"""
        grid = Grid([
            [o, _, _, _, X, o, _, X, _],
            [_, _, o, _, _, _, _, o, _],
            [X, o, _, _, o, X, _, _, _],
            [o, _, X, o, _, _, _, o, X],
            [_, _, o, _, X, _, _, o, _],
            [X, _, _, _, o, _, X, _, _],
            [o, _, o, X, _, _, _, _, X],
            [_, _, _, _, o, _, _, o, o],
            [_, X, _, _, X, _, _, _, _],
        ])
        expected_solution_str = (
            "┌───────┬─┬───┬─┬─┐\n"
            "├───┬───┴─┴─┐ ├─┘ │\n"
            "├─┐ └─┬─┬─┬─┤ ├─┐ │\n"
            "├─┴─┬─┤ │ └─┼─┘ ├─┤\n"
            "│   ├─┤ ├─┐ │ ┌─┴─┤\n"
            "├─┬─┘ │ ├─┴─┼─┤   │\n"
            "├─┤ ┌─┼─┤   ├─┴─┬─┤\n"
            "│ └─┤ ├─┴───┤   ├─┤\n"
            "│ ┌─┤ └─┬─┐ ├───┘ │\n"
            "└─┴─┴───┴─┴─┴─────┘\n"
        )
        solver = YonmasuSolver(grid)
        solver._solver.parameters.max_time_in_seconds = 60
        solution = solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(RegionsGrid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
