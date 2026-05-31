import unittest
from unittest import TestCase

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.RegionsGrid import RegionsGrid
from PuzzleSolver.Puzzles.Deddoanguru.DeddoanguruSolver import DeddoanguruSolver

_ = -1


class DeddoanguruSolverTests(TestCase):
    def test_no_solution(self):
        grid = Grid([
            [2, _],
            [_, _],
        ])

        solver = DeddoanguruSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(RegionsGrid.empty(), solution)

    def test_2_solutions_4x4_3e09k(self):
        """https://gridpuzzle.com/deddoanguru/3e09k"""
        grid = Grid([
            [_, 3, 4, _],
            [_, _, _, _],
            [_, _, _, _],
            [_, 1, 0, _],
        ])
        solver = DeddoanguruSolver(grid)
        solution = solver.get_solution()
        self.assertIsInstance(solution, RegionsGrid)
        self.assertNotEqual(RegionsGrid.empty(), solution)
        other_solution = solver.get_other_solution()
        self.assertIsInstance(other_solution, RegionsGrid)
        self.assertNotEqual(RegionsGrid.empty(), other_solution)
        self.assertEqual(RegionsGrid.empty(), solver.get_other_solution())

    def test_solution_5x5_569d0(self):
        """https://gridpuzzle.com/deddoanguru/569d0"""
        grid = Grid([
            [_, _, _, 1, _],
            [_, 2, _, 4, _],
            [_, _, _, _, _],
            [_, 2, _, 3, _],
            [_, 1, _, _, _],
        ])

        expected = (
            "┌─────┬───┐\n"
            "├─┐ ┌─┼─┐ │\n"
            "│ └─┤ │ └─┤\n"
            "├─┐ │ └─┐ │\n"
            "│ └─┤ ┌─┘ │\n"
            "└───┴─┴───┘\n"
        )

        solver = DeddoanguruSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(RegionsGrid.empty(), other_solution)

    def test_solution_6x6_7pv9m(self):
        """https://gridpuzzle.com/deddoanguru/7pv9m"""
        grid = Grid([
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [0, 2, _, _, 2, _],
            [0, 1, 1, _, _, _],
            [4, _, _, _, _, _],
            [_, _, _, _, 1, _],
        ])

        expected = (
            "┌─┬─────┬───┐\n"
            "│ │ ┌───┤   │\n"
            "│ │ │ ┌─┘   │\n"
            "├─┼─┤ └─────┤\n"
            "├─┤ └─┬─┬───┤\n"
            "│ └───┘ │   │\n"
            "└───────┴───┘\n"
        )

        solver = DeddoanguruSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(RegionsGrid.empty(), other_solution)

    def test_solution_7x7_21gey(self):
        """https://gridpuzzle.com/deddoanguru/21gey"""
        grid = Grid([
            [_, 3, _, _, 3, _, _],
            [_, _, 3, _, _, _, _],
            [_, _, _, 3, _, 2, _],
            [_, _, _, 4, 1, _, _],
            [_, _, _, _, _, 0, _],
            [_, _, _, _, _, _, 0],
            [4, _, _, _, 0, _, 0],
        ])

        expected = (
            '┌─┬─────┬─────┐\n'
            '│ └───┐ └─┐   │\n'
            '│ ┌───┴─┐ ├─┐ │\n'
            '│ │ ┌───┼─┤ └─┤\n'
            '├─┘ │ ┌─┘ ├─┐ │\n'
            '├───┘ ├───┴─┼─┤\n'
            '├─────┘ ┌─┐ ├─┤\n'
            '└───────┴─┴─┴─┘\n'
        )

        solver = DeddoanguruSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(RegionsGrid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
