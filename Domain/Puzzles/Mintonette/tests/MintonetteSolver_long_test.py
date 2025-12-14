import unittest

from Domain.Board.Grid import Grid
from Domain.Puzzles.Mintonette.MintonetteSolver_or_tools import MintonetteSolver

_ = MintonetteSolver.Empty
o = MintonetteSolver.Unknown


class MintonetteSolverLongTests(unittest.TestCase):
    def test_solution_15x15_evil_1q56r(self):
        """https://gridpuzzle.com/mintonette/1q56r"""
        values_grid = Grid([
            [o, o, 0, 0, _, 0, 2, o, _, 5, _, _, _, 1, _],
            [o, 0, _, o, _, _, _, _, _, 5, _, _, _, o, _],
            [o, _, _, _, _, _, _, 1, _, _, _, _, o, 0, 1],
            [_, o, 0, 3, 5, _, o, 0, _, o, _, o, _, _, o],
            [_, _, o, _, 2, _, _, _, _, _, _, _, _, 9, 4],
            [0, o, 2, _, 3, 5, _, 0, o, 0, _, _, _, _, _],
            [0, _, 2, _, _, 1, 2, _, _, 2, _, _, 4, _, _],
            [o, _, o, _, 1, _, o, 2, _, _, o, _, _, _, o],
            [o, o, _, o, o, o, o, _, _, _, o, _, 5, _, 0],
            [_, o, _, o, _, _, 1, _, 9, _, _, _, _, _, o],
            [_, _, _, _, _, _, _, o, o, _, 0, 2, _, _, _],
            [0, _, 0, 4, _, _, _, 0, _, _, 0, _, _, o, o],
            [o, 3, 0, 0, _, 0, _, o, o, 0, _, o, 2, _, 0],
            [_, _, _, 1, o, _, _, 1, _, _, _, o, _, _, o],
            [o, 2, o, 1, _, 3, 1, _, 2, o, _, 2, _, _, 2]
        ])

        expected_solution_string = (
            ' ╷  ╶──╴  ╶─────╴  ╷  ╷  ┌──╴  ┌─────┐  ╶──┐ \n'
            ' ╵  ╷  ┌──╴  ┌──┐  └──┘  │  ╶──┘  ┌──┘  ╷  │ \n'
            ' ╷  │  └──┐  │  │  ┌──╴  │  ┌──┐  │  ╷  ╵  ╵ \n'
            ' │  ╵  ╷  ╵  ╵  │  ╵  ╷  │  ╵  │  ╵  └─────╴ \n'
            ' └──┐  ╵  ┌──╴  └──┐  │  └─────┘  ┌──┐  ╷  ╷ \n'
            ' ╷  ╵  ╶──┘  ╷  ╶──┘  ╵  ╶──╴  ┌──┘  └──┘  │ \n'
            ' ╵  ┌──╴  ┌──┘  ╷  ╶─────┐  ╷  └──┐  ╷  ┌──┘ \n'
            ' ╶──┘  ╶──┘  ╶──┘  ╷  ╶──┘  │  ╷  │  └──┘  ╷ \n'
            ' ╶──╴  ┌──╴  ╷  ╷  ╵  ┌─────┘  ╵  │  ╶──┐  ╵ \n'
            ' ┌──╴  │  ╶──┘  └──╴  │  ╶────────┘  ┌──┘  ╷ \n'
            ' └──┐  └───────────┐  ╵  ╶─────╴  ╷  └─────┘ \n'
            ' ╷  │  ╷  ╶────────┘  ╶────────╴  └──┐  ╷  ╷ \n'
            ' ╵  ╵  ╵  ╶─────╴  ┌──╴  ╶──╴  ┌──╴  ╵  │  ╵ \n'
            ' ┌──┐  ┌──╴  ╷  ┌──┘  ╷  ┌──┐  │  ╶──┐  └──╴ \n'
            ' ╵  ╵  ╵  ╶──┘  ╵  ╶──┘  ╵  ╵  └──╴  └─────╴ '
        )

        solver = MintonetteSolver(values_grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
