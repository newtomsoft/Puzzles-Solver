import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GrandTour.GrandTourSolver import GrandTourSolver

_ = 0


class GrandTourSolverTests(TestCase):
    def test_basic_grid_without_island(self):
        grid = Grid([
            [_, _, _, _],
            [_, _, _, _],
        ])
        expected_solution_str = (
            ' ┌────────┐ \n'
            ' └────────┘ '
        )
        game_solver = GrandTourSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_basic_grid_without_island_2(self):
        grid = Grid([
            [_, _],
            [_, _],
            [_, _],
        ])
        expected_solution_str = (
            ' ┌──┐ \n'
            ' │  │ \n'
            ' └──┘ '
        )
        game_solver = GrandTourSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_basic_grid_without_island_no_solution(self):
        grid = Grid([
            [_, _, _],
            [_, _, _],
            [_, _, _],
        ])
        game_solver = GrandTourSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(IslandGrid.empty(), solution)

    def test_4x4(self):
        grid = Grid([
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])

        island11 = Island(Position(1, 1), 1)
        island11.set_bridge_to_position(Position(1, 2), 1)
        island11.set_bridges_count_according_to_directions_bridges()

        island21 = Island(Position(2, 1), 2)
        island21.set_bridge_to_position(Position(2, 2), 1)
        island21.set_bridge_to_position(Position(3, 1), 1)
        island21.set_bridges_count_according_to_directions_bridges()

        grid[Position(1, 1)] = island11
        grid[Position(2, 1)] = island21

        expected_solution_str = (
            ' ┌──┐  ┌──┐ \n'
            ' │  └──┘  │ \n'
            ' │  ┌──┐  │ \n'
            ' └──┘  └──┘ '
        )
        game_solver = GrandTourSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_4x4_0x84r(self):
        # https://gridpuzzle.com/grandtour/0x84r
        grid = Grid([
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        island11 = Island(Position(1, 1), 1)
        island11.set_bridge_to_position(Position(1, 2), 1)
        island11.set_bridges_count_according_to_directions_bridges()
        island20 = Island(Position(2, 0), 1)
        island20.set_bridge_to_position(Position(2, 1), 1)
        island20.set_bridges_count_according_to_directions_bridges()
        grid[Position(1, 1)] = island11
        grid[Position(2, 0)] = island20

        expected_solution_str = (
            ' ┌────────┐ \n'
            ' └─────┐  │ \n'
            ' ┌─────┘  │ \n'
            ' └────────┘ '
        )

        game_solver = GrandTourSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_4x4_31jg9(self):
        # https://gridpuzzle.com/grandtour/31jg9
        grid = Grid([
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        island10 = Island(Position(1, 0), 1)
        island10.set_bridge_to_position(Position(2, 0), 1)
        island10.set_bridges_count_according_to_directions_bridges()
        island22 = Island(Position(2, 2), 1)
        island22.set_bridge_to_position(Position(2, 3), 1)
        island22.set_bridges_count_according_to_directions_bridges()
        grid[Position(1, 0)] = island10
        grid[Position(2, 2)] = island22

        expected_solution_str = (
            ' ┌────────┐ \n'
            ' │  ┌─────┘ \n'
            ' │  └─────┐ \n'
            ' └────────┘ '
        )

        game_solver = GrandTourSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_6x6_oyzr4(self):
        # https://gridpuzzle.com/grandtour/0yzr4
        grid = Grid([
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _]
        ])
        island01 = Island(Position(0, 1), 1)
        island01.set_bridge_to_position(Position(0, 2), 1)
        island01.set_bridges_count_according_to_directions_bridges()
        island10 = Island(Position(1, 0), 1)
        island10.set_bridge_to_position(Position(2, 0), 1)
        island10.set_bridges_count_according_to_directions_bridges()
        island23 = Island(Position(2, 3), 1)
        island23.set_bridge_to_position(Position(2, 4), 1)
        island23.set_bridges_count_according_to_directions_bridges()
        island24 = Island(Position(2, 4), 1)
        island24.set_bridge_to_position(Position(2, 5), 1)
        island24.set_bridges_count_according_to_directions_bridges()
        island31 = Island(Position(3, 1), 1)
        island31.set_bridge_to_position(Position(3, 2), 1)
        island31.set_bridges_count_according_to_directions_bridges()
        island33 = Island(Position(3, 3), 1)
        island33.set_bridge_to_position(Position(4, 3), 1)
        island33.set_bridges_count_according_to_directions_bridges()
        island43 = Island(Position(4, 3), 1)
        island43.set_bridge_to_position(Position(5, 3), 1)
        island43.set_bridges_count_according_to_directions_bridges()
        island53 = Island(Position(5, 3), 1)
        island53.set_bridge_to_position(Position(5, 4), 1)
        island53.set_bridges_count_according_to_directions_bridges()
        grid[Position(0, 1)] = island01
        grid[Position(1, 0)] = island10
        grid[Position(2, 3)] = island23
        grid[Position(2, 4)] = island24
        grid[Position(3, 1)] = island31
        grid[Position(3, 3)] = island33
        grid[Position(4, 3)] = island43
        grid[Position(5, 3)] = island53

        expected_solution_str = (
          ' ┌──────────────┐ \n'
          ' │  ┌───────────┘ \n'
          ' │  └───────────┐ \n'
          ' │  ┌─────┐  ┌──┘ \n'
          ' │  └──┐  │  └──┐ \n'
          ' └─────┘  └─────┘ '
        )

        game_solver = GrandTourSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

if __name__ == '__main__':
    unittest.main()
