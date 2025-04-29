import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.Creeks.CreeksSolver import CreeksSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine

_ = -1


class CreeksSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_map_position(self):
        grid = Grid([
            [1, 1, 0],
            [1, 1, 0],
            [1, 0, 0]
        ])
        solution_grid = Grid([
            [1, 0],
            [0, 0],
        ])

        game_solver = CreeksSolver(grid, self.get_solver_engine())
        position = Position(0, 0)
        mapped_position = game_solver._get_positions_in_solution_grid(solution_grid, position)
        expected_mapped_position = {Position(0, 0)}
        self.assertEqual(expected_mapped_position, mapped_position)

        position = Position(0, 1)
        mapped_position = game_solver._get_positions_in_solution_grid(solution_grid, position)
        expected_mapped_position = {Position(0, 0), Position(0, 1)}
        self.assertEqual(expected_mapped_position, mapped_position)

        position = Position(0, 2)
        mapped_position = game_solver._get_positions_in_solution_grid(solution_grid, position)
        expected_mapped_position = {Position(0, 1)}
        self.assertEqual(expected_mapped_position, mapped_position)

        position = Position(1, 0)
        mapped_position = game_solver._get_positions_in_solution_grid(solution_grid, position)
        expected_mapped_position = {Position(0, 0), Position(1, 0)}
        self.assertEqual(expected_mapped_position, mapped_position)

        position = Position(1, 1)
        mapped_position = game_solver._get_positions_in_solution_grid(solution_grid, position)
        expected_mapped_position = {Position(0, 0), Position(1, 0), Position(1, 1), Position(0, 1)}
        self.assertEqual(expected_mapped_position, mapped_position)

        position = Position(1, 2)
        mapped_position = game_solver._get_positions_in_solution_grid(solution_grid, position)
        expected_mapped_position = {Position(0, 1), Position(1, 1)}
        self.assertEqual(expected_mapped_position, mapped_position)

        position = Position(2, 0)
        mapped_position = game_solver._get_positions_in_solution_grid(solution_grid, position)
        expected_mapped_position = {Position(1, 0)}
        self.assertEqual(expected_mapped_position, mapped_position)

        position = Position(2, 1)
        mapped_position = game_solver._get_positions_in_solution_grid(solution_grid, position)
        expected_mapped_position = {Position(1, 0), Position(1, 1)}
        self.assertEqual(expected_mapped_position, mapped_position)

        position = Position(2, 2)
        mapped_position = game_solver._get_positions_in_solution_grid(solution_grid, position)
        expected_mapped_position = {Position(1, 1)}
        self.assertEqual(expected_mapped_position, mapped_position)

    def test_solution_basic_grid(self):
        grid = Grid([
            [1, 1, 0],
            [1, 1, 0],
            [0, 0, 0]
        ])
        game_solver = CreeksSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 0],
            [0, 0],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_3eyv2(self):
        # https://gridpuzzle.com/creek/3eyv2
        grid = Grid([
            [0, _, 0, _, 0],
            [1, 2, 1, 1, 1],
            [_, 3, _, 1, _],
            [1, _, 1, _, 0],
            [0, 0, 1, 1, 0]
        ])
        game_solver = CreeksSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [0, 0, 0, 0],
            [1, 1, 0, 1],
            [1, 0, 0, 0],
            [0, 0, 1, 0],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_with_adjacent_watter_constraint_3ekygn(self):
        # https://gridpuzzle.com/creek/ekygn
        grid = Grid([
            [_, _, 1, _, _],
            [_, 2, _, _, 1],
            [2, _, _, _, _],
            [_, 2, _, 1, _],
            [0, _, _, _, _]
        ])
        game_solver = CreeksSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 0, 1, 1],
            [1, 0, 0, 0],
            [1, 1, 0, 1],
            [0, 0, 0, 0],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
