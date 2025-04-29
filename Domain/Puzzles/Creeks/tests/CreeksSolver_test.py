import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.Creeks.CreeksSolver import CreeksSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine


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
        mapped_position = game_solver.map_position(solution_grid, position)
        expected_mapped_position = {Position(0, 0)}
        self.assertEqual(expected_mapped_position, mapped_position)

        position = Position(0, 1)
        mapped_position = game_solver.map_position(solution_grid, position)
        expected_mapped_position = {Position(0, 0), Position(0, 1)}
        self.assertEqual(expected_mapped_position, mapped_position)

        position = Position(0, 2)
        mapped_position = game_solver.map_position(solution_grid, position)
        expected_mapped_position = {Position(0, 1)}
        self.assertEqual(expected_mapped_position, mapped_position)


    def test_solution_basic_grid(self):
        grid = Grid([
            [1, 1, 0],
            [1, 1, 0],
            [1, 0, 0]
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

if __name__ == '__main__':
    unittest.main()
