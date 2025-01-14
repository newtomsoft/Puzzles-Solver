import unittest
from unittest import TestCase

from Puzzles.Shingoki.ShingokiGame import ShingokiGame
from Utils.Grid import Grid


class ShingokiGameTests(TestCase):
    def test_solution_white_horizontal_2(self):
        grid = Grid([
            [' ', 'w2', ' '],
            [' ', 'w2', ' '],
        ])

        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_horizontal_3_0(self):
        grid = Grid([
            [' ', 'w3', ' ', ' '],
            [' ', 'w3', ' ', ' '],
        ])

        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌────────┐ \n'
            ' └────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_horizontal_3_1(self):
        grid = Grid([
            [' ', ' ', 'w3', ' '],
            [' ', 'w3', ' ', ' '],
        ])

        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌────────┐ \n'
            ' └────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_vertical_2(self):
        grid = Grid([
            [' ', ' '],
            ['w2', 'w2'],
            [' ', ' '],
        ])

        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌──┐ \n'
            ' │  │ \n'
            ' └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_vertical_3_0(self):
        grid = Grid([
            [' ', ' '],
            ['w3', 'w3'],
            [' ', ' '],
            [' ', ' '],
        ])

        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌──┐ \n'
            ' │  │ \n'
            ' │  │ \n'
            ' └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_vertical_3_1(self):
        grid = Grid([
            [' ', ' '],
            ['w3', ' '],
            [' ', 'w3'],
            [' ', ' '],
        ])

        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌──┐ \n'
            ' │  │ \n'
            ' │  │ \n'
            ' └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_horizontal_vertical_0(self):
        grid = Grid([
            [' ', 'w2', ' '],
            ['w2', ' ', ' '],
            [' ', 'w2', ' ']
        ])

        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' │     │ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_horizontal_vertical_1(self):
        grid = Grid([
            [' ', 'w3', ' ', ' '],
            ['w3', ' ', ' ', 'w2'],
            [' ', ' ', ' ', ' '],
            [' ', 'w2', ' ', ' ']
        ])

        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌────────┐ \n'
            ' │        │ \n'
            ' │     ┌──┘ \n'
            ' └─────┘    '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_horizontal_vertical_2(self):
        grid = Grid([
            [' ', 'w3', ' ', ' '],
            ['w3', ' ', ' ', ' '],
            [' ', ' ', 'w2', ' '],
            [' ', 'w2', ' ', ' ']
        ])

        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌────────┐ \n'
            ' │     ┌──┘ \n'
            ' │     │    \n'
            ' └─────┘    '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
