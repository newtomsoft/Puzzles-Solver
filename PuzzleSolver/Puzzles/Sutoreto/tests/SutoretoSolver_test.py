from unittest import TestCase
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Sutoreto.SutoretoSolver import SutoretoSolver

_ = 0
x = True
o = False


class SutoretoSolverTests(TestCase):
    def test_4x4_easy(self):
        # https://gridpuzzle.com/sutoreto/lg4ym
        numbers_grid = Grid([
            [2, _, 8, 9],
            [5, _, 7, _],
            [_, _, _, 6],
            [_, 5, _, _]
        ])
        blacks_grid = Grid([
            [o, x, o, o],
            [o, o, o, o],
            [o, o, o, o],
            [o, o, o, o]
        ])
        solver = SutoretoSolver(numbers_grid, blacks_grid)
        solution, blank = solver.get_solution()
        
        expected_solution = Grid([[2, 0, 8, 9], [5, 6, 7, 8], [3, 4, 5, 6], [4, 5, 6, 7]])
        self.assertEqual(expected_solution, solution)
        
        other_solution, __ = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_4x4_evil(self):
        # https://gridpuzzle.com/sutoreto/21rd8
        numbers_grid = Grid([
            [_, 5, 2, _],
            [_, 2, _, _],
            [7, _, _, _],
            [_, _, _, _]
        ])
        blacks_grid = Grid([
            [o, o, o, o],
            [o, o, o, o],
            [o, o, o, o],
            [o, o, o, o]
        ])
        solver = SutoretoSolver(numbers_grid, blacks_grid)
        solution, blank = solver.get_solution()
        
        expected_solution = Grid([
            [4, 5, 2, 3],
            [5, 2, 3, 4],
            [7, 4, 5, 6],
            [6, 3, 4, 5]
        ])
        self.assertEqual(expected_solution, solution)
        
        other_solution, __ = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_7x7_easy(self):
        # https://gridpuzzle.com/sutoreto/rqmyg
        numbers_grid = Grid([
            [_, 1, _, 4, _, _, 6],
            [2, _, 4, _, _, _, _],
            [_, _, _, _, _, _, 4],
            [_, 2, _, 5, 4, 3, _],
            [_, _, 5, _, _, _, _],
            [4, _, _, 7, 6, _, 2],
            [5, _, 9, 8, _, 3, 4]
        ])
        blacks_grid = Grid([
            [x, o, o, o, o, x, o],
            [o, x, o, x, o, o, o],
            [o, o, o, o, x, o, o],
            [o, o, x, o, o, o, x],
            [x, o, o, x, o, o, o],
            [o, o, x, o, o, x, o],
            [o, x, o, o, x, o, o]
        ])
        solver = SutoretoSolver(numbers_grid, blacks_grid)
        solution, blank = solver.get_solution()
        
        expected_solution = Grid([
            [_, 1, 2, 4, 3, _, 6],
            [2, _, 4, _, 4, 6, 5],
            [4, 5, 3, 6, _, 5, 4],
            [3, 2, _, 5, 4, 3, _],
            [_, 4, 5, _, 5, 4, 3],
            [4, 3, _, 7, 6, _, 2],
            [5, _, 9, 8, _, 3, 4]
        ])
        self.assertEqual(expected_solution, solution)
        
        other_solution, __ = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_7x7_evil(self):
        # https://gridpuzzle.com/sutoreto/j6909
        numbers_grid = Grid([
            [_, 1, _, _, 6, _, _],
            [5, _, _, _, _, 9, _],
            [_, 2, _, _, _, _, _],
            [_, _, _, _, _, _, 6],
            [1, _, _, _, _, 1, _],
            [_, 1, _, _, _, _, 3],
            [2, _, _, _, 4, _, _]
        ])
        blacks_grid = Grid([
            [x, o, o, x, o, o, x],
            [o, o, o, o, x, o, o],
            [x, o, x, o, o, o, o],
            [o, o, o, x, o, x, o],
            [o, x, o, o, o, o, x],
            [o, o, o, o, x, o, o],
            [o, x, o, x, o, o, o]
        ])
        solver = SutoretoSolver(numbers_grid, blacks_grid)
        solution, blank = solver.get_solution()
        
        expected_solution = Grid([
            [_, 1, 2, _, 6, 7, _],
            [5, 4, 3, 6, _, 9, 8],
            [_, 2, _, 5, 6, 8, 7],
            [4, 3, 5, _, 5, _, 6],
            [1, _, 2, 3, 4, 1, _],
            [3, 1, 4, 2, _, 2, 3],
            [2, _, 3, _, 4, 3, 2]
        ])
        self.assertEqual(expected_solution, solution)
        
        other_solution, __ = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_10x10_easy(self):
        # https://gridpuzzle.com/sutoreto/w2zk2
        numbers_grid = Grid([
            [2, _, 1, _, _, 2, _, _, 1, _],
            [_, _, 2, _, 5, _, 4, 3, _, 4],
            [_, 2, _, 4, _, 2, _, 2, _, _],
            [_, 3, _, _, _, 3, _, _, _, 3],
            [6, _, 4, _, 2, _, _, 6, 4, _],
            [3, _, 5, _, _, 4, 2, _, _, 4],
            [_, 5, _, 4, _, _, _, 4, _, 2],
            [_, _, 4, _, 3, _, _, 5, _, _],
            [_, _, _, 6, _, _, 5, _, 2, _],
            [4, _, 6, _, 2, _, _, 4, _, 2],
        ])
        blacks_grid = Grid([
            [o, x, o, x, o, o, o, x, o, o],
            [o, o, o, o, o, x, o, o, x, o],
            [x, o, o, o, x, o, x, o, o, o],
            [o, o, x, o, o, o, o, x, o, o],
            [o, x, o, o, o, x, o, o, o, x],
            [o, o, o, x, o, o, o, x, o, o],
            [o, o, x, o, x, o, o, o, x, o],
            [o, x, o, o, o, o, x, o, o, o],
            [x, o, o, o, x, o, o, x, o, x],
            [o, o, o, x, o, o, x, o, o, o],
        ])
        solver = SutoretoSolver(numbers_grid, blacks_grid)
        solution, blank = solver.get_solution()

        expected_solution = Grid([
            [2, _, 1, _, 4, 2, 3, _, 1, 2],
            [3, 4, 2, 1, 5, _, 4, 3, _, 4],
            [_, 2, 3, 4, _, 2, _, 2, 3, 1],
            [2, 3, _, 2, 1, 3, 4, _, 2, 3],
            [6, _, 4, 3, 2, _, 5, 6, 4, _],
            [3, 4, 5, _, 3, 4, 2, _, 5, 4],
            [4, 5, _, 4, _, 5, 3, 4, _, 2],
            [5, _, 4, 5, 3, 2, _, 5, 4, 3],
            [_, 4, 5, 6, _, 6, 5, _, 2, _],
            [4, 5, 6, _, 2, 3, _, 4, 3, 2]
        ])
        self.assertEqual(expected_solution, solution)

        other_solution, __ = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_10x10_evil(self):
        # https://gridpuzzle.com/sutoreto/zz7vy
        numbers_grid = Grid([
            [2, _, _, _, 6, _, 8, _, 2, _],
            [_, 3, _, 2, _, _, _, _, _, _],
            [2, _, 2, _, 3, _, _, _, _, 6],
            [5, 2, _, _, _, _, _, _, _, _],
            [_, _, _, _, 6, _, _, _, _, _],
            [_, 4, _, _, _, 8, _, _, 4, _],
            [_, _, _, _, 8, _, _, 1, _, _],
            [_, _, _, _, _, _, 1, _, _, _],
            [_, _, 1, _, _, 2, _, _, _, 1],
            [4, 3, _, _, 5, _, _, _, 6, 5],
        ])
        blacks_grid = Grid([
            [o, o, o, x, o, o, o, x, o, o],
            [x, o, o, o, x, o, o, o, o, o],
            [o, x, o, x, o, o, o, o, x, o],
            [o, o, o, o, x, o, x, o, o, o],
            [o, x, o, x, o, x, o, o, o, x],
            [o, o, x, o, o, o, o, x, o, o],
            [x, o, o, x, o, x, o, o, o, o],
            [o, x, o, o, o, o, o, x, o, o],
            [o, o, o, o, x, o, o, o, x, o],
            [o, o, x, o, o, o, x, o, o, o],
        ])

        solver = SutoretoSolver(numbers_grid, blacks_grid)
        solution, blank = solver.get_solution()

        expected_solution = Grid([
            [2, 4, 3, _, 6, 7, 8, _, 2, 3],
            [_, 3, 1, 2, _, 6, 7, 4, 3, 5],
            [2, _, 2, _, 3, 4, 6, 5, _, 6],
            [5, 2, 4, 3, _, 5, _, 6, 5, 4],
            [4, _, 5, _, 6, _, 2, 3, 1, _],
            [3, 4, _, 6, 7, 8, 5, _, 4, 3],
            [_, 3, 2, _, 8, _, 3, 1, 2, 4],
            [3, _, 3, 2, 5, 4, 1, _, 3, 2],
            [2, 4, 1, 3, _, 2, 4, 3, _, 1],
            [4, 3, _, 4, 5, 3, _, 4, 6, 5]
        ])

        self.assertEqual(expected_solution, solution)
        other_solution, __ = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
