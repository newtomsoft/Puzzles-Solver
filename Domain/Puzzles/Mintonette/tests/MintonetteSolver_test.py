import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Mintonette.MintonetteSolver import MintonetteSolver


class MintonetteSolverTests(TestCase):
    def test_solution_4x4_easy(self):
        values_grid = Grid([
            [0, 0, None, None],
            [0, 1, None, 0],
            [None, 0, 1, 0],
            [None, None, 0, 0]
        ])

        solver = MintonetteSolver(values_grid)
        solution = solver.get_solution()
        
        # TODO: Verify the solution once solver is implemented
        # For now, just check that we get a non-empty solution
        self.assertIsNotNone(solution)

    def test_solution_4x4_evil(self):
        values_grid = Grid([
            [0, 0, None, None],
            [0, 1, None, 0],
            [None, 0, 1, 0],
            [None, None, 0, 0]
        ])

        solver = MintonetteSolver(values_grid)
        solution = solver.get_solution()
        
        # TODO: Verify the solution once solver is implemented
        # For now, just check that we get a non-empty solution
        self.assertIsNotNone(solution)


if __name__ == '__main__':
    unittest.main()
