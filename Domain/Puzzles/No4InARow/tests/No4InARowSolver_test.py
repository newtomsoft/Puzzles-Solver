import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.No4InARow.No4InARowSolver import No4InARowSolver

_ = -1


class No4InARowSolverTests(TestCase):
    def test_solution_grid_too_small(self):
        grid = Grid([
            [_, _, _],
            [_, _, 0],
            [1, _, _],
        ])

        with self.assertRaises(ValueError) as context:
            No4InARowSolver(grid)

        self.assertEqual("No 4 in a Row grid must be at least 4x4", str(context.exception))

    def test_initial_constraint(self):
        grid = Grid([
            [1, 0, 0, 0, 1, 1],
            [1, 0, 1, 0, 0, 0],
            [0, 1, 1, 0, 1, 0],
            [0, 1, 0, 1, 1, 0],
            [1, 1, 1, 0, 0, 1],
            [0, 0, 0, 1, 1, 0],
        ])
        expected_grid = Grid([
            [1, 0, 0, 0, 1, 1],
            [1, 0, 1, 0, 0, 0],
            [0, 1, 1, 0, 1, 0],
            [0, 1, 0, 1, 1, 0],
            [1, 1, 1, 0, 0, 1],
            [0, 0, 0, 1, 1, 0],
        ])
        game_solver = No4InARowSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_horizontally_constraint(self):
        grid = Grid([
            [1, 0, 0, 0, _, 1],
            [1, 0, _, 0, 0, 0],
            [0, 1, 1, 0, 1, 0],
            [0, 1, 0, 1, 1, 0],
            [1, 1, 1, _, 0, 1],
            [0, 0, 0, _, 1, 0],
        ])
        expected_grid = Grid([
            [1, 0, 0, 0, 1, 1],
            [1, 0, 1, 0, 0, 0],
            [0, 1, 1, 0, 1, 0],
            [0, 1, 0, 1, 1, 0],
            [1, 1, 1, 0, 0, 1],
            [0, 0, 0, 1, 1, 0],
        ])
        game_solver = No4InARowSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_vertically_constraint(self):
        grid = Grid([
            [1, 0, 0, 0, 1, _],
            [1, _, 1, 0, 0, 0],
            [0, 1, 1, 0, 1, 0],
            [0, 1, 0, _, 1, 0],
            [1, 1, 1, 0, 0, _],
            [0, _, 0, 1, 1, 0],
        ])
        expected_grid = Grid([
            [1, 0, 0, 0, 1, 1],
            [1, 0, 1, 0, 0, 0],
            [0, 1, 1, 0, 1, 0],
            [0, 1, 0, 1, 1, 0],
            [1, 1, 1, 0, 0, 1],
            [0, 0, 0, 1, 1, 0],
        ])
        game_solver = No4InARowSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_diagonally_constraint(self):
        grid = Grid([
            [1, 0, 0, 0, 1, 1],
            [1, 0, 1, 0, 0, 0],
            [_, 1, 1, 0, _, 0],
            [0, 1, 0, 1, 1, 0],
            [1, 1, 1, 0, 0, 1],
            [0, 0, 0, 1, 1, 0],
        ])
        expected_grid = Grid([
            [1, 0, 0, 0, 1, 1],
            [1, 0, 1, 0, 0, 0],
            [0, 1, 1, 0, 1, 0],
            [0, 1, 0, 1, 1, 0],
            [1, 1, 1, 0, 0, 1],
            [0, 0, 0, 1, 1, 0],
        ])
        game_solver = No4InARowSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
