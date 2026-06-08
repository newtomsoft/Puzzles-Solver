import unittest
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Kurotto.KurottoSolver import KurottoSolver

U = KurottoSolver.cell_unknown
_ = KurottoSolver.cell_empty

class KurottoSolverTests(unittest.TestCase):
    def test_no_solution_impossible_clue(self):
        grid = Grid([
            [4, _],
            [_, _],
        ])
        solver = KurottoSolver(grid)
        self.assertEqual(Grid.empty(), solver.get_solution())

    def test_gridpuzzle_5x5_easy_3j99e(self):
        """https://gridpuzzle.com/kurotto/3j99e"""
        grid = Grid([
            [_, 3, _, 2, _],
            [_, 3, _, _, 2],
            [_, _, _, _, _],
            [7, _, _, 4, _],
            [_, 4, _, 5, _],
        ])
        solver = KurottoSolver(grid)
        solution = solver.get_solution()
        self.assertNotEqual(Grid.empty(), solution)
        expected = Grid([
            [1, _, _, _, 1],
            [1, _, _, 1, _],
            [1, _, 1, _, _],
            [_, 1, 1, _, _],
            [_, _, 1, _, 1],
        ])
        self.assertEqual(expected, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())

    def test_gridpuzzle_5x5_medium_1ny86(self):
        """https://gridpuzzle.com/kurotto/1ny86"""
        grid = Grid([
            [_, _, _, 3, _],
            [_, _, 6, _, _],
            [2, 4, _, 5, 2],
            [_, _, 4, _, _],
            [_, 2, _, _, _],
        ])

        expected = Grid([
            [_, _, 1, _, _],
            [1, 1, _, 1, 1],
            [_, _, 1, _, _],
            [_, 1, _, 1, _],
            [1, _, _, 1, _],
        ])

        solver = KurottoSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())

    def test_gridpuzzle_7x7_evil_2p9qz(self):
        """https://gridpuzzle.com/kurotto/2p9qz"""
        grid = Grid([
            [1, _, _, _, 6, 6, _],
            [_, _, _, 6, _, _, _],
            [3, _, _, _, _, _, 5],
            [_, _, _, 3, _, _, _],
            [5, _, _, _, _, _, 3],
            [_, _, _, 3, _, _, _],
            [_, U, 3, _, _, _, U],
        ])

        expected = Grid([
            [_, 1, _, 1, _, _, 1],
            [_, _, _, _, 1, 1, _],
            [_, 1, _, _, 1, 1, _],
            [1, 1, _, _, _, 1, _],
            [_, _, 1, 1, _, _, _],
            [1, _, 1, _, _, 1, 1],
            [1, _, _, _, _, 1, _],
        ])

        solver = KurottoSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())

    def test_gridpuzzle_9x9_evil_0vdmg(self):
        """https://gridpuzzle.com/kurotto/0vdmg"""
        grid = Grid([
            [4, _, _, _, _, _, 5, _, 3],
            [_, _, _, _, U, _, _, _, _],
            [6, U, _, _, _, _, 1, _, _],
            [_, _, 8, _, 0, _, _, _, _],
            [5, _, _, _, _, _, _, _, 5],
            [_, _, _, _, 9, _, 8, _, _],
            [_, _, 4, _, _, _, _, 3, 1],
            [_, _, _, _, 4, _, _, _, _],
            [4, _, 2, _, _, _, _, _, 1],
        ])
        
        expected = Grid([
            [_, 1, 1, _, 1, 1, _, 1, _],
            [1, 1, _, 1, _, _, _, 1, 1],
            [_, _, 1, 1, _, 1, _, _, _],
            [1, 1, _, _, _, _, _, 1, _],
            [_, _, 1, _, _, 1, 1, 1, _],
            [1, _, 1, 1, _, 1, _, _, _],
            [1, _, _, _, 1, _, 1, _, _],
            [1, _, 1, _, _, 1, 1, _, 1],
            [_, 1, _, _, _, _, _, _, _],

        ])

        solver = KurottoSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())

    def test_gridpuzzle_10x10_evil_11kj9(self):
        """https://gridpuzzle.com/kurotto/11kj9"""
        grid = Grid([
            [1, _, _, _, _, _, _, _, _, 2],
            [_, _, _, 7, _, 7, _, 5, _, _],
            [U, _, _, _, _, 2, _, _, _, _],
            [_, _, 3, _, _, 2, _, 4, _, _],
            [_, 3, _, _, _, _, U, _, U, _],
            [_, 4, _, 3, _, _, _, _, 2, _],
            [_, _, 3, _, 6, _, _, 4, _, _],
            [_, _, _, _, 4, _, _, _, _, 3],
            [_, _, 4, _, 5, _, U, _, _, _],
            [2, _, _, _, _, _, _, _, _, 3],
        ])

        expected = Grid([
            [_, _, 1, 1, 1, 1, _, 1, _, _],
            [1, _, _, _, 1, _, 1, _, 1, 1],
            [_, _, 1, 1, _, _, 1, _, _, _],
            [_, 1, _, _, 1, _, _, _, 1, 1],
            [1, _, _, _, _, 1, _, 1, _, _],
            [1, _, 1, _, 1, _, _, 1, _, _],
            [_, 1, _, 1, _, 1, _, _, _, _],
            [_, _, _, _, _, 1, _, 1, 1, _],
            [1, 1, _, 1, _, 1, _, _, _, 1],
            [_, _, 1, _, _, 1, _, 1, 1, _],
        ])

        solver = KurottoSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())


if __name__ == '__main__':
    unittest.main()
