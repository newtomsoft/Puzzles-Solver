import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Heyablock.HeyablockSolver import HeyablockSolver

_ = None

class HeyablockSolverTests(TestCase):
    def test_less_than_2_regions_raises(self):
        grid = Grid([
            [_, _, _],
            [_, _, _],
            [_, _, _],
        ])
        region_grid = Grid([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ])
        with self.assertRaises(ValueError) as context:
            HeyablockSolver(grid, region_grid)
        self.assertEqual("The grid must have at least 2 regions", str(context.exception))

    def test_4x4_no_numbers(self):
        grid = Grid([
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        region_grid = Grid([
            [0, 0, 1, 1],
            [0, 0, 1, 1],
            [0, 0, 1, 1],
            [2, 2, 1, 1],
        ])
        game_solver = HeyablockSolver(grid, region_grid)
        solution = game_solver.get_solution()
        self.assertNotEqual(Grid.empty(), solution)

    def test_4x4_with_numbers(self):
        grid = Grid([
            [2, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        region_grid = Grid([
            [0, 0, 1, 1],
            [0, 0, 1, 1],
            [0, 0, 1, 1],
            [2, 2, 1, 1],
        ])
        game_solver = HeyablockSolver(grid, region_grid)
        solution = game_solver.get_solution()
        self.assertNotEqual(Grid.empty(), solution)

    def test_6x6_with_numbers(self):
        grid = Grid([
            [2, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
        ])
        region_grid = Grid([
            [0, 0, 1, 1, 2, 2],
            [0, 0, 1, 1, 2, 2],
            [0, 0, 1, 1, 2, 2],
            [3, 3, 4, 4, 5, 5],
            [3, 3, 4, 4, 5, 5],
            [6, 6, 4, 4, 7, 7],
        ])
        game_solver = HeyablockSolver(grid, region_grid)
        solution = game_solver.get_solution()
        self.assertNotEqual(Grid.empty(), solution)

    def test_8x8_real_puzzle_0mdx8(self):
        """https://gridpuzzle.com/heyablock/0mdx8"""
        value_grid = Grid([
            [3, _, _, 1, 1, _, 1, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, 0, _, _],
            [_, _, _, _, _, _, _, 1],
            [4, _, _, _, 1, _, _, _],
            [_, 1, _, _, _, _, _, _],
            [_, _, _, _, 1, _, _, _],
            [1, _, _, _, _, _, _, _],
        ])
        region_grid = Grid([
            [0, 0, 0, 1, 2, 3, 4, 4],
            [0, 0, 0, 1, 2, 3, 4, 4],
            [0, 5, 0, 1, 2, 6, 6, 6],
            [5, 5, 7, 8, 8, 6, 6, 9],
            [7, 7, 7, 7, 10, 10, 6, 9],
            [7, 11, 7, 12, 12, 13, 14, 14],
            [7, 11, 11, 15, 13, 13, 14, 14],
            [15, 15, 15, 15, 13, 13, 13, 13],
        ])

        expected_solution = Grid([
            [0, 0, 0, 1, 1, 0, 1, 1],
            [1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 0, 1, 1],
            [0, 1, 1, 0, 0, 1, 1, 1],
            [0, 1, 0, 1, 1, 1, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 0],
        ])

        game_solver = HeyablockSolver(value_grid, region_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        self.assertEqual(Grid.empty(), game_solver.get_other_solution())

    def test_8x8_real_puzzle_1g799(self):
        """https://gridpuzzle.com/heyablock/1g799"""
        value_grid = Grid([
            [_, 2, _, 1, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, 1],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [0, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, 0, _, 2, _],
        ])
        region_grid = Grid([
            [0, 0, 0, 1, 1, 2, 2, 2],
            [3, 0, 0, 1, 4, 2, 5, 2],
            [3, 3, 3, 1, 4, 4, 5, 6],
            [3, 7, 8, 8, 8, 6, 6, 6],
            [7, 7, 9, 8, 10, 10, 11, 6],
            [7, 12, 9, 8, 13, 13, 11, 14],
            [12, 12, 9, 15, 15, 13, 14, 14],
            [12, 12, 12, 13, 13, 13, 14, 14],
        ])
        
        game_solver = HeyablockSolver(value_grid, region_grid)
        solution = game_solver.get_solution()
        self.assertNotEqual(Grid.empty(), solution)

    def test_8x8_real_puzzle_01wq1(self):
        """https://gridpuzzle.com/heyablock/01wq1"""
        value_grid = Grid[int | None]([
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, 1, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, 4, _],
            [_, 1, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, 3, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
        ])
        region_grid = Grid([
            [0, 1, 1, 2, 2, 2, 3, 4],
            [0, 0, 1, 1, 5, 5, 3, 4],
            [0, 0, 0, 5, 5, 5, 5, 4],
            [6, 0, 0, 0, 5, 5, 5, 4],
            [6, 0, 6, 6, 5, 7, 7, 4],
            [6, 6, 6, 8, 9, 7, 10, 4],
            [6, 6, 6, 8, 9, 7, 10, 10],
            [11, 11, 8, 8, 9, 9, 12, 12],
        ])
        
        expected_solution = Grid([
            [1, 1, 1, 0, 1, 1, 0, 1],
            [1, 1, 0, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 1],
            [1, 1, 0, 1, 1, 0, 1, 0],
            [1, 0, 0, 1, 0, 1, 0, 1],
            [1, 1, 1, 1, 0, 1, 1, 1],
            [0, 1, 0, 1, 1, 1, 0, 0],
        ])

        game_solver = HeyablockSolver(value_grid, region_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        self.assertEqual(Grid.empty(), game_solver.get_other_solution())


if __name__ == '__main__':
    unittest.main()
