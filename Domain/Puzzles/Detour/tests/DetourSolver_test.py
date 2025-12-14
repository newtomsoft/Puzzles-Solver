import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Detour.DetourSolver import DetourSolver

# region
_ = DetourSolver.empty
a = 10
b = 11
c = 12
d = 13
e = 14
f = 15
g = 16
h = 17
i = 18
j = 19
k = 20
l = 21
m = 22
n = 23
o = 24
p = 25
q = 26


# endregion


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

    def test_8x8_evil_e5j72(self):
        """https://gridpuzzle.com/detour/e5j72"""
        regions_grid = Grid([
            [1, 1, 2, 2, 2, 3, 3, 3],
            [1, 1, 4, 2, 3, 3, 5, 3],
            [6, 1, 4, 2, 5, 5, 5, 3],
            [6, 6, 4, 2, 7, 7, 7, 7],
            [8, 6, 6, 6, 9, 7, 7, 7],
            [8, 8, a, 9, 9, 7, b, b],
            [8, a, a, 9, 9, c, c, c],
            [8, 8, 8, 9, 9, c, c, c],
        ])
        clues_grid = Grid([
            [4, _, 5, _, _, 3, _, _],
            [_, _, 1, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, 2, _, _, _],
            [6, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, 5, _, _],
            [_, _, _, _, _, _, _, _],
        ])

        expected_solution_str = (
            ' ┌────────┐  ┌──┐  ┌──┐ \n'
            ' └──┐  ┌──┘  │  │  │  │ \n'
            ' ┌──┘  │  ┌──┘  │  │  │ \n'
            ' └──┐  │  └──┐  │  │  │ \n'
            ' ┌──┘  └─────┘  │  │  │ \n'
            ' └──┐  ┌─────┐  └──┘  │ \n'
            ' ┌──┘  │  ┌──┘  ┌──┐  │ \n'
            ' └─────┘  └─────┘  └──┘ '
        )

        game_solver = DetourSolver(clues_grid, regions_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_10x10_evil_e5j72(self):
        """https://gridpuzzle.com/detour/65wjq"""
        regions_grid = Grid([
            [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
            [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
            [6, 1, 2, 7, 7, 7, 7, 4, 5, 8],
            [6, 1, 9, a, a, a, a, b, 5, 8],
            [6, 9, 9, 9, a, a, b, b, b, 8],
            [6, 9, c, c, a, a, d, d, b, 8],
            [e, e, c, c, a, a, d, d, f, f],
            [e, e, e, g, g, g, g, f, f, f],
            [e, e, h, h, i, i, j, j, f, f],
            [h, h, h, h, i, i, j, j, j, j],
        ])
        clues_grid = Grid([
            [5, _, 4, _, 0, _, 1, _, 4, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, 1],
            [_, _, 2, 7, _, _, _, 3, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, 2, _, _, _, 2, _, _, _],
            [4, _, _, _, _, _, _, _, 3, _],
            [_, _, _, 2, _, _, _, _, _, _],
            [_, _, 3, _, 0, _, 1, _, _, _],
            [_, _, _, _, _, _, _, _, _, _],
        ])

        expected_solution_str = (
            ' ┌──┐  ┌────────────────────┐ \n'
            ' │  └──┘  ┌─────────────────┘ \n'
            ' └──┐  ┌──┘  ┌────────┐  ┌──┐ \n'
            ' ┌──┘  └─────┘  ┌──┐  └──┘  │ \n'
            ' │  ┌───────────┘  │  ┌──┐  │ \n'
            ' │  │  ┌────────┐  └──┘  │  │ \n'
            ' │  │  └─────┐  └────────┘  │ \n'
            ' └──┘  ┌──┐  └───────────┐  │ \n'
            ' ┌─────┘  └──────────────┘  │ \n'
            ' └──────────────────────────┘ '
        )

        game_solver = DetourSolver(clues_grid, regions_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)




if __name__ == '__main__':
    unittest.main()
