import unittest
from unittest import TestCase

from parameterized import parameterized

from Bimaru.BimaruSolver import BimaruSolver
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine


class BimaruGameTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    @staticmethod
    def _to_bool(grid: Grid):
        if grid.is_empty():
            return Grid.empty()
        return Grid([[True if grid[Position(r, c)] > 0 else False for c in range(6)] for r in range(6)])

    def test_grid_must_be_square_raises_value_error(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        ships = {'column': [1, 0, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0, 0, 0]}
        ships_number_by_size = {1: 1}
        with self.assertRaises(ValueError) as context:
            BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        self.assertEqual("The grid must be square", str(context.exception))

    def test_grid_must_be_at_least_4x4_raises_value_error(self):
        grid = Grid([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ])
        ships = {'column': [1, 0, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0, 0, 0]}
        ships_number_by_size = {1: 1}
        with self.assertRaises(ValueError) as context:
            BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        self.assertEqual("The grid must be at least 6x6", str(context.exception))

    def test_boats_number_by_size_not_filled(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        ships = {'column': [1, 0, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0, 0]}
        ships_number_by_size = {}
        with self.assertRaises(ValueError) as context:
            BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        self.assertEqual("At least one boat must be placed", str(context.exception))

    def test_boats_column_not_compliant(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        ships = {'column': [1, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0, 0]}
        ships_number_by_size = {1: 1}
        with self.assertRaises(ValueError) as context:
            BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        self.assertEqual("Boat cells column must have the same length as the columns number", str(context.exception))

    def test_boats_rows_not_compliant(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        ships = {'column': [1, 0, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0]}
        ships_number_by_size = {1: 1}
        with self.assertRaises(ValueError) as context:
            BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        self.assertEqual("Boat cells row must have the same length as the rows number", str(context.exception))

    def test_boats_rows_columns_not_equal(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        ships = {'column': [2, 1, 1, 0, 0, 0], 'row': [1, 1, 1, 0, 0, 0]}
        ships_number_by_size = {1: 2, 2: 1}
        with self.assertRaises(ValueError) as context:
            BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        self.assertEqual("The sum of boat cells by row and column must be equal", str(context.exception))

    def test_boats_cell_number_not_compliant(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        ships = {'column': [2, 1, 1, 0, 0, 0], 'row': [1, 2, 1, 0, 0, 0]}
        ships_number_by_size = {1: 3, 2: 1}
        with self.assertRaises(ValueError) as context:
            BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        self.assertEqual("The sum of the size of the ships must be equal to the sum of ships cells", str(context.exception))

    def test_solution_with_sums_constraints(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        ships = {'column': [2, 0, 2, 0, 2, 0], 'row': [3, 0, 3, 0, 0, 0]}
        ships_number_by_size = {1: 6}
        expected_solution = Grid([
            [6, 0, 6, 0, 6, 0],
            [0, 0, 0, 0, 0, 0],
            [6, 0, 6, 0, 6, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(self._to_bool(expected_solution), self._to_bool(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), self._to_bool(other_solution))

    def test_solution_with_initials_constraints_0(self):
        grid = Grid([
            [BimaruSolver.ship_single, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        ships = {'column': [1, 1, 0, 0, 0, 0], 'row': [1, 1, 0, 0, 0, 0]}
        ships_number_by_size = {1: 2}
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_with_initials_constraints_1(self):
        grid = Grid([
            [BimaruSolver.ship_top, -1, -1, -1, -1, -1],
            [BimaruSolver.ship_bottom, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        ships = {'column': [2, 0, 0, 0, 0, 0], 'row': [1, 1, 0, 0, 0, 0]}
        ships_number_by_size = {2: 1}
        expected_solution = Grid([
            [BimaruSolver.ship_top, 0, 0, 0, 0, 0],
            [BimaruSolver.ship_bottom, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(self._to_bool(expected_solution), self._to_bool(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), self._to_bool(other_solution))

    def test_solution_with_initials_constraints_2(self):
        grid = Grid([
            [BimaruSolver.ship_top, -1, -1, -1, -1, -1],
            [BimaruSolver.ship_bottom, -1, -1, -1, -1, -1],
            [BimaruSolver.ship_bottom, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        ships = {'column': [3, 0, 0, 0, 0, 0], 'row': [1, 1, 1, 0, 0, 0]}
        ships_number_by_size = {3: 1}
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), self._to_bool(solution))

    def test_solution_with_initials_constraints_ship2_horizontal(self):
        grid = Grid([
            [BimaruSolver.ship_left, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        ships = {'column': [1, 1, 0, 0, 0, 0], 'row': [2, 0, 0, 0, 0, 0]}
        ships_number_by_size = {2: 1}
        expected_solution = Grid([
            [BimaruSolver.ship_left, BimaruSolver.ship_right, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(self._to_bool(expected_solution), self._to_bool(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), self._to_bool(other_solution))

    def test_solution_with_initials_constraints_ship3_horizontal(self):
        grid = Grid([
            [BimaruSolver.ship_left, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        ships = {'column': [1, 1, 1, 0, 0, 0], 'row': [3, 0, 0, 0, 0, 0]}
        ships_number_by_size = {3: 1}
        expected_solution = Grid([
            [BimaruSolver.ship_left, BimaruSolver.ship_middle_horizontal, BimaruSolver.ship_right, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(self._to_bool(expected_solution), self._to_bool(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), self._to_bool(other_solution))

    def test_solution_6x6_1(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, 2, -1, -1],
        ])
        ships = {'column': [2, 1, 2, 3, 1, 1], 'row': [1, 3, 0, 1, 4, 1]}
        ships_number_by_size = {1: 3, 2: 2, 3: 1}
        expected_solution = Grid([
            [0, 0, 1, 0, 0, 0],
            [7, 0, 2, 0, 7, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [3, 4, 0, 5, 0, 7],
            [0, 0, 0, 2, 0, 0]
        ])
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_2(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, 7],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        ships = {'column': [2, 3, 0, 3, 1, 1], 'row': [1, 3, 1, 3, 0, 2]}
        ships_number_by_size = {1: 3, 2: 2, 3: 1}
        expected_solution = Grid([
            [0, 0, 0, 0, 0, 7],
            [3, 4, 0, 1, 0, 0],
            [0, 0, 0, 5, 0, 0],
            [3, 4, 0, 2, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 7, 0, 0, 7, 0]
        ])
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_3(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        ships = {'column': [4, 1, 1, 1, 2, 1], 'row': [2, 2, 3, 0, 3, 0]}
        ships_number_by_size = {1: 3, 2: 2, 3: 1}
        expected_solution = Grid([
            [1, 0, 0, 0, 7, 0],
            [5, 0, 7, 0, 0, 0],
            [2, 0, 0, 0, 3, 4],
            [0, 0, 0, 0, 0, 0],
            [3, 4, 0, 7, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ])
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_4(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, +7],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        ships = {'column': [3, 1, 3, 1, 1, 1], 'row': [3, 2, 0, 3, 0, 2]}
        ships_number_by_size = {1: 3, 2: 2, 3: 1}
        expected_solution = Grid([
            [1, 0, 1, 0, 0, 7],
            [2, 0, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 3, 6, 4, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [7, 0, 0, 0, 7, 0],
        ])
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_1(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1, -1, +0],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, +4, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1],
        ])
        ships = {'column': [3, 0, 4, 3, 2, 4, 1, 2], 'row': [2, 4, 0, 4, 0, 5, 2, 2]}
        ships_number_by_size = {1: 3, 2: 3, 3: 2, 4: 1}
        expected_solution = Grid([
            [0, 0, 0, 1, 0, 1, 0, 0],
            [7, 0, 0, 2, 0, 2, 0, 7],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 6, 6, 4, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 3, 6, 4, 0],
            [2, 0, 5, 0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0, 0, 0, 7],
        ])
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_1(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1, +3, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, +8, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, +3, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        ])
        ships = {'column': [2, 1, 2, 2, 2, 2, 1, 4, 2, 2], 'row': [2, 2, 3, 2, 0, 4, 4, 0, 3, 0]}
        ships_number_by_size = {1: 4, 2: 3, 3: 2, 4: 1}
        expected_solution = Grid([
            [0, 0, 0, 0, 0, 0, 3, 4, 0, 0],
            [7, 0, 7, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 3, 6, 4],
            [0, 0, 0, 0, 3, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 7, 0, 3, 6, 4],
            [3, 6, 6, 4, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 3, 4, 0, 0, 7, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_15x15_1(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1, +3, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, +8, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, +3, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        ])
        ships = {'column': [2, 1, 2, 2, 2, 2, 1, 4, 2, 2], 'row': [2, 2, 3, 2, 0, 4, 4, 0, 3, 0]}
        ships_number_by_size = {1: 4, 2: 3, 3: 2, 4: 1}
        expected_solution = Grid([
            [0, 0, 0, 0, 0, 0, 3, 4, 0, 0],
            [7, 0, 7, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 3, 6, 4],
            [0, 0, 0, 0, 3, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 7, 0, 3, 6, 4],
            [3, 6, 6, 4, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 3, 4, 0, 0, 7, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_20x20_1(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 7, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 8, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 7],
            [8, -1, -1, -1, -1, -1, -1, -1, -1, 3, -1, -1, -1, -1, 4, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [8, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, 4, -1, 0, -1, 0, -1, 3, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, 4, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, 7, -1, -1, 1, -1],
            [-1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        ])
        ships = {'column': [7, 2, 5, 3, 8, 3, 3, 5, 4, 3, 8, 5, 4, 7, 2, 4, 2, 5, 2, 2], 'row': [8, 2, 7, 4, 2, 1, 11, 1, 2, 8, 3, 3, 9, 0, 3, 3, 6, 8, 3, 0]}
        ships_number_by_size = {1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}
        expected_solution = Grid([
            [0, 0, 0, 0, 0, 0, 0, 3, 6, 6, 6, 6, 6, 4, 0, 0, 0, 0, 0, 7],
            [0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 3, 6, 6, 4, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 3, 6, 6, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0],
            [0, 0, 0, 3, 6, 4, 0, 3, 6, 6, 6, 6, 4, 0, 0, 1, 0, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
            [5, 0, 1, 0, 0, 0, 0, 0, 0, 3, 6, 6, 6, 6, 4, 0, 0, 0, 0, 0],
            [5, 0, 5, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [5, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [2, 0, 0, 0, 3, 6, 6, 6, 4, 0, 0, 0, 0, 0, 3, 4, 0, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 7, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 3, 6, 4, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0, 0],
            [3, 6, 4, 0, 5, 0, 0, 0, 0, 0, 2, 0, 0, 5, 0, 7, 0, 0, 1, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


class BimaruGameLongTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_25x25_1(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [8, -1, -1, -1, 3, -1, -1, -1, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 7, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, 1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, 3, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, 3, -1, -1, -1, 8, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, 3, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 8, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3, -1, -1, -1, -1, 3, -1, 4, -1, -1],
            [-1, -1, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 7, -1, 1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        ])
        ships = {'column': [3, 2, 2, 4, 6, 6, 7, 5, 2, 5, 4, 9, 7, 3, 11, 2, 12, 1, 2, 13, 3, 4, 3, 3, 1], 'row': [6, 0, 10, 2, 7, 8, 2, 2, 14, 3, 3, 3, 9, 2, 3, 10, 2, 7, 7, 3, 2, 5, 4, 4, 2]}
        ships_number_by_size = {1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}
        expected_solution = Grid([
            [0, 0, 0, 0, 0, 0, 3, 4, 0, 3, 6, 6, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 3, 6, 4, 0, 0, 0, 0, 0, 0, 0, 0, 3, 6, 6, 6, 6, 6, 4, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [5, 0, 0, 0, 3, 6, 4, 0, 7, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 1, 0, 7, 0, 0, 0, 0, 3, 6, 6, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 3, 6, 6, 6, 4, 0, 0, 0, 5, 0, 0, 2, 0, 1, 0, 3, 6, 6, 6, 4, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 5, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 6, 6, 6, 6, 4, 0, 0, 0, 2, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0],
            [0, 0, 3, 6, 6, 6, 4, 0, 0, 0, 1, 0, 1, 0, 2, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 5, 0, 0, 3, 4, 0, 0, 0, 3, 6, 4, 0, 0],
            [0, 0, 3, 6, 6, 6, 6, 4, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 2, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 5, 0, 7, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 5, 0, 0, 0, 0, 5, 0, 0, 0, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 0, 5, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_30x30_1(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1],
            [1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 8, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3, -1, -1, -1, 4, -1, -1, 8, -1, 4, -1, -1],
            [-1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 8, -1, -1, 2, -1, -1, -1, 7, -1, 0, -1, 7, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4, -1, -1, -1, -1],
            [-1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, 8, -1, -1, -1, 8, -1, 8, -1, -1, 4, -1, -1, -1, 0, -1, -1, -1, -1, 4, -1, -1, -1],
            [-1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 7],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3, -1, -1, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1],
            [-1, -1, -1, -1, 7, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, 8, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3, -1, 4, -1, -1],
            [-1, -1, 1, -1, -1, -1, -1, 2, -1, 2, -1, 7, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, 7, -1, -1, -1, -1, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        ])
        ships = {'column': [3, 6, 8, 4, 8, 3, 3, 8, 2, 5, 16, 2, 2, 12, 5, 6, 4, 3, 6, 3, 12, 5, 8, 11, 5, 4, 3, 5, 1, 2], 'row': [8, 4, 7, 4, 3, 12, 3, 6, 3, 11, 3, 6, 1, 8, 1, 17, 1, 8, 3, 7, 9, 7, 4, 5, 3, 7, 6, 3, 4, 1]}
        ships_number_by_size = {1: 9, 2: 8, 3: 7, 4: 6, 5: 5, 6: 4, 7: 3, 8: 2, 9: 1}
        expected_solution = Grid([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 6, 6, 6, 6, 6, 4, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3, 6, 4],
            [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 3, 6, 6, 6, 4, 0, 3, 6, 6, 4, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 2, 0, 0, 0, 7, 0, 0, 0, 7, 0, 0, 0, 0, 0],
            [0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 5, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 3, 6, 6, 6, 6, 6, 6, 4, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 6, 6, 6, 4, 0, 0, 0, 0],
            [0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 0, 0, 3, 6, 4, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 6, 4, 0, 0, 0, 0, 0, 0],
            [0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 0, 0, 0, 0, 3, 6, 6, 4, 0, 3, 6, 6, 6, 6, 6, 4, 0, 0, 0, 0, 3, 6, 6, 6, 4, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 3, 6, 6, 6, 6, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0, 0],
            [7, 0, 1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 1, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0, 7],
            [0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0, 3, 6, 6, 4, 0, 0, 5, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0, 0],
            [0, 0, 5, 0, 7, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0, 0],
            [0, 0, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0, 0, 0, 5, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 2, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 6, 4, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 2, 0, 2, 0, 7, 0, 5, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 5, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


class BimaruGameTestsParameterized(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    @parameterized.expand([
        ("ship_top", BimaruSolver.ship_top, Grid.empty()),
        ("ship_bottom", BimaruSolver.ship_bottom, Grid.empty()),
        ("ship_left", BimaruSolver.ship_left, Grid.empty()),
        ('ship_right', BimaruSolver.ship_right, Grid.empty()),
        ("ship_middle", BimaruSolver.ship_middle_input, Grid.empty()),
    ])
    def test_solution_with_initials_constraints_position_0_0(self, test_name, value, expected):
        grid = Grid([
            [value, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        ships = {'column': [1, 0, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0, 0]}
        ships_number_by_size = {1: 1}
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(expected, solution)

    @parameterized.expand([
        ("ship_top", BimaruSolver.ship_top, Grid.empty()),
        ("ship_bottom", BimaruSolver.ship_bottom, Grid.empty()),
        ("ship_left", BimaruSolver.ship_left, Grid.empty()),
        ('ship_right', BimaruSolver.ship_right, Grid.empty()),
        ("ship_middle", BimaruSolver.ship_middle_input, Grid.empty()),
    ])
    def test_solution_with_initials_constraints_position_0_x(self, test_name, value, expected):
        grid = Grid([
            [-1, value, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        ships = {'column': [0, 1, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0, 0]}
        ships_number_by_size = {1: 1}
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(expected, solution)

    @parameterized.expand([
        ("ship_top", BimaruSolver.ship_top, Grid.empty()),
        ("ship_bottom", BimaruSolver.ship_bottom, Grid.empty()),
        ("ship_left", BimaruSolver.ship_left, Grid.empty()),
        ('ship_right', BimaruSolver.ship_right, Grid.empty()),
        ("ship_middle", BimaruSolver.ship_middle_input, Grid.empty()),
    ])
    def test_solution_with_initials_constraints_position_0_max(self, test_name, value, expected):
        grid = Grid([
            [-1, -1, -1, -1, -1, value],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        ships = {'column': [0, 1, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0, 0]}
        ships_number_by_size = {1: 1}
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(expected, solution)

    @parameterized.expand([
        ("ship_top", BimaruSolver.ship_top, Grid.empty()),
        ("ship_bottom", BimaruSolver.ship_bottom, Grid.empty()),
        ("ship_left", BimaruSolver.ship_left, Grid.empty()),
        ('ship_right', BimaruSolver.ship_right, Grid.empty()),
        ("ship_middle", BimaruSolver.ship_middle_input, Grid.empty()),
    ])
    def test_solution_with_initials_constraints_position_x_0(self, test_name, value, expected):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [value, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        ships = {'column': [0, 1, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0, 0]}
        ships_number_by_size = {1: 1}
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(expected, solution)

    @parameterized.expand([
        ("ship_top", BimaruSolver.ship_top, Grid.empty()),
        ("ship_bottom", BimaruSolver.ship_bottom, Grid.empty()),
        ("ship_left", BimaruSolver.ship_left, Grid.empty()),
        ('ship_right', BimaruSolver.ship_right, Grid.empty()),
        ("ship_middle", BimaruSolver.ship_middle_input, Grid.empty()),
    ])
    def test_solution_with_initials_constraints_position_max_0(self, test_name, value, expected):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [value, -1, -1, -1, -1, -1],
        ])
        ships = {'column': [0, 1, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0, 0]}
        ships_number_by_size = {1: 1}
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(expected, solution)

    @parameterized.expand([
        ("ship_top", BimaruSolver.ship_top, Grid.empty()),
        ("ship_bottom", BimaruSolver.ship_bottom, Grid.empty()),
        ("ship_left", BimaruSolver.ship_left, Grid.empty()),
        ('ship_right', BimaruSolver.ship_right, Grid.empty()),
        ("ship_middle", BimaruSolver.ship_middle_input, Grid.empty()),
    ])
    def test_solution_with_initials_constraints_position_max_x(self, test_name, value, expected):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, value, -1, -1, -1],
        ])
        ships = {'column': [0, 1, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0, 0]}
        ships_number_by_size = {1: 1}
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(expected, solution)

    @parameterized.expand([
        ("ship_top", BimaruSolver.ship_top, Grid.empty()),
        ("ship_bottom", BimaruSolver.ship_bottom, Grid.empty()),
        ("ship_left", BimaruSolver.ship_left, Grid.empty()),
        ('ship_right', BimaruSolver.ship_right, Grid.empty()),
        ("ship_middle", BimaruSolver.ship_middle_input, Grid.empty()),
    ])
    def test_solution_with_initials_constraints_position_max_max(self, test_name, value, expected):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, value],
        ])
        ships = {'column': [0, 1, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0, 0]}
        ships_number_by_size = {1: 1}
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(expected, solution)

    @parameterized.expand([
        ("ship_top", BimaruSolver.ship_top, Grid.empty()),
        ("ship_bottom", BimaruSolver.ship_bottom, Grid.empty()),
        ("ship_left", BimaruSolver.ship_left, Grid.empty()),
        ('ship_right', BimaruSolver.ship_right, Grid.empty()),
        ("ship_middle", BimaruSolver.ship_middle_input, Grid.empty()),
    ])
    def test_solution_with_initials_constraints_position_x_max(self, test_name, value, expected):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, value],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        ships = {'column': [0, 1, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0, 0]}
        ships_number_by_size = {1: 1}
        game_solver = BimaruSolver(grid, ships, ships_number_by_size, self.solver_engine)
        solution = game_solver.get_solution()
        self.assertEqual(expected, solution)


if __name__ == '__main__':
    unittest.main()
