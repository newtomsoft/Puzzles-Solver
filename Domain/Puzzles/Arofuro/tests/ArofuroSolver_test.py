import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Arofuro.ArofuroSolver import ArofuroSolver

_ = ArofuroSolver.Empty
B = ArofuroSolver.Black
N = ArofuroSolver.up
S = ArofuroSolver.down
E = ArofuroSolver.right
W = ArofuroSolver.left
a = 10
b = 11
c = 12
d = 13
e = 14
f = 15

class ArofuroSolverTests(TestCase):
    def test_3x3_invalid(self):
        values_grid = Grid([
            [_, 3, _],
            [_, _, _],
            [_, 3, _]
        ])

        solver = ArofuroSolver(values_grid)
        solution = solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_4x4_basic_with_black(self):
        values_grid = Grid([
            [2, _, _, B],
            [_, B, _, _],
            [_, _, B, 5],
            [2, B, _, _],
        ])

        expected_solution_str = (
            '• ← ↓ • \n'
            '↑ • → ↓ \n'
            '↓ ← • • \n'
            '• • → ↑ '
        )

        solver = ArofuroSolver(values_grid)
        solution_string = solver.solution_to_string()
        self.assertEqual(expected_solution_str, solution_string)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_valid(self):
        values_grid = Grid([
            [5, _, _, 3],
            [_, _, _, _],
            [_, _, _, _],
            [2, _, _, 2],
        ])

        expected_solution_str = (
            '• ↓ → • \n'
            '↑ ← ↑ ← \n'
            '↓ ↑ ← ↓ \n'
            '• ← → • '
        )

        solver = ArofuroSolver(values_grid)
        solution_string = solver.solution_to_string()
        self.assertEqual(expected_solution_str, solution_string)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_evil_375gk(self):
        """https://gridpuzzle.com/arofuro/375gk"""
        values_grid = Grid([
            [1, _, _, 3],
            [B, _, _, B],
            [_, _, _, _],
            [5, _, _, 1]
        ])

        expected_solution_str = (
            '• ← → • \n'
            '• → ↑ • \n'
            '→ ↓ ← ↓ \n'
            '• ← ↑ • '
        )

        solver = ArofuroSolver(values_grid)
        solution_string = solver.solution_to_string()
        self.assertEqual(expected_solution_str, solution_string)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_7x7_evil_jpjm4(self):
        """https://gridpuzzle.com/arofuro/jpjm4"""
        values_grid = Grid([
            [2, _, _, _, 5, _, _],
            [B, _, 5, B, _, _, B],
            [_, _, _, _, _, 8, _],
            [_, 5, _, _, B, _, _],
            [_, B, _, _, _, _, _],
            [3, _, _, _, _, _, _],
            [B, _, _, _, _, 8, _]
        ])

        expected_solution_str = (
            '• ← ↓ → • ↓ ← \n'
            '• ↑ • • ↑ ← • \n'
            '↓ → ↑ ← → • ← \n'
            '→ • ← ↑ • → ↑ \n'
            '↓ • ↑ ← → ↑ ← \n'
            '• ← ↓ → ↓ ← ↑ \n'
            '• ↑ → ↑ → • ← '
        )

        solver = ArofuroSolver(values_grid)
        solution_string = solver.solution_to_string()
        self.assertEqual(expected_solution_str, solution_string)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_9x9_evil_7x8e9(self):
        """https://gridpuzzle.com/arofuro/7x8e9"""
        values_grid = Grid([
            [B, _, _, _, _, _, _, _, B],
            [_, _, B, _, 4, _, B, _, _],
            [_, _, d, _, _, _, f, _, _],
            [B, _, _, B, _, B, _, _, B],
            [_, _, _, 8, _, 4, _, _, _],
            [_, _, _, _, B, _, _, _, _],
            [_, B, _, _, _, _, _, B, _],
            [_, 5, _, _, _, _, _, 5, _],
            [B, _, _, 2, B, 2, _, _, B],
        ])

        expected_solution_str = (
            '• ↓ ← → ↓ ← → ↓ • \n'
            '↓ ← • ↓ • ↓ • → ↓ \n'
            '→ ↓ • ← ↑ → • ↓ ← \n'
            '• → ↑ • ↓ • ↑ ← • \n'
            '→ ↑ → • ← • → ↑ ← \n'
            '↑ → ↑ ← • ↑ ← → ↑ \n'
            '↓ • ↓ ↑ ← → ↑ • ↓ \n'
            '→ • ← ↓ → ↓ → • ← \n'
            '• ↑ → • • • ↑ ← • '
        )

        solver = ArofuroSolver(values_grid)
        solution_string = solver.solution_to_string()
        self.assertEqual(expected_solution_str, solution_string)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
