from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Neighbours.NeighboursSolver import NeighboursSolver

_ = NeighboursSolver.empty
U = NeighboursSolver.unknow

class NeighboursSolverTests(TestCase):
    def test_by_2_4x4_easy_31yn9(self):
        """https://gridpuzzle.com/neighbours/31yn9"""
        grid = Grid([
            [_, _, _, 2],
            [2, 3, 3, _],
            [4, _, _, 4],
            [_, 2, _, 2],
        ])

        game_solver = NeighboursSolver(grid)
        solution = game_solver.get_solution()
        expected_string = (
            '┌─┬─┬─┬─┐\n'
            '│ │ │ │ │\n'
            '├─┴─┼─┴─┤\n'
            '├───┼───┤\n'
            '└───┴───┘\n'
        )
        self.assertEqual(expected_string, self.grid_to_string(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_by_5_5x5_evil_1ygx0(self):
        """https://gridpuzzle.com/neighbours/1ygx0"""
        grid = Grid([
            [2, _, _, _, _],
            [2, _, 3, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, 2, 1],
        ])

        game_solver = NeighboursSolver(grid)
        solution = game_solver.get_solution()
        expected_string = (
            '┌───┬─┬─┬─┐\n'
            '├─┐ │ │ │ │\n'
            '│ │ │ │ │ │\n'
            '│ │ │ │ │ │\n'
            '│ └─┤ │ │ │\n'
            '└───┴─┴─┴─┘\n'
        )
        self.assertEqual(expected_string, self.grid_to_string(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_by_4_6x6_evil_0pvkr(self):
        """https://gridpuzzle.com/neighbours/0pvkr"""
        grid = Grid([
            [3, _, _, _, _, 2],
            [_, _, _, _, _, _],
            [_, 5, 4, _, _, 5],
            [3, _, _, _, _, _],
            [_, _, _, _, _, _],
            [3, _, 3, _, 2, _],
        ])

        game_solver = NeighboursSolver(grid)
        solution = game_solver.get_solution()
        expected_string = (
            '┌─────┬─┬───┐\n'
            '├─┬─┐ │ │   │\n'
            '│ │ ├─┘ ├───┤\n'
            '│ │ └─┬─┘ ┌─┤\n'
            '│ ├───┼───┤ │\n'
            '├─┘ ┌─┘ ┌─┘ │\n'
            '└───┴───┴───┘\n'
        )
        self.assertEqual(expected_string, self.grid_to_string(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)





    def test_by_4_10x10_evil_1dxp0(self):
        """https://gridpuzzle.com/neighbours/1dxp0"""
        grid = Grid([
            [_, _, _, _, 4, _, _, _, _, 3],
            [_, 3, 7, _, _, _, _, _, _, _],
            [_, _, _, _, 4, _, _, 5, 3, _],
            [U, _, 7, _, _, U, _, _, 3, _],
            [_, _, _, U, _, _, _, 5, _, _],
            [_, 3, _, _, _, _, U, _, _, _],
            [4, _, _, _, _, _, _, _, _, U],
            [U, _, _, _, 4, U, _, _, _, _],
            [U, _, _, _, U, _, _, 4, _, _],
            [_, _, _, _, _, _, _, 5, _, 2]
        ])

        game_solver = NeighboursSolver(grid)
        solution = game_solver.get_solution()
        expected_string = (
            '┌───┬───────┬───────┐\n'
            '│   ├─┬─────┼───┬───┤\n'
            '├───┤ └─┐ ┌─┤   │   │\n'
            '│   ├─┐ ├─┘ └─┬─┼───┤\n'
            '├───┤ ├─┴─────┤ └─┐ │\n'
            '│   │ └─┬───┬─┼─┐ │ │\n'
            '├───┴─┬─┴─┐ │ │ └─┴─┤\n'
            '├───┐ │   │ │ ├─────┤\n'
            '├─┐ └─┼───┼─┤ │ ┌───┤\n'
            '│ └───┤   │ └─┴─┤   │\n'
            '└─────┴───┴─────┴───┘\n'
        )
        self.assertEqual(expected_string, self.grid_to_string(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
