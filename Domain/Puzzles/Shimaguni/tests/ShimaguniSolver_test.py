import unittest
from unittest import TestCase
from Domain.Board.Grid import Grid
from Domain.Puzzles.Shimaguni.ShimaguniSolver import ShimaguniSolver

_ = None

class ShimaguniSolverTests(TestCase):
    def test_solver_returns_non_empty_for_5x5(self):
        # Grid from https://gridpuzzle.com/shimaguni/1nze0
        values_grid = Grid([
            [3, _, 2, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [1, _, _, _, _],
            [4, _, _, 3, _],
        ])
        
        regions_grid = Grid([
            [1, 1, 2, 2, 3],
            [1, 1, 2, 2, 4],
            [1, 5, 5, 5, 4],
            [5, 5, 6, 6, 4],
            [6, 6, 6, 4, 4],
        ])

        solver = ShimaguniSolver(values_grid, regions_grid)
        solution = solver.get_solution()
        
        self.assertNotEqual(Grid.empty(), solution)
        self.assertEqual(values_grid.rows_number, solution.rows_number)
        self.assertEqual(values_grid.columns_number, solution.columns_number)
        
        # Verify unique solution
        self.assertEqual(Grid.empty(), solver.get_other_solution())

    def test_solver_6x6_placeholder(self):
        # Placeholder test for 6x6 grid
        rows, cols = 6, 6
        values_grid = Grid([[None for _ in range(cols)] for _ in range(rows)])
        # Add a few clues
        values_grid[0, 2] = 2
        values_grid[3, 0] = 1
        values_grid[5, 3] = 3

        # Simplified regions_grid for 6x6, ensuring different region IDs
        regions_grid = Grid([
            [1, 1, 2, 2, 2, 2],
            [1, 1, 1, 2, 2, 2],
            [3, 3, 3, 3, 3, 3],
            [4, 4, 4, 4, 4, 4],
            [5, 5, 5, 5, 5, 5],
            [6, 6, 6, 6, 6, 6],
        ])

        solver = ShimaguniSolver(values_grid, regions_grid)
        solution = solver.get_solution()
        
        self.assertNotEqual(Grid.empty(), solution)
        self.assertEqual(rows, solution.rows_number)
        self.assertEqual(cols, solution.columns_number)
        
        # Assuming unique solution for now, might change if solver finds multiple
        self.assertEqual(Grid.empty(), solver.get_other_solution())

    def test_solver_7x7_placeholder(self):
        # Placeholder test for 7x7 grid
        rows, cols = 7, 7
        values_grid = Grid([[None for _ in range(cols)] for _ in range(rows)])
        # Add a few clues
        values_grid[0, 2] = 2
        values_grid[3, 0] = 1
        values_grid[5, 3] = 3

        # Simplified regions_grid for 7x7
        regions_grid = Grid([
            [1, 1, 1, 2, 2, 2, 2],
            [1, 1, 1, 2, 2, 2, 2],
            [3, 3, 3, 3, 3, 3, 3],
            [4, 4, 4, 4, 4, 4, 4],
            [5, 5, 5, 5, 5, 5, 5],
            [6, 6, 6, 6, 6, 6, 6],
            [7, 7, 7, 7, 7, 7, 7],
        ])

        solver = ShimaguniSolver(values_grid, regions_grid)
        solution = solver.get_solution()
        
        self.assertNotEqual(Grid.empty(), solution)
        self.assertEqual(rows, solution.rows_number)
        self.assertEqual(cols, solution.columns_number)
        
        # Assuming unique solution for now
        self.assertEqual(Grid.empty(), solver.get_other_solution())

if __name__ == '__main__':
    unittest.main()
