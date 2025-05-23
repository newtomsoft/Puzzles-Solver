import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.KenKen.KenKenSolverOrTools import KenKenSolverOrTools


class KenKenSolverOrToolsTests(TestCase):
    def test_solution_grid_square(self):
        regions_operators_results = [
            ([Position(0, 0), Position(0, 1), Position(0, 2)], '+', 8),
            ([Position(1, 0), Position(1, 1), Position(1, 2)], '+', 4),
        ]
        with self.assertRaises(ValueError) as context:
            KenKenSolverOrTools(regions_operators_results)

        self.assertEqual("KenKen grid must be square", str(context.exception))

    def test_solution_3x3_add_sub_only(self):
        regions_operators_results = [
            ([Position(0, 0), Position(1, 0), Position(1, 1)], '+', 6),
            ([Position(0, 1), Position(0, 2), Position(1, 2), Position(2, 2)], '+', 7),
            ([Position(2, 1), Position(2, 2)], '-', 1),
        ]
        kenken_game = KenKenSolverOrTools(regions_operators_results)
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
        kenken_game = KenKenSolverOrTools(regions_operators_results)

        solution = kenken_game.get_solution()
        other_solution0 = kenken_game.get_other_solution()
        other_solution1 = kenken_game.get_other_solution()
        other_solution2 = kenken_game.get_other_solution()
        other_solution3 = kenken_game.get_other_solution()
        other_solution4 = kenken_game.get_other_solution()
        print(solution)
        print(other_solution0)
        print(other_solution1)
        print(other_solution2)
        print(other_solution3)
        print(other_solution4)
        # self.assertEqual(Grid.empty(), other_solution4)


if __name__ == '__main__':
    unittest.main()
