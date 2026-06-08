import unittest
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Island.IslandSolver import IslandSolver

_ = IslandSolver.cell_empty
c = IslandSolver.clue
x = IslandSolver.sea
o = IslandSolver.land

class IslandSolverTests(unittest.TestCase):
    def test_basic_1x3_1(self):
        grid = Grid([
            [1, _, _]
        ])
        expected_solution = Grid([
            [c, o, x]
        ])
        game_solver = IslandSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_basic_1x4_2(self):
        grid = Grid([
            [2, _, _, _],
        ])
        expected_solution = Grid([
            [c, o, o, x]
        ])
        game_solver = IslandSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_basic_1x4_3(self):
        grid = Grid([
            [3, _, _, _],
        ])
        expected_solution = Grid([
            [c, o, o, o],
        ])
        
        game_solver = IslandSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_basic_2x3(self):
        grid = Grid([
                [2, _, _],
                [2, _, _],
        ])
        expected_solution = Grid([
                [c, o, x],
                [c, o, x],
        ])

        game_solver = IslandSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_basic_1x3_2(self):
        grid = Grid([
            [1, _, 1]
        ])
        expected_solution = Grid([
            [c, o, c]
        ])
        game_solver = IslandSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_basic_2x2_1(self):
        grid = Grid([
            [2, _],
            [_, 2]
        ])
        expected_solution = Grid([
            [c, o],
            [o, c],
        ])
        game_solver = IslandSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_basic_3x3(self):
        grid = Grid([
            [1, _, 1],
            [_, _, _],
            [2, _, 2]
        ])
        expected_solution = Grid([
            [c, x, c],
            [o, x, o],
            [c, o, c]
        ])

        game_solver = IslandSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_basic_1x4_with_connectivity(self):
        grid = Grid([
            [1, _, _, _]
        ])
        expected_solution = Grid([
                [c, o, x, x],
        ])

        game_solver = IslandSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())


    def test_5x5_easy_3166d(self):
        """https://gridpuzzle.com/island/3166d"""
        grid = Grid([
            [_, 1, _, _, _],
            [_, _, _, _, 3],
            [_, 2, _, 3, _],
            [_, 2, 1, _, 1],
            [2, _, _, _, _]
        ])
        expected_solution = Grid([
            [x, c, x, x, o],
            [x, o, x, o, c],
            [x, c, o, c, o],
            [o, c, c, x, c],
            [c, o, x, x, x]
        ])
        game_solver = IslandSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_5x5_evil_31rq6(self):
        """https://gridpuzzle.com/island/31rq6"""
        grid = Grid([
            [_, 1, 4, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [6, _, _, 8, _],
            [_, _, _, _, 5]
        ])
        expected_solution = Grid([
            [o, c, c, o, x],
            [x, x, o, x, x],
            [o, x, o, o, x],
            [c, o, x, c, x],
            [o, o, o, o, c],
        ])
        game_solver = IslandSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_6x6_evil_169e6(self):
        """https://gridpuzzle.com/island/169e6"""
        grid = Grid([
            [_, _, _, _, _, 1],
            [_, _, _, _, 8, _],
            [_, _, _, _, _, 2],
            [14, _, _, _, _, _],
            [_, 11, _, 13, _, _],
            [_, _, _, _, 7, _]
        ])
        expected_solution = Grid([
            [o, x, x, x, x, c],
            [o, x, o, o, c, o],
            [o, x, o, x, o, c],
            [c, o, o, o, x, x],
            [o, c, x, c, o, o],
            [o, o, o, o, c, x],
        ])
        game_solver = IslandSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_7x7_evil_080q1(self):
        """https://gridpuzzle.com/island/080q1"""
        grid = Grid([
            [_, 2, _, _, _, _, _],
            [1, _, 4, _, _, 2, _],
            [_, _, _, _, 5, _, _],
            [_, _, _, _, _, _, _],
            [_, 2, _, 2, 4, 1, _],
            [_, _, 6, _, _, _, _],
            [_, _, _, _, _, _, _]
        ])
        expected_solution = Grid([
            [x, c, o, x, x, x, x],
            [c, o, c, o, x, c, x],
            [x, x, x, o, c, o, o],
            [x, x, o, x, o, x, x],
            [x, c, o, c, c, c, o],
            [o, x, c, x, o, x, x],
            [o, o, o, x, o, o, x],
        ])
        game_solver = IslandSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_10x10_evil_01m9g(self):
        """https://gridpuzzle.com/island/01m9g"""
        grid = Grid([
            [_, _, _, 5, _, _, 2, _, _, _],
            [_, 4, _, _, 5, 6, _, _, 5, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, 3, 8, _, _, _, _, 5, 9, _],
            [_, _, _, _, _, _, _, _, _, _],
            [5, _, _, 5, _, _, 13, _, _, 11],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, 5, _, 5, 4, _, 10, _, _],
            [_, 10, _, _, _, _, _, _, 7, _]
        ])
        expected_solution = Grid([
            [o, o, o, c, x, o, c, x, o, o],
            [o, c, x, o, c, c, o, x, c, o],
            [x, x, o, x, o, o, x, o, x, o],
            [x, c, c, o, o, x, x, c, c, o],
            [x, o, o, x, x, x, o, o, o, x],
            [c, x, o, c, o, o, c, x, o, c],
            [o, o, x, x, x, x, o, o, x, o],
            [o, x, o, o, x, o, x, o, o, o],
            [o, x, c, o, c, c, o, c, o, x],
            [o, c, o, o, x, o, o, x, c, x],
        ])

        game_solver = IslandSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())
