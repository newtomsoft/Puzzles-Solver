import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Creek.CreekSolver import CreekSolver

_ = -1
x = 0


class CreekSolverTests(TestCase):


    def test_solution_basic_grid(self):
        grid = Grid([
            [1, 1, 0],
            [1, 1, 0],
            [0, 0, 0]
        ])
        game_solver = CreekSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 0],
            [0, 0],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_3eyv2(self):
        # https://gridpuzzle.com/creek/3eyv2
        grid = Grid([
            [0, _, 0, _, 0],
            [1, 2, 1, 1, 1],
            [_, 3, _, 1, _],
            [1, _, 1, _, 0],
            [0, 0, 1, 1, 0]
        ])
        game_solver = CreekSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [x, x, x, x],
            [1, 1, x, 1],
            [1, x, x, x],
            [x, x, 1, x],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_with_adjacent_watter_constraint_ekygn(self):
        # https://gridpuzzle.com/creek/ekygn
        grid = Grid([
            [_, _, 1, _, _],
            [_, 2, _, _, 1],
            [2, _, _, _, 1],
            [_, 2, _, 1, _],
            [0, _, _, _, _]
        ])
        game_solver = CreekSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, x, 1, 1],
            [1, x, x, x],
            [1, 1, x, 1],
            [x, x, x, x],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_grid_51ppw(self):
        # https://gridpuzzle.com/creek/51ppw
        grid = Grid([
            [_, 1, _, _, 0, _],
            [_, _, 3, 2, _, _],
            [_, 1, _, _, 2, _],
            [_, _, 4, 2, _, _],
            [_, 1, _, _, 2, _],
            [_, _, _, _, _, _],
        ])
        game_solver = CreekSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [x, 1, 1, x, x],
            [x, x, 1, x, 1],
            [x, 1, 1, x, 1],
            [x, 1, 1, x, 1],
            [x, x, x, x, 1],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_medium_19040(self):
        # https://gridpuzzle.com/creek/19040
        grid = Grid([
            [1, _, _, 1, _, 2, 1],
            [_, 3, _, _, 2, _, 2],
            [1, _, 1, _, 1, 1, _],
            [1, 2, _, 2, _, _, 1],
            [_, _, 1, 1, 2, _, 1],
            [0, 1, _, _, _, 0, _],
            [0, _, _, 2, 1, _, 0],
        ])
        game_solver = CreekSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, x, x, 1, 1, 1, ],
            [1, 1, x, x, x, 1, ],
            [x, x, x, 1, x, x, ],
            [1, 1, x, 1, 1, 1, ],
            [x, x, x, x, x, x, ],
            [x, 1, 1, 1, x, x, ],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_7x7_medium_0vm8g(self):
        # https://gridpuzzle.com/creek/0vm8g
        grid = Grid([
            [0, 1, _, 2, _, 2, 1, 0],
            [_, _, 3, _, 2, _, _, 0],
            [1, 1, _, _, _, 2, _, 0],
            [_, _, 1, _, _, _, _, 0],
            [2, _, 0, 1, _, 3, 2, 1],
            [_, 2, _, 3, _, _, 4, _],
            [1, _, 1, _, 1, 1, _, 1],
            [0, 0, _, 0, _, 0, 0, 0],
        ])
        game_solver = CreekSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [x, 1, 1, 1, 1, 1, x],
            [x, x, 1, x, x, x, x],
            [1, x, 1, x, 1, 1, x],
            [1, x, x, x, 1, x, x],
            [1, x, x, 1, 1, 1, 1],
            [1, x, 1, 1, x, 1, 1],
            [x, x, x, x, x, x, x],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_7x7_expert_0dd0r(self):
        # https://gridpuzzle.com/creek/0dd0r
        grid = Grid([
            [_, _, 2, _, 2, _, 1, 0],
            [_, _, _, 2, _, 2, _, 0],
            [_, 2, _, _, 1, _, 0, _],
            [_, _, 2, _, 2, 2, _, 0],
            [2, _, _, 3, _, 2, _, _],
            [_, _, 1, _, 1, 1, _, 0],
            [1, _, _, _, 1, _, _, _],
            [0, _, 1, _, 0, 0, _, 1],
        ])
        game_solver = CreekSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1, 1, 1, 1, x],
            [1, x, x, x, x, x, x],
            [1, x, 1, x, 1, x, x],
            [1, x, 1, 1, x, 1, x],
            [1, x, 1, x, x, 1, x],
            [1, x, x, 1, x, x, x],
            [x, x, 1, x, x, x, 1],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_7x7_evil_0g948(self):
        # https://gridpuzzle.com/creek/0g948
        grid = Grid([
            [_, 0, _, _, _, 2, _, 0],
            [_, _, _, _, _, _, _, _],
            [1, _, 2, _, _, _, _, _],
            [0, 1, _, 3, _, 3, _, _],
            [_, _, 2, _, _, _, _, 1],
            [0, 1, _, _, 4, _, 2, _],
            [_, _, _, 3, _, _, _, _],
            [_, _, 0, _, _, 2, _, _],
        ])
        game_solver = CreekSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [x, x, x, x, 1, 1, x],
            [1, x, 1, x, x, x, x],
            [x, x, 1, x, 1, 1, x],
            [x, 1, 1, 1, 1, x, x],
            [x, x, x, 1, 1, x, 1],
            [x, 1, 1, 1, 1, x, 1],
            [x, x, x, 1, 1, 1, 1],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_15x15_evil_0x6zx8(self):
        # https://gridpuzzle.com/creek/0x6zx8
        grid = Grid([
            [_, _, _, 2, _, 1, 1, _, 1, _, 1, 0, _, _, _, _],
            [_, 3, _, _, 1, _, 2, 2, _, _, 2, _, _, 2, _, _],
            [_, _, 2, _, _, _, _, 2, _, 2, _, 3, _, _, 3, _],
            [_, _, _, 1, 2, _, _, 2, _, _, _, 2, _, 1, 2, _],
            [0, _, _, _, _, _, 3, _, _, _, 2, _, _, 1, _, 2],
            [1, 2, _, 3, _, _, _, 2, _, 1, _, _, 1, _, _, _],
            [1, _, 1, _, _, _, _, _, 1, _, 3, 3, _, _, 2, _],
            [_, 2, _, 2, _, _, 3, _, _, 1, _, _, 3, _, _, _],
            [0, _, 1, _, _, _, 2, _, 0, 2, _, 2, _, 1, _, 2],
            [1, _, 2, _, _, 2, _, 2, _, _, _, _, _, _, 2, _],
            [_, 2, _, 2, _, 1, _, _, _, 2, _, 2, _, 3, _, _],
            [_, _, 2, 2, _, _, 2, _, 2, 1, _, _, _, _, 1, _],
            [_, 1, _, _, 2, 2, _, 1, 3, _, 0, 1, _, 0, _, 2],
            [_, _, 1, _, _, 2, 2, 1, _, _, 1, 2, _, _, 3, _],
            [_, _, _, _, 2, _, _, _, _, _, _, _, 1, _, _, 1],
            [0, _, 2, 2, _, 2, _, _, _, _, 2, _, 0, _, _, _],
        ])
        game_solver = CreekSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1, 1, x, 1, x, 1, x, 1, x, x, x, 1, 1],
            [x, 1, x, x, x, 1, x, 1, x, 1, x, 1, x, 1, 1],
            [x, 1, x, 1, 1, x, x, 1, x, 1, 1, 1, x, x, 1],
            [x, x, x, x, x, x, 1, x, x, 1, x, x, 1, x, 1],
            [x, 1, 1, 1, x, 1, 1, 1, x, x, 1, x, x, x, 1],
            [1, x, x, 1, x, x, x, x, x, 1, 1, x, 1, x, 1],
            [x, 1, x, 1, x, 1, 1, 1, x, x, 1, 1, x, x, 1],
            [x, 1, x, 1, x, x, 1, x, x, 1, 1, 1, 1, x, 1],
            [x, x, x, x, 1, x, 1, x, x, 1, x, x, x, x, 1],
            [1, 1, 1, x, 1, x, 1, x, 1, 1, x, 1, 1, 1, x],
            [x, x, 1, x, x, x, 1, x, x, x, x, 1, 1, x, x],
            [x, 1, x, 1, x, 1, x, 1, 1, x, x, 1, x, x, 1],
            [x, x, x, 1, x, 1, x, x, 1, x, x, x, x, x, 1],
            [x, 1, x, x, x, 1, x, 1, x, x, 1, 1, x, 1, 1],
            [x, 1, 1, 1, 1, 1, x, x, x, 1, 1, x, x, x, x],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
