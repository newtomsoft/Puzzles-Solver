from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Renkatsu.RenkatsuSolver import RenkatsuSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine

_ = 0


class RenkatsuSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_2_regions(self):
        grid = Grid([
            [1, 2, 3],
            [1, 2, 4],
            [3, 5, 4],
        ])

        game_solver = RenkatsuSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1],
            [2, 2, 1],
            [2, 2, 2],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_3_regions(self):
        grid = Grid([
            [2, 1, 1],
            [2, 3, 3],
            [4, 1, 2],
        ])

        game_solver = RenkatsuSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 2],
            [3, 3, 2],
            [3, 3, 2],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4(self):
        # https://gridpuzzle.com/renkatsu/3155d
        grid = Grid([
            [4, 5, 2, 2],
            [3, 1, 3, 4],
            [3, 1, 5, 1],
            [1, 4, 2, 2]
        ])

        game_solver = RenkatsuSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1, 2],
            [1, 1, 2, 2],
            [3, 2, 2, 4],
            [3, 3, 3, 4],
        ])
        self.assertEqual(expected_solution, solution)

    def test_solution_5x5(self):
        grid = Grid([
            [2, 2, 6, 1, 3],
            [5, 2, 3, 2, 4],
            [3, 4, 1, 1, 5],
            [6, 1, 4, 1, 2],
            [5, 2, 1, 6, 3]
        ])

        game_solver = RenkatsuSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 2, 2, 2, 2],
            [1, 3, 3, 4, 2],
            [1, 1, 3, 4, 2],
            [1, 1, 5, 6, 6],
            [5, 5, 5, 5, 5]
        ])
        self.assertEqual(expected_solution, solution)

    def test_solution_6x6_31k76(self):
        # https://gridpuzzle.com/renkatsu/31k76
        grid = Grid([
            [1, 2, 5, 5, 3, 4],
            [7, 2, 1, 6, 2, 5],
            [3, 3, 1, 3, 6, 4],
            [4, 4, 2, 2, 1, 3],
            [6, 5, 2, 5, 1, 4],
            [2, 1, 1, 3, 3, 1]
        ])

        game_solver = RenkatsuSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1, 2, 2, 2],
            [1, 2, 2, 2, 3, 3],
            [1, 4, 5, 5, 3, 3],
            [1, 4, 5, 6, 3, 3],
            [1, 4, 7, 6, 6, 6],
            [4, 4, 7, 7, 6, 8],
        ])
        self.assertEqual(expected_solution, solution)
    # @unittest.skip("This test is too slow (approx 25 sec)")
    def test_solution_6x6_31k50(self):
        # https://gridpuzzle.com/renkatsu/31k50
        grid = Grid([
            [3, 3, 5, 1, 3, 1],
            [2, 4, 4, 7, 7, 2],
            [1, 5, 6, 1, 6, 2],
            [1, 4, 2, 6, 5, 4],
            [7, 3, 3, 2, 5, 1],
            [1, 2, 2, 4, 1, 2]
        ])

        game_solver = RenkatsuSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 2, 2, 3, 3, 4],
            [1, 1, 2, 2, 3, 4],
            [1, 5, 5, 2, 3, 3],
            [5, 5, 5, 2, 3, 3],
            [5, 5, 6, 2, 6, 7],
            [8, 8, 6, 6, 6, 7]
        ])
        self.assertEqual(expected_solution, solution)

    # @unittest.skip("This test is too slow (approx 15 mn)")
    def test_solution_7x7_0x9y8(self):
        # https://gridpuzzle.com/renkatsu/0x9y8
        grid = Grid([
            [3, 4, 6, 2, 5, 4, 3],
            [5, 1, 4, 1, 2, 3, 2],
            [3, 6, 2, 4, 5, 6, 1],
            [1, 3, 2, 3, 4, 1, 1],
            [1, 2, 5, 6, 1, 2, 3],
            [4, 2, 3, 5, 2, 3, 1],
            [1, 2, 4, 1, 5, 5, 2]
        ])

        game_solver = RenkatsuSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1, 1, 1, 2, 3],
            [4, 1, 4, 5, 2, 2, 3],
            [4, 4, 4, 5, 2, 2, 3],
            [4, 6, 5, 5, 7, 2, 8],
            [6, 6, 6, 5, 7, 8, 8],
            [6, 9, 9, 5, 7, 7, 10],
            [11, 11, 9, 9, 9, 7, 10]
        ])
        self.assertEqual(expected_solution, solution)

    # @unittest.skip("This test is too slow (approx 1 hour)")
    def test_solution_8x8_1nd00(self):
        # https://gridpuzzle.com/renkatsu/1nd00
        grid = Grid([
            [2, 4, 3, 5, 1, 4, 8, 1],
            [1, 5, 3, 2, 5, 3, 1, 3],
            [2, 5, 4, 2, 4, 9, 6, 3],
            [2, 1, 2, 7, 1, 6, 4, 2],
            [6, 4, 3, 6, 1, 4, 1, 5],
            [5, 1, 1, 7, 3, 6, 2, 7],
            [7, 3, 8, 2, 8, 5, 3, 4],
            [7, 4, 5, 3, 5, 4, 1, 2]
        ])

        game_solver = RenkatsuSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1, 2, 2, 2, 3, 4],
            [1, 1, 5, 2, 3, 2, 3, 3],
            [5, 5, 5, 3, 3, 3, 3, 6],
            [7, 5, 8, 3, 6, 6, 6, 6],
            [7, 7, 8, 8, 9, 9, 10, 6],
            [7, 7, 8, 9, 9, 9, 10, 6],
            [7, 7, 8, 9, 9, 9, 10, 10],
            [8, 8, 8, 11, 11, 11, 11, 11],
        ])
        self.assertEqual(expected_solution, solution)

    def test_multi_solutions(self):
        grid = Grid([
            [1, 2, 3],
            [2, 1, 3],
            [3, 2, 1],
        ])

        game_solver = RenkatsuSolver(grid, self.get_solver_engine())
        solution0 = game_solver.get_solution()
        solution1 = game_solver.get_other_solution()
        solution2 = game_solver.get_other_solution()
        solution3 = game_solver.get_other_solution()
        solutions = {solution0, solution1, solution2, solution3}

        grid0 = Grid([[1, 1, 1], [2, 2, 2], [3, 3, 3]])
        grid1 = Grid([[1, 1, 1], [2, 2, 3], [2, 3, 3]])
        grid2 = Grid([[1, 2, 2], [1, 2, 3], [1, 3, 3]])
        grid3 = Grid.empty()
        expected_solutions = {grid0, grid1, grid2, grid3}

        self.assertEqual(expected_solutions, solutions)
