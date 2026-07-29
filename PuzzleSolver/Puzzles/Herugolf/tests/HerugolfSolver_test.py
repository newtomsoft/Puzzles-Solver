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
        expected_str = (
            "↓ _ W\n"
            "↓ → H\n"
            "→ H _"
        )
        
        solver = HerugolfSolver(grid)
        solution = solver.get_solution()
        self.assertFalse(solution.is_empty())
        self.assertEqual(expected_str, str(solution))

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
        expected_str = (
            "→ → → ↓ _ _ _ _ _ _ H ↓ _\n"
            "H ← _ ↓ _ _ _ _ → → ↑ ↓ _\n"
            "_ ↑ _ H ↓ ← ← ← ↓ _ _ ↓ _\n"
            "_ ↑ _ _ ↓ _ _ _ ↓ H ← ← _\n"
            "_ ↑ _ H ← _ _ H ← H _ _ _\n"
            "_ ↑ _ _ _ _ _ _ _ ↑ ← ← _\n"
            "_ ↑ ↓ _ _ _ _ _ _ _ _ ↑ _\n"
            "_ _ ↓ _ _ W W _ _ _ _ ↑ _\n"
            "_ _ ↓ _ _ W W _ _ _ _ ↑ _\n"
            "↓ ← ← _ _ _ _ _ _ _ _ H ←\n"
            "H _ _ _ _ _ _ _ _ _ _ _ ↑\n"
            "→ → → → → → → → → → → → ↑"
        )
        
        solver = HerugolfSolver(grid)
        solution = solver.get_solution()
        self.assertFalse(solution.is_empty())
        self.assertEqual(expected_str, str(solution))
