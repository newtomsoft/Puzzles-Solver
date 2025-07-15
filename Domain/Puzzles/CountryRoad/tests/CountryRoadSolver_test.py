import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Puzzles.CountryRoad.CountryRoadSolver import CountryRoadSolver

_ = None


class CountryRoadSolverTests(TestCase):
    def test_basic_grid(self):
        numbers_grid = Grid([
            [3, 3, _],
            [_, _, _],
            [2, _, _]
        ])
        regions_grid = Grid([
            [1, 2, 2],
            [1, 1, 2],
            [3, 3, 3],
        ])
        expected_solution_str = (
           ' ┌─────┐ \n'
           ' └──┐  │ \n'
           ' ·  └──┘ '
        )
        game_solver = CountryRoadSolver(numbers_grid, regions_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_4x4_easy_3nd9w(self):
        numbers_grid = Grid([
            [4, _, _, _],
            [_, 1, _, 3],
            [1, 2, 1, _],
            [_, _, _, _],
        ])
        regions_grid = Grid([
            [1, 1, 1, 1],
            [1, 2, 2, 3],
            [4, 5, 6, 3],
            [4, 5, 6, 3],
        ])

        expected_solution_str = (
            ' ┌─────┐  · \n'
            ' │  ·  └──┐ \n'
            ' └──┐  ·  │ \n'
            ' ·  └─────┘ '
        )
        game_solver = CountryRoadSolver(numbers_grid, regions_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

if __name__ == '__main__':
    unittest.main()
