import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Detour.DetourSolver import DetourSolver

_ = DetourSolver.empty


class DetourSolverTest(TestCase):
    def test_4x4_easy_l9wxr(self):
        """https://gridpuzzle.com/detour/l9wxr"""
        regions_grid = Grid([
            [1, 2, 2, 3],
            [1, 2, 4, 3],
            [5, 5, 4, 6],
            [7, 5, 4, 6],
        ])
        clues_grid = Grid([
            [1, 1, _, 1],
            [_, _, 2, _],
            [1, _, _, 1],
            [1, _, _, _],
        ])

        expected_solution_str = (
            ' ┌────────┐ \n'
            ' │  ┌──┐  │ \n'
            ' │  │  │  │ \n'
            ' └──┘  └──┘ '
        )

        game_solver = DetourSolver(clues_grid, regions_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_6x6_evil_kd80m(self):
        """https://gridpuzzle.com/detour/kd80m"""
        regions_grid = Grid([
            [1, 1, 1, 2, 2, 2],
            [3, 3, 1, 2, 3, 3],
            [3, 3, 3, 3, 3, 3],
            [3, 4, 4, 4, 4, 3],
            [3, 4, 5, 6, 4, 3],
            [7, 7, 5, 6, 8, 8],
        ])
        clues_grid = Grid([
            [3, _, _, _, _, _],
            [7, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, 2, 0, _, _],
            [_, _, _, _, _, _],
        ])

        expected_solution_str = (
            ' ┌─────┐  ┌─────┐ \n'
            ' │  ┌──┘  │  ┌──┘ \n'
            ' │  └─────┘  └──┐ \n'
            ' │  ┌────────┐  │ \n'
            ' │  │  ┌─────┘  │ \n'
            ' └──┘  └────────┘ '
        )

        game_solver = DetourSolver(clues_grid, regions_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

if __name__ == '__main__':
    unittest.main()
