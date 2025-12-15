import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.KenKen.KenKenSolver import KenKenSolver


class KenKenSolverTests(TestCase):
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
        regions_grid = Grid([
            [1, 3, 3],
            [2, 2, 3],
            [5, 4, 4]
        ])
        operations_grid = Grid([
            ['2', '6+', None],
            ['2-', None, None],
            ['3', '1-', None]
        ])

        kenken_game = KenKenSolver(regions_grid, operations_grid)
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
        # R1: (0,0), (1,0) -> 4x. ID 1
        # R2: (0,1), (0,2) -> 7+. ID 2
        # R3: (0,3), (1,3) -> 2÷. ID 3
        # R4: (1,1), (1,2) -> 6x. ID 4
        # R5: (2,0), (2,1) -> 1-. ID 5
        # R6: (2,2), (3,2) -> 5+. ID 6
        # R7: (2,3), (3,3) -> 1-. ID 7
        # R8: (3,0), (3,1) -> 2÷. ID 8

        regions_grid = Grid([
            [1, 2, 2, 3],
            [1, 4, 4, 3],
            [5, 5, 6, 7],
            [8, 8, 6, 7]
        ])

        operations_grid = Grid([
            ['4x', '7+', None, '2÷'],
            [None, '6x', None, None],
            ['1-', None, '5+', '1-'],
            ['2÷', None, None, None]
        ])

        expected_solution = Grid([
            [1, 4, 3, 2],
            [4, 3, 2, 1],
            [3, 2, 1, 4],
            [2, 1, 4, 3],
        ])
        kenken_game = KenKenSolver(regions_grid, operations_grid)

        solution = kenken_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = kenken_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_hard(self):
        # R1: (0,0), (1,0) -> 1-. ID 1
        # R2: (0,1), (0,2), (0,3), (1,2), (1,3) -> 11+. ID 2
        # R3: (1,1), (2,1) -> 2÷. ID 3
        # R4: (2,0), (3,0), (3,1) -> 6x. ID 4
        # R5: (2,2), (3,2) -> 2-. ID 5
        # R6: (2,3), (3,3) -> 2÷. ID 6

        regions_grid = Grid([
            [1, 2, 2, 2],
            [1, 3, 2, 2],
            [4, 3, 5, 6],
            [4, 4, 5, 6]
        ])

        operations_grid = Grid([
            ['1-', '11+', None, None],
            [None, '2÷', None, None],
            ['6x', None, '2-', '2÷'],
            [None, None, None, None]
        ])

        expected_solution = Grid([
            [4, 1, 2, 3],
            [3, 2, 4, 1],
            [1, 4, 3, 2],
            [2, 3, 1, 4],
        ])
        kenken_game = KenKenSolver(regions_grid, operations_grid)

        solution = kenken_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = kenken_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_hard(self):
        # 6x6 actually
        # regions_operators_results = [
        #     ([Position(1, 0), Position(0, 0)], '-', 2),
        #     ([Position(0, 1), Position(1, 1)], '+', 8),
        #     ([Position(0, 2), Position(1, 2)], '÷', 3),
        #     ([Position(0, 3), Position(0, 4), Position(0, 5)], '+', 11),
        #     ([Position(2, 3), Position(1, 3)], 'x', 6),
        #     ([Position(1, 4), Position(1, 5)], '-', 4),
        #     ([Position(2, 0), Position(3, 0)], '-', 4),
        #     ([Position(3, 1), Position(2, 1)], '÷', 3),
        #     ([Position(3, 2), Position(3, 3), Position(4, 2), Position(2, 2)], 'x', 120),
        #     ([Position(2, 4), Position(2, 5)], '+', 8),
        #     ([Position(3, 4), Position(3, 5)], '-', 3),
        #     ([Position(4, 0), Position(5, 0)], 'x', 6),
        #     ([Position(4, 1), Position(5, 1), Position(5, 2)], 'x', 24),
        #     ([Position(5, 3), Position(4, 3)], 'x', 10),
        #     ([Position(4, 4), Position(5, 4)], '-', 1),
        #     ([Position(4, 5), Position(5, 5)], '+', 7)
        # ]

        regions_grid = Grid([
            [1, 2, 3, 4, 4, 4],
            [1, 2, 3, 5, 6, 6],
            [7, 8, 9, 5, 10, 10],
            [7, 8, 9, 9, 11, 11],
            [12, 13, 9, 14, 15, 16],
            [12, 13, 13, 14, 15, 16]
        ])

        operations_grid = Grid([
            ['2-', '8+', '3÷', '11+', None, None],
            [None, None, None, '6x', '4-', None],
            ['4-', '3÷', '120x', None, '8+', None],
            [None, None, None, None, '3-', None],
            ['6x', '24x', None, '10x', '1-', '7+'],
            [None, None, None, None, None, None]
        ])

        expected_solution = Grid([
            [6, 3, 1, 4, 2, 5],
            [4, 5, 3, 1, 6, 2],
            [1, 2, 4, 6, 5, 3],
            [5, 6, 2, 3, 1, 4],
            [3, 1, 5, 2, 4, 6],
            [2, 4, 6, 5, 3, 1]
        ])
        kenken_game = KenKenSolver(regions_grid, operations_grid)

        solution = kenken_game.get_solution()
        self.assertEqual(expected_solution, solution)


if __name__ == '__main__':
    unittest.main()
