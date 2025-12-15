import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.KenKen.KenKenSolver import KenKenSolver


class KenKenSolverTests(TestCase):
    def _create_solver_from_data(self, regions_operators_results):
        # Determine grid size
        all_positions = [pos for sublist, _, _ in regions_operators_results for pos in sublist]
        max_r = max(pos.r for pos in all_positions)
        max_c = max(pos.c for pos in all_positions)
        rows = max_r + 1
        cols = max_c + 1

        # Use square grid based on max dimension
        size = max(rows, cols)

        regions_grid_data = [[0] * size for _ in range(size)]
        operations_grid_data = [[None] * size for _ in range(size)]

        for idx, (positions, op, res) in enumerate(regions_operators_results):
            # Find top left
            top_left = sorted(positions, key=lambda p: (p.r, p.c))[0]

            # Construct op string
            op_str = f"{res}{op}"
            if op is None or op == '':
                op_str = f"{res}"

            operations_grid_data[top_left.r][top_left.c] = op_str

            for pos in positions:
                regions_grid_data[pos.r][pos.c] = idx + 1 # region id

        return KenKenSolver(Grid(regions_grid_data), Grid(operations_grid_data))

    def test_solution_grid_square_check(self):
        # We simulate the check by passing invalid grids
        # Valid regions but invalid size match with ops
        regions = Grid([[1, 2], [3, 4]]) # 2x2
        ops = Grid([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) # 3x3

        with self.assertRaisesRegex(ValueError, "Regions grid and operations grid must have the same dimensions"):
            KenKenSolver(regions, ops)

        # Non-square check
        regions_nonsquare = Grid([[1, 2, 3], [4, 5, 6]])
        ops_nonsquare = Grid([[1, 2, 3], [4, 5, 6]])
        with self.assertRaisesRegex(ValueError, "KenKen grid must be square"):
            KenKenSolver(regions_nonsquare, ops_nonsquare)

    def test_solution_3x3_add_sub_only(self):
        # Modified to be a valid partition with a unique solution matching the expected one.
        # R1: (0,0) -> 2
        # R2: (1,0), (1,1) -> -2
        # R3: (0,1), (0,2), (1,2) -> +6
        # R4: (2,1), (2,2) -> -1
        # R5: (2,0) -> 3

        regions_operators_results = [
            ([Position(0, 0)], '', 2),
            ([Position(1, 0), Position(1, 1)], '-', 2),
            ([Position(0, 1), Position(0, 2), Position(1, 2)], '+', 6),
            ([Position(2, 1), Position(2, 2)], '-', 1),
            ([Position(2, 0)], '', 3)
        ]

        kenken_game = self._create_solver_from_data(regions_operators_results)
        solution = kenken_game.get_solution()
        expected_solution = Grid([
            [2, 1, 3],
            [1, 3, 2],
            [3, 2, 1],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = kenken_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4(self):
        regions_operators_results = [
            ([Position(0, 0), Position(1, 0)], 'x', 4),
            ([Position(0, 1), Position(0, 2)], '+', 7),
            ([Position(0, 3), Position(1, 3)], '÷', 2),
            ([Position(1, 1), Position(1, 2)], 'x', 6),
            ([Position(2, 0), Position(2, 1)], '-', 1),
            ([Position(2, 2), Position(3, 2)], '+', 5),
            ([Position(2, 3), Position(3, 3)], '-', 1),
            ([Position(3, 0), Position(3, 1)], '÷', 2),
        ]
        expected_solution = Grid([
            [1, 4, 3, 2],
            [4, 3, 2, 1],
            [3, 2, 1, 4],
            [2, 1, 4, 3],
        ])
        kenken_game = self._create_solver_from_data(regions_operators_results)

        solution = kenken_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = kenken_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_hard(self):
        regions_operators_results = [
            ([Position(0, 0), Position(1, 0)], '-', 1),
            ([Position(0, 1), Position(0, 2), Position(0, 3), Position(1, 2), Position(1, 3)], '+', 11),
            ([Position(1, 1), Position(2, 1)], '÷', 2),
            ([Position(2, 0), Position(3, 0), Position(3, 1)], 'x', 6),
            ([Position(2, 2), Position(3, 2)], '-', 2),
            ([Position(2, 3), Position(3, 3)], '÷', 2),
        ]
        expected_solution = Grid([
            [4, 1, 2, 3],
            [3, 2, 4, 1],
            [1, 4, 3, 2],
            [2, 3, 1, 4],
        ])
        kenken_game = self._create_solver_from_data(regions_operators_results)

        solution = kenken_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = kenken_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_hard(self):
        regions_operators_results = [
            ([Position(1, 0), Position(0, 0)], '-', 2),
            ([Position(0, 1), Position(1, 1)], '+', 8),
            ([Position(0, 2), Position(1, 2)], '÷', 3),
            ([Position(0, 3), Position(0, 4), Position(0, 5)], '+', 11),
            ([Position(2, 3), Position(1, 3)], 'x', 6),
            ([Position(1, 4), Position(1, 5)], '-', 4),
            ([Position(2, 0), Position(3, 0)], '-', 4),
            ([Position(3, 1), Position(2, 1)], '÷', 3),
            ([Position(3, 2), Position(3, 3), Position(4, 2), Position(2, 2)], 'x', 120),
            ([Position(2, 4), Position(2, 5)], '+', 8),
            ([Position(3, 4), Position(3, 5)], '-', 3), ([Position(4, 0), Position(5, 0)], 'x', 6),
            ([Position(4, 1), Position(5, 1), Position(5, 2)], 'x', 24),
            ([Position(5, 3), Position(4, 3)], 'x', 10),
            ([Position(4, 4), Position(5, 4)], '-', 1), ([Position(4, 5), Position(5, 5)], '+', 7)
        ]
        expected_solution = Grid([
            [6, 3, 1, 4, 2, 5],
            [4, 5, 3, 1, 6, 2],
            [1, 2, 4, 6, 5, 3],
            [5, 6, 2, 3, 1, 4],
            [3, 1, 5, 2, 4, 6],
            [2, 4, 6, 5, 3, 1]
        ])
        kenken_game = self._create_solver_from_data(regions_operators_results)

        solution = kenken_game.get_solution()
        self.assertEqual(expected_solution, solution)


if __name__ == '__main__':
    unittest.main()
