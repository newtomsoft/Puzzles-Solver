from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Corral.CorralSolver import CorralSolver

_ = CorralSolver.empty


class CorralSolverTests(TestCase):
    def test_corral_562kr(self):
        """https://gridpuzzle.com/cave/562kr"""
        grid = Grid([
            [_, _, _, _, 3],
            [_, _, 3, _, _],
            [4, _, 5, _, 5],
            [_, _, 5, _, _],
            [5, _, _, _, _],
        ])

        expected_solution = Grid([
            [_, _, _, _, 0],
            [0, _, 0, _, 0],
            [0, _, 0, 0, 0],
            [0, 0, 0, _, _],
            [0, 0, _, _, _],
        ])

        solver = CorralSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_corral_19qmk(self):
        """https://gridpuzzle.com/cave/19qmk"""
        grid = Grid([
            [_, 4, _, _, _, 8, _, _],
            [_, _, _, 4, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [4, _, 5, _, _, _, 6, 7],
            [_, _, _, _, _, 7, _, _],
            [_, _, 5, _, _, _, 6, _],
            [_, 3, _, _, _, _, _, 4],
            [_, _, 8, _, _, _, _, _],
        ])

        expected_solution = Grid([
            [_, 0, _, 0, 0, 0, _, 0],
            [_, 0, 0, 0, _, 0, 0, 0],
            [0, 0, 0, _, _, 0, 0, 0],
            [0, 0, 0, _, 0, 0, 0, 0],
            [_, _, _, _, 0, 0, _, _],
            [0, 0, 0, _, 0, 0, 0, 0],
            [_, 0, 0, _, _, _, 0, 0],
            [_, _, 0, 0, 0, 0, 0, 0],
        ])

        solver = CorralSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_corral_2d0x5(self):
        """https://gridpuzzle.com/cave/2d0x5"""
        grid = Grid([
            [_, _, _, 3, _, _, _, _, _, 2],
            [_, _, _, _, _, _, _, _, 9, _],
            [2, _, _, _, _, 5, _, _, _, _],
            [_, _, _, 8, _, _, _, 8, _, _],
            [_, 9, _, _, _, _, _, _, _, 5],
            [_, _, _, _, _, 2, _, _, 11, _],
            [2, _, _, _, _, _, _, 5, _, _],
            [_, 9, _, 5, _, _, _, _, _, _],
            [2, _, _, _, 7, _, _, _, _, _],
            [_, _, _, _, _, 4, _, _, _, 2],
        ])

        expected_solution = Grid([
            [_, 0, 0, 0, _, _, _, _, 0, 0],
            [_, 0, _, _, _, 0, _, _, 0, _],
            [0, 0, _, 0, 0, 0, _, 0, 0, 0],
            [_, 0, _, 0, 0, 0, 0, 0, 0, 0],
            [_, 0, _, _, _, _, _, _, 0, 0],
            [_, 0, 0, 0, _, 0, _, 0, 0, 0],
            [0, 0, _, 0, _, 0, 0, 0, 0, _],
            [_, 0, _, 0, _, _, _, _, 0, _],
            [0, 0, _, 0, 0, 0, 0, 0, 0, 0],
            [_, _, _, 0, _, 0, 0, 0, _, 0],
        ])

        solver = CorralSolver(grid)
        solution = solver.get_solution()

        self.assertEqual(expected_solution, solution)

    def test_corral_11q2r(self):
        """https://gridpuzzle.com/cave/11q2r"""
        grid = Grid([
            [_, _, _, 5, _, _, _, 2, _, _, _, _],
            [_, _, _, _, 8, _, _, _, _, _, _, 6],
            [6, _, 16, _, _, _, _, _, _, _, 5, _],
            [_, _, _, _, _, _, _, _, 6, _, _, 6],
            [_, _, _, _, _, 5, 3, _, _, _, _, _],
            [_, _, 12, _, _, _, _, _, 5, _, _, _],
            [_, _, _, 5, _, _, _, _, _, 16, _, _],
            [_, _, _, _, _, 4, 3, _, _, _, _, _],
            [5, _, _, 5, _, _, _, _, _, _, _, _],
            [_, 6, _, _, _, _, _, _, _, 12, _, 4],
            [7, _, _, _, _, _, _, 4, _, _, _, _],
            [_, _, _, _, 7, _, _, _, 7, _, _, _],
        ])

        expected_solution = Grid([
            [0, _, 0, 0, _, _, _, 0, _, 0, _, _],
            [0, 0, 0, 0, 0, _, 0, 0, 0, 0, 0, 0],
            [0, _, 0, 0, 0, 0, 0, _, 0, 0, 0, _],
            [0, _, 0, 0, 0, 0, _, _, 0, 0, 0, 0],
            [0, _, 0, _, 0, 0, 0, _, _, 0, _, 0],
            [0, _, 0, _, _, _, _, _, 0, 0, _, 0],
            [_, _, 0, 0, _, 0, 0, 0, 0, 0, _, _],
            [0, _, 0, 0, _, 0, 0, _, 0, 0, _, 0],
            [0, _, 0, 0, _, 0, _, _, 0, 0, _, 0],
            [0, 0, 0, 0, _, _, _, _, _, 0, _, 0],
            [0, 0, 0, _, _, 0, 0, 0, _, 0, 0, 0],
            [0, 0, 0, _, 0, 0, 0, 0, 0, 0, 0, _],
        ])

        solver = CorralSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        self.assertTrue(solver.get_other_solution().is_empty())
