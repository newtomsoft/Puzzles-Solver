import unittest
from unittest import TestCase

from Puzzles.Suriza.SurizaGame import SurizaGame
from Utils.Grid import Grid


class SurizaGameTests(TestCase):
    def test_solution_with_013_0(self):
        grid = Grid([
            [1, ' '],
            [3, ' '],
            [' ', 3],
            [0, ' '],
        ])
        game = SurizaGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            '         \n'
            ' ┌─────┐ \n'
            ' └──┐  │ \n'
            '    └──┘ \n'
            '         '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_with_013_1(self):
        grid = Grid([
            [0, ' '],
            [' ', 3],
            [3, ' '],
            [1, ' '],
        ])
        game = SurizaGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            '         \n'
            '    ┌──┐ \n'
            ' ┌──┘  │ \n'
            ' └─────┘ \n'
            '         '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_with_2(self):
        grid = Grid([
            [2, 2],
            [2, 2]
        ])
        game = SurizaGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' │     │ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6(self):
        grid = Grid([
            [' ', ' ', ' ', ' ', 2],
            [' ', ' ', ' ', 2, ' '],
            [' ', ' ', 3, 2, ' '],
            [' ', ' ', 0, ' ', ' '],
            [' ', 3, 3, ' ', 3]
        ])
        game = SurizaGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌──────────────┐ \n'
            ' │  ┌────────┐  │ \n'
            ' │  │  ┌──┐  └──┘ \n'
            ' │  └──┘  └─────┐ \n'
            ' │  ┌──┐  ┌──┐  │ \n'
            ' └──┘  └──┘  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8(self):
        grid = Grid([
            [' ', ' ', 3, ' ', ' ', 2, ' '],
            [2, 1, 3, ' ', 3, ' ', 3],
            [2, 2, ' ', 2, ' ', ' ', 3],
            [' ', ' ', ' ', ' ', ' ', ' ', 3],
            [' ', ' ', ' ', 2, 3, ' ', ' '],
            [2, ' ', 2, 1, 2, 2, ' '],
            [' ', 3, 3, ' ', 3, 2, 3]
        ])
        game = SurizaGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌────────┐     ┌─────┐ \n'
            ' │     ┌──┘  ┌──┘  ┌──┘ \n'
            ' └──┐  └──┐  └──┐  └──┐ \n'
            '    └──┐  └─────┘  ┌──┘ \n'
            ' ┌──┐  └──┐  ┌──┐  └──┐ \n'
            ' │  └─────┘  │  └──┐  │ \n'
            ' └──┐  ┌──┐  └──┐  │  │ \n'
            '    └──┘  └─────┘  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_11x11(self):
        grid = Grid([
            [' ', 2, 3, ' ', ' ', 1, ' ', 1, ' ', 3],
            [' ', 3, ' ', 2, ' ', 3, ' ', ' ', 3, ' '],
            [2, 1, 1, ' ', ' ', ' ', ' ', 2, ' ', ' '],
            [' ', 2, ' ', ' ', ' ', ' ', ' ', ' ', 1, 3],
            [' ', 1, ' ', 3, ' ', 3, 0, ' ', ' ', 3],
            [3, ' ', ' ', ' ', ' ', ' ', ' ', 2, ' ', ' '],
            [' ', 1, ' ', ' ', 1, 3, ' ', ' ', 3, ' '],
            [' ', 3, ' ', ' ', 2, 2, ' ', ' ', ' ', 3],
            [1, ' ', ' ', ' ', ' ', ' ', ' ', ' ', 3, 2],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', 2, ' ', ' ']
        ])
        game = SurizaGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌──┐  ┌──┐  ┌─────────────────┐ \n'
            ' │  │  │  │  └──┐  ┌──┐  ┌─────┘ \n'
            ' │  └──┘  └──┐  └──┘  │  └──┐    \n'
            ' └──┐  ┌──┐  └─────┐  └──┐  └──┐ \n'
            ' ┌──┘  │  └──┐  ┌──┘     │  ┌──┘ \n'
            ' └──┐  │  ┌──┘  └──┐  ┌──┘  └──┐ \n'
            ' ┌──┘  │  │     ┌──┘  │  ┌─────┘ \n'
            ' └──┐  │  └──┐  └──┐  │  └─────┐ \n'
            '    └──┘     └──┐  └──┘  ┌─────┘ \n'
            ' ┌──────────────┘  ┌──┐  └─────┐ \n'
            ' └─────────────────┘  └────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    @unittest.skip("This test is too slow (approx. 8 seconds)")
    def test_solution_16x16(self):
        grid = Grid([
            [' ', ' ', 2, 3, ' ', 2, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 2, ' ', 2, 2, 3, 3, 3, 2, ' ', ' ', 3, ' ', ' '],
            [' ', ' ', 2, ' ', 3, ' ', ' ', ' ', ' ', 1, ' ', ' ', 2, 2, 2],
            [3, ' ', 3, 2, ' ', 0, 2, ' ', ' ', 3, 2, 2, ' ', 1, ' '],
            [' ', 2, ' ', ' ', ' ', 3, ' ', ' ', 2, ' ', ' ', 1, 3, 2, ' '],
            [' ', ' ', 2, ' ', ' ', 2, ' ', 1, ' ', ' ', ' ', ' ', 2, ' ', ' '],
            [' ', ' ', ' ', ' ', 2, ' ', 3, ' ', 3, 1, 2, ' ', ' ', ' ', 1],
            [2, 1, ' ', 2, ' ', 1, ' ', ' ', 2, 3, 1, ' ', 1, 3, ' '],
            [3, 1, ' ', 1, 2, 2, 3, ' ', ' ', ' ', ' ', ' ', 3, ' ', ' '],
            [' ', ' ', ' ', ' ', 2, 3, 2, 1, ' ', ' ', ' ', ' ', ' ', 2, 2],
            [' ', ' ', 2, 3, ' ', ' ', 2, 2, ' ', 2, ' ', 2, ' ', 2, 1],
            [3, ' ', ' ', ' ', ' ', 2, ' ', 1, ' ', ' ', 2, 3, ' ', 3, ' '],
            [3, 0, ' ', 3, ' ', 2, ' ', 3, 3, 3, 2, ' ', ' ', ' ', 1],
            [3, 2, 2, 2, ' ', ' ', 3, ' ', ' ', ' ', ' ', 3, ' ', ' ', 2],
            [' ', ' ', ' ', ' ', 2, ' ', ' ', 3, ' ', 3, ' ', 2, 2, ' ', 3]
        ])
        game = SurizaGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌─────┐  ┌──┐  ┌──────────────┐  ┌───────────┐ \n'
            ' │  ┌──┘  │  │  │  ┌──┐  ┌──┐  │  │  ┌─────┐  │ \n'
            ' │  └─────┘  │  │  │  └──┘  │  └──┘  └──┐  └──┘ \n'
            ' └──┐  ┌──┐  └──┘  └─────┐  │  ┌─────┐  └─────┐ \n'
            ' ┌──┘  │  └─────┐  ┌──┐  │  └──┘     └──┐  ┌──┘ \n'
            ' │  ┌──┘  ┌──┐  └──┘  │  └──┐  ┌────────┘  └──┐ \n'
            ' │  │  ┌──┘  └─────┐  │  ┌──┘  └──┐  ┌────────┘ \n'
            ' └──┘  └──┐  ┌──┐  └──┘  └─────┐  └──┘  ┌──┐    \n'
            ' ┌────────┘  │  │  ┌──┐  ┌─────┘  ┌──┐  │  └──┐ \n'
            ' └──┐  ┌──┐  │  │  │  │  └─────┐  │  └──┘  ┌──┘ \n'
            ' ┌──┘  │  │  │  └──┘  │  ┌─────┘  └──┐  ┌──┘    \n'
            ' └──┐  │  └──┘     ┌──┘  └────────┐  │  │  ┌──┐ \n'
            ' ┌──┘  └─────┐  ┌──┘  ┌──┐  ┌──┐  └──┘  └──┘  │ \n'
            ' └──┐  ┌─────┘  │  ┌──┘  └──┘  └─────┐  ┌──┐  │ \n'
            ' ┌──┘  │  ┌─────┘  └─────┐  ┌────────┘  │  │  │ \n'
            ' └─────┘  └──────────────┘  └───────────┘  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
