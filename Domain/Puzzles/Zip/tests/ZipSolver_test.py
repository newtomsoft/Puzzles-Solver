from unittest import TestCase

from Domain.Grid.Grid import Grid
from Domain.Position import Position
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine
from Zip.ZipSolver import ZipSolver


class ZipSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_basic_grid(self):
        grid = Grid([
            [1, 0, 4],
            [0, 5, 0],
            [2, 0, 3]
        ])
        game_solver = ZipSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 4, 4],
            [1, 5, 3],
            [2, 2, 3],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6(self):
        grid = Grid([
            [0, 0, 0, 4, 7, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 8, 1, 0, 0],
            [5, 3, 0, 0, 2, 6],
            [0, 0, 0, 0, 0, 0],
        ])
        game_solver = ZipSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [4, 4, 4, 4, 7, 6],
            [4, 3, 3, 3, 7, 6],
            [4, 3, 7, 7, 7, 6],
            [4, 3, 8, 1, 1, 6],
            [5, 3, 2, 2, 2, 6],
            [5, 5, 5, 5, 5, 5],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_7x7(self):
        grid = Grid([
            [7, 0, 0, 0, 0, 0, 6],
            [0, 2, 0, 0, 0, 0, 0],
            [0, 0, 9, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 8, 0, 0],
            [0, 0, 0, 0, 0, 3, 0],
            [4, 0, 0, 0, 0, 0, 5],
        ])
        game_solver = ZipSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [7, 6, 6, 6, 6, 6, 6],
            [7, 2, 2, 2, 2, 2, 5],
            [7, 1, 9, 8, 8, 2, 5],
            [7, 1, 1, 1, 8, 2, 5],
            [7, 7, 7, 7, 8, 2, 5],
            [3, 3, 3, 3, 3, 3, 5],
            [4, 4, 4, 4, 4, 4, 5],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_with_wall(self):
        grid = Grid([
            [3, 0, 0, 0, 0, 9],
            [0, 2, 0, 0, 10, 0],
            [0, 0, 1, 8, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 4, 0, 0, 6, 0],
            [0, 0, 5, 7, 0, 0],
        ])
        grid.add_walls(
            {
                frozenset([Position(0, 2), Position(0, 3)]),
                frozenset([Position(1, 2), Position(1, 3)]),
                frozenset([Position(2, 2), Position(2, 3)]),
                frozenset([Position(4, 2), Position(4, 3)]),
                frozenset([Position(5, 2), Position(5, 3)]),
            }
        )
        game_solver = ZipSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [3, 2, 2, 8, 8, 9],
            [3, 2, 2, 8, 10, 9],
            [3, 1, 1, 8, 7, 7],
            [3, 3, 5, 5, 5, 7],
            [4, 4, 5, 6, 6, 7],
            [4, 4, 5, 7, 7, 7],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_with_u_turn(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0, 5],
            [0, 0, 0, 0, 0, 3],
            [6, 0, 0, 0, 0, 0],
            [1, 0, 0, 4, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        game_solver = ZipSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [5, 5, 5, 5, 5, 5],
            [5, 1, 2, 4, 4, 5],
            [5, 1, 2, 4, 3, 3],
            [6, 1, 2, 4, 3, 2],
            [1, 1, 2, 4, 3, 2],
            [1, 1, 2, 2, 2, 2],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_with_wall_and_u_turn(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 6, 0, 0, 2],
            [0, 5, 0, 0, 3, 0],
            [0, 8, 0, 0, 1, 0],
            [7, 0, 0, 4, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        grid.add_walls(
            {
                frozenset([Position(1, 0), Position(1, 1)]),
                frozenset([Position(2, 0), Position(2, 1)]),
                frozenset([Position(2, 1), Position(3, 1)]),
                frozenset([Position(3, 1), Position(3, 2)]),
                frozenset([Position(4, 1), Position(4, 2)]),

                frozenset([Position(1, 3), Position(1, 4)]),
                frozenset([Position(2, 3), Position(2, 4)]),
                frozenset([Position(2, 4), Position(3, 4)]),
                frozenset([Position(3, 4), Position(3, 5)]),
                frozenset([Position(4, 4), Position(4, 5)]),
            }
        )
        game_solver = ZipSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [6, 6, 6, 1, 1, 1],
            [6, 5, 6, 1, 2, 2],
            [6, 5, 4, 1, 3, 3],
            [6, 8, 4, 1, 1, 3],
            [7, 7, 4, 4, 3, 3],
            [7, 7, 4, 4, 3, 3],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_2025_03_24(self):
        grid = Grid([
            [6, 0, 0, 0, 0, 7],
            [0, 3, 0, 0, 0, 0],
            [0, 0, 0, 5, 0, 0],
            [0, 0, 4, 0, 0, 0],
            [0, 0, 0, 0, 2, 0],
            [1, 0, 0, 0, 0, 8],
        ])
        game_solver = ZipSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [6, 6, 6, 6, 6, 7],
            [5, 3, 2, 2, 2, 7],
            [5, 3, 4, 5, 2, 7],
            [5, 3, 4, 5, 2, 7],
            [5, 5, 5, 5, 2, 7],
            [1, 1, 1, 1, 1, 8],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_2025_03_25(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 4, 0],
            [0, 0, 6, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [3, 0, 7, 0, 5, 0],
            [0, 0, 1, 0, 0, 0],
        ])
        game_solver = ZipSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1, 1, 1, 1],
            [2, 3, 3, 3, 4, 1],
            [2, 3, 6, 5, 4, 1],
            [2, 3, 6, 5, 4, 1],
            [3, 3, 7, 5, 5, 1],
            [3, 3, 1, 1, 1, 1],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_2025_03_26(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0],
            [0, 0, 0, 0, 2, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        grid.add_walls({
            frozenset([Position(1, 0), Position(1, 1)]),
            frozenset([Position(2, 0), Position(2, 1)]),
            frozenset([Position(3, 0), Position(3, 1)]),
            frozenset([Position(4, 0), Position(4, 1)]),

            frozenset([Position(1, 2), Position(1, 3)]),
            frozenset([Position(2, 2), Position(2, 3)]),
            frozenset([Position(3, 2), Position(3, 3)]),
            frozenset([Position(4, 2), Position(4, 3)]),

            frozenset([Position(1, 4), Position(1, 5)]),
            frozenset([Position(2, 4), Position(2, 5)]),
            frozenset([Position(3, 4), Position(3, 5)]),
            frozenset([Position(4, 4), Position(4, 5)]),

            frozenset([Position(2, 1), Position(3, 1)]),
            frozenset([Position(2, 2), Position(3, 2)]),
        })
        game_solver = ZipSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 3, 3, 2, 2],
            [1, 1, 3, 3, 2, 2],
            [1, 4, 3, 3, 2, 2],
            [1, 1, 1, 3, 3, 2],
            [1, 1, 1, 1, 2, 2],
            [1, 1, 1, 1, 2, 2],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_2025_03_27(self):
        grid = Grid([
            [6, 0, 0, 0, 0, 5],
            [0, 0, 0, 0, 0, 0],
            [0, 7, 1, 8, 2, 0],
            [0, 0, 0, 0, 0, 0],
            [3, 0, 0, 0, 0, 4],
            [0, 0, 0, 0, 0, 0],
        ])
        game_solver = ZipSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [6, 5, 5, 5, 5, 5],
            [6, 6, 1, 1, 1, 4],
            [7, 7, 1, 8, 2, 4],
            [7, 7, 7, 7, 2, 4],
            [3, 2, 2, 2, 2, 4],
            [3, 3, 3, 3, 3, 3],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_2025_03_28(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 5, 3, 0],
            [0, 0, 4, 0, 0, 0],
            [0, 0, 0, 2, 0, 0],
            [0, 1, 6, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        grid.add_walls({
            frozenset([Position(0, 1), Position(1, 1)]),
            frozenset([Position(0, 2), Position(1, 2)]),
            frozenset([Position(1, 1), Position(1, 2)]),
            frozenset([Position(2, 1), Position(2, 2)]),

            frozenset([Position(2, 3), Position(3, 3)]),
            frozenset([Position(2, 4), Position(3, 4)]),
            frozenset([Position(3, 3), Position(3, 4)]),
            frozenset([Position(4, 3), Position(4, 4)]),
        })
        game_solver = ZipSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [5, 5, 5, 5, 2, 2],
            [5, 5, 4, 5, 3, 2],
            [5, 5, 4, 3, 3, 2],
            [5, 1, 1, 2, 2, 2],
            [5, 1, 6, 2, 2, 2],
            [5, 5, 5, 2, 2, 2],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
