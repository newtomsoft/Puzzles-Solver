import unittest
from unittest import TestCase

from Domain.Board.IslandsGrid import IslandGrid
from Domain.Puzzles.GrandTour.GrandTourSolver import GrandTourSolver

_ = 0


class GrandTourSolverTests(TestCase):
    def test_basic_grid_without_island(self):
        grid = IslandGrid([
            [_, _, _, _],
            [_, _, _, _],
        ])
        expected_solution_str = (
            ' ┌────────┐ \n'
            ' └────────┘ '
        )
        game_solver = GrandTourSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_basic_grid_without_island_2(self):
        grid = IslandGrid([
            [_, _],
            [_, _],
            [_, _],
        ])
        expected_solution_str = (
            ' ┌──┐ \n'
            ' │  │ \n'
            ' └──┘ '
        )
        game_solver = GrandTourSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_basic_grid_without_island_no_solution(self):
        grid = IslandGrid([
            [_, _, _],
            [_, _, _],
            [_, _, _],
        ])
        game_solver = GrandTourSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(IslandGrid.empty(), solution)

    def test_asic_grid_without_island_no_solution(self):
        grid = IslandGrid([
            [_, _, _],
            [_, _, _],
            [_, _, _],
        ])
        game_solver = GrandTourSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(IslandGrid.empty(), solution)

    def test_3x3_grid_without_island_no_solution(self):
        grid = IslandGrid([
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        game_solver = GrandTourSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(IslandGrid.empty(), solution)


if __name__ == '__main__':
    unittest.main()
