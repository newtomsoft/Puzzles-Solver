from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.Zip.ZipSolver import ZipSolver

_ = 0
a = 10

class ZipSolverTests(TestCase):
    def test_solution_basic_grid(self):
        grid = Grid([
            [1, _, 4],
            [_, 5, _],
            [2, _, 3]
        ])
        game_solver = ZipSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╷  ┌──┐ \n'
            ' │  ↓  │ \n'
            ' └─────┘ '
        )

        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6(self):
        grid = Grid([
            [_, _, _, 4, 7, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, 8, 1, _, _],
            [5, 3, _, _, 2, 6],
            [_, _, _, _, _, _],
        ])
        game_solver = ZipSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ┌────────┐  ┌──┐ \n'
            ' │  ┌─────┘  │  │ \n'
            ' │  │  ┌─────┘  │ \n'
            ' │  │  ↓  ╶──┐  │ \n'
            ' │  └────────┘  │ \n'
            ' └──────────────┘ '
        )

        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_7x7(self):
        grid = Grid([
            [7, _, _, _, _, _, 6],
            [_, 2, _, _, _, _, _],
            [_, _, 9, _, _, _, _],
            [_, _, _, 1, _, _, _],
            [_, _, _, _, 8, _, _],
            [_, _, _, _, _, 3, _],
            [4, _, _, _, _, _, 5],
        ])
        game_solver = ZipSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ┌─────────────────┐ \n'
            ' │  ┌───────────┐  │ \n'
            ' │  │   ←────┐  │  │ \n'
            ' │  └─────╴  │  │  │ \n'
            ' └───────────┘  │  │ \n'
            ' ┌──────────────┘  │ \n'
            ' └─────────────────┘ '
        )

        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_with_wall(self):
        grid = Grid([
            [3, _, _, _, _, 9],
            [_, 2, _, _, a, _],
            [_, _, 1, 8, _, _],
            [_, _, _, _, _, _],
            [_, 4, _, _, 6, _],
            [_, _, 5, 7, _, _],
        ])
        grid.set_walls(
            {
                frozenset([Position(0, 2), Position(0, 3)]),
                frozenset([Position(1, 2), Position(1, 3)]),
                frozenset([Position(2, 2), Position(2, 3)]),
                frozenset([Position(4, 2), Position(4, 3)]),
                frozenset([Position(5, 2), Position(5, 3)]),
            }
        )
        game_solver = ZipSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ┌─────┐  ┌─────┐ \n'
            ' │  ┌──┘  │   ←─┘ \n'
            ' │  └──╴  └─────┐ \n'
            ' └──┐  ┌─────┐  │ \n'
            ' ┌──┘  │  ┌──┘  │ \n'
            ' └─────┘  └─────┘ '
        )

        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_with_u_turn(self):
        grid = Grid([
            [_, _, _, _, _, _],
            [_, _, 2, _, _, 5],
            [_, _, _, _, _, 3],
            [6, _, _, _, _, _],
            [1, _, _, 4, _, _],
            [_, _, _, _, _, _],
        ])
        game_solver = ZipSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ┌──────────────┐ \n'
            ' │  ┌──┐  ┌─────┘ \n'
            ' │  │  │  │  ┌──┐ \n'
            ' ↓  │  │  │  │  │ \n'
            ' ╷  │  │  └──┘  │ \n'
            ' └──┘  └────────┘ '
        )

        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_with_wall_and_u_turn(self):
        grid = Grid([
            [_, _, _, _, _, _],
            [_, _, 6, _, _, 2],
            [_, 5, _, _, 3, _],
            [_, 8, _, _, 1, _],
            [7, _, _, 4, _, _],
            [_, _, _, _, _, _],
        ])
        grid.set_walls(
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
        game_solver = ZipSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ┌─────┐  ┌─────┐ \n'
            ' │  ┌──┘  │  ┌──┘ \n'
            ' │  └──┐  │  └──┐ \n'
            ' │  ↑  │  └──╴  │ \n'
            ' │  │  │  ┌──┐  │ \n'
            ' └──┘  └──┘  └──┘ '
        )

        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_2025_03_24(self):
        grid = Grid([
            [6, _, _, _, _, 7],
            [_, 3, _, _, _, _],
            [_, _, _, 5, _, _],
            [_, _, 4, _, _, _],
            [_, _, _, _, 2, _],
            [1, _, _, _, _, 8],
        ])
        game_solver = ZipSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ┌──────────────┐ \n'
            ' │  ┌────────┐  │ \n'
            ' │  │  ┌──┐  │  │ \n'
            ' │  └──┘  │  │  │ \n'
            ' └────────┘  │  │ \n'
            ' ╶───────────┘  ↓ '
        )

        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_2025_03_25(self):
        grid = Grid([
            [_, _, _, _, _, _],
            [2, _, _, _, 4, _],
            [_, _, 6, _, _, _],
            [_, _, _, _, _, _],
            [3, _, 7, _, 5, _],
            [_, _, 1, _, _, _],
        ])
        game_solver = ZipSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ┌──────────────┐ \n'
            ' │  ┌────────┐  │ \n'
            ' │  │  ┌──┐  │  │ \n'
            ' │  │  │  │  │  │ \n'
            ' │  │  ↓  └──┘  │ \n'
            ' └──┘  ╶────────┘ '
        )

        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_2025_03_26(self):
        grid = Grid([
            [_, _, _, _, _, _],
            [_, 1, _, _, _, _],
            [_, 4, _, _, _, _],
            [_, _, _, _, 3, _],
            [_, _, _, _, 2, _],
            [_, _, _, _, _, _],
        ])
        grid.set_walls({
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
        game_solver = ZipSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ┌──┐  ┌──┐  ┌──┐ \n'
            ' │  ╵  │  │  │  │ \n'
            ' │   ←─┘  │  │  │ \n'
            ' │  ┌──┐  └──┘  │ \n'
            ' │  │  │  ┌──┐  │ \n'
            ' └──┘  └──┘  └──┘ '
        )

        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_2025_03_27(self):
        grid = Grid([
            [6, _, _, _, _, 5],
            [_, _, _, _, _, _],
            [_, 7, 1, 8, 2, _],
            [_, _, _, _, _, _],
            [3, _, _, _, _, 4],
            [_, _, _, _, _, _],
        ])
        game_solver = ZipSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ┌──────────────┐ \n'
            ' └──┐  ┌─────┐  │ \n'
            ' ┌──┘  ╵  ↑  │  │ \n'
            ' └────────┘  │  │ \n'
            ' ┌───────────┘  │ \n'
            ' └──────────────┘ '
        )

        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_2025_03_28(self):
        grid = Grid([
            [_, _, _, _, _, _],
            [_, _, _, 5, 3, _],
            [_, _, 4, _, _, _],
            [_, _, _, 2, _, _],
            [_, 1, 6, _, _, _],
            [_, _, _, _, _, _],
        ])
        grid.set_walls({
            frozenset([Position(0, 1), Position(1, 1)]),
            frozenset([Position(0, 2), Position(1, 2)]),
            frozenset([Position(1, 1), Position(1, 2)]),
            frozenset([Position(2, 1), Position(2, 2)]),
            frozenset([Position(2, 3), Position(3, 3)]),
            frozenset([Position(2, 4), Position(3, 4)]),
            frozenset([Position(3, 3), Position(3, 4)]),
            frozenset([Position(4, 3), Position(4, 4)]),
        })
        game_solver = ZipSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ┌────────┐  ┌──┐ \n'
            ' └──┐  ┌──┘  │  │ \n'
            ' ┌──┘  └─────┘  │ \n'
            ' │  ┌─────┐  ┌──┘ \n'
            ' │  ╵  ↑  │  └──┐ \n'
            ' └─────┘  └─────┘ '
        )

        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_2025_03_29(self):
        grid = Grid([
            [6, _, _, _, _, 5],
            [_, _, _, _, _, _],
            [_, 7, 1, 8, 2, _],
            [_, _, _, _, _, _],
            [3, _, _, _, _, 4],
            [_, _, _, _, _, _],
        ])
        game_solver = ZipSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ┌──────────────┐ \n'
            ' └──┐  ┌─────┐  │ \n'
            ' ┌──┘  ╵  ↑  │  │ \n'
            ' └────────┘  │  │ \n'
            ' ┌───────────┘  │ \n'
            ' └──────────────┘ '
        )

        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_2025_03_30(self):
        grid = Grid([
            [_, _, _, _, _, 3],
            [_, 6, _, _, _, _],
            [_, _, 7, _, _, 4],
            [1, _, _, 2, _, _],
            [_, _, _, _, 8, _],
            [5, _, _, _, _, _],
        ])
        game_solver = ZipSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ┌────────┐  ┌──┐ \n'
            ' │  ┌──┐  │  │  │ \n'
            ' │  │  │  │  │  │ \n'
            ' ╵  │  │  └──┘  │ \n'
            ' ┌──┘  └────→   │ \n'
            ' └──────────────┘ '
        )

        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_2025_03_31(self):
        grid = Grid([
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, 2, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, 1]
        ])
        grid.set_walls({
            frozenset({Position(1, 4), Position(1, 5)}),
            frozenset({Position(1, 0), Position(1, 1)}),
            frozenset({Position(3, 0), Position(3, 1)}),
            frozenset({Position(1, 2), Position(2, 2)}),
            frozenset({Position(3, 2), Position(3, 3)}),
            frozenset({Position(3, 3), Position(3, 4)}),
            frozenset({Position(0, 3), Position(1, 3)}),
            frozenset({Position(3, 2), Position(4, 2)}),
            frozenset({Position(2, 1), Position(2, 2)}),
            frozenset({Position(4, 2), Position(5, 2)}),
            frozenset({Position(2, 4), Position(2, 5)}),
            frozenset({Position(3, 4), Position(3, 5)}),
            frozenset({Position(3, 1), Position(3, 2)}),
            frozenset({Position(2, 0), Position(2, 1)}),
            frozenset({Position(4, 4), Position(4, 5)}),
            frozenset({Position(0, 1), Position(1, 1)}),
            frozenset({Position(0, 2), Position(1, 2)}),
            frozenset({Position(4, 0), Position(4, 1)}),
            frozenset({Position(0, 4), Position(1, 4)}),
            frozenset({Position(4, 1), Position(5, 1)}),
            frozenset({Position(2, 3), Position(2, 4)}),
            frozenset({Position(1, 3), Position(2, 3)})
        })
        game_solver = ZipSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ┌──────────────┐ \n'
            ' │  ┌────────┐  │ \n'
            ' │  │  ┌──┐  │  │ \n'
            ' │  │  ↓  │  │  │ \n'
            ' │  └─────┘  │  │ \n'
            ' └───────────┘  ╵ '
        )

        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_2025_04_01(self):
        grid = Grid([
            [1, _, _, 2, _, _, 3],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _]
        ])
        grid.set_walls({
            frozenset({Position(5, 5), Position(6, 5)}),
            frozenset({Position(4, 3), Position(5, 3)}),
            frozenset({Position(1, 3), Position(1, 4)}),
            frozenset({Position(4, 5), Position(4, 6)}),
            frozenset({Position(0, 6), Position(1, 6)}),
            frozenset({Position(5, 5), Position(5, 6)}),
            frozenset({Position(5, 1), Position(6, 1)}),
            frozenset({Position(4, 2), Position(4, 3)}),
            frozenset({Position(3, 2), Position(3, 3)}),
            frozenset({Position(0, 3), Position(1, 3)}),
            frozenset({Position(2, 1), Position(2, 2)}),
            frozenset({Position(3, 1), Position(3, 2)}),
            frozenset({Position(0, 5), Position(1, 5)}),
            frozenset({Position(5, 1), Position(5, 2)}),
            frozenset({Position(0, 0), Position(1, 0)}),
            frozenset({Position(5, 2), Position(6, 2)}),
            frozenset({Position(2, 3), Position(3, 3)}),
            frozenset({Position(3, 5), Position(4, 5)}),
            frozenset({Position(1, 1), Position(2, 1)}),
            frozenset({Position(4, 1), Position(4, 2)}),
            frozenset({Position(3, 5), Position(3, 6)}),
            frozenset({Position(2, 5), Position(2, 6)}),
            frozenset({Position(1, 5), Position(2, 5)}),
            frozenset({Position(2, 3), Position(2, 4)}),
        })
        game_solver = ZipSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = (
            ' ╶──┐  ┌──────────→  \n'
            ' ┌──┘  └──┐  ┌─────┐ \n'
            ' └──┐  ┌──┘  └──┐  │ \n'
            ' ┌──┘  │  ┌─────┘  │ \n'
            ' └──┐  │  └─────┐  │ \n'
            ' ┌──┘  └────────┘  │ \n'
            ' └─────────────────┘ '
        )

        self.assertEqual(expected_solution, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
