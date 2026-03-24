import unittest

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.Summandum.SummandumSolver import SummandumSolver

_ = SummandumSolver.Empty

class SummandumSolverTests(unittest.TestCase):
    def test_solve_4x4_easy_ap317pk(self):
        """https://gridpuzzle.com/summandum/317pk"""
        grid = Grid([
            [3, _, 2, 0],
            [_, 4, _, 3],
            [4, _, 3, _],
            [5, 3, _, 2]
        ])
        expected_solution = Grid([
            [_, 3, 1, 2, 0],
            [0, 3, _, 2, 0],
            [3, _, 4, _, 3],
            [1, 4, _, 3, _],
            [2, 5, 3, _, 2]
        ])

        solver = SummandumSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solve_4x4_evil_37kdk(self):
        """https://gridpuzzle.com/summandum/37kdk"""
        grid = Grid([
            [_, 4, _, 3],
            [1, _, _, _],
            [_, _, _, 5],
            [3, _, 2, _]
        ])
        expected_solution = Grid([
            [_, 1, 3, 0, 2],
            [1, _, 4, _, 3],
            [0, 1, _, _, _],
            [3, _, _, _, 5],
            [2, 3, _, 2, _]
        ])

        solver = SummandumSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solve_5x5_evil_ap0x2mr(self):
        """https://gridpuzzle.com/summandum/ap0x2mr"""
        grid = Grid([
            [2, _, _, _, _],
            [_, _, 6, _, _],
            [_, 2, _, 1, _],
            [_, _, 8, _, _],
            [_, _, _, _, 6]
        ])
        expected_solution = Grid([
            [_, 2, 1, 4, 0, 3],
            [0, 2, _, _, _, _],
            [2, _, _, 6, _, _],
            [1, _, 2, _, 1, _],
            [4, _, _, 8, _, _],
            [3, _, _, _, _, 6]
        ])

        solver = SummandumSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solve_10x10_evil_ap0m5yw(self):
        """https://gridpuzzle.com/summandum/ap0m5yw"""
        grid = Grid([
            [10, _, _, _, _, _, _, _, _, 12],
            [_, _, _, 9, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, 9, _, _],
            [_, 9, _, 4, _, _, _, _, _, _],
            [_, _, _, _, _, 8, _, _, _, _],
            [_, _, _, _, 13, _, _, _, _, _],
            [_, _, _, _, _, _, 10, _, 18, _],
            [_, _, 6, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, 1, _, _, _],
            [5, _, _, _, _, _, _, _, _, 7]
        ])
        expected_solution = Grid([
            [_, 4, 7, 3, 2, 8, 0, 1, 5, 9, 6],
            [6, 10, _, _, _, _, _, _, _, _, 12],
            [7, _, _, _, 9, _, _, _, _, _, _],
            [4, _, _, _, _, _, _, _, 9, _, _],
            [2, _, 9, _, 4, _, _, _, _, _, _],
            [8, _, _, _, _, _, 8, _, _, _, _],
            [5, _, _, _, _, 13, _, _, _, _, _],
            [9, _, _, _, _, _, _, 10, _, 18, _],
            [3, _, _, 6, _, _, _, _, _, _, _],
            [0, _, _, _, _, _, _, 1, _, _, _],
            [1, 5, _, _, _, _, _, _, _, _, 7]
        ])

        solver = SummandumSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solve_20x20_evil_02zr2(self):
        """https://gridpuzzle.com/summandum/02zr2"""
        grid = Grid([
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, 20],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, 19, _, _, _, _, _, _],
            [_, _, 29, _, _, 25, _, _, _, _, _, _, _, _, _, _, _, _, _, 32],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 20, _, _, _],
            [_, _, _, _, 24, _, _, _, _, _, 8, _, _, _, _, _, _, _, _, _],
            [_, _, 33, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 16, _],
            [_, _, _, _, _, _, _, _, _, _, _, 19, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, 15, _, _, _, 16, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 21, _, _, _, _],
            [_, _, _, _, 26, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, 25, _, _, _, 18, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, 12, _, _, _, _, _, _, _, _, _, _, _],
            [_, 27, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 0, _, _],
            [_, _, _, _, _, _, _, _, _, 5, _, _, _, _, _, 7, _, _, _, _],
            [_, _, _, 24, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [26, _, _, _, _, _, _, _, _, _, _, _, _, _, 27, _, _, 16, _, _],
            [_, _, _, _, _, _, 13, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [24, _, 30, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _]
        ])
        expected_solution = Grid([
            [_, 10, 8, 16, 9, 18, 12, 4, 14, 5, 1, 2, 7, 6, 17, 11, 3, 15, 0, 13, 19],
            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, 20],
            [2, _, _, _, _, _, _, _, _, _, _, _, _, _, 19, _, _, _, _, _, _],
            [13, _, _, 29, _, _, 25, _, _, _, _, _, _, _, _, _, _, _, _, _, 32],
            [5, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 20, _, _, _],
            [6, _, _, _, _, 24, _, _, _, _, _, 8, _, _, _, _, _, _, _, _, _],
            [17, _, _, 33, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 16, _],
            [12, _, _, _, _, _, _, _, _, _, _, _, 19, _, _, _, _, _, _, _, _],
            [10, _, _, _, _, _, _, _, _, 15, _, _, _, 16, _, _, _, _, _, _, _],
            [18, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 21, _, _, _, _],
            [8, _, _, _, _, 26, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [11, _, _, _, _, _, _, _, 25, _, _, _, 18, _, _, _, _, _, _, _, _],
            [7, _, _, _, _, _, _, _, _, 12, _, _, _, _, _, _, _, _, _, _, _],
            [19, _, 27, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [0, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 0, _, _],
            [4, _, _, _, _, _, _, _, _, _, 5, _, _, _, _, _, 7, _, _, _, _],
            [15, _, _, _, 24, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [16, 26, _, _, _, _, _, _, _, _, _, _, _, _, _, 27, _, _, 16, _, _],
            [9, _, _, _, _, _, _, 13, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [14, 24, _, 30, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _]
        ])

        solver = SummandumSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)



if __name__ == '__main__':
    unittest.main()