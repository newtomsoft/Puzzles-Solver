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
        """https://gridpuzzle.com/country-road/3nd9w"""
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

    def test_solution_4x4_evil_3nd9w(self):
        """https://gridpuzzle.com/country-road/316n9"""
        numbers_grid = Grid([
            [_, _, _, _],
            [1, _, _, _],
            [_, _, 1, _],
            [_, _, _, _]
        ])
        regions_grid = Grid([
            [1, 1, 1, 2],
            [3, 3, 2, 2],
            [4, 4, 5, 5],
            [6, 6, 6, 5]
        ])

        expected_solution_str = (
            ' ┌────────┐ \n'
            ' │  ·  ┌──┘ \n'
            ' └──┐  │  · \n'
            ' ·  └──┘  · '
        )
        game_solver = CountryRoadSolver(numbers_grid, regions_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_8x8_medium_1pew0(self):
        """https://gridpuzzle.com/country-road/1pew0"""
        numbers_grid = Grid([
            [3, 2, 3, _, _, _, _, _],
            [_, _, _, 2, 2, _, 2, _],
            [_, _, 4, _, _, _, _, _],
            [_, _, _, _, _, 2, _, _],
            [3, _, _, _, _, 3, _, _],
            [2, _, _, 2, _, _, _, _],
            [_, 2, _, 1, 4, _, _, _],
            [_, _, _, _, _, _, _, _]
        ])
        regions_grid = Grid([
            [1, 2, 3, 3, 3, 4, 4, 4],
            [1, 2, 3, 5, 6, 6, 7, 8],
            [1, 1, 9, 5, 10, 10, 7, 8],
            [1, 1, 9, 5, 5, 11, 11, 8],
            [12, 12, 9, 5, 5, 13, 13, 13],
            [14, 12, 9, 15, 15, 13, 13, 13],
            [14, 16, 16, 17, 18, 19, 19, 13],
            [20, 20, 17, 17, 18, 18, 18, 13]
        ])

        expected_solution_str = (
            ' ·  ┌───────────┐  ·  · \n'
            ' ┌──┘  ·  ┌─────┘  ┌──┐ \n'
            ' └─────┐  └────────┘  │ \n'
            ' ·  ·  │  ·  ·  ┌─────┘ \n'
            ' ┌──┐  │  ·  ·  │  ·  · \n'
            ' │  └──┘  ┌──┐  └──┐  · \n'
            ' │  ┌─────┘  │  ·  │  · \n'
            ' └──┘  ·  ·  └─────┘  · '
        )
        game_solver = CountryRoadSolver(numbers_grid, regions_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_12x12_evil_0vdpg(self):
        """https://gridpuzzle.com/country-road/0vdpg"""
        numbers_grid = Grid([
            [10, _, 3, _, _, _, 2, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, 5, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, 1, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, 2],
            [_, _, 2, 5, _, _, _, 2, _, _, _, _],
            [_, _, _, _, 2, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, 3],
            [_, 7, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _]
        ])
        regions_grid = Grid([
            [1, 1, 2, 2, 2, 3, 4, 4, 4, 5, 5, 6],
            [1, 7, 2, 2, 2, 3, 3, 8, 4, 5, 6, 6],
            [1, 7, 9, 2, 10, 11, 8, 8, 12, 12, 12, 13],
            [1, 14, 14, 14, 10, 11, 15, 15, 15, 16, 16, 13],
            [1, 1, 1, 17, 10, 10, 10, 10, 18, 16, 16, 16],
            [1, 1, 1, 17, 17, 17, 10, 10, 18, 18, 18, 19],
            [20, 20, 21, 22, 22, 22, 22, 23, 24, 24, 19, 19],
            [25, 26, 21, 22, 27, 28, 28, 23, 24, 24, 29, 29],
            [25, 26, 21, 22, 27, 30, 23, 23, 23, 31, 29, 32],
            [25, 33, 27, 27, 27, 30, 23, 34, 34, 31, 35, 32],
            [25, 33, 33, 33, 33, 30, 34, 34, 34, 35, 35, 32],
            [25, 33, 33, 33, 33, 30, 36, 36, 36, 37, 32, 32]
        ])

        expected_solution_str = (
           ' ┌──┐  ·  ·  ·  ┌─────┐  ·  ┌──┐  · \n'
           ' │  │  ·  ┌─────┘  ·  │  ·  │  └──┐ \n'
           ' │  └─────┘  ·  ┌─────┘  ┌──┘  ·  │ \n'
           ' │  ·  ┌─────┐  └────────┘  ┌──┐  │ \n'
           ' └──┐  │  ·  └─────┐  ·  ┌──┘  └──┘ \n'
           ' ·  └──┘  ·  ·  ┌──┘  ·  └─────┐  · \n'
           ' ┌──┐  ·  ┌─────┘  ·  ┌──┐  ·  └──┐ \n'
           ' │  └──┐  │  ·  ┌─────┘  └──┐  ┌──┘ \n'
           ' │  ·  │  │  ·  │  ·  ·  ·  │  └──┐ \n'
           ' └──┐  └──┘  ·  │  ·  ┌─────┘  ·  │ \n'
           ' ·  │  ·  ·  ┌──┘  ┌──┘  ·  ┌─────┘ \n'
           ' ·  └────────┘  ·  └────────┘  ·  · '
        )
        game_solver = CountryRoadSolver(numbers_grid, regions_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
