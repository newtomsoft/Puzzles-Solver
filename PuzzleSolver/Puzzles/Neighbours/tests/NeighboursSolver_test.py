from unittest import TestCase

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.RegionsGrid import RegionsGrid
from PuzzleSolver.Puzzles.Neighbours.NeighboursSolver import NeighboursSolver


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
        self.assertIsInstance(solution, RegionsGrid)
        self.assertEqual(expected_string, str(solution))
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
        self.assertIsInstance(solution, RegionsGrid)
        self.assertEqual(expected_string, str(solution))
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
        self.assertIsInstance(solution, RegionsGrid)
        self.assertEqual(expected_string, str(solution))
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
        self.assertIsInstance(solution, RegionsGrid)
        self.assertEqual(expected_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_by_4_10x10_evil_nv4j9(self):
        """https://gridpuzzle.com/neighbours/nv4j9"""
        grid = Grid([
            [3, _, _, 4, 3, _, _, _, _, 4],
            [_, _, 4, _, _, _, _, _, _, 3],
            [_, _, _, _, _, _, 5, _, 5, _],
            [_, 5, _, _, 4, _, _, _, _, _],
            [_, _, 4, 6, _, _, _, 6, _, _],
            [4, _, _, _, _, _, 7, _, _, _],
            [_, _, _, 5, _, _, _, _, _, 4],
            [_, _, _, 5, _, 6, _, 5, _, _],
            [3, _, 4, _, _, _, _, _, _, 4],
            [_, _, _, 3, _, _, _, _, _, 4]
        ])

        game_solver = NeighboursSolver(grid)
        solution = game_solver.get_solution()
        expected_string = (
            '┌─┬─┬───┬───┬───────┐\n'
            '│ │ └─┐ │   ├─┬─┬───┤\n'
            '│ ├─┐ │ ├───┘ │ └─┐ │\n'
            '│ │ ├─┴─┼─────┼─┐ │ │\n'
            '├─┤ ├─┐ └─┬─┐ │ ├─┴─┤\n'
            '│ │ │ └───┤ └─┤ └─┐ │\n'
            '│ └─┼─────┴─┐ ├─┬─┤ │\n'
            '├───┴───┬───┴─┤ │ └─┤\n'
            '├───┬───┴───┐ │ └─┐ │\n'
            '│   ├───────┼─┴───┴─┤\n'
            '└───┴───────┴───────┘\n'
        )
        self.assertIsInstance(solution, RegionsGrid)
        self.assertEqual(expected_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_by_4_10x10_evil_74x6m(self):
        """https://gridpuzzle.com/neighbours/74x6m"""
        grid = Grid([
            [_, _, 4, 4, _, _, _, _, _, _],
            [U, _, _, _, _, _, 6, _, 3, _],
            [_, _, _, _, 5, _, _, _, 4, _],
            [_, 6, _, _, 5, _, _, _, 6, _],
            [6, _, _, _, U, _, _, 5, _, _],
            [_, _, _, _, _, _, _, _, _, U],
            [4, _, _, U, _, _, _, 4, _, _],
            [_, U, _, _, 6, 5, _, _, 4, _],
            [_, _, U, _, _, _, 5, _, _, _],
            [_, _, _, _, _, U, _, 3, _, _]
        ])

        game_solver = NeighboursSolver(grid)
        solution = game_solver.get_solution()
        expected_string = (
            '┌─┬───┬─────┬─────┬─┐\n'
            '│ │   │ ┌─┬─┴───┐ │ │\n'
            '│ ├─┬─┴─┘ ├───┐ ├─┘ │\n'
            '│ │ └───┬─┘ ┌─┴─┴─┬─┤\n'
            '├─┴───┬─┴───┴─┬─┐ │ │\n'
            '├─┬─┐ ├───┬─┬─┘ ├─┘ │\n'
            '│ │ └─┴─┐ │ │ ┌─┴───┤\n'
            '│ ├─────┤ │ └─┼───┐ │\n'
            '│ │ ┌─┬─┼─┴───┤   ├─┤\n'
            '├─┴─┘ │ └───┐ ├───┘ │\n'
            '└─────┴─────┴─┴─────┘\n'
        )
        self.assertIsInstance(solution, RegionsGrid)
        self.assertEqual(expected_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_by_4_8x8_hard_2kdz5(self):
        """https://gridpuzzle.com/neighbours/2kdz5"""
        grid = Grid([
            [4, _, 3, _, _, _, _, 4],
            [_, _, _, _, _, _, 3, _],
            [_, _, 6, _, 6, _, _, _],
            [_, 4, _, _, 6, _, _, _],
            [_, _, _, 4, _, _, _, _],
            [3, _, _, 6, _, _, _, _],
            [_, _, 4, _, _, 6, _, 4],
            [_, _, _, 2, _, _, _, 3],
        ])

        game_solver = NeighboursSolver(grid)
        solution = game_solver.get_solution()
        expected_string = (
            '┌─┬───────┬───┬─┐\n'
            '│ └───┬───┤   │ │\n'
            '├───┬─┴─┐ └─┬─┘ │\n'
            '├─┐ │   ├───┴─┬─┤\n'
            '│ │ ├─┬─┴───┐ │ │\n'
            '│ └─┤ └───┐ ├─┤ │\n'
            '├───┴───┬─┴─┘ │ │\n'
            '├───────┼─────┴─┤\n'
            '└───────┴───────┘\n'
        )
        self.assertIsInstance(solution, RegionsGrid)
        self.assertEqual(expected_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_by_3_9x9_evil_0me88(self):
        """https://gridpuzzle.com/neighbours/0me88"""
        grid = Grid([
            [_, _, 3, _, _, U, 3, _, _],
            [4, _, 5, _, _, _, _, _, 2],
            [_, U, _, _, _, U, _, _, _],
            [U, _, 5, _, _, _, _, U, 4],
            [_, _, 5, _, _, 4, 5, _, _],
            [U, _, _, _, _, U, _, U, _],
            [4, _, _, U, 5, _, 5, _, _],
            [_, _, _, _, _, _, U, _, 3],
            [_, U, _, 4, 3, _, _, _, _]
        ])

        game_solver = NeighboursSolver(grid)
        solution = game_solver.get_solution()
        expected_string = (
            '┌─┬─────┬───┬─┬───┐\n'
            '│ └─┬───┴─┐ │ └─┐ │\n'
            '├─┬─┴───┬─┴─┼───┼─┤\n'
            '│ └─┬───┼─┐ ├─┐ │ │\n'
            '├─┬─┴─┐ │ └─┤ └─┤ │\n'
            '│ └─┐ ├─┴───┼───┴─┤\n'
            '├───┼─┴─┬─┬─┴───┬─┤\n'
            '├─┐ ├─┐ │ └─┬───┤ │\n'
            '│ └─┤ └─┼───┴─┐ │ │\n'
            '└───┴───┴─────┴─┴─┘\n'
        )
        self.assertIsInstance(solution, RegionsGrid)
        self.assertEqual(expected_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
