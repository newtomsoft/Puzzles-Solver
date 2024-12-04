import unittest
from unittest import TestCase

from Puzzles.Skyscrapers.SkyscrapersGame import SkyscrapersGame
from Utils.Grid import Grid


class SkyscrapersGameTests(TestCase):
    def test_grid_must_be_square_raises_value_error(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        viewable_skyscrapers = {'by_east': [1, 2, 2, 2, 0, 0, 0], 'by_west': [4, 1, 2, 3, 0, 0, 0], 'by_south': [3, 2, 1, 4, 0], 'by_north': [2, 2, 2, 1, 0]}
        with self.assertRaises(ValueError) as context:
            SkyscrapersGame((grid, viewable_skyscrapers))
        self.assertEqual(str(context.exception), "The grid must be square")

    def test_grid_must_be_at_least_4x4_raises_value_error(self):
        grid = Grid([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ])
        viewable_skyscrapers = {'by_east': [1, 2, 2], 'by_west': [4, 1, 2], 'by_south': [3, 2, 1], 'by_north': [2, 2, 2]}
        with self.assertRaises(ValueError) as context:
            SkyscrapersGame((grid, viewable_skyscrapers))
        self.assertEqual(str(context.exception), "The grid must be at least 4x4")

    def test_viewable_by_east_skyscrapers_not_compliant(self):
        grid = Grid([
            [1, 2, 3, 4],
            [4, 1, 2, 3],
            [3, 4, 1, 2],
            [2, 3, 4, 1],
        ])
        viewable_skyscrapers = {'by_east': [1, 2, 2], 'by_west': [4, 1, 2, 3], 'by_south': [3, 2, 1, 4], 'by_north': [2, 2, 2, 1]}
        with self.assertRaises(ValueError) as context:
            SkyscrapersGame((grid, viewable_skyscrapers))
        self.assertEqual(str(context.exception), "The 'by_east' viewable skyscrapers list must have the same length as the rows number")

    def test_viewable_by_west_skyscrapers_not_compliant(self):
        grid = Grid([
            [1, 2, 3, 4],
            [4, 1, 2, 3],
            [3, 4, 1, 2],
            [2, 3, 4, 1],
        ])
        viewable_skyscrapers = {'by_east': [1, 2, 2, 2], 'by_west': [4, 1, 2], 'by_south': [3, 2, 1, 4], 'by_north': [2, 2, 2, 1]}
        with self.assertRaises(ValueError) as context:
            SkyscrapersGame((grid, viewable_skyscrapers))
        self.assertEqual(str(context.exception), "The 'by_west' viewable skyscrapers list must have the same length as the rows number")

    def test_viewable_by_north_skyscrapers_not_compliant(self):
        grid = Grid([
            [1, 2, 3, 4],
            [4, 1, 2, 3],
            [3, 4, 1, 2],
            [2, 3, 4, 1],
        ])
        viewable_skyscrapers = {'by_east': [1, 2, 2, 2], 'by_west': [4, 1, 2, 3], 'by_south': [3, 2, 1, 4], 'by_north': [2, 2, 2]}
        with self.assertRaises(ValueError) as context:
            SkyscrapersGame((grid, viewable_skyscrapers))
        self.assertEqual(str(context.exception), "The 'by_north' viewable skyscrapers list must have the same length as the columns number")

    def test_viewable_by_south_skyscrapers_not_compliant(self):
        grid = Grid([
            [1, 2, 3, 4],
            [4, 1, 2, 3],
            [3, 4, 1, 2],
            [2, 3, 4, 1],
        ])
        viewable_skyscrapers = {'by_east': [1, 2, 2, 2], 'by_west': [4, 1, 2, 3], 'by_south': [3, 2, 1], 'by_north': [2, 2, 2, 1]}
        with self.assertRaises(ValueError) as context:
            SkyscrapersGame((grid, viewable_skyscrapers))
        self.assertEqual(str(context.exception), "The 'by_south' viewable skyscrapers list must have the same length as the columns number")

    def test_solution_with_initials_levels_values(self):
        grid = Grid([
            [1, 2, 3, 5],
            [4, 1, 2, 3],
            [3, 4, 1, 2],
            [2, 3, 4, 1],
        ])
        viewable_skyscrapers = {'by_east': [1, 2, 2, 2], 'by_west': [4, 1, 2, 3], 'by_south': [3, 2, 1, 4], 'by_north': [2, 2, 2, 1]}
        skyscrapers_game = SkyscrapersGame((grid, viewable_skyscrapers))
        solution = skyscrapers_game.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_with_distinct_constraints(self):
        grid = Grid([
            [1, 2, 3, 0],
            [0, 1, 2, 0],
            [0, 0, 1, 2],
            [0, 0, 0, 1],
        ])
        expected_solution = Grid([
            [1, 2, 3, 4],
            [4, 1, 2, 3],
            [3, 4, 1, 2],
            [2, 3, 4, 1],
        ])
        viewable_skyscrapers = {'by_west': [0, 0, 0, 0], 'by_east': [0, 0, 0, 0], 'by_north': [0, 0, 0, 0], 'by_south': [0, 0, 0, 0]}
        skyscrapers_game = SkyscrapersGame((grid, viewable_skyscrapers))
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_with_viewable_skyscrapers_contraint_4(self):
        grid = Grid([
            [0, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [1, 2, 3, 4],
            [2, 1, 4, 3],
            [3, 4, 1, 2],
            [4, 3, 2, 1],
        ])
        viewable_skyscrapers = {'by_west': [4, 0, 0, 0], 'by_east': [0, 0, 0, 0], 'by_north': [4, 0, 0, 0], 'by_south': [0, 0, 0, 4]}
        skyscrapers_game = SkyscrapersGame((grid, viewable_skyscrapers))
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_with_viewable_skyscrapers_contraint_1(self):
        grid = Grid([
            [0, 0, 0, 0],
            [0, 2, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [3, 4, 2, 1],
            [1, 2, 3, 4],
            [4, 3, 1, 2],
            [2, 1, 4, 3],
        ])
        viewable_skyscrapers = {'by_west': [0, 0, 0, 0], 'by_east': [0, 1, 0, 0], 'by_north': [0, 1, 0, 0], 'by_south': [0, 0, 0, 0]}
        skyscrapers_game = SkyscrapersGame((grid, viewable_skyscrapers))
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_with_viewable_skyscrapers_3(self):
        grid = Grid([
            [0, 0, 0, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [3, 4, 2, 1],
            [1, 2, 4, 3],
            [4, 1, 3, 2],
            [2, 3, 1, 4],
        ])
        viewable_skyscrapers = {'by_west': [0, 3, 0, 3], 'by_east': [0, 0, 0, 0], 'by_north': [0, 0, 0, 0], 'by_south': [0, 0, 3, 0]}
        skyscrapers_game = SkyscrapersGame((grid, viewable_skyscrapers))
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_with_viewable_skyscrapers_3_and1(self):
        grid = Grid([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 1, 0, 0],
        ])
        expected_solution = Grid([
            [3, 2, 1, 4],
            [1, 4, 3, 2],
            [2, 3, 4, 1],
            [4, 1, 2, 3],
        ])
        viewable_skyscrapers = {'by_west': [0, 0, 3, 0], 'by_east': [0, 3, 0, 0], 'by_north': [0, 0, 0, 1], 'by_south': [0, 0, 0, 0]}
        skyscrapers_game = SkyscrapersGame((grid, viewable_skyscrapers))
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_with_viewable_skyscrapers_2(self):
        grid = Grid([
            [0, 3, 0, 0],
            [2, 0, 0, 0],
            [0, 0, 3, 2],
            [3, 0, 0, 0],
        ])
        expected_solution = Grid([
            [4, 3, 2, 1],
            [2, 1, 4, 3],
            [1, 4, 3, 2],
            [3, 2, 1, 4],
        ])
        viewable_skyscrapers = {'by_west': [0, 0, 2, 0], 'by_east': [0, 0, 0, 0], 'by_north': [0, 0, 0, 0], 'by_south': [0, 0, 0, 0]}
        skyscrapers_game = SkyscrapersGame((grid, viewable_skyscrapers))
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_with_viewable_skyscrapers_2_old(self):
        grid = Grid([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [3, 4, 1, 2],
            [1, 2, 4, 3],
            [4, 3, 2, 1],
            [2, 1, 3, 4],
        ])
        viewable_skyscrapers = {'by_west': [0, 3, 0, 0], 'by_east': [0, 0, 4, 0], 'by_north': [0, 0, 0, 0], 'by_south': [0, 0, 2, 0]}
        skyscrapers_game = SkyscrapersGame((grid, viewable_skyscrapers))
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4(self):
        grid = Grid([
            [1, 0, 0, 2],
            [0, 0, 0, 4],
            [0, 0, 0, 1],
            [0, 4, 1, 3],
        ])
        expected_solution = Grid([
            [1, 3, 4, 2],
            [3, 1, 2, 4],
            [4, 2, 3, 1],
            [2, 4, 1, 3],
        ])
        viewable_skyscrapers = {'by_west': [0, 0, 0, 0], 'by_east': [0, 0, 0, 2], 'by_north': [3, 0, 0, 2], 'by_south': [2, 0, 3, 0]}
        skyscrapers_game = SkyscrapersGame((grid, viewable_skyscrapers))
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
