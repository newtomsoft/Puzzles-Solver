from unittest import TestCase

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Herugolf.HerugolfSolver import HerugolfSolver

_ = HerugolfSolver.cell_empty
W = HerugolfSolver.cell_water
H = HerugolfSolver.cell_hole


class HerugolfSolverTests(TestCase):
    def test_solver_with_puzzlink_3x3_grid(self):
        """https://puzz.link/p?herugolf/3/3/402k1hihi"""
        grid = Grid([
            [2, _, W],
            [_, 1, H],
            [_, H, _],
        ])
        expected = Grid([
            [1, _, W],
            [_, 2, H],
            [2, H, _],
        ])

        solver = HerugolfSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected, solution)

    def test_solver_with_puzzlink_13x12_grid(self):
        """https://puzz.link/p?herugolf/13/12/0000000000000000000c01g0000000003qh3iho2ohk32uhnhkhihy33zx3thiht5t"""
        grid = Grid([
            [3, _, _, _, _, _, _, _, _, _, H, 3, _],
            [H, _, _, _, _, _, _, _, 2, _, _, _, _],
            [_, _, _, H, _, _, _, 3, 2, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, H, _, _, _],
            [_, _, _, H, _, _, _, H, _, H, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, 3, 3, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, W, W, _, _, _, _, _, _],
            [_, _, _, _, _, W, W, _, _, _, _, 3, _],
            [_, _, _, _, _, _, _, _, _, _, _, H, _],
            [H, _, _, _, _, _, _, _, _, _, _, _, _],
            [5, _, _, _, _, _, _, _, _, _, _, _, _],
        ])
        expected = Grid([
            [2, _, _, 1, _, _, _, _, _, _, H, 1, _],
            [H, 4, _, _, _, _, _, _, 2, _, 3, _, _],
            [_, _, _, H, 1, _, _, 4, 1, _, _, _, _],
            [_, 3, _, _, _, _, _, _, _, H, _, 4, _],
            [_, _, _, H, 4, _, _, H, 4, H, _, _, _],
            [_, _, _, _, _, _, _, _, _, 3, _, 4, _],
            [_, 3, 1, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, W, W, _, _, _, _, _, _],
            [_, _, _, _, _, W, W, _, _, _, _, 3, _],
            [1, _, 4, _, _, _, _, _, _, _, _, H, 4],
            [H, _, _, _, _, _, _, _, _, _, _, _, _],
            [2, _, _, _, _, 2, _, _, _, 2, _, _, 3],
        ])
        
        solver = HerugolfSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected, solution)
