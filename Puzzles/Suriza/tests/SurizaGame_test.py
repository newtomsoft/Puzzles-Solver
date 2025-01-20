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


if __name__ == '__main__':
    unittest.main()
