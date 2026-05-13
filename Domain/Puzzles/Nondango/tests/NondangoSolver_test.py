import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Nondango.NondangoSolver import NondangoSolver


class NondangoSolverTests(TestCase):
    @staticmethod
    def _verify_constraints(solution: Grid, regions_grid: Grid, has_circle_mask: Grid):
        rows = solution.rows_number
        cols = solution.columns_number

        for r in range(rows):
            for c in range(cols - 2):
                if not all(has_circle_mask.value(r, c + i) == 1 for i in range(3)):
                    continue
                if solution.value(r, c) == solution.value(r, c + 1) == solution.value(r, c + 2):
                    return False, "3 consecutive same in row"

        for c in range(cols):
            for r in range(rows - 2):
                if not all(has_circle_mask.value(r + i, c) == 1 for i in range(3)):
                    continue
                if solution.value(r, c) == solution.value(r + 1, c) == solution.value(r + 2, c):
                    return False, "3 consecutive same in column"

        for r in range(rows - 2):
            for c in range(cols - 2):
                if not all(has_circle_mask.value(r + i, c + i) == 1 for i in range(3)):
                    continue
                if solution.value(r, c) == solution.value(r + 1, c + 1) == solution.value(r + 2, c + 2):
                    return False, "3 consecutive same in diagonal (top-left to bottom-right)"

        for r in range(rows - 2):
            for c in range(2, cols):
                if not all(has_circle_mask.value(r + i, c - i) == 1 for i in range(3)):
                    continue
                if solution.value(r, c) == solution.value(r + 1, c - 1) == solution.value(r + 2, c - 2):
                    return False, "3 consecutive same in diagonal (top-right to bottom-left)"

        regions = regions_grid.get_regions()
        for region_id, positions in regions.items():
            circled_positions = [p for p in positions if has_circle_mask[p] == 1]
            if not circled_positions:
                continue
            black_count = sum(1 for pos in circled_positions if solution[pos] == 1)
            if black_count != 1:
                return False, f"Region {region_id} has {black_count} blacks instead of 1"

        return True, "valid"

    @staticmethod
    def _verify_empty_cells(solution: Grid, has_circle_mask: Grid):
        for r in range(solution.rows_number):
            for c in range(solution.columns_number):
                if has_circle_mask.value(r, c) == 0:
                    if solution.value(r, c) is not None:
                        return False, f"Cell ({r},{c}) should be None but has {solution.value(r, c)}"
                else:
                    if solution.value(r, c) not in (0, 1):
                        return False, f"Cell ({r},{c}) should be 0 or 1 but has {solution.value(r, c)}"
        return True, "valid"

    def test_solution_6x6_all_circles(self):
        """6x6 with 2x1 vertical regions, all cells have circles"""
        has_circle_mask = Grid([
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
        ])
        regions_grid = Grid([
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [7, 8, 9, 10, 11, 12],
            [7, 8, 9, 10, 11, 12],
            [13, 14, 15, 16, 17, 18],
            [13, 14, 15, 16, 17, 18],
        ])

        game_solver = NondangoSolver(regions_grid, has_circle_mask)
        solution = game_solver.get_solution()
        self.assertNotEqual(Grid.empty(), solution)
        valid, msg = self._verify_constraints(solution, regions_grid, has_circle_mask)
        self.assertTrue(valid, msg)
        valid, msg = self._verify_empty_cells(solution, has_circle_mask)
        self.assertTrue(valid, msg)

        other_solution = game_solver.get_other_solution()
        self.assertNotEqual(Grid.empty(), other_solution)
        valid, msg = self._verify_constraints(other_solution, regions_grid, has_circle_mask)
        self.assertTrue(valid, msg)

    def test_solution_6x6_partial_circles(self):
        """6x6 with 2x1 vertical regions, some cells without circles"""
        has_circle_mask = Grid([
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 1, 1],
        ])
        regions_grid = Grid([
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [7, 8, 9, 10, 11, 12],
            [7, 8, 9, 10, 11, 12],
            [13, 14, 15, 16, 17, 18],
            [13, 14, 15, 16, 17, 18],
        ])

        game_solver = NondangoSolver(regions_grid, has_circle_mask)
        solution = game_solver.get_solution()
        self.assertNotEqual(Grid.empty(), solution)
        valid, msg = self._verify_constraints(solution, regions_grid, has_circle_mask)
        self.assertTrue(valid, msg)
        valid, msg = self._verify_empty_cells(solution, has_circle_mask)
        self.assertTrue(valid, msg)

        self.assertIsNone(solution.value(5, 2))
        self.assertIsNone(solution.value(5, 3))

    def test_solution_2x2_all_black(self):
        """2x2 where each cell is its own region → each must be black. Works since 2 < 3."""
        has_circle_mask = Grid([
            [1, 1],
            [1, 1],
        ])
        regions_grid = Grid([
            [1, 2],
            [3, 4],
        ])

        game_solver = NondangoSolver(regions_grid, has_circle_mask)
        solution = game_solver.get_solution()
        self.assertNotEqual(Grid.empty(), solution)
        valid, msg = self._verify_constraints(solution, regions_grid, has_circle_mask)
        self.assertTrue(valid, msg)

        for r in range(2):
            for c in range(2):
                self.assertEqual(1, solution.value(r, c))

    def test_solution_4x4_impossible(self):
        """4x4 where each cell is its own region → all must be black → 4 consecutive blacks in row → impossible"""
        has_circle_mask = Grid([
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
        ])
        regions_grid = Grid([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ])

        game_solver = NondangoSolver(regions_grid, has_circle_mask)
        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)


if __name__ == '__main__':
    unittest.main()
