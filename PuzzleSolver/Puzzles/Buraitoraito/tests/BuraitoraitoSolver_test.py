import unittest
from unittest import TestCase
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Buraitoraito.BuraitoraitoSolver import BuraitoraitoSolver

class BuraitoraitoSolverTests(TestCase):
    def test_6x6_puzzle(self):
        grid = Grid([
            [0, 2, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 2, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ])
        solver = BuraitoraitoSolver(grid)
        solution = solver.get_solution()
        self.assertNotEqual(Grid.empty(), solution)

if __name__ == '__main__':
    unittest.main()
