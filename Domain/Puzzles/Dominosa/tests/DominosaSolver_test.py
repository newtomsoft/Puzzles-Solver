import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Dominosa.DominosaSolver import DominosaSolver


class DominosaSolverTests(TestCase):
    def test_solution_not_min_grid(self):
        grid = Grid(
            [
                [0, 0],  #
                [0, 1],
            ]
        )
        with self.assertRaises(ValueError) as context:
            DominosaSolver(grid)
        self.assertEqual("The grid must be at least 2x3", str(context.exception))

    def test_solution_not_r_c_grid(self):
        grid = Grid(
            [
                [0, 0, 0],  #
                [0, 0, 0],
                [0, 0, 0],
            ]
        )
        with self.assertRaises(ValueError) as context:
            DominosaSolver(grid)
        self.assertEqual("The grid must be RxC with C = R + 1", str(context.exception))

    def test_solution_values_not_0_1(self):
        grid = Grid(
            [
                [0, 1, 1],  #
                [1, 0, 2],
            ]
        )
        with self.assertRaises(ValueError) as context:
            DominosaSolver(grid)
        self.assertEqual("Values on dominoes must be between x and x + 1", str(context.exception))

    def test_solution_values_not_1_2_3(self):
        grid = Grid(
            [
                [1, 2, 3, 4],  #
                [2, 3, 1, 1],
                [3, 1, 2, 1],
            ]
        )
        with self.assertRaises(ValueError) as context:
            DominosaSolver(grid)
        self.assertEqual("Values on dominoes must be between x and x + 2", str(context.exception))

    def test_solution_not_r_c_grid_2(self):
        grid = Grid(
            [
                [0, 1, 0],  #
                [1, 0, 1],
            ]
        )
        solution = DominosaSolver(grid).get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_2x3(self):
        grid = Grid(
            [
                [0, 1, 1],  #
                [1, 0, 0],
            ]
        )

        expected_grid_str = (
            "⊓ ⊏ ⊐\n"  #
            "⊔ ⊏ ⊐"
        )

        solver = DominosaSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_grid_str, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x5(self):
        grid = Grid(
            [
                [1, 3, 3, 0, 0],  #
                [1, 2, 2, 1, 0],
                [3, 0, 1, 2, 2],
                [3, 1, 0, 3, 2],
            ]
        )

        expected_grid_str = (
            "⊓ ⊏ ⊐ ⊏ ⊐\n"  #
            "⊔ ⊏ ⊐ ⊓ ⊓\n"
            "⊏ ⊐ ⊓ ⊔ ⊔\n"
            "⊏ ⊐ ⊔ ⊏ ⊐"
        )

        solver = DominosaSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_grid_str, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x5_2(self):
        grid = Grid(
            [
                [0, 1, 0, 3, 2],  #
                [3, 1, 2, 0, 1],
                [1, 3, 0, 0, 2],
                [2, 2, 3, 3, 1],
            ]
        )

        expected_grid_str = (
            "⊓ ⊓ ⊓ ⊏ ⊐\n"  #
            "⊔ ⊔ ⊔ ⊏ ⊐\n"
            "⊏ ⊐ ⊏ ⊐ ⊓\n"
            "⊏ ⊐ ⊏ ⊐ ⊔"
        )

        solver = DominosaSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_grid_str, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x6(self):
        grid = Grid(
            [
                [4, 0, 4, 3, 3, 3],  #
                [1, 4, 3, 4, 2, 1],
                [3, 4, 2, 0, 4, 0],
                [2, 0, 0, 0, 3, 1],
                [2, 2, 2, 1, 1, 1],
            ]
        )

        expected_grid_str = (
            "⊓ ⊏ ⊐ ⊏ ⊐ ⊓\n"  #
            "⊔ ⊓ ⊏ ⊐ ⊓ ⊔\n"
            "⊓ ⊔ ⊏ ⊐ ⊔ ⊓\n"
            "⊔ ⊏ ⊐ ⊏ ⊐ ⊔\n"
            "⊏ ⊐ ⊏ ⊐ ⊏ ⊐"
        )

        solver = DominosaSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_grid_str, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x7(self):
        grid = Grid(
            [
                [3, 1, 2, 1, 4, 4, 0],  #
                [1, 5, 2, 1, 4, 3, 0],
                [0, 3, 3, 2, 4, 3, 5],
                [2, 3, 5, 2, 1, 5, 1],
                [2, 4, 0, 4, 2, 0, 0],
                [3, 4, 0, 5, 5, 5, 1],
            ]
        )

        expected_grid_str = (
            "⊓ ⊏ ⊐ ⊓ ⊓ ⊏ ⊐\n"  #
            "⊔ ⊏ ⊐ ⊔ ⊔ ⊓ ⊓\n"
            "⊏ ⊐ ⊓ ⊓ ⊓ ⊔ ⊔\n"
            "⊏ ⊐ ⊔ ⊔ ⊔ ⊏ ⊐\n"
            "⊏ ⊐ ⊓ ⊓ ⊏ ⊐ ⊓\n"
            "⊏ ⊐ ⊔ ⊔ ⊏ ⊐ ⊔"
        )

        solver = DominosaSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_grid_str, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_7x8(self):
        grid = Grid(
            [
                [3, 3, 5, 2, 6, 4, 6, 5],  #
                [5, 6, 3, 4, 1, 4, 0, 5],
                [0, 6, 4, 2, 1, 6, 3, 2],
                [1, 0, 5, 2, 1, 6, 3, 1],
                [5, 4, 0, 0, 5, 6, 0, 4],
                [2, 3, 1, 3, 3, 4, 2, 2],
                [6, 0, 2, 0, 4, 1, 1, 5],
            ]
        )

        expected_grid_str = (
            "⊓ ⊓ ⊏ ⊐ ⊓ ⊓ ⊓ ⊓\n"  #
            "⊔ ⊔ ⊏ ⊐ ⊔ ⊔ ⊔ ⊔\n"
            "⊓ ⊏ ⊐ ⊓ ⊓ ⊓ ⊏ ⊐\n"
            "⊔ ⊏ ⊐ ⊔ ⊔ ⊔ ⊏ ⊐\n"
            "⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊓ ⊓\n"
            "⊓ ⊓ ⊓ ⊏ ⊐ ⊓ ⊔ ⊔\n"
            "⊔ ⊔ ⊔ ⊏ ⊐ ⊔ ⊏ ⊐"
        )

        solver = DominosaSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_grid_str, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x11(self):
        grid = Grid(
            [
                [5, 2, 3, 8, 7, 5, 4, 7, 9, 0, 9],  #
                [3, 1, 2, 8, 6, 5, 7, 3, 2, 1, 6],
                [4, 0, 1, 8, 2, 1, 5, 7, 7, 8, 9],
                [2, 1, 4, 9, 0, 1, 9, 5, 4, 8, 2],
                [6, 0, 3, 0, 3, 7, 1, 6, 8, 4, 2],
                [3, 5, 5, 2, 0, 6, 8, 3, 9, 5, 8],
                [6, 5, 0, 2, 1, 5, 4, 9, 6, 3, 3],
                [7, 7, 8, 7, 5, 4, 9, 9, 6, 1, 9],
                [4, 8, 6, 4, 0, 2, 6, 6, 7, 4, 4],
                [3, 7, 0, 1, 0, 2, 3, 9, 0, 8, 1],
            ]
        )

        expected_grid_str = (
            "⊏ ⊐ ⊏ ⊐ ⊓ ⊓ ⊓ ⊏ ⊐ ⊏ ⊐\n"  #
            "⊏ ⊐ ⊏ ⊐ ⊔ ⊔ ⊔ ⊓ ⊓ ⊏ ⊐\n"
            "⊏ ⊐ ⊓ ⊓ ⊓ ⊓ ⊓ ⊔ ⊔ ⊓ ⊓\n"
            "⊏ ⊐ ⊔ ⊔ ⊔ ⊔ ⊔ ⊏ ⊐ ⊔ ⊔\n"
            "⊓ ⊓ ⊓ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐\n"
            "⊔ ⊔ ⊔ ⊓ ⊏ ⊐ ⊓ ⊏ ⊐ ⊏ ⊐\n"
            "⊏ ⊐ ⊓ ⊔ ⊏ ⊐ ⊔ ⊓ ⊓ ⊏ ⊐\n"
            "⊏ ⊐ ⊔ ⊏ ⊐ ⊏ ⊐ ⊔ ⊔ ⊏ ⊐\n"
            "⊓ ⊓ ⊏ ⊐ ⊓ ⊏ ⊐ ⊓ ⊓ ⊏ ⊐\n"
            "⊔ ⊔ ⊏ ⊐ ⊔ ⊏ ⊐ ⊔ ⊔ ⊏ ⊐"
        )

        solver = DominosaSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_grid_str, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_20x21(self):
        grid = Grid(
            [
                [13, 14, 7, 5, 11, 20, 0, 12, 7, 14, 9, 16, 2, 16, 11, 12, 3, 9, 9, 10, 14, 9],  #
                [3, 17, 10, 2, 15, 3, 3, 13, 3, 5, 1, 17, 15, 10, 11, 2, 20, 17, 19, 14, 5, 0],
                [7, 0, 19, 1, 13, 8, 2, 9, 0, 19, 3, 7, 11, 16, 20, 20, 11, 11, 19, 19, 12, 2],
                [7, 1, 0, 6, 18, 18, 3, 9, 2, 2, 3, 5, 18, 16, 4, 11, 14, 8, 8, 20, 15, 8],
                [20, 4, 4, 5, 18, 17, 2, 19, 8, 5, 19, 2, 3, 2, 10, 15, 9, 9, 3, 8, 2, 16],
                [0, 3, 6, 2, 5, 3, 3, 5, 1, 15, 1, 16, 18, 14, 17, 13, 6, 17, 10, 6, 14, 4],
                [17, 5, 5, 5, 1, 16, 7, 11, 9, 0, 18, 17, 18, 14, 20, 15, 18, 10, 3, 4, 0, 1],
                [14, 16, 3, 20, 19, 3, 11, 17, 7, 20, 12, 12, 15, 17, 9, 9, 14, 11, 6, 10, 6, 7],
                [5, 1, 18, 9, 13, 9, 7, 14, 0, 14, 8, 19, 8, 16, 12, 12, 6, 2, 4, 9, 0, 10],
                [18, 20, 13, 5, 13, 16, 13, 18, 17, 7, 7, 6, 8, 8, 20, 14, 6, 16, 14, 15, 18, 14],
                [19, 7, 13, 0, 4, 14, 10, 9, 11, 1, 13, 4, 7, 2, 0, 10, 7, 17, 12, 2, 15, 11],
                [6, 6, 7, 8, 19, 1, 7, 15, 8, 18, 0, 18, 7, 0, 17, 12, 13, 6, 12, 16, 19, 13],
                [14, 20, 13, 16, 2, 20, 5, 0, 16, 13, 18, 12, 0, 5, 1, 0, 16, 10, 3, 16, 11, 9],
                [8, 7, 10, 19, 19, 4, 7, 6, 20, 8, 15, 15, 2, 4, 19, 9, 17, 11, 9, 4, 11, 12],
                [11, 17, 2, 9, 19, 4, 0, 11, 15, 1, 18, 4, 18, 16, 8, 5, 20, 20, 12, 12, 15, 7],
                [11, 4, 2, 12, 1, 19, 0, 2, 10, 10, 10, 1, 3, 15, 0, 20, 6, 20, 9, 3, 1, 16],
                [14, 4, 8, 15, 20, 8, 17, 14, 19, 6, 8, 8, 5, 11, 10, 1, 10, 4, 5, 14, 0, 13],
                [13, 6, 16, 16, 16, 12, 7, 14, 6, 12, 1, 1, 17, 6, 17, 13, 19, 16, 3, 19, 11, 12],
                [13, 18, 4, 13, 2, 5, 8, 4, 3, 13, 10, 13, 12, 7, 17, 1, 11, 5, 15, 18, 2, 17],
                [19, 18, 20, 9, 18, 4, 3, 1, 6, 8, 9, 20, 1, 10, 17, 15, 8, 15, 18, 4, 15, 6],
                [4, 17, 10, 15, 13, 14, 10, 5, 1, 6, 15, 12, 20, 12, 4, 0, 11, 5, 10, 12, 6, 19],
            ]
        )

        expected_grid_str = (
            "⊏ ⊐ ⊏ ⊐ ⊓ ⊓ ⊓ ⊏ ⊐ ⊓ ⊏ ⊐ ⊓ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊓ ⊏ ⊐\n"  #
            "⊏ ⊐ ⊓ ⊓ ⊔ ⊔ ⊔ ⊏ ⊐ ⊔ ⊏ ⊐ ⊔ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊔ ⊏ ⊐\n"
            "⊏ ⊐ ⊔ ⊔ ⊓ ⊓ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊓ ⊓ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐\n"
            "⊏ ⊐ ⊓ ⊓ ⊔ ⊔ ⊏ ⊐ ⊏ ⊐ ⊓ ⊓ ⊔ ⊔ ⊏ ⊐ ⊏ ⊐ ⊓ ⊏ ⊐ ⊓\n"
            "⊓ ⊓ ⊔ ⊔ ⊓ ⊏ ⊐ ⊓ ⊏ ⊐ ⊔ ⊔ ⊏ ⊐ ⊏ ⊐ ⊓ ⊓ ⊔ ⊓ ⊓ ⊔\n"
            "⊔ ⊔ ⊏ ⊐ ⊔ ⊏ ⊐ ⊔ ⊓ ⊓ ⊓ ⊓ ⊓ ⊓ ⊏ ⊐ ⊔ ⊔ ⊓ ⊔ ⊔ ⊓\n"
            "⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊔ ⊔ ⊔ ⊔ ⊔ ⊔ ⊓ ⊓ ⊏ ⊐ ⊔ ⊓ ⊓ ⊔\n"
            "⊏ ⊐ ⊓ ⊏ ⊐ ⊏ ⊐ ⊓ ⊏ ⊐ ⊓ ⊓ ⊏ ⊐ ⊔ ⊔ ⊓ ⊏ ⊐ ⊔ ⊔ ⊓\n"
            "⊏ ⊐ ⊔ ⊏ ⊐ ⊏ ⊐ ⊔ ⊏ ⊐ ⊔ ⊔ ⊓ ⊏ ⊐ ⊓ ⊔ ⊏ ⊐ ⊏ ⊐ ⊔\n"
            "⊏ ⊐ ⊏ ⊐ ⊓ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊓ ⊔ ⊏ ⊐ ⊔ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐\n"
            "⊏ ⊐ ⊏ ⊐ ⊔ ⊓ ⊏ ⊐ ⊓ ⊏ ⊐ ⊔ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊓ ⊓ ⊓ ⊓\n"
            "⊏ ⊐ ⊓ ⊏ ⊐ ⊔ ⊏ ⊐ ⊔ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊓ ⊏ ⊐ ⊔ ⊔ ⊔ ⊔\n"
            "⊏ ⊐ ⊔ ⊓ ⊓ ⊏ ⊐ ⊏ ⊐ ⊓ ⊏ ⊐ ⊓ ⊓ ⊓ ⊔ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐\n"
            "⊏ ⊐ ⊓ ⊔ ⊔ ⊏ ⊐ ⊏ ⊐ ⊔ ⊏ ⊐ ⊔ ⊔ ⊔ ⊓ ⊓ ⊓ ⊏ ⊐ ⊏ ⊐\n"
            "⊏ ⊐ ⊔ ⊏ ⊐ ⊓ ⊓ ⊓ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊓ ⊔ ⊔ ⊔ ⊓ ⊏ ⊐ ⊓\n"
            "⊓ ⊓ ⊓ ⊏ ⊐ ⊔ ⊔ ⊔ ⊏ ⊐ ⊓ ⊓ ⊏ ⊐ ⊔ ⊓ ⊓ ⊓ ⊔ ⊓ ⊓ ⊔\n"
            "⊔ ⊔ ⊔ ⊓ ⊓ ⊏ ⊐ ⊏ ⊐ ⊓ ⊔ ⊔ ⊏ ⊐ ⊓ ⊔ ⊔ ⊔ ⊓ ⊔ ⊔ ⊓\n"
            "⊓ ⊓ ⊓ ⊔ ⊔ ⊓ ⊏ ⊐ ⊓ ⊔ ⊏ ⊐ ⊓ ⊓ ⊔ ⊏ ⊐ ⊓ ⊔ ⊏ ⊐ ⊔\n"
            "⊔ ⊔ ⊔ ⊏ ⊐ ⊔ ⊏ ⊐ ⊔ ⊏ ⊐ ⊓ ⊔ ⊔ ⊓ ⊏ ⊐ ⊔ ⊓ ⊏ ⊐ ⊓\n"
            "⊏ ⊐ ⊓ ⊏ ⊐ ⊓ ⊏ ⊐ ⊓ ⊏ ⊐ ⊔ ⊏ ⊐ ⊔ ⊏ ⊐ ⊓ ⊔ ⊏ ⊐ ⊔\n"
            "⊏ ⊐ ⊔ ⊏ ⊐ ⊔ ⊏ ⊐ ⊔ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊔ ⊏ ⊐ ⊏ ⊐"
        )

        solver = DominosaSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_grid_str, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_25x26(self):
        grid = Grid(
            [
                [20, 18, 7, 7, 11, 24, 0, 9, 23, 22, 15, 8, 18, 8, 22, 10, 17, 22, 11, 11, 19, 15, 17, 14, 3, 14, 10],  #
                [11, 2, 22, 5, 23, 23, 22, 19, 16, 6, 16, 12, 3, 7, 6, 13, 13, 4, 14, 4, 24, 9, 19, 4, 10, 16, 21],
                [3, 10, 5, 21, 12, 21, 4, 24, 0, 13, 13, 3, 22, 5, 9, 22, 12, 16, 6, 5, 22, 21, 2, 23, 17, 2, 9],
                [2, 10, 11, 6, 24, 2, 22, 11, 13, 20, 11, 3, 1, 21, 2, 2, 9, 6, 20, 17, 11, 4, 1, 16, 9, 24, 22],
                [12, 9, 18, 8, 18, 10, 15, 11, 18, 22, 16, 2, 5, 20, 1, 13, 17, 14, 0, 23, 22, 0, 19, 0, 24, 17, 12],
                [3, 13, 17, 4, 16, 8, 3, 8, 5, 18, 10, 13, 21, 5, 12, 14, 24, 2, 15, 6, 9, 24, 23, 10, 18, 25, 5],
                [23, 1, 25, 9, 13, 16, 23, 13, 25, 4, 25, 23, 21, 24, 22, 17, 1, 14, 18, 22, 4, 18, 18, 12, 25, 12, 19],
                [5, 16, 22, 3, 8, 13, 2, 23, 25, 4, 20, 24, 4, 8, 14, 0, 23, 8, 7, 7, 2, 4, 24, 12, 6, 23, 9],
                [19, 11, 3, 11, 23, 6, 19, 7, 18, 19, 15, 8, 13, 4, 23, 18, 0, 5, 5, 24, 3, 19, 16, 17, 18, 19, 25],
                [13, 19, 6, 4, 14, 10, 21, 21, 15, 16, 20, 23, 8, 0, 24, 2, 21, 17, 5, 22, 9, 6, 3, 4, 7, 12, 21],
                [21, 21, 5, 6, 1, 25, 23, 24, 25, 8, 5, 11, 5, 21, 1, 8, 11, 17, 15, 25, 11, 12, 6, 8, 23, 20, 18],
                [3, 0, 5, 6, 8, 9, 4, 13, 16, 5, 8, 22, 3, 7, 25, 4, 14, 2, 7, 18, 22, 21, 1, 10, 14, 9, 4],
                [23, 18, 23, 20, 20, 1, 11, 21, 14, 0, 24, 24, 4, 21, 2, 11, 8, 17, 9, 15, 0, 20, 16, 8, 17, 16, 9],
                [19, 10, 10, 8, 11, 0, 15, 15, 12, 1, 10, 3, 20, 16, 4, 3, 13, 20, 24, 9, 7, 1, 2, 21, 17, 6, 3],
                [25, 5, 15, 22, 19, 19, 6, 21, 7, 20, 2, 25, 2, 14, 0, 12, 18, 25, 22, 1, 16, 16, 1, 17, 6, 11, 17],
                [12, 11, 15, 5, 5, 14, 7, 0, 23, 13, 19, 10, 2, 12, 19, 4, 14, 11, 19, 19, 15, 20, 1, 25, 13, 25, 1],
                [15, 10, 1, 6, 3, 20, 0, 17, 16, 5, 11, 0, 7, 3, 4, 1, 11, 2, 10, 20, 18, 10, 14, 12, 9, 20, 8],
                [4, 13, 16, 7, 16, 17, 1, 14, 24, 2, 21, 4, 1, 25, 24, 3, 25, 17, 3, 24, 16, 12, 23, 20, 20, 13, 4],
                [11, 15, 17, 4, 21, 23, 16, 10, 19, 11, 6, 6, 9, 1, 7, 25, 25, 23, 7, 1, 12, 24, 2, 9, 21, 7, 22],
                [25, 15, 22, 23, 12, 18, 16, 20, 6, 7, 25, 19, 5, 22, 15, 9, 14, 20, 14, 11, 23, 19, 7, 0, 1, 9, 10],
                [15, 8, 11, 3, 1, 15, 21, 17, 17, 19, 20, 8, 9, 22, 2, 12, 0, 9, 9, 5, 14, 1, 2, 10, 18, 21, 25],
                [3, 19, 15, 7, 0, 16, 20, 6, 18, 9, 13, 14, 18, 19, 2, 0, 24, 10, 18, 21, 21, 24, 22, 15, 13, 6, 19],
                [4, 9, 12, 20, 0, 17, 3, 19, 20, 8, 8, 8, 5, 2, 6, 23, 12, 17, 18, 13, 17, 5, 1, 7, 20, 10, 14],
                [4, 22, 6, 3, 15, 24, 14, 14, 14, 5, 6, 11, 0, 25, 7, 3, 8, 19, 3, 20, 12, 18, 1, 12, 12, 15, 14],
                [24, 24, 13, 2, 12, 21, 24, 8, 1, 0, 7, 17, 13, 2, 15, 9, 7, 14, 16, 16, 15, 18, 13, 7, 5, 15, 7],
                [25, 10, 12, 17, 16, 15, 10, 0, 25, 3, 7, 6, 22, 13, 0, 13, 14, 18, 25, 10, 23, 0, 10, 6, 0, 8, 10],
            ]
        )

        expected_grid_str = (
            "⊓ ⊓ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊓ ⊏ ⊐ ⊓ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊓ ⊏ ⊐ ⊏ ⊐ ⊓ ⊓\n"  #
            "⊔ ⊔ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊔ ⊏ ⊐ ⊔ ⊓ ⊓ ⊏ ⊐ ⊓ ⊓ ⊓ ⊓ ⊔ ⊏ ⊐ ⊏ ⊐ ⊔ ⊔\n"
            "⊓ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊓ ⊔ ⊔ ⊏ ⊐ ⊔ ⊔ ⊔ ⊔ ⊏ ⊐ ⊏ ⊐ ⊓ ⊏ ⊐\n"
            "⊔ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊓ ⊓ ⊔ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊓ ⊓ ⊔ ⊓ ⊓\n"
            "⊓ ⊏ ⊐ ⊓ ⊓ ⊏ ⊐ ⊏ ⊐ ⊔ ⊔ ⊏ ⊐ ⊓ ⊓ ⊏ ⊐ ⊓ ⊓ ⊓ ⊏ ⊐ ⊔ ⊔ ⊓ ⊔ ⊔\n"
            "⊔ ⊓ ⊓ ⊔ ⊔ ⊓ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊓ ⊔ ⊔ ⊏ ⊐ ⊔ ⊔ ⊔ ⊏ ⊐ ⊏ ⊐ ⊔ ⊓ ⊓\n"
            "⊓ ⊔ ⊔ ⊓ ⊓ ⊔ ⊏ ⊐ ⊓ ⊏ ⊐ ⊓ ⊔ ⊓ ⊓ ⊓ ⊓ ⊓ ⊓ ⊓ ⊓ ⊏ ⊐ ⊓ ⊓ ⊔ ⊔\n"
            "⊔ ⊏ ⊐ ⊔ ⊔ ⊏ ⊐ ⊓ ⊔ ⊏ ⊐ ⊔ ⊓ ⊔ ⊔ ⊔ ⊔ ⊔ ⊔ ⊔ ⊔ ⊏ ⊐ ⊔ ⊔ ⊏ ⊐\n"
            "⊓ ⊏ ⊐ ⊏ ⊐ ⊓ ⊓ ⊔ ⊓ ⊓ ⊓ ⊓ ⊔ ⊏ ⊐ ⊏ ⊐ ⊓ ⊏ ⊐ ⊏ ⊐ ⊓ ⊏ ⊐ ⊓ ⊓\n"
            "⊔ ⊏ ⊐ ⊓ ⊓ ⊔ ⊔ ⊓ ⊔ ⊔ ⊔ ⊔ ⊏ ⊐ ⊓ ⊓ ⊓ ⊔ ⊓ ⊓ ⊓ ⊓ ⊔ ⊏ ⊐ ⊔ ⊔\n"
            "⊓ ⊓ ⊓ ⊔ ⊔ ⊏ ⊐ ⊔ ⊏ ⊐ ⊓ ⊓ ⊏ ⊐ ⊔ ⊔ ⊔ ⊓ ⊔ ⊔ ⊔ ⊔ ⊓ ⊓ ⊏ ⊐ ⊓\n"
            "⊔ ⊔ ⊔ ⊏ ⊐ ⊏ ⊐ ⊓ ⊏ ⊐ ⊔ ⊔ ⊓ ⊏ ⊐ ⊏ ⊐ ⊔ ⊓ ⊏ ⊐ ⊓ ⊔ ⊔ ⊏ ⊐ ⊔\n"
            "⊓ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊔ ⊏ ⊐ ⊏ ⊐ ⊔ ⊓ ⊏ ⊐ ⊏ ⊐ ⊔ ⊓ ⊓ ⊔ ⊓ ⊓ ⊓ ⊏ ⊐\n"
            "⊔ ⊏ ⊐ ⊓ ⊓ ⊓ ⊓ ⊏ ⊐ ⊓ ⊏ ⊐ ⊓ ⊔ ⊓ ⊏ ⊐ ⊏ ⊐ ⊔ ⊔ ⊓ ⊔ ⊔ ⊔ ⊏ ⊐\n"
            "⊏ ⊐ ⊓ ⊔ ⊔ ⊔ ⊔ ⊏ ⊐ ⊔ ⊓ ⊓ ⊔ ⊓ ⊔ ⊓ ⊏ ⊐ ⊏ ⊐ ⊓ ⊔ ⊓ ⊏ ⊐ ⊏ ⊐\n"
            "⊏ ⊐ ⊔ ⊓ ⊓ ⊏ ⊐ ⊏ ⊐ ⊓ ⊔ ⊔ ⊓ ⊔ ⊓ ⊔ ⊏ ⊐ ⊏ ⊐ ⊔ ⊓ ⊔ ⊏ ⊐ ⊏ ⊐\n"
            "⊓ ⊏ ⊐ ⊔ ⊔ ⊏ ⊐ ⊓ ⊓ ⊔ ⊏ ⊐ ⊔ ⊓ ⊔ ⊓ ⊓ ⊏ ⊐ ⊏ ⊐ ⊔ ⊓ ⊓ ⊓ ⊏ ⊐\n"
            "⊔ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊔ ⊔ ⊏ ⊐ ⊏ ⊐ ⊔ ⊓ ⊔ ⊔ ⊓ ⊏ ⊐ ⊏ ⊐ ⊔ ⊔ ⊔ ⊓ ⊓\n"
            "⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊓ ⊏ ⊐ ⊓ ⊏ ⊐ ⊏ ⊐ ⊔ ⊓ ⊓ ⊔ ⊏ ⊐ ⊓ ⊏ ⊐ ⊏ ⊐ ⊔ ⊔\n"
            "⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊔ ⊏ ⊐ ⊔ ⊓ ⊓ ⊓ ⊓ ⊓ ⊔ ⊔ ⊏ ⊐ ⊓ ⊔ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐\n"
            "⊓ ⊏ ⊐ ⊓ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊔ ⊔ ⊔ ⊔ ⊔ ⊏ ⊐ ⊏ ⊐ ⊔ ⊓ ⊏ ⊐ ⊏ ⊐ ⊓ ⊓\n"
            "⊔ ⊏ ⊐ ⊔ ⊓ ⊏ ⊐ ⊏ ⊐ ⊓ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊓ ⊓ ⊏ ⊐ ⊔ ⊏ ⊐ ⊏ ⊐ ⊔ ⊔\n"
            "⊓ ⊏ ⊐ ⊓ ⊔ ⊏ ⊐ ⊏ ⊐ ⊔ ⊏ ⊐ ⊓ ⊏ ⊐ ⊓ ⊔ ⊔ ⊓ ⊓ ⊓ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐\n"
            "⊔ ⊏ ⊐ ⊔ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊏ ⊐ ⊔ ⊓ ⊓ ⊔ ⊓ ⊓ ⊔ ⊔ ⊔ ⊏ ⊐ ⊓ ⊓ ⊏ ⊐\n"
            "⊓ ⊏ ⊐ ⊏ ⊐ ⊓ ⊓ ⊏ ⊐ ⊓ ⊏ ⊐ ⊓ ⊔ ⊔ ⊓ ⊔ ⊔ ⊓ ⊓ ⊓ ⊏ ⊐ ⊔ ⊔ ⊓ ⊓\n"
            "⊔ ⊏ ⊐ ⊏ ⊐ ⊔ ⊔ ⊏ ⊐ ⊔ ⊏ ⊐ ⊔ ⊏ ⊐ ⊔ ⊏ ⊐ ⊔ ⊔ ⊔ ⊏ ⊐ ⊏ ⊐ ⊔ ⊔"
        )

        solver = DominosaSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_grid_str, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_multiple_solutions(self):
        grid = Grid(
            [
                [0, 0, 1],  #
                [0, 1, 1],
            ]
        )

        solver = DominosaSolver(grid)
        solution0 = solver.get_solution()
        self.assertNotEqual(Grid.empty(), solution0)
        solution1 = solver.get_other_solution()
        self.assertNotEqual(Grid.empty(), solution1)
        solution2 = solver.get_other_solution()
        self.assertNotEqual(Grid.empty(), solution2)
        solution3 = solver.get_other_solution()
        self.assertEqual(Grid.empty(), solution3)


if __name__ == "__main__":
    unittest.main()
