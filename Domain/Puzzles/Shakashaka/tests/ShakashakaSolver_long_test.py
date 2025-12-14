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


class ShakashakaSolverLongTests(unittest.TestCase):
    def test_25x25_9641761(self):
        grid = Grid([
            [0, _, _, _, B, _, B, _, _, B, B, _, _, B, _, _, _, 2, _, B, _, B, _, _, _],
            [_, _, _, B, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
            [_, _, _, _, _, _, _, _, _, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [B, _, _, 2, _, _, _, _, _, _, _, _, _, B, _, 1, _, _, _, 1, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, 2, B, _, _, _, _, _, _, B, _, _, _, B, B, _, _],
            [0, _, _, _, _, _, 1, _, _, _, _, _, B, _, _, B, _, _, _, _, _, _, _, B, 0],
            [B, _, _, 3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 4, _, _, _, _, 0, _],
            [B, _, _, _, _, B, _, _, _, _, B, _, _, _, _, _, 1, _, _, _, _, _, _, B, _],
            [_, B, 2, _, _, _, _, B, _, _, _, _, B, _, _, _, B, _, _, _, 2, _, _, _, _],
            [_, _, _, _, 4, _, _, _, _, 4, _, _, B, _, _, _, B, _, _, _, _, _, B, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, B, _, B, 1, _, _, _, 2, _, _, _, _, _, _],
            [_, _, _, _, _, _, B, _, _, _, B, _, _, _, _, _, _, _, _, B, 1, 2, _, _, _],
            [B, _, _, B, _, _, _, _, _, B, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 0],
            [_, _, B, _, _, 2, B, _, _, _, _, _, _, _, _, _, _, _, 3, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, B, _, _, _, _, _, _, _, 0, _, B, _, _, B, _, _, _, _],
            [3, _, _, 4, _, _, _, _, _, _, _, _, _, _, _, _, _, _, B, B, _, _, _, _, _],
            [_, _, 4, _, _, _, _, _, 3, _, _, _, _, _, _, _, _, _, _, _, _, _, 2, _, _],
            [_, _, _, _, _, _, _, _, _, 3, _, _, _, _, 4, _, _, B, _, _, _, _, _, _, _],
            [B, _, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, B, B, _, _],
            [_, _, _, _, _, _, _, _, _, _, 1, _, _, _, _, B, 2, _, _, _, _, _, _, _, B],
            [B, _, _, _, _, _, _, _, _, _, B, _, _, B, _, _, _, B, _, _, 4, _, _, _, 0],
            [B, _, B, _, 1, _, _, _, _, _, 2, _, _, 0, _, _, _, 0, _, _, _, B, _, _, _],
            [B, _, B, _, _, 2, _, _, _, _, _, B, B, B, _, _, _, B, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, B, _, _, _, _, _, _, _, B],
            [_, _, B, _, 2, _, _, _, B, _, _, B, _, _, _, _, _, _, _, 3, _, _, _, _, _]
        ])

        expected_solution = Grid([
            [bf, wf, wf, wf, bf, wf, bf, wf, wf, bf, bf, br, bl, bf, wf, br, bl, bf, wf, bf, wf, bf, br, bl, wf],
            [wf, br, bl, bf, br, bl, wf, br, bl, wf, wf, tr, tl, br, bl, tr, tl, br, bl, wf, br, bl, tr, tl, bf],
            [wf, tr, tl, wf, tr, wf, bl, tr, tl, wf, wf, bf, wf, tr, tl, wf, br, wf, tl, wf, tr, wf, bl, wf, wf],
            [bf, br, bl, bf, wf, tr, tl, br, bl, wf, wf, br, bl, bf, wf, bf, tr, tl, wf, bf, wf, tr, tl, wf, wf],
            [wf, tr, tl, br, bl, wf, wf, tr, tl, bf, bf, tr, tl, br, bl, wf, wf, bf, br, bl, wf, bf, bf, wf, wf],
            [bf, wf, wf, tr, wf, bl, bf, wf, wf, br, bl, wf, bf, tr, tl, bf, br, bl, tr, wf, bl, wf, wf, bf, bf],
            [bf, wf, wf, bf, tr, tl, wf, br, bl, tr, tl, br, bl, wf, wf, wf, tr, tl, bf, tr, tl, wf, wf, bf, wf],
            [bf, wf, wf, br, bl, bf, wf, tr, wf, bl, bf, tr, tl, wf, wf, wf, bf, wf, br, bl, wf, br, bl, bf, wf],
            [wf, bf, bf, tr, tl, br, bl, bf, tr, tl, br, bl, bf, wf, wf, wf, bf, br, wf, tl, bf, tr, tl, br, bl],
            [br, bl, br, bl, bf, tr, tl, br, bl, bf, tr, tl, bf, wf, wf, wf, bf, tr, tl, wf, wf, wf, bf, tr, tl],
            [tr, tl, tr, tl, br, bl, wf, tr, wf, bl, wf, bf, wf, bf, bf, br, bl, wf, bf, wf, wf, wf, br, bl, wf],
            [wf, br, bl, wf, tr, tl, bf, wf, tr, tl, bf, wf, br, bl, wf, tr, tl, br, bl, bf, bf, bf, tr, tl, wf],
            [bf, tr, tl, bf, wf, wf, wf, br, bl, bf, br, bl, tr, wf, bl, wf, br, wf, tl, br, bl, br, bl, wf, bf],
            [br, bl, bf, br, bl, bf, bf, tr, tl, br, wf, wf, bl, tr, tl, wf, tr, tl, bf, tr, tl, tr, wf, bl, wf],
            [tr, wf, bl, tr, tl, br, bl, bf, br, wf, wf, wf, wf, bl, wf, bf, wf, bf, wf, wf, bf, wf, tr, tl, wf],
            [bf, tr, tl, bf, br, wf, wf, bl, tr, wf, wf, wf, wf, wf, bl, wf, br, bl, bf, bf, br, bl, wf, br, bl],
            [br, bl, bf, br, wf, wf, wf, tl, bf, tr, wf, wf, wf, wf, tl, wf, tr, tl, wf, wf, tr, tl, bf, tr, tl],
            [tr, tl, br, wf, wf, wf, tl, wf, wf, bf, tr, wf, wf, tl, bf, br, bl, bf, br, bl, wf, wf, wf, br, bl],
            [bf, br, wf, wf, wf, tl, wf, bf, br, bl, wf, tr, tl, br, bl, tr, tl, br, wf, wf, bl, bf, bf, tr, tl],
            [wf, tr, wf, wf, tl, br, bl, wf, tr, tl, bf, wf, wf, tr, tl, bf, bf, tr, wf, wf, tl, br, bl, wf, bf],
            [bf, wf, tr, tl, wf, tr, wf, bl, br, bl, bf, wf, wf, bf, wf, wf, wf, bf, tr, tl, bf, tr, tl, wf, bf],
            [bf, wf, bf, wf, bf, wf, tr, tl, tr, tl, bf, wf, wf, bf, wf, wf, wf, bf, wf, br, bl, bf, br, bl, wf],
            [bf, wf, bf, br, bl, bf, wf, br, bl, br, bl, bf, bf, bf, wf, wf, wf, bf, br, wf, tl, wf, tr, tl, wf],
            [br, bl, wf, tr, tl, br, bl, tr, tl, tr, tl, wf, br, bl, br, bl, bf, br, wf, tl, br, bl, br, bl, bf],
            [tr, tl, bf, wf, bf, tr, tl, wf, bf, wf, wf, bf, tr, tl, tr, tl, wf, tr, tl, bf, tr, tl, tr, tl, wf],
        ])

        solver = ShakashakaSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
