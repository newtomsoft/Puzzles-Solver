from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Snake.SnakeSolver import SnakeSolver

_ = 0


class SnakeSolverTests(TestCase):


    def test_solution_only_cells_sum_constraint(self):
        grid = Grid([
            [1, _, _],
            [_, _, _],
            [_, _, 1],
        ])
        row_numbers = [1, 1, 3]
        column_numbers = [3, 1, 1]

        game_solver = SnakeSolver(grid, row_numbers, column_numbers)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, _, _],
            [1, _, _],
            [1, 1, 1],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_3jzyo(self):
        # https://gridpuzzle.com/snake/3jzyo
        grid = Grid([
            [_, _, _, _, 1, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, 1],
        ])
        row_numbers = [5, 1, 1, 1, 4, 3]
        column_numbers = [5, 2, 2, 3, 2, 1]

        game_solver = SnakeSolver(grid, row_numbers, column_numbers)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1, 1, 1, _],
            [1, _, _, _, _, _],
            [1, _, _, _, _, _],
            [1, _, _, _, _, _],
            [1, 1, 1, 1, _, _],
            [_, _, _, 1, 1, 1],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_l89r4(self):
        # https://gridpuzzle.com/snake/l89r4
        grid = Grid([
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, 1, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [1, _, _, _, _, _],
        ])
        row_numbers = [4, 2, 3, 3, 1, 1]
        column_numbers = [3, 1, 4, 1, 2, 3]

        game_solver = SnakeSolver(grid, row_numbers, column_numbers)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [_, _, 1, 1, 1, 1],
            [_, _, 1, _, _, 1],
            [_, _, 1, _, 1, 1],
            [1, 1, 1, _, _, _],
            [1, _, _, _, _, _],
            [1, _, _, _, _, _],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_some_unknown_sums_lqr79(self):
        # https://gridpuzzle.com/snake/lqr79
        grid = Grid([
            [_, _, _, _, 1, _],
            [1, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
        ])
        row_numbers = [2, 2, 2, 3, -1, 3]
        column_numbers = [4, -1, 2, 1, -1, 4]

        game_solver = SnakeSolver(grid, row_numbers, column_numbers)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [_, _, _, _, 1, 1],
            [1, _, _, _, _, 1],
            [1, _, _, _, _, 1],
            [1, _, _, _, 1, 1],
            [1, 1, 1, _, 1, _],
            [_, _, 1, 1, 1, _],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_evil_dn07p(self):
        # https://gridpuzzle.com/snake/dn07p
        grid = Grid([
            [_, _, _, _, 1, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [1, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
        ])
        row_numbers = [-1, 2, -1, -1, 3, -1]
        column_numbers = [3, -1, -1, -1, 4, 3]

        game_solver = SnakeSolver(grid, row_numbers, column_numbers)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [_, _, _, _, 1, _],
            [_, _, _, _, 1, 1],
            [_, _, _, _, _, 1],
            [1, _, _, _, 1, 1],
            [1, _, _, 1, 1, _],
            [1, 1, 1, 1, _, _],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
