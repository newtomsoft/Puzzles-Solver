import unittest

from Domain.Board.Grid import Grid
from Domain.Puzzles.Shakashaka.ShakashakaSolver import ShakashakaSolver, ShakashakaCellType

_ = ShakashakaSolver.input_white
B = ShakashakaSolver.input_black

wf = ShakashakaCellType.WHITE_FULL
tl = ShakashakaCellType.WHITE_TL
tr = ShakashakaCellType.WHITE_TR
bl = ShakashakaCellType.WHITE_BL
br = ShakashakaCellType.WHITE_BR
bf = ShakashakaCellType.BLACK_FULL


class ShakashakaSolverTests(unittest.TestCase):
    def test_2x2_empty(self):
        """2x2 Empty Grid -> All Empty (0,0,0,0) or Diamond (1,2,4,3)"""
        grid = Grid([
            [_, _],
            [_, _]
        ])
        expected_white = Grid([[wf, wf], [wf, wf]])
        expected_diamond = Grid([[br, bl], [tr, tl]])
        expected_solutions = {expected_white, expected_diamond}

        solver = ShakashakaSolver(grid)
        solution = solver.get_solution()
        other_solution = solver.get_other_solution()
        solutions = {solution, other_solution}

        self.assertEqual(expected_solutions, solutions)

    def test_impossible_shape(self):
        """2x2 grid, Top-Left 0"""
        grid = Grid([
            [0, _],
            [_, _]
        ])
        solver = ShakashakaSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_3x3_rising(self):
        grid = Grid([
            [2, _, _],
            [_, _, _],
            [_, _, 2],
        ])

        expected_solution = Grid([
            [bf, br, bl],
            [br, wf, tl],
            [tr, tl, bf],
        ])

        solver = ShakashakaSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_3x3_descending(self):
        grid = Grid([
            [_, _, 2],
            [_, _, _],
            [2, _, _],
        ])

        expected_solution = Grid([
            [br, bl, bf],
            [tr, wf, bl],
            [bf, tr, tl],
        ])

        solver = ShakashakaSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_5x5_2169532(self):
        grid = Grid([
            [_, _, _, B, B],
            [B, _, _, _, _],
            [_, _, B, _, _],
            [_, _, _, _, 1],
            [_, B, _, _, _],
        ])

        expected_solution = Grid([
            [wf, br, bl, bf, bf],
            [bf, tr, tl, wf, wf],
            [br, bl, bf, wf, wf],
            [tr, tl, br, bl, bf],
            [wf, bf, tr, tl, wf],
        ])

        solver = ShakashakaSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_10x10_9853297(self):
        grid = Grid([
            [B, _, _, B, _, _, B, _, _, 2],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, B, _, _, B, _, _, _, _],
            [_, 3, _, _, _, _, 4, _, _, _],
            [B, _, _, _, _, _, _, _, _, B],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [3, _, _, _, B, _, 3, _, _, 3],
            [_, _, B, _, _, _, _, _, _, _],
            [_, _, 1, _, _, _, _, _, _, _],
        ])

        expected_solution = Grid([
            [bf, br, bl, bf, br, bl, bf, br, bl, bf],
            [br, wf, tl, wf, tr, tl, br, wf, wf, bl],
            [tr, tl, bf, br, bl, bf, tr, wf, wf, tl],
            [wf, bf, br, wf, wf, bl, bf, tr, tl, wf],
            [bf, br, wf, wf, wf, tl, br, bl, wf, bf],
            [br, wf, wf, wf, tl, br, wf, tl, br, bl],
            [tr, wf, wf, tl, wf, tr, tl, br, wf, tl],
            [bf, tr, tl, wf, bf, wf, bf, tr, tl, bf],
            [br, bl, bf, wf, br, bl, br, bl, br, bl],
            [tr, tl, bf, wf, tr, tl, tr, tl, tr, tl],
        ])

        solver = ShakashakaSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_15x15_5164364(self):
        grid = Grid([
            [B, _, _, _, _, 2, _, _, B, _, _, B, _, _, _],
            [_, _, _, _, _, _, _, 1, _, _, _, _, 3, _, _],
            [_, _, _, _, 3, _, _, _, _, _, _, _, _, _, B],
            [_, _, _, _, _, _, 4, _, _, _, _, _, _, _, _],
            [B, _, 1, B, _, _, _, _, _, _, _, _, 4, _, _],
            [_, _, _, _, B, _, _, _, B, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, B, _, _, B, 0],
            [_, _, _, B, _, B, _, _, B, _, _, _, B, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, 1, _, _],
            [2, _, _, _, _, _, _, B, _, _, B, _, _, _, _],
            [_, _, B, 1, _, B, _, B, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, B, B, B, _, B, B, _, _, _],
            [_, _, _, _, _, _, _, _, _, B, _, _, _, _, 2],
            [B, 2, _, _, _, _, _, B, _, _, _, _, _, _, _],
            [_, _, _, B, _, _, 2, _, _, _, B, 0, _, B, _]
        ])

        expected_solution = Grid([
            [bf, br, bl, br, bl, bf, wf, wf, bf, br, bl, bf, wf, br, bl],
            [wf, tr, tl, tr, tl, br, bl, bf, wf, tr, wf, bl, bf, tr, tl],
            [br, bl, wf, wf, bf, tr, tl, wf, br, bl, tr, tl, br, bl, bf],
            [tr, tl, wf, wf, br, bl, bf, br, wf, tl, br, bl, tr, wf, bl],
            [bf, wf, bf, bf, tr, tl, br, wf, tl, br, wf, tl, bf, tr, tl],
            [br, bl, br, bl, bf, br, wf, tl, bf, tr, tl, br, bl, wf, wf],
            [tr, tl, tr, tl, wf, tr, tl, wf, wf, wf, bf, tr, tl, bf, bf],
            [br, bl, wf, bf, wf, bf, br, bl, bf, br, bl, wf, bf, wf, wf],
            [tr, wf, bl, wf, br, bl, tr, tl, wf, tr, tl, wf, bf, wf, wf],
            [bf, tr, tl, wf, tr, tl, wf, bf, br, bl, bf, br, bl, wf, wf],
            [wf, wf, bf, bf, wf, bf, wf, bf, tr, tl, wf, tr, tl, br, bl],
            [br, bl, wf, br, bl, wf, bf, bf, bf, wf, bf, bf, wf, tr, tl],
            [tr, tl, br, wf, tl, br, bl, wf, wf, bf, wf, wf, br, bl, bf],
            [bf, bf, tr, tl, br, wf, tl, bf, br, bl, wf, wf, tr, tl, wf],
            [wf, wf, wf, bf, tr, tl, bf, wf, tr, tl, bf, bf, wf, bf, wf],
        ])

        solver = ShakashakaSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_20x20_4144598(self):
        grid = Grid([
            [B, B, B, B, B, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, B],
            [B, _, _, _, B, _, _, _, _, _, _, _, B, _, _, _, _, _, _, _],
            [B, _, _, _, 0, 0, 2, _, _, _, _, _, _, _, _, _, 0, _, _, 0],
            [B, _, _, _, B, _, _, _, _, _, _, _, _, _, _, _, 1, _, _, _],
            [_, _, 2, _, _, _, _, _, _, _, _, _, 3, _, _, _, _, _, _, _],
            [_, _, _, _, _, B, _, _, 4, _, _, B, _, _, _, _, _, _, _, B],
            [_, 1, _, _, _, _, _, _, _, _, _, _, _, B, _, _, _, B, _, _],
            [_, B, _, _, _, _, _, _, _, B, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, B, _, _, _, _, B, _, _, B, _, _, _, _, _, _],
            [_, _, _, B, _, _, _, B, _, _, 1, _, _, B, B, _, _, _, _, _],
            [_, _, 2, _, _, _, _, B, _, _, 2, _, _, _, _, _, _, _, _, 1],
            [_, _, _, _, _, _, _, _, B, 1, _, _, 2, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, B, _, _, B, _, _, B, _],
            [_, _, _, _, _, _, _, _, B, B, _, _, _, 0, B, _, _, 4, _, _],
            [B, _, 0, _, _, _, 2, 0, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, B, _, B, _, _, B, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, B, _, _, B, _, _, B, _, _, _, _, _, 2, _, _, _, _],
            [_, _, B, _, _, _, _, _, _, _, _, B, _, _, 4, _, _, 4, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, B, B],
            [2, _, _, _, _, 0, _, _, _, 3, _, _, 2, _, _, B, _, _, _, _]
        ])

        expected_solution = Grid([
            [bf, bf, bf, bf, bf, wf, wf, bf, wf, wf, br, bl, wf, wf, br, bl, wf, br, bl, bf],
            [bf, wf, wf, wf, bf, wf, wf, br, bl, br, wf, tl, bf, br, wf, tl, wf, tr, tl, wf],
            [bf, wf, wf, wf, bf, bf, bf, tr, tl, tr, tl, br, bl, tr, tl, wf, bf, wf, wf, bf],
            [bf, wf, wf, wf, bf, wf, br, bl, br, bl, br, wf, tl, br, bl, wf, bf, br, bl, wf],
            [br, bl, bf, br, bl, wf, tr, tl, tr, tl, tr, tl, bf, tr, wf, bl, wf, tr, tl, wf],
            [tr, tl, wf, tr, tl, bf, br, bl, bf, br, bl, bf, wf, wf, tr, wf, bl, wf, wf, bf],
            [wf, bf, wf, br, bl, br, wf, wf, bl, tr, tl, br, bl, bf, wf, tr, tl, bf, br, bl],
            [wf, bf, br, wf, tl, tr, wf, wf, tl, bf, wf, tr, tl, wf, br, bl, br, bl, tr, tl],
            [br, bl, tr, tl, wf, bf, tr, tl, wf, wf, bf, wf, wf, bf, tr, tl, tr, tl, wf, wf],
            [tr, tl, wf, bf, br, bl, wf, bf, wf, wf, bf, br, bl, bf, bf, wf, br, bl, wf, wf],
            [wf, wf, bf, br, wf, wf, bl, bf, wf, wf, bf, tr, tl, wf, wf, br, wf, wf, bl, bf],
            [wf, wf, br, wf, wf, wf, wf, bl, bf, bf, br, bl, bf, wf, wf, tr, wf, wf, tl, wf],
            [br, bl, tr, wf, wf, wf, wf, tl, wf, wf, tr, tl, bf, wf, wf, bf, tr, tl, bf, wf],
            [tr, tl, wf, tr, wf, wf, tl, wf, bf, bf, br, bl, wf, bf, bf, br, bl, bf, br, bl],
            [bf, wf, bf, wf, tr, tl, bf, bf, wf, br, wf, wf, bl, wf, wf, tr, wf, bl, tr, tl],
            [br, bl, wf, bf, wf, bf, wf, wf, bf, tr, wf, wf, tl, br, bl, wf, tr, wf, bl, wf],
            [tr, tl, wf, bf, br, bl, bf, br, bl, bf, tr, tl, br, wf, tl, bf, wf, tr, wf, bl],
            [br, bl, bf, br, wf, tl, br, wf, wf, bl, wf, bf, tr, tl, bf, br, bl, bf, tr, tl],
            [tr, wf, bl, tr, tl, wf, tr, wf, wf, tl, br, bl, wf, br, bl, tr, wf, bl, bf, bf],
            [bf, tr, tl, wf, wf, bf, wf, tr, tl, bf, tr, tl, bf, tr, tl, bf, tr, tl, wf, wf],
        ])

        solver = ShakashakaSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
