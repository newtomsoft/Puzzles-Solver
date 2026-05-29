import unittest

from Domain.Board.Grid import Grid
from Domain.Board.RegionsGrid import RegionsGrid
from Domain.Puzzles.Hanare.HanareSolver import HanareSolver

_ = HanareSolver.empty


class HanareSolverTests(unittest.TestCase):
    def test_no_solution_for_contradictory_regions(self):
        regions = RegionsGrid([
            [1, 2, 3],
            [1, 4, 3],
        ])
        solver = HanareSolver(regions)
        solution = solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_5x5_easy_1n8xk(self):
        """https://gridpuzzle.com/hanare/1n8xk"""
        regions = RegionsGrid([
            [1, 2, 2, 3, 3],
            [1, 2, 4, 5, 6],
            [1, 4, 4, 5, 6],
            [7, 7, 7, 5, 6],
            [7, 7, 5, 5, 6],
        ])
        clues = Grid([
            [3, _, _, 2, _],
            [_, _, _, _, _],
            [_, _, 3, _, 4],
            [_, 5, _, _, _],
            [_, _, _, _, _],
        ])
        
        expected_solution = Grid([
            [3, 3, _, 2, _],
            [_, _, _, _, _],
            [_, _, 3, _, 4],
            [_, 5, _, _, _],
            [_, _, _, 5, _]
        ])

        solver = HanareSolver(regions, clues)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())

    def test_known_gridpuzzle_puzzle_6x6_evil_0eqx1(self):
        """https://gridpuzzle.com/hanare/0eqx1"""
        regions = RegionsGrid([
            [1, 2, 2, 2, 3, 3],
            [1, 4, 4, 4, 5, 5],
            [1, 1, 4, 6, 6, 6],
            [7, 8, 8, 8, 9, 9],
            [7, 7, 10, 9, 9, 11],
            [12, 12, 10, 11, 11, 11],
        ])

        expected_solution = Grid([
            [_, _, _, 3, _, 2],
            [4, 4, _, _, 2, _],
            [_, _, _, _, _, 3],
            [3, 3, _, _, _, _],
            [_, _, _, _, 4, 4],
            [_, 2, 2, _, _, _],
        ])

        solver = HanareSolver(regions)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())

    def test_known_gridpuzzle_puzzle_12x12_evil_106j6(self):
        """https://gridpuzzle.com/hanare/106j6"""
        regions = RegionsGrid([
            [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3],
            [1, 1, 1, 1, 4, 1, 2, 2, 2, 2, 3, 3],
            [5, 5, 5, 6, 4, 4, 4, 2, 2, 2, 3, 3],
            [5, 5, 6, 6, 6, 6, 4, 2, 2, 3, 3, 3],
            [5, 5, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8],
            [5, 5, 5, 9, 9, 10, 10, 7, 8, 8, 8, 11],
            [5, 12, 9, 9, 7, 7, 7, 7, 8, 8, 8, 11],
            [5, 12, 12, 9, 9, 7, 13, 7, 13, 11, 11, 11],
            [14, 12, 12, 12, 9, 13, 13, 13, 13, 13, 13, 13],
            [14, 14, 12, 9, 9, 9, 9, 15, 15, 13, 16, 13],
            [14, 12, 12, 9, 17, 17, 15, 15, 15, 16, 16, 16],
            [14, 14, 12, 9, 17, 15, 15, 15, 16, 16, 16, 16],
        ])
        clues = Grid([
            [_, _, 11, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
        ])

        expected_solution = Grid([
            [_, _, 11, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, 13, _, _, _],
            [_, _, 12, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, 5, _, _, _, _, 9],
            [_, _, _, _, 8, _, _, _, 11, _, _, 9],
            [_, _, _, _, _, 2, _, _, _, _, _, _],
            [_, 10, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, 5, _, _],
            [_, _, _, _, _, _, _, _, _, _, 11, _],
            [_, _, _, _, _, _, _, 8, _, _, _, _],
            [6, _, _, _, 3, _, _, _, _, _, _, _],
            [_, _, _, 13, _, _, _, _, _, 8, _, _],
        ])

        solver = HanareSolver(regions, clues)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())


if __name__ == '__main__':
    unittest.main()
