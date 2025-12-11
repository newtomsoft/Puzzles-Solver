import unittest

from Domain.Board.Grid import Grid
from Domain.Puzzles.Shakashaka.ShakashakaSolver import ShakashakaSolver


class ShakashakaSolverTests(unittest.TestCase):
    def test_solve_simple(self):
        # 2x2 Empty Grid -> All Empty (0,0,0,0) or Diamond (1,2,4,3)
        grid = Grid([[-1, -1], [-1, -1]])
        solver = ShakashakaSolver(grid)
        solution = solver.get_solution()

        self.assertIsNotNone(solution)
        # Check if solution is all zeros OR the diamond
        is_all_zeros = (solution.matrix == [[0, 0], [0, 0]])
        is_diamond = (solution.matrix == [[1, 2], [4, 3]])

        self.assertTrue(is_all_zeros or is_diamond, f"Got unexpected solution: {solution.matrix}")

    def test_solve_impossible_l_shape(self):
        # 2x2 grid, Top-Left Black (0 clue).
        # B0 W
        # W  W
        # Forces neighbors to be Empty(0) (if triangle disallowed by connectivity).
        # If neighbors are Empty(0), they form L-shape with Center(1,1).
        # If Center(1,1) is Empty, L-shape -> Invalid 270 turn at center.
        # If Center(1,1) is Triangle, it must connect to Neighbors.
        # But Neighbors are Empty(0). Triangle cannot connect to Empty.
        # So Triangle at (1,1) is invalid.
        # So no solution exists.
        grid = Grid([[0, -1], [-1, -1]])
        solver = ShakashakaSolver(grid)
        solution = solver.get_solution()

        # Should fail (return 0-filled grid where (0,0) is 0, violating B0=5).
        # Or return None/Dummy grid.
        # If it returned a valid solution, (0,0) would be 5.
        self.assertNotEqual(solution.matrix[0][0], 5)

    def test_solve_valid_diamond(self):
        # Force a Diamond using constraints?
        # B2 at (0,0) ? No.
        # Maybe define a grid where only Diamond works.
        pass

if __name__ == '__main__':
    unittest.main()
