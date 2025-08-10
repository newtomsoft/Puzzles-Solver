from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.RegionalYajilin.RegionalYajilinSolver import RegionalYajilinSolver

_ = -1


class RegionalYajilinSolverTests(TestCase):
    def test_solution_5x5_easy_217gy(self):
        """https://gridpuzzle.com/regional-yajilin/217gy"""
        region_grid = Grid([
            [1, 1, 1, 2, 2],
            [1, 1, 1, 2, 2],
            [1, 1, 1, 2, 2],
            [1, 1, 1, 4, 4],
            [3, 3, 3, 4, 4],
        ])
        blacks_count_grid = Grid([
            [2, _, _, 2, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, 0, _],
            [1, _, _, _, _],
        ])

        game_solver = RegionalYajilinSolver(blacks_count_grid, region_grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ■  ┌─────┐  ■ \n'
            ' ┌──┘  ■  └──┐ \n'
            ' │  ┌──┐  ■  │ \n'
            ' │  │  └──┐  │ \n'
            ' └──┘  ■  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_evil_01j11(self):
        """https://gridpuzzle.com/regional-yajilin/01j11"""
        region_grid = Grid([
            [1, 1, 1, 1, 1, 1, 2, 2],
            [3, 3, 3, 4, 4, 4, 4, 4],
            [3, 3, 3, 4, 4, 4, 4, 4],
            [5, 5, 5, 4, 4, 4, 4, 4],
            [5, 5, 5, 6, 6, 7, 7, 7],
            [8, 8, 9, 9, 9, 10, 10, 10],
            [8, 8, 9, 9, 9, 11, 11, 12],
            [8, 8, 9, 9, 9, 11, 11, 12]
        ])
        blacks_count_grid = Grid([
            [1, _, _, _, _, _, 1, _],
            [2, _, _, 3, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, 1, _, _],
            [2, _, 2, _, _, 1, _, _],
            [_, _, _, _, _, 0, _, 0],
            [_, _, _, _, _, _, _, _],
        ])

        game_solver = RegionalYajilinSolver(blacks_count_grid, region_grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐  ■  ┌─────┐  ■ \n'
            ' │  ■  └─────┘  ■  └──┐ \n'
            ' └──┐  ■  ┌─────┐  ■  │ \n'
            ' ■  │  ┌──┘  ■  └──┐  │ \n'
            ' ┌──┘  │  ┌──┐  ■  └──┘ \n'
            ' │  ■  └──┘  └─────┐  ■ \n'
            ' └──┐  ■  ┌─────┐  └──┐ \n'
            ' ■  └─────┘  ■  └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_evil_580d0(self):
        """https://gridpuzzle.com/regional-yajilin/580d0"""
        region_grid = Grid([
            [1, 1, 1, 1, 2, 3, 3, 3, 4, 5],
            [1, 1, 1, 1, 2, 2, 4, 4, 4, 5],
            [6, 1, 7, 2, 2, 4, 4, 4, 4, 5],
            [6, 7, 7, 7, 2, 8, 9, 9, 10, 10],
            [11, 12, 7, 7, 13, 8, 8, 10, 10, 14],
            [11, 12, 12, 13, 13, 8, 15, 15, 10, 14],
            [12, 12, 16, 16, 13, 17, 15, 15, 15, 18],
            [19, 20, 20, 20, 20, 17, 17, 15, 21, 18],
            [19, 20, 20, 20, 17, 17, 21, 21, 21, 21],
            [19, 20, 22, 22, 22, 17, 21, 21, 21, 21]
        ])
        blacks_count_grid = Grid([
            [1, _, _, _, _, 1, _, _, 2, _],
            [_, _, _, _, _, _, _, _, _, _],
            [1, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, 1, 1, _, 1, _],
            [_, 2, _, _, 1, _, _, _, _, 1],
            [_, _, _, _, _, _, 1, _, _, _],
            [_, _, 1, _, _, 1, _, _, _, _],
            [1, 1, _, _, _, _, _, _, 2, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _]
        ])

        game_solver = RegionalYajilinSolver(blacks_count_grid, region_grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌───────────┐  ■  ┌─────┐  ■ \n'
            ' └─────┐  ■  └─────┘  ■  └──┐ \n'
            ' ■  ┌──┘  ┌───────────┐  ■  │ \n'
            ' ┌──┘  ■  └─────┐  ■  └──┐  │ \n'
            ' │  ■  ┌──┐  ■  └──┐  ■  └──┘ \n'
            ' └──┐  │  └──┐  ■  └─────┐  ■ \n'
            ' ■  │  │  ■  └─────┐  ■  └──┐ \n'
            ' ┌──┘  └─────┐  ■  └──┐  ■  │ \n'
            ' └──┐  ■  ┌──┘  ┌─────┘  ┌──┘ \n'
            ' ■  └─────┘  ■  └────────┘  ■ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
