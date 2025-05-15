import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Skyscrapers.SkyscrapersSolver import SkyscrapersSolver


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
        visible_skyscrapers = {'by_east': [1, 2, 2, 2, 0, 0, 0], 'by_west': [4, 1, 2, 3, 0, 0, 0], 'by_south': [3, 2, 1, 4, 0], 'by_north': [2, 2, 2, 1, 0]}
        with self.assertRaises(ValueError) as context:
            SkyscrapersSolver(grid, visible_skyscrapers)
        self.assertEqual(str(context.exception), "The grid must be square")

    def test_grid_must_be_at_least_4x4_raises_value_error(self):
        grid = Grid([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ])
        visible_skyscrapers = {'by_east': [1, 2, 2], 'by_west': [4, 1, 2], 'by_south': [3, 2, 1], 'by_north': [2, 2, 2]}
        with self.assertRaises(ValueError) as context:
            SkyscrapersSolver(grid, visible_skyscrapers)
        self.assertEqual(str(context.exception), "The grid must be at least 4x4")

    def test_viewable_by_east_skyscrapers_not_compliant(self):
        grid = Grid([
            [1, 2, 3, 4],
            [4, 1, 2, 3],
            [3, 4, 1, 2],
            [2, 3, 4, 1],
        ])
        visible_skyscrapers = {'by_east': [1, 2, 2], 'by_west': [4, 1, 2, 3], 'by_south': [3, 2, 1, 4], 'by_north': [2, 2, 2, 1]}
        with self.assertRaises(ValueError) as context:
            SkyscrapersSolver(grid, visible_skyscrapers)
        self.assertEqual(str(context.exception), "The 'by_east' viewable skyscrapers list must have the same length as the rows number")

    def test_viewable_by_west_skyscrapers_not_compliant(self):
        grid = Grid([
            [1, 2, 3, 4],
            [4, 1, 2, 3],
            [3, 4, 1, 2],
            [2, 3, 4, 1],
        ])
        visible_skyscrapers = {'by_east': [1, 2, 2, 2], 'by_west': [4, 1, 2], 'by_south': [3, 2, 1, 4], 'by_north': [2, 2, 2, 1]}
        with self.assertRaises(ValueError) as context:
            SkyscrapersSolver(grid, visible_skyscrapers)
        self.assertEqual(str(context.exception), "The 'by_west' viewable skyscrapers list must have the same length as the rows number")

    def test_viewable_by_north_skyscrapers_not_compliant(self):
        grid = Grid([
            [1, 2, 3, 4],
            [4, 1, 2, 3],
            [3, 4, 1, 2],
            [2, 3, 4, 1],
        ])
        visible_skyscrapers = {'by_east': [1, 2, 2, 2], 'by_west': [4, 1, 2, 3], 'by_south': [3, 2, 1, 4], 'by_north': [2, 2, 2]}
        with self.assertRaises(ValueError) as context:
            SkyscrapersSolver(grid, visible_skyscrapers)
        self.assertEqual(str(context.exception), "The 'by_north' viewable skyscrapers list must have the same length as the columns number")

    def test_viewable_by_south_skyscrapers_not_compliant(self):
        grid = Grid([
            [1, 2, 3, 4],
            [4, 1, 2, 3],
            [3, 4, 1, 2],
            [2, 3, 4, 1],
        ])
        visible_skyscrapers = {'by_east': [1, 2, 2, 2], 'by_west': [4, 1, 2, 3], 'by_south': [3, 2, 1], 'by_north': [2, 2, 2, 1]}
        with self.assertRaises(ValueError) as context:
            SkyscrapersSolver(grid, visible_skyscrapers)
        self.assertEqual(str(context.exception), "The 'by_south' viewable skyscrapers list must have the same length as the columns number")

    def test_solution_with_initials_levels_values(self):
        grid = Grid([
            [1, 2, 3, 5],
            [4, 1, 2, 3],
            [3, 4, 1, 2],
            [2, 3, 4, 1],
        ])
        visible_skyscrapers = {'by_east': [1, 2, 2, 2], 'by_west': [4, 1, 2, 3], 'by_south': [3, 2, 1, 4], 'by_north': [2, 2, 2, 1]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
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
        visible_skyscrapers = {'by_west': [0, 0, 0, 0], 'by_east': [0, 0, 0, 0], 'by_north': [0, 0, 0, 0], 'by_south': [0, 0, 0, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_with_2_visible_skyscrapers_when_1(self):
        grid = Grid([
            [4, 2, 1, 3],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        visible_skyscrapers = {'by_west': [2, 0, 0, 0], 'by_east': [0, 0, 0, 0], 'by_north': [0, 0, 0, 0], 'by_south': [0, 0, 0, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_4x4_with_2_visible_skyscrapers_when_4(self):
        grid = Grid([
            [1, 2, 3, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        visible_skyscrapers = {'by_west': [2, 0, 0, 0], 'by_east': [0, 0, 0, 0], 'by_north': [0, 0, 0, 0], 'by_south': [0, 0, 0, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_4x4_with_2_visible_skyscrapers_column(self):
        grid = Grid([
            [4, 0, 0, 0],
            [2, 0, 0, 0],
            [1, 0, 0, 0],
            [3, 0, 0, 0],
        ])
        visible_skyscrapers = {'by_west': [0, 0, 0, 0], 'by_east': [0, 0, 0, 0], 'by_north': [2, 0, 0, 0], 'by_south': [0, 0, 0, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_4x4_with_3_visible_skyscrapers(self):
        grid = Grid([
            [2, 1, 4, 3],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        visible_skyscrapers = {'by_west': [3, 0, 0, 0], 'by_east': [0, 0, 0, 0], 'by_north': [0, 0, 0, 0], 'by_south': [0, 0, 0, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_4x4_exist_with_3_visible_skyscrapers_2134(self):
        grid = Grid([
            [2, 1, 3, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        visible_skyscrapers = {'by_west': [3, 0, 0, 0], 'by_east': [0, 0, 0, 0], 'by_north': [0, 0, 0, 0], 'by_south': [0, 0, 0, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertNotEqual(Grid.empty(), solution)

    def test_solution_4x4_exist_with_3_visible_skyscrapers_1324(self):
        grid = Grid([
            [1, 3, 2, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        visible_skyscrapers = {'by_west': [3, 0, 0, 0], 'by_east': [0, 0, 0, 0], 'by_north': [0, 0, 0, 0], 'by_south': [0, 0, 0, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertNotEqual(Grid.empty(), solution)

    def test_solution_4x4_unique_with_4_visible_skyscrapers(self):
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
        visible_skyscrapers = {'by_west': [4, 0, 0, 0], 'by_east': [0, 0, 0, 0], 'by_north': [4, 0, 0, 0], 'by_south': [0, 0, 0, 4]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_unique_with_1_visible_skyscrapers(self):
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
        visible_skyscrapers = {'by_west': [0, 0, 0, 0], 'by_east': [0, 1, 0, 0], 'by_north': [0, 1, 0, 0], 'by_south': [0, 0, 0, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_unique_with_2_visible_skyscrapers(self):
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
        visible_skyscrapers = {'by_west': [0, 0, 2, 0], 'by_east': [0, 0, 0, 0], 'by_north': [0, 0, 0, 0], 'by_south': [0, 0, 0, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_unique_with_3_visible_skyscrapers(self):
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
        visible_skyscrapers = {'by_west': [0, 3, 0, 3], 'by_east': [0, 0, 0, 0], 'by_north': [0, 0, 0, 0], 'by_south': [0, 0, 3, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_unique_with_3_1_visible_skyscrapers(self):
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
        visible_skyscrapers = {'by_west': [0, 0, 3, 0], 'by_east': [0, 3, 0, 0], 'by_north': [0, 0, 0, 1], 'by_south': [0, 0, 0, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_with_3_visible_skyscrapers(self):
        grid = Grid([
            [2, 3, 4, 5, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ])
        visible_skyscrapers = {'by_west': [3, 0, 0, 0, 0], 'by_east': [0, 0, 0, 0, 0], 'by_north': [0, 0, 0, 0, 0], 'by_south': [0, 0, 0, 0, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_8x8_exist_with_3_visible_skyscrapers(self):
        grid = Grid([
            [2, 0, 0, 0, 0, 0, 7, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ])
        visible_skyscrapers = {'by_west': [3, 0, 0, 0, 0, 0, 0, 0], 'by_east': [0, 0, 0, 0, 0, 0, 0, 0], 'by_north': [0, 0, 0, 0, 0, 0, 0, 0], 'by_south': [0, 0, 0, 0, 0, 0, 0, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertNotEqual(Grid.empty(), solution)

    def test_solution_4x4_1(self):
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
        visible_skyscrapers = {'by_west': [0, 0, 0, 0], 'by_east': [0, 0, 0, 2], 'by_north': [3, 0, 0, 2], 'by_south': [2, 0, 3, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_2(self):
        grid = Grid([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [2, 4, 1, 3],
            [1, 3, 4, 2],
            [3, 1, 2, 4],
            [4, 2, 3, 1],
        ])
        visible_skyscrapers = {'by_west': [0, 0, 2, 0], 'by_east': [0, 2, 0, 0], 'by_north': [0, 1, 0, 0], 'by_south': [0, 3, 2, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_3(self):
        grid = Grid([
            [0, 2, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [3, 2, 4, 1],
            [2, 3, 1, 4],
            [1, 4, 2, 3],
            [4, 1, 3, 2],
        ])
        visible_skyscrapers = {'by_west': [0, 0, 0, 0], 'by_east': [0, 0, 0, 0], 'by_north': [2, 0, 0, 0], 'by_south': [0, 2, 0, 3]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_4(self):
        grid = Grid([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [3, 2, 1, 4],
            [1, 4, 3, 2],
            [4, 3, 2, 1],
            [2, 1, 4, 3],
        ])
        visible_skyscrapers = {'by_west': [0, 0, 0, 0], 'by_east': [0, 0, 4, 0], 'by_north': [2, 2, 0, 0], 'by_south': [0, 0, 1, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_with_visible_skyscrapers_3(self):
        grid = Grid([
            [2, 1, 5, 3, 4],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ])
        visible_skyscrapers = {'by_west': [3, 0, 0, 0, 0], 'by_east': [0, 0, 0, 0, 0], 'by_north': [0, 0, 0, 0, 0], 'by_south': [0, 0, 0, 0, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_5x5_1(self):
        grid = Grid([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [4, 1, 5, 3, 2],
            [3, 5, 4, 2, 1],
            [2, 4, 1, 5, 3],
            [5, 3, 2, 1, 4],
            [1, 2, 3, 4, 5],
        ])
        visible_skyscrapers = {'by_west': [2, 2, 3, 1, 5], 'by_east': [3, 4, 2, 2, 1], 'by_north': [2, 2, 1, 2, 4], 'by_south': [2, 4, 3, 2, 1]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_2(self):
        grid = Grid([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [5, 3, 1, 4, 2],
            [2, 4, 3, 5, 1],
            [1, 5, 4, 2, 3],
            [3, 2, 5, 1, 4],
            [4, 1, 2, 3, 5],
        ])
        visible_skyscrapers = {'by_west': [1, 0, 0, 2, 0], 'by_east': [3, 2, 3, 0, 0], 'by_north': [0, 0, 0, 0, 4], 'by_south': [2, 3, 2, 0, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_3(self):
        grid = Grid([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [5, 4, 3, 2, 1],
            [2, 5, 1, 4, 3],
            [1, 2, 4, 3, 5],
            [4, 3, 5, 1, 2],
            [3, 1, 2, 5, 4],
        ])
        visible_skyscrapers = {'by_west': [0, 0, 4, 2, 0], 'by_east': [5, 3, 0, 2, 0], 'by_north': [0, 0, 0, 0, 0], 'by_south': [3, 0, 2, 0, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_4(self):
        grid = Grid([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [5, 2, 4, 1, 3],
            [3, 5, 1, 2, 4],
            [1, 4, 5, 3, 2],
            [2, 1, 3, 4, 5],
            [4, 3, 2, 5, 1],
        ])
        visible_skyscrapers = {'by_west': [1, 0, 3, 4, 0], 'by_east': [0, 0, 0, 0, 0], 'by_north': [0, 0, 2, 5, 0], 'by_south': [2, 3, 0, 0, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_1(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [6, 4, 1, 2, 5, 3],
            [1, 2, 3, 5, 4, 6],
            [5, 3, 6, 1, 2, 4],
            [2, 6, 5, 4, 3, 1],
            [4, 1, 2, 3, 6, 5],
            [3, 5, 4, 6, 1, 2],
        ])
        visible_skyscrapers = {'by_west': [1, 5, 2, 2, 2, 3], 'by_east': [3, 1, 2, 5, 2, 2], 'by_north': [1, 2, 3, 3, 2, 2], 'by_south': [4, 2, 3, 1, 2, 3]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_2(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 0],
            [0, 0, 0, 0, 3, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [6, 3, 1, 5, 2, 4],
            [3, 6, 2, 4, 1, 5],
            [2, 5, 4, 1, 6, 3],
            [5, 1, 3, 2, 4, 6],
            [4, 2, 5, 6, 3, 1],
            [1, 4, 6, 3, 5, 2],
        ])
        visible_skyscrapers = {'by_west': [1, 2, 0, 2, 0, 0], 'by_east': [3, 0, 0, 1, 3, 0], 'by_north': [0, 0, 5, 2, 2, 0], 'by_south': [0, 3, 0, 0, 0, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_3(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [1, 3, 2, 5, 4, 6],
            [4, 1, 6, 3, 5, 2],
            [6, 2, 3, 4, 1, 5],
            [2, 4, 5, 6, 3, 1],
            [3, 5, 1, 2, 6, 4],
            [5, 6, 4, 1, 2, 3],
        ])
        visible_skyscrapers = {'by_west': [4, 2, 0, 4, 0, 0], 'by_east': [0, 3, 0, 3, 2, 3], 'by_north': [0, 4, 0, 2, 3, 0], 'by_south': [0, 0, 3, 3, 0, 4]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_7x7_1(self):
        grid = Grid([
            [0, 0, 0, 0, 2, 0, 0],
            [0, 0, 4, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0],
            [0, 0, 6, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 5, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [5, 4, 1, 7, 2, 3, 6],
            [6, 7, 4, 3, 5, 1, 2],
            [1, 6, 5, 2, 7, 4, 3],
            [2, 3, 6, 4, 1, 7, 5],
            [3, 1, 2, 6, 4, 5, 7],
            [7, 5, 3, 1, 6, 2, 4],
            [4, 2, 7, 5, 3, 6, 1],
        ])
        visible_skyscrapers = {'by_west': [2, 0, 3, 0, 3, 0, 0], 'by_east': [2, 3, 3, 0, 0, 3, 0], 'by_north': [0, 2, 0, 0, 0, 3, 0], 'by_south': [0, 0, 1, 0, 0, 2, 3]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_1(self):
        grid = Grid([
            [0, 0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 4, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 8, 0, 5],
            [2, 0, 0, 6, 0, 0, 0, 0],
            [0, 0, 0, 3, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [5, 4, 7, 8, 3, 6, 1, 2],
            [6, 8, 2, 5, 4, 7, 3, 1],
            [1, 6, 5, 7, 2, 3, 8, 4],
            [8, 2, 1, 4, 7, 5, 6, 3],
            [7, 3, 4, 1, 6, 8, 2, 5],
            [2, 5, 3, 6, 1, 4, 7, 8],
            [4, 1, 6, 3, 8, 2, 5, 7],
            [3, 7, 8, 2, 5, 1, 4, 6],
        ])
        visible_skyscrapers = {'by_west': [3, 0, 4, 0, 0, 5, 3, 3], 'by_east': [0, 4, 0, 4, 0, 0, 2, 2], 'by_north': [3, 0, 2, 0, 0, 0, 3, 4], 'by_south': [4, 2, 0, 5, 2, 4, 0, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_9x9_1(self):
        grid = Grid([
            [4, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 6, 0, 0, 4, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 0, 3, 0, 2, 0],
            [0, 5, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 4, 0, 2, 0, 0, 0, 0],
            [0, 0, 5, 0, 7, 4, 0, 0, 0],
            [0, 0, 0, 3, 0, 5, 0, 0, 0],
            [0, 0, 2, 0, 0, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [4, 2, 8, 1, 3, 6, 5, 7, 9],
            [5, 7, 1, 8, 6, 2, 9, 4, 3],
            [2, 9, 3, 5, 8, 7, 4, 1, 6],
            [9, 1, 6, 4, 5, 3, 8, 2, 7],
            [6, 5, 7, 2, 9, 8, 1, 3, 4],
            [8, 3, 4, 6, 2, 9, 7, 5, 1],
            [1, 6, 5, 9, 7, 4, 3, 8, 2],
            [7, 4, 9, 3, 1, 5, 2, 6, 8],
            [3, 8, 2, 7, 4, 1, 6, 9, 5]
        ])
        visible_skyscrapers = {'by_west': [0, 4, 0, 1, 3, 0, 3, 0, 0], 'by_east': [0, 3, 4, 3, 3, 0, 3, 0, 0], 'by_north': [3, 0, 2, 0, 4, 4, 0, 3, 0], 'by_south': [4, 2, 2, 0, 3, 3, 4, 0, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    @unittest.skip("This puzzle have multiple solutions")
    def test_solution_6x6_multiple(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [4, 3, 2, 1, 5, 6],
            [6, 1, 3, 5, 2, 4],
            [5, 2, 6, 4, 1, 3],
            [2, 6, 1, 3, 4, 5],
            [1, 5, 4, 6, 3, 2],
            [3, 4, 5, 2, 6, 1],
        ])
        visible_skyscrapers = {'by_west': [3, 1, 0, 0, 3, 4], 'by_east': [0, 0, 3, 0, 3, 0], 'by_north': [0, 0, 3, 0, 0, 0], 'by_south': [3, 3, 0, 0, 0, 4]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    @unittest.skip("This puzzle have multiple solutions")
    def test_solution_6x6_multiple_2(self):
        grid = Grid([
            [0, 0, 0, 6, 5, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [1, 4, 3, 6, 5, 2],
            [4, 6, 2, 5, 1, 3],
            [6, 5, 4, 2, 3, 1],
            [2, 1, 5, 3, 6, 4],
            [3, 2, 6, 1, 4, 5],
            [5, 3, 1, 4, 2, 6],
        ])
        visible_skyscrapers = {'by_west': [3, 0, 0, 0, 0, 0], 'by_east': [0, 0, 0, 0, 0, 0], 'by_north': [0, 0, 0, 0, 0, 0], 'by_south': [0, 0, 0, 0, 0, 0]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
