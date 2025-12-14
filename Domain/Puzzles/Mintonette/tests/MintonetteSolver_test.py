import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Mintonette.MintonetteSolver_or_tools import MintonetteSolver

_ = MintonetteSolver.Empty
o = MintonetteSolver.Unknown


class MintonetteSolverTests(TestCase):
    def test_solution_4x4_easy_31n1r(self):
        """https://gridpuzzle.com/mintonette/31n1r"""
        values_grid = Grid([
            [1, _, 0, 0],
            [0, 1, _, 4],
            [_, _, _, 0],
            [0, _, 4, 0],
        ])

        expected_solution_string = (
            ' ╶──┐  ╶──╴ \n'
            ' ╷  ╵  ┌──╴ \n'
            ' │  ┌──┘  ╷ \n'
            ' ╵  └──╴  ╵ '
        )

        solver = MintonetteSolver(values_grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_expert_n10kr(self):
        """https://gridpuzzle.com/mintonette/n10kr"""
        values_grid = Grid([
            [o, _, _, _, 1],
            [2, _, 1, _, _],
            [_, _, _, o, o],
            [_, 1, _, o, o],
            [o, _, 1, 1, _]
        ])

        expected_solution_string = (
            ' ╶──┐  ┌─────╴ \n'
            ' ╶──┘  ╵  ┌──┐ \n'
            ' ┌─────┐  ╵  ╵ \n'
            ' │  ╷  └──╴  ╷ \n'
            ' ╵  └──╴  ╶──┘ '
        )

        solver = MintonetteSolver(values_grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_evil_15ye9(self):
        """https://gridpuzzle.com/mintonette/15ye9"""
        values_grid = Grid([
            [o, 3, _, 0, 0, 2],
            [o, 3, _, _, _, _],
            [o, _, _, o, 1, 0],
            [_, o, _, _, _, 0],
            [_, _, _, o, o, 2],
            [3, _, _, 0, _, _]
        ])

        expected_solution_string = (
            ' ╷  ╶──┐  ╶──╴  ╷ \n'
            ' ╵  ╷  │  ┌─────┘ \n'
            ' ╷  └──┘  ╵  ╷  ╷ \n'
            ' │  ╶────────┘  ╵ \n'
            ' └─────┐  ╷  ╷  ╷ \n'
            ' ╶─────┘  ╵  └──┘ '
        )

        solver = MintonetteSolver(values_grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_evil_01wxw(self):
        """https://gridpuzzle.com/mintonette/01wxw"""
        values_grid = Grid([
            [o, _, _, 5, 1, _, _, 2],
            [0, _, _, _, _, 1, _, o],
            [4, 0, _, _, _, _, o, 0],
            [_, o, 5, 1, o, _, _, o],
            [_, _, o, _, o, o, _, o],
            [4, _, _, o, _, _, _, o],
            [_, _, _, 0, _, 5, _, _],
            [o, _, _, 0, 0, _, 0, 5]
        ])

        expected_solution_string = (
            ' ╷  ┌─────╴  ╶──┐  ┌──╴ \n'
            ' ╵  └────────┐  ╵  └──╴ \n'
            ' ╷  ╷  ┌─────┘  ┌──╴  ╷ \n'
            ' │  ╵  ╵  ╷  ╷  └──┐  ╵ \n'
            ' └──┐  ╶──┘  ╵  ╶──┘  ╷ \n'
            ' ╷  │  ┌──╴  ┌─────┐  ╵ \n'
            ' └──┘  │  ╷  └──╴  └──┐ \n'
            ' ╶─────┘  ╵  ╶─────╴  ╵ '
        )

        solver = MintonetteSolver(values_grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_evil_0d4v1(self):
        """https://gridpuzzle.com/mintonette/0d4v1"""
        values_grid = Grid([
            [o, _, _, o, 0, _, 6, _, _, 6],
            [2, _, _, 2, 0, _, _, _, _, _],
            [o, o, 0, 0, _, 0, _, _, _, _],
            [_, 0, 1, _, _, 0, _, o, 6, _],
            [_, 0, 0, 0, _, _, 8, _, 2, _],
            [o, 1, _, _, _, _, _, _, o, _],
            [o, _, _, o, o, _, _, o, _, _],
            [0, 0, _, 1, _, _, 0, _, _, 6],
            [_, o, 2, _, _, 8, o, 0, _, _],
            [1, 1, _, _, 0, _, o, 0, _, o]
        ])

        expected_solution_string = (
            ' ╶──┐  ┌──╴  ╷  ┌──╴  ┌─────╴ \n'
            ' ╶──┘  └──╴  ╵  └──┐  │  ┌──┐ \n'
            ' ╷  ╶──╴  ╶─────╴  └──┘  │  │ \n'
            ' │  ╷  ╶─────┐  ╶─────╴  ╵  │ \n'
            ' │  ╵  ╶──╴  │  ┌──╴  ┌──╴  │ \n'
            ' ╵  ╷  ┌──┐  │  └──┐  └──╴  │ \n'
            ' ╶──┘  │  ╵  ╵  ┌──┘  ╷  ┌──┘ \n'
            ' ╶──╴  │  ╷  ┌──┘  ╷  │  │  ╷ \n'
            ' ┌──╴  ╵  │  └──╴  ╵  ╵  └──┘ \n'
            ' ╵  ╶─────┘  ╶─────╴  ╶─────╴ '
        )

        solver = MintonetteSolver(values_grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_15x15_easy_0jdw8(self):
        """https://gridpuzzle.com/mintonette/0jdw8"""
        values_grid = Grid([
            [0, 0, 0, _, 0, _, _, _, 0, 0, 5, _, 1, _, 1],
            [2, 2, 1, _, _, _, 0, _, 7, 0, 0, _, _, 1, _],
            [_, _, 0, 0, _, _, 0, 1, _, _, _, 5, _, 1, _],
            [0, _, _, 4, 1, _, 0, 0, _, _, _, _, _, 1, _],
            [_, _, _, 7, _, _, 5, _, _, 2, 1, 0, 0, 0, 1],
            [_, 4, _, _, _, 6, _, _, 2, 3, _, _, 0, 0, 0],
            [0, 1, _, _, 6, _, _, _, _, 5, _, _, 0, 2, _],
            [1, _, _, _, _, _, 1, _, _, _, 3, _, _, _, 0],
            [0, _, _, 0, _, _, 0, 1, _, _, 0, _, 4, _, 1],
            [_, 3, _, 3, 0, _, 0, 1, _, _, _, 2, _, 1, 0],
            [0, 0, 0, 0, 0, _, 0, _, 1, 0, _, 3, _, _, 0],
            [_, _, _, 0, 1, _, 3, 3, 1, 0, _, _, _, _, _],
            [_, 3, 3, 1, _, _, _, _, _, 1, 0, 1, _, 3, 4],
            [1, _, _, _, 0, 1, 0, _, 0, 0, 0, _, 0, _, 2],
            [0, _, 0, 1, 0, _, _, 1, 0, 0, 1, _, 0, _, 2]
        ])

        expected_solution_string = (
            ' ╶──╴  ╶─────╴  ┌─────┐  ╶──╴  ╶──┐  ╶──┐  ╷ \n'
            ' ╷  ╷  ╶─────┐  │  ╷  └──╴  ╶──╴  └──┐  ╵  │ \n'
            ' └──┘  ╶──╴  │  │  ╵  ╶────────┐  ╷  │  ╶──┘ \n'
            ' ╷  ┌─────╴  ╵  │  ╶──╴  ┌──┐  │  └──┘  ╶──┐ \n'
            ' │  └──┐  ╷  ┌──┘  ╶──┐  │  ╵  ╵  ╶──╴  ╷  ╵ \n'
            ' │  ╶──┘  └──┘  ╶──┐  │  ╵  ╶─────┐  ╷  ╵  ╷ \n'
            ' ╵  ╷  ┌─────╴  ┌──┘  └──┐  ╷  ┌──┘  ╵  ╷  │ \n'
            ' ╶──┘  └────────┘  ╶──┐  │  │  ╵  ┌─────┘  ╵ \n'
            ' ╷  ┌──┐  ╶────────╴  ╵  │  │  ╷  │  ╷  ┌──╴ \n'
            ' │  ╵  └──╴  ╶─────╴  ╷  └──┘  │  ╵  │  ╵  ╷ \n'
            ' ╵  ╶──╴  ╷  ╶─────╴  └──╴  ╷  │  ╷  └──┐  ╵ \n'
            ' ┌─────┐  ╵  ╷  ┌──╴  ╷  ╷  ╵  │  └──┐  └──┐ \n'
            ' └──╴  ╵  ╶──┘  └─────┘  └──╴  ╵  ╷  └──╴  ╵ \n'
            ' ╶────────┐  ╷  ╷  ╶─────╴  ╶──╴  │  ╷  ┌──╴ \n'
            ' ╶─────╴  ╵  ╵  └─────╴  ╶──╴  ╶──┘  ╵  └──╴ '
        )

        solver = MintonetteSolver(values_grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_15x15_evil_2qp8y(self):
        """https://gridpuzzle.com/mintonette/2qp8y"""
        values_grid = Grid([
            [o, _, _, 1, _, _, o, _, _, _, o, 1, o, _, 3],
            [0, _, _, _, _, 2, _, 1, 1, _, 0, _, 1, _, _],
            [0, _, 1, _, 4, 1, _, _, 2, o, 0, 1, o, _, _],
            [o, _, 0, o, 1, _, 1, _, o, o, _, _, 0, 2, o],
            [o, 0, o, _, 1, o, _, _, _, _, 0, o, o, _, _],
            [o, _, _, 1, _, _, 3, _, _, o, 0, _, 0, 0, 0],
            [_, 1, o, 0, _, _, o, o, _, _, _, 0, o, 1, o],
            [_, _, 1, _, _, _, _, o, o, o, 3, _, _, _, 0],
            [4, _, o, o, _, _, _, _, _, _, o, _, o, _, o],
            [_, _, o, o, _, 0, 0, o, 6, _, _, 2, o, _, 0],
            [_, _, _, _, _, o, _, _, 0, o, _, o, o, _, 0],
            [_, 2, 0, 0, _, 2, 0, _, _, _, _, _, 4, _, _],
            [0, _, o, o, _, 4, _, _, _, _, _, _, 2, _, o],
            [o, 1, o, _, _, 0, _, _, _, 5, 0, _, o, _, 0],
            [0, o, o, o, 2, 0, _, _, _, _, _, _, 0, _, 0]
        ])

        expected_solution_string = (
            ' ╶──┐  ┌──╴  ┌─────╴  ┌────────╴  ╷  ╶──┐  ╷ \n'
            ' ╷  │  │  ┌──┘  ╶──┐  ╵  ╶──┐  ╷  └──╴  │  │ \n'
            ' ╵  │  ╵  └──╴  ╷  └─────╴  ╵  ╵  ╷  ╷  └──┘ \n'
            ' ╶──┘  ╷  ╷  ╶──┘  ╷  ┌──╴  ╶─────┘  ╵  ╷  ╷ \n'
            ' ╶──╴  ╵  └──╴  ╶──┘  └─────┐  ╷  ╷  ╷  └──┘ \n'
            ' ╷  ┌─────╴  ┌──┐  ╶─────┐  ╵  ╵  │  ╵  ╶──╴ \n'
            ' │  ╵  ╶──╴  │  │  ╶──╴  └─────┐  ╵  ╷  ╷  ╷ \n'
            ' └──┐  ╶──┐  │  └─────╴  ╶──╴  ╵  ┌──┘  │  ╵ \n'
            ' ╷  │  ╷  ╵  └──────────────┐  ╷  │  ╶──┘  ╷ \n'
            ' └──┘  ╵  ╶─────╴  ╷  ╷  ╶──┘  │  ╵  ╶──┐  ╵ \n'
            ' ┌──────────────╴  │  │  ╶──╴  │  ╶──╴  │  ╷ \n'
            ' └──╴  ╶──╴  ┌──╴  ╵  └─────┐  │  ┌──╴  │  │ \n'
            ' ╷  ┌──╴  ╶──┘  ╶──┐  ┌─────┘  │  │  ╶──┘  ╵ \n'
            ' ╵  ╵  ╷  ┌──┐  ╷  │  └─────╴  ╵  │  ╶─────╴ \n'
            ' ╶──╴  ╵  ╵  ╵  ╵  └──────────────┘  ╶─────╴ '
        )

        solver = MintonetteSolver(values_grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)




if __name__ == '__main__':
    unittest.main()
