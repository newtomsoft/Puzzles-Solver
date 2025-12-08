import unittest
from Domain.Board.Grid import Grid
from Domain.Puzzles.Slant.SlantSolver import SlantSolver

class SlantSolverTests(unittest.TestCase):
    def test_solve_skeleton(self):
        grid = Grid([['', ''], ['', '']])
        solver = SlantSolver(grid)
        solution = solver.get_solution()
        self.assertIsNotNone(solution)
