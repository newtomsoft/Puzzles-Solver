import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Skyscrapers.SkyscrapersSolver import SkyscrapersSolver

_ = 0


class SkyscrapersGameTests(TestCase):
    def test_grid_must_be_square_raises_value_error(self):
        grid = Grid([
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
        ])
        visible_skyscrapers = {'by_east': [1, 2, 2, 2, _, _, _], 'by_west': [4, 1, 2, 3, _, _, _], 'by_south': [3, 2, 1, 4, _], 'by_north': [2, 2, 2, 1, _]}
        with self.assertRaises(ValueError) as context:
            SkyscrapersSolver(grid, visible_skyscrapers)
        self.assertEqual(str(context.exception), "The grid must be square")

    def test_grid_must_be_at_least_4x4_raises_value_error(self):
        grid = Grid([
            [_, _, _],
            [_, _, _],
            [_, _, _],
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
            [1, 2, 3, _],
            [_, 1, 2, _],
            [_, _, 1, 2],
            [_, _, _, 1],
        ])
        expected_solution = Grid([
            [1, 2, 3, 4],
            [4, 1, 2, 3],
            [3, 4, 1, 2],
            [2, 3, 4, 1],
        ])
        visible_skyscrapers = {'by_west': [_, _, _, _], 'by_east': [_, _, _, _], 'by_north': [_, _, _, _], 'by_south': [_, _, _, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_with_2_visible_skyscrapers_when_1(self):
        grid = Grid([
            [4, 2, 1, 3],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        visible_skyscrapers = {'by_west': [2, _, _, _], 'by_east': [_, _, _, _], 'by_north': [_, _, _, _], 'by_south': [_, _, _, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_4x4_with_2_visible_skyscrapers_when_4(self):
        grid = Grid([
            [1, 2, 3, 4],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        visible_skyscrapers = {'by_west': [2, _, _, _], 'by_east': [_, _, _, _], 'by_north': [_, _, _, _], 'by_south': [_, _, _, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_4x4_with_2_visible_skyscrapers_column(self):
        grid = Grid([
            [4, _, _, _],
            [2, _, _, _],
            [1, _, _, _],
            [3, _, _, _],
        ])
        visible_skyscrapers = {'by_west': [_, _, _, _], 'by_east': [_, _, _, _], 'by_north': [2, _, _, _], 'by_south': [_, _, _, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_4x4_with_3_visible_skyscrapers(self):
        grid = Grid([
            [2, 1, 4, 3],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        visible_skyscrapers = {'by_west': [3, _, _, _], 'by_east': [_, _, _, _], 'by_north': [_, _, _, _], 'by_south': [_, _, _, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_4x4_exist_with_3_visible_skyscrapers_2134(self):
        grid = Grid([
            [2, 1, 3, 4],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        visible_skyscrapers = {'by_west': [3, _, _, _], 'by_east': [_, _, _, _], 'by_north': [_, _, _, _], 'by_south': [_, _, _, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertNotEqual(Grid.empty(), solution)

    def test_solution_4x4_exist_with_3_visible_skyscrapers_1324(self):
        grid = Grid([
            [1, 3, 2, 4],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        visible_skyscrapers = {'by_west': [3, _, _, _], 'by_east': [_, _, _, _], 'by_north': [_, _, _, _], 'by_south': [_, _, _, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertNotEqual(Grid.empty(), solution)

    def test_solution_4x4_unique_with_4_visible_skyscrapers(self):
        grid = Grid([
            [_, _, _, _],
            [_, 1, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        expected_solution = Grid([
            [1, 2, 3, 4],
            [2, 1, 4, 3],
            [3, 4, 1, 2],
            [4, 3, 2, 1],
        ])
        visible_skyscrapers = {'by_west': [4, _, _, _], 'by_east': [_, _, _, _], 'by_north': [4, _, _, _], 'by_south': [_, _, _, 4]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_unique_with_1_visible_skyscrapers(self):
        grid = Grid([
            [_, _, _, _],
            [_, 2, _, _],
            [_, _, 1, _],
            [_, _, _, _],
        ])
        expected_solution = Grid([
            [3, 4, 2, 1],
            [1, 2, 3, 4],
            [4, 3, 1, 2],
            [2, 1, 4, 3],
        ])
        visible_skyscrapers = {'by_west': [_, _, _, _], 'by_east': [_, 1, _, _], 'by_north': [_, 1, _, _], 'by_south': [_, _, _, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_unique_with_2_visible_skyscrapers(self):
        grid = Grid([
            [_, 3, _, _],
            [2, _, _, _],
            [_, _, 3, 2],
            [3, _, _, _],
        ])
        expected_solution = Grid([
            [4, 3, 2, 1],
            [2, 1, 4, 3],
            [1, 4, 3, 2],
            [3, 2, 1, 4],
        ])
        visible_skyscrapers = {'by_west': [_, _, 2, _], 'by_east': [_, _, _, _], 'by_north': [_, _, _, _], 'by_south': [_, _, _, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_unique_with_3_visible_skyscrapers(self):
        grid = Grid([
            [_, _, _, 1],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        expected_solution = Grid([
            [3, 4, 2, 1],
            [1, 2, 4, 3],
            [4, 1, 3, 2],
            [2, 3, 1, 4],
        ])
        visible_skyscrapers = {'by_west': [_, 3, _, 3], 'by_east': [_, _, _, _], 'by_north': [_, _, _, _], 'by_south': [_, _, 3, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_unique_with_3_1_visible_skyscrapers(self):
        grid = Grid([
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, 1],
            [_, 1, _, _],
        ])
        expected_solution = Grid([
            [3, 2, 1, 4],
            [1, 4, 3, 2],
            [2, 3, 4, 1],
            [4, 1, 2, 3],
        ])
        visible_skyscrapers = {'by_west': [_, _, 3, _], 'by_east': [_, 3, _, _], 'by_north': [_, _, _, 1], 'by_south': [_, _, _, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_with_3_visible_skyscrapers(self):
        grid = Grid([
            [2, 3, 4, 5, 1],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
        ])
        visible_skyscrapers = {'by_west': [3, _, _, _, _], 'by_east': [_, _, _, _, _], 'by_north': [_, _, _, _, _], 'by_south': [_, _, _, _, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_8x8_exist_with_3_visible_skyscrapers(self):
        grid = Grid([
            [2, _, _, _, _, _, 7, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
        ])
        visible_skyscrapers = {'by_west': [3, _, _, _, _, _, _, _], 'by_east': [_, _, _, _, _, _, _, _], 'by_north': [_, _, _, _, _, _, _, _], 'by_south': [_, _, _, _, _, _, _, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertNotEqual(Grid.empty(), solution)

    def test_solution_4x4_1(self):
        grid = Grid([
            [1, _, _, 2],
            [_, _, _, 4],
            [_, _, _, 1],
            [_, 4, 1, 3],
        ])
        expected_solution = Grid([
            [1, 3, 4, 2],
            [3, 1, 2, 4],
            [4, 2, 3, 1],
            [2, 4, 1, 3],
        ])
        visible_skyscrapers = {'by_west': [_, _, _, _], 'by_east': [_, _, _, 2], 'by_north': [3, _, _, 2], 'by_south': [2, _, 3, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_2(self):
        grid = Grid([
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        expected_solution = Grid([
            [2, 4, 1, 3],
            [1, 3, 4, 2],
            [3, 1, 2, 4],
            [4, 2, 3, 1],
        ])
        visible_skyscrapers = {'by_west': [_, _, 2, _], 'by_east': [_, 2, _, _], 'by_north': [_, 1, _, _], 'by_south': [_, 3, 2, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_3(self):
        grid = Grid([
            [_, 2, _, _],
            [_, _, 1, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        expected_solution = Grid([
            [3, 2, 4, 1],
            [2, 3, 1, 4],
            [1, 4, 2, 3],
            [4, 1, 3, 2],
        ])
        visible_skyscrapers = {'by_west': [_, _, _, _], 'by_east': [_, _, _, _], 'by_north': [2, _, _, _], 'by_south': [_, 2, _, 3]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_4(self):
        grid = Grid([
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        expected_solution = Grid([
            [3, 2, 1, 4],
            [1, 4, 3, 2],
            [4, 3, 2, 1],
            [2, 1, 4, 3],
        ])
        visible_skyscrapers = {'by_west': [_, _, _, _], 'by_east': [_, _, 4, _], 'by_north': [2, 2, _, _], 'by_south': [_, _, 1, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_with_visible_skyscrapers_3(self):
        grid = Grid([
            [2, 1, 5, 3, 4],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
        ])
        visible_skyscrapers = {'by_west': [3, _, _, _, _], 'by_east': [_, _, _, _, _], 'by_north': [_, _, _, _, _], 'by_south': [_, _, _, _, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_5x5_1(self):
        grid = Grid([
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
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
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
        ])
        expected_solution = Grid([
            [5, 3, 1, 4, 2],
            [2, 4, 3, 5, 1],
            [1, 5, 4, 2, 3],
            [3, 2, 5, 1, 4],
            [4, 1, 2, 3, 5],
        ])
        visible_skyscrapers = {'by_west': [1, _, _, 2, _], 'by_east': [3, 2, 3, _, _], 'by_north': [_, _, _, _, 4], 'by_south': [2, 3, 2, _, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_3(self):
        grid = Grid([
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
        ])
        expected_solution = Grid([
            [5, 4, 3, 2, 1],
            [2, 5, 1, 4, 3],
            [1, 2, 4, 3, 5],
            [4, 3, 5, 1, 2],
            [3, 1, 2, 5, 4],
        ])
        visible_skyscrapers = {'by_west': [_, _, 4, 2, _], 'by_east': [5, 3, _, 2, _], 'by_north': [_, _, _, _, _], 'by_south': [3, _, 2, _, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_4(self):
        grid = Grid([
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
        ])
        expected_solution = Grid([
            [5, 2, 4, 1, 3],
            [3, 5, 1, 2, 4],
            [1, 4, 5, 3, 2],
            [2, 1, 3, 4, 5],
            [4, 3, 2, 5, 1],
        ])
        visible_skyscrapers = {'by_west': [1, _, 3, 4, _], 'by_east': [_, _, _, _, _], 'by_north': [_, _, 2, 5, _], 'by_south': [2, 3, _, _, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_0(self):
        grid = Grid([
            [_, _, _, _, _, _],
            [_, _, 3, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, 4, _, _],
            [_, 1, _, _, _, _],
            [_, _, _, _, _, _],
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

    def test_solution_6x6_1(self):
        grid = Grid([
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [2, _, _, _, _, _],
            [_, _, _, 2, _, _],
            [_, _, _, _, 3, _],
            [_, _, _, _, _, _],
        ])
        expected_solution = Grid([
            [6, 3, 1, 5, 2, 4],
            [3, 6, 2, 4, 1, 5],
            [2, 5, 4, 1, 6, 3],
            [5, 1, 3, 2, 4, 6],
            [4, 2, 5, 6, 3, 1],
            [1, 4, 6, 3, 5, 2],
        ])
        visible_skyscrapers = {'by_west': [1, 2, _, 2, _, _], 'by_east': [3, _, _, 1, 3, _], 'by_north': [_, _, 5, 2, 2, _], 'by_south': [_, 3, _, _, _, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_2(self):
        grid = Grid([
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
        ])
        expected_solution = Grid([
            [1, 3, 2, 5, 4, 6],
            [4, 1, 6, 3, 5, 2],
            [6, 2, 3, 4, 1, 5],
            [2, 4, 5, 6, 3, 1],
            [3, 5, 1, 2, 6, 4],
            [5, 6, 4, 1, 2, 3],
        ])
        visible_skyscrapers = {'by_west': [4, 2, _, 4, _, _], 'by_east': [_, 3, _, 3, 2, 3], 'by_north': [_, 4, _, 2, 3, _], 'by_south': [_, _, 3, 3, _, 4]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_7x7(self):
        grid = Grid([
            [_, _, _, _, 2, _, _],
            [_, _, 4, _, _, _, _],
            [_, _, _, 2, _, _, _],
            [_, _, 6, _, _, _, _],
            [_, _, _, _, 4, 5, _],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
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
        visible_skyscrapers = {'by_west': [2, _, 3, _, 3, _, _], 'by_east': [2, 3, 3, _, _, 3, _], 'by_north': [_, 2, _, _, _, 3, _], 'by_south': [_, _, 1, _, _, 2, 3]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8(self):
        grid = Grid([
            [_, _, _, _, 3, _, _, _],
            [_, _, _, _, 4, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, 1, _, 8, _, 5],
            [2, _, _, 6, _, _, _, _],
            [_, _, _, 3, _, _, _, _],
            [_, _, _, _, _, _, _, _],
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
        visible_skyscrapers = {'by_west': [3, _, 4, _, _, 5, 3, 3], 'by_east': [_, 4, _, 4, _, _, 2, 2], 'by_north': [3, _, 2, _, _, _, 3, 4], 'by_south': [4, 2, _, 5, 2, 4, _, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_9x9(self):
        grid = Grid([
            [4, _, _, _, _, _, _, _, _],
            [_, _, _, _, 6, _, _, 4, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, 4, _, 3, _, 2, _],
            [_, 5, _, _, _, _, _, _, _],
            [_, _, 4, _, 2, _, _, _, _],
            [_, _, 5, _, 7, 4, _, _, _],
            [_, _, _, 3, _, 5, _, _, _],
            [_, _, 2, _, _, _, _, _, _],
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
        visible_skyscrapers = {'by_west': [_, 4, _, 1, 3, _, 3, _, _], 'by_east': [_, 3, 4, 3, 3, _, 3, _, _], 'by_north': [3, _, 2, _, 4, 4, _, 3, _], 'by_south': [4, 2, 2, _, 3, 3, 4, _, _]}
        skyscrapers_game = SkyscrapersSolver(grid, visible_skyscrapers)
        solution = skyscrapers_game.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = skyscrapers_game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
