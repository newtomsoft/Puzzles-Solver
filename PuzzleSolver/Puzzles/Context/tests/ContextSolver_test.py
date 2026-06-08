import unittest

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Context.ContextSolver import ContextSolver

_ = ContextSolver.cell_empty
B = ContextSolver.black
W = ContextSolver.white

class ContextSolverTests(unittest.TestCase):
    def test_simple_2x2(self):
        grid = Grid([
            [1, _],
            [_, _],
        ])

        expected0 = Grid([
            [W, W],
            [B, W]
        ])
        expected1 = Grid([
            [W, B],
            [W, W]
        ])

        solver = ContextSolver(grid)
        solution0 = solver.get_solution()
        solution1 = solver.get_other_solution()
        self.assertEqual({expected0, expected1}, {solution0, solution1})
        other = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other)

    def test_8x8_from_puzzlink(self):
        # Grid from: https://puzz.link/p?context/8/8/k1j2i3h2h3n1j3n1h2h2i2j2k
        grid = Grid([
            [_, _, _, _, _, 1, _, _],
            [_, _, 2, _, _, _, 3, _],
            [_, 2, _, _, 3, _, _, _],
            [_, _, _, _, _, 1, _, _],
            [_, _, 3, _, _, _, _, _],
            [_, _, _, 1, _, _, 2, _],
            [_, 2, _, _, _, 2, _, _],
            [_, _, 2, _, _, _, _, _],
        ])
        solver = ContextSolver(grid)
        solution = solver.get_solution()
        expected = Grid([
            [W, W, W, W, W, W, W, W],
            [W, B, W, B, W, B, W, B],
            [B, W, W, W, B, W, B, W],
            [W, W, W, B, W, W, W, W],
            [W, W, B, W, W, B, W, W],
            [W, B, W, B, W, W, B, W],
            [W, W, W, W, W, B, W, W],
            [W, B, W, B, W, W, B, W],
        ])
        self.assertEqual(expected, solution)
        other = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other)


if __name__ == '__main__':
    unittest.main()
