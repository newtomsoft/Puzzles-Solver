import unittest
from Domain.Puzzles.Kurodoko.KurodokoSolver import KurodokoSolver
from Domain.Board.Grid import Grid

class KurodokoSolverTests(unittest.TestCase):
    def test_solve_simple(self):
        # A simple 3x3 or 5x5 example.
        # Let's try a tiny 3x3 one if possible, or just a known 5x5 pattern.
        # 3x3:
        # 2 . .
        # . . 2
        # . . .
        # This might be ambiguous or invalid.

        # Let's take a trivial row: 5 . . . . in 5x5.
        # If (0,0) is 5, then (0,1)..(0,4) must be white (assuming vertical is blocked or valid).

        # Let's try a constructed easy case.
        # 2 2
        # 2 2
        # (This is 2x2).
        # (0,0)=2 -> sees (0,1) or (1,0).
        # If (0,0) sees (0,1), then (0,1) must be white.
        # (0,1) has 2. It sees (0,0). So (0,1) sees (0,0). Total 2. Correct.
        # (1,0) has 2. Sees (1,1).
        # (1,1) has 2. Sees (1,0).
        # But are they connected?
        # (0,0)-(0,1) connected. (1,0)-(1,1) connected.
        # But group 1 and group 2 not connected.
        # So we need a bridge.

        # Let's rely on the solver to handle the logic.
        # 5x5 with a single '9' in the center (2,2).
        # It sees center, plus 2 up, 2 down, 2 left, 2 right => 1+2+2+2+2 = 9.
        # All 9 cells in the cross must be white.
        # The corners must be ... ?
        # If corners are black, connectivity holds (the cross is connected).
        # No adjacent blacks?
        # Corners are (0,0), (0,4), (4,0), (4,4).
        # They are not adjacent to each other.
        # So a cross of whites and 4 black corners is valid for center=9.

        matrix = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 9, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        grid = Grid(matrix)
        solver = KurodokoSolver()
        result = solver.solve(grid)

        # Check center is white (or 9)
        self.assertNotEqual(result.matrix[2][2], 0)

        # Check corners are black (0)
        # Wait, are they constrained to be black?
        # If they were white, they would need to be connected to the center.
        # They would be connected via the arms.
        # But if they are white, the count at center would be > 9?
        # No, visibility is blocked by black cells.
        # If there are NO black cells, the count is 5 (row) + 5 (col) - 1 = 9.
        # So if ALL cells are white, the count is 9.
        # So "All White" is a valid solution for a single '9' clue in center?
        # Yes, 5x5 all white = 9 visible from center.
        # And connectivity holds.
        # And no black cells, so no adjacent black cells.
        # So the corners could be white.

        # So the test might be ambiguous.
        # Let's enforce corners to be black by putting '2' at (0,1).
        # (0,1) sees (0,0)?? No.
        # If (0,1) is 2, and (0,2) is white (part of center cross), (0,1) sees (0,2).
        # That's 2 cells. So (0,0) must be black.

        matrix = [
            [0, 2, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 9, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        # (0,1) is 2.
        # Center cross is White (from 9). So (0,2) is White.
        # (0,1) is White (clue).
        # (0,1) sees (0,2). Distance 1. Total seen so far: 2.
        # It cannot see (0,0) or (0,0) would make it 3. So (0,0) must be Black.
        # It cannot see (1,1) ...

        grid = Grid(matrix)
        result = solver.solve(grid)

        self.assertEqual(result.matrix[0][0], 0) # Black
        self.assertNotEqual(result.matrix[2][2], 0) # White
        self.assertNotEqual(result.matrix[0][1], 0) # White

if __name__ == '__main__':
    unittest.main()
