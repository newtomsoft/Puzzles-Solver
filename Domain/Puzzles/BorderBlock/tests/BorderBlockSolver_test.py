import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.BorderBlock.BorderBlockSolver import BorderBlockSolver
from Domain.Puzzles.utils import positions

# region constant
_ = BorderBlockSolver.empty
A = 10
B = 11
C = 12
D = 13
E = 14
F = 15
G = 16
H = 17
I = 18
J = 19
K = 20
L = 21


# endregion

class BorderBlockSolverTests(TestCase):
    def test_multiple_solution(self):
        grid = Grid([
            [1, _, 2],
            [_, _, _],
            [_, _, _],
        ])
        dots_positions = positions([(-0.5, 0.5), (2.5, 0.5)])

        game_solver = BorderBlockSolver(grid, dots_positions)
        self.assertNotEqual(Grid.empty(), game_solver.get_solution())
        self.assertNotEqual(Grid.empty(), game_solver.get_other_solution())
        self.assertEqual(Grid.empty(), game_solver.get_other_solution())

    def test_unique_solution(self):
        grid = Grid([
            [1, _, _],
            [_, 2, _],
            [_, _, 3],
        ])
        dots_positions = positions([(-0.5, 0.5), (0.5, -0.5), (2.5, 1.5), (1.5, 2.5)])

        expected_grid = Grid([
            [1, 2, 2],
            [2, 2, 2],
            [2, 2, 3]
        ])
        game_solver = BorderBlockSolver(grid, dots_positions)
        self.assertEqual(expected_grid, game_solver.get_solution())
        self.assertEqual(Grid.empty(), game_solver.get_other_solution())

    def test_impossible_configuration(self):
        grid = Grid([
            [1, _, _],
            [1, 2, _],
            [_, _, _],
        ])
        dots_positions = positions([(-0.5, 0.5), (0.5, -0.5)])

        game_solver = BorderBlockSolver(grid, dots_positions)
        self.assertEqual(Grid.empty(), game_solver.get_solution())

    def test_basic_3x3(self):
        grid = Grid([
            [1, _, _],
            [4, 2, 3],
            [_, _, _],
        ])
        dots_positions = positions([(-0.5, 0.5), (0.5, -0.5), (0.5, 0.5), (2.5, 0.5), (2.5, 1.5)])

        expected_grid = Grid([
            [1, 3, 3],
            [4, 2, 3],
            [4, 2, 3]
        ])
        game_solver = BorderBlockSolver(grid, dots_positions)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_5x5_easy_37zjk(self):
        """https://gridpuzzle.com/bodaburokku/37zjk"""
        grid = Grid([
            [_, 3, _, 3, _],
            [_, 3, 6, 5, _],
            [7, _, _, _, 1],
            [_, _, 6, _, _],
            [2, _, 4, _, 4]
        ])
        dots_positions = positions([
            (-0.5, 0.5),
            (0.5, 2.5), (0.5, 4.5),
            (1.5, 1.5), (1.5, 4.5),
            (2.5, -0.5), (2.5, 0.5), (2.5, 2.5), (2.5, 3.5),
            (3.5, 1.5), (3.5, 4.5),
            (4.5, 1.5)
        ])

        expected_grid = Grid([
            [7, 3, 3, 3, 3],
            [7, 3, 6, 5, 5],
            [7, 7, 6, 5, 1],
            [2, 6, 6, 4, 1],
            [2, 2, 4, 4, 4],
        ])
        game_solver = BorderBlockSolver(grid, dots_positions)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_5x5_evil_319d0(self):
        """https://gridpuzzle.com/bodaburokku/319d0"""
        grid = Grid([
            [_, _, _, _, _],
            [_, 5, 1, 4, _],
            [5, _, 1, _, 6],
            [_, 3, _, 3, _],
            [_, _, 2, _, _]
        ])
        dots_positions = positions([
            (-0.5, 2.5),
            (0.5, 2.5),
            (1.5, 2.5), (1.5, 4.5),
            (2.5, 1.5), (2.5, 2.5), (2.5, 3.5), (2.5, 4.5),
            (3.5, 0.5),
            (4.5, 0.5)
        ])

        expected_grid = Grid([
            [5, 5, 5, 4, 4],
            [5, 5, 1, 4, 4],
            [5, 5, 1, 6, 6],
            [5, 3, 3, 3, 2],
            [5, 2, 2, 2, 2],
        ])
        game_solver = BorderBlockSolver(grid, dots_positions)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_8x8_evil_0p608(self):
        """https://gridpuzzle.com/bodaburokku/0p608"""
        grid = Grid([
            [1, _, _, _, _, _, F, _],
            [_, _, _, E, _, _, _, _],
            [_, _, _, 5, _, _, 6, _],
            [_, _, 9, _, _, _, _, 2],
            [4, _, _, _, E, _, D, _],
            [A, _, _, _, _, _, G, _],
            [_, 8, 3, _, D, _, _, C],
            [B, _, _, _, _, 7, _, _]
        ])
        dots_positions = positions([
            (-0.5, 1.5), (-0.5, 3.5), (-0.5, 4.5), (-0.5, 6.5), (1.5, -0.5), (1.5, 1.5), (1.5, 4.5),
            (1.5, 5.5), (1.5, 7.5), (2.5, 2.5), (2.5, 6.5), (3.5, -0.5), (3.5, 1.5), (3.5, 2.5),
            (3.5, 6.5), (3.5, 7.5), (4.5, -0.5), (4.5, 0.5), (4.5, 3.5), (4.5, 4.5), (5.5, -0.5),
            (5.5, 0.5), (5.5, 5.5), (5.5, 7.5), (6.5, 5.5), (6.5, 7.5), (7.5, 0.5), (7.5, 1.5),
            (7.5, 2.5)
        ])

        expected_grid = Grid([
            [1, 1, 5, 5, E, F, F, 6],
            [1, 1, 5, E, E, F, 6, 6],
            [9, 9, 5, 5, E, D, 6, 2],
            [9, 9, 9, E, E, D, D, 2],
            [4, 4, 3, 3, E, D, D, G],
            [A, 3, 3, 7, 7, D, G, G],
            [B, 8, 3, 7, D, D, C, C],
            [B, 8, 3, 7, 7, 7, 7, 7],
        ])
        game_solver = BorderBlockSolver(grid, dots_positions)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_10x10_evil_7nny9(self):
        """https://gridpuzzle.com/bodaburokku/7nny9"""
        grid = Grid([
            [_, _, 8, _, _, _, _, 6, _, _],
            [_, _, 2, _, _, _, _, B, _, _],
            [2, _, _, 3, _, _, 7, _, _, A],
            [_, 3, _, _, _, _, _, _, 7, _],
            [_, G, _, _, _, _, _, _, A, _],
            [_, _, G, _, 5, 4, _, 7, _, _],
            [_, _, E, _, _, _, _, 5, _, _],
            [_, _, _, 5, 5, D, F, _, _, _],
            [_, C, _, _, _, _, _, _, 9, _],
            [_, _, _, _, 1, 1, _, _, _, _]
        ])
        dots_positions = positions([
            (-0.5, 0.5), (-0.5, 4.5), (-0.5, 5.5), (-0.5, 7.5), (-0.5, 8.5),
            (1.5, 2.5), (1.5, 3.5), (1.5, 7.5),
            (2.5, -0.5), (2.5, 2.5), (2.5, 5.5),
            (3.5, 2.5), (3.5, 3.5), (3.5, 6.5),
            (4.5, -0.5), (4.5, 7.5),
            (5.5, 7.5), (5.5, 9.5),
            (6.5, 0.5), (6.5, 5.5), (6.5, 9.5),
            (7.5, -0.5), (7.5, 2.5), (7.5, 4.5), (7.5, 5.5),
            (8.5, 4.5), (8.5, 6.5),
            (9.5, 2.5), (9.5, 6.5)
        ])

        expected_grid = Grid([
            [2, 8, 8, 8, 8, B, 6, 6, B, A],
            [2, 2, 2, 8, B, B, B, B, B, A],
            [2, 3, 3, 3, 4, B, 7, 7, A, A],
            [3, 3, G, 4, 4, 4, 4, 7, 7, A],
            [3, G, G, E, 5, 4, 5, 7, A, A],
            [G, G, G, E, 5, 4, 5, 7, F, A],
            [G, E, E, E, 5, 5, 5, 5, F, F],
            [G, C, E, 5, 5, D, F, F, F, 9],
            [C, C, C, C, C, D, 1, F, 9, 9],
            [C, C, C, 1, 1, 1, 1, 9, 9, 9],
        ])

        game_solver = BorderBlockSolver(grid, dots_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    @unittest.skip("more than one solution")
    def test_10x10_evil_k9724(self):
        """https://gridpuzzle.com/bodaburokku/k9724"""
        grid = Grid([
            [_, _, G, _, A, _, _, _, _, _],
            [_, _, _, 2, _, L, _, _, 6, _],
            [_, _, _, _, _, _, _, _, _, 4],
            [_, _, 7, _, F, H, _, B, _, _],
            [_, 3, _, _, _, _, _, _, _, _],
            [_, _, 9, _, _, _, _, _, _, _],
            [_, _, 5, _, 1, 1, _, _, C, _],
            [_, _, _, _, _, 1, D, _, I, _],
            [E, _, K, _, 1, _, _, _, _, _],
            [_, _, 8, _, _, _, _, _, _, J]
        ])
        dots_positions = positions([
            (-0.5, 0.5), (-0.5, 2.5), (-0.5, 7.5),
            (0.5, 0.5), (0.5, 2.5), (0.5, 3.5), (0.5, 4.5), (0.5, 6.5), (0.5, 9.5),
            (1.5, 3.5), (1.5, 6.5),
            (2.5, 1.5), (2.5, 3.5), (2.5, 5.5), (2.5, 6.5), (2.5, 7.5), (2.5, 9.5),
            (3.5, -0.5), (3.5, 1.5), (3.5, 2.5), (3.5, 8.5),
            (4.5, 4.5), (4.5, 8.5),
            (5.5, -0.5), (5.5, 4.5),
            (6.5, 1.5), (6.5, 2.5),
            (7.5, 1.5), (7.5, 2.5), (7.5, 6.5),
            (8.5, 2.5), (8.5, 6.5), (8.5, 8.5), (8.5, 9.5),
            (9.5, 0.5), (9.5, 3.5), (9.5, 4.5)
        ])

        expected_grid = Grid([
            [3, G, G, A, A, A, A, A, 6, 6],
            [3, 2, 2, 2, F, L, L, 6, 6, 4],
            [3, 2, 7, 7, F, F, F, 6, 4, 4],
            [3, 3, 7, H, F, H, D, B, 4, C],
            [9, 3, 9, H, H, H, D, B, B, C],
            [9, 9, 9, 9, 9, D, D, D, D, C],
            [E, 9, 5, 9, 1, 1, D, C, C, C],
            [E, E, 5, 1, 1, 1, D, C, I, C],
            [E, 8, K, 1, 1, 1, 1, I, I, C],
            [E, 8, 8, 8, 1, J, J, J, J, J],
        ])
        expected_grid1 = Grid([
            [3, G, G, A, A, A, A, A, 6, 6],
            [3, 2, 2, 2, F, L, L, 6, 6, 4],
            [3, 2, 7, 7, F, F, F, 6, 4, 4],
            [3, 3, 7, H, F, H, D, B, 4, C],
            [9, 3, 9, H, H, H, D, B, B, C],
            [9, 9, 9, 9, 9, D, D, D, D, C],
            [E, 9, 5, 9, 1, 1, D, C, C, C],
            [E, E, E, 1, 1, 1, D, C, I, C],
            [E, 8, K, 1, 1, 1, 1, I, I, C],
            [E, 8, 8, 8, 1, J, J, J, J, J],
        ])
        expected_grid2 = Grid([
            [3, G, G, A, A, A, A, A, 6, 6],
            [3, 2, 2, 2, F, L, L, 6, 6, 4],
            [3, 2, 7, 7, F, F, F, 6, 4, 4],
            [3, 3, 7, H, F, H, D, B, 4, C],
            [9, 3, 9, H, H, H, D, B, B, C],
            [9, 9, 9, 9, 9, D, D, D, D, C],
            [E, 9, 5, 9, 1, 1, D, C, C, C],
            [E, E, E, 9, 9, 1, D, C, I, C],
            [E, 8, K, 1, 1, 1, 1, I, I, C],
            [E, 8, 8, 8, 1, J, J, J, J, J],
        ])
        expected_grids = {expected_grid, expected_grid1, expected_grid2}

        game_solver = BorderBlockSolver(grid, dots_positions)
        solution = game_solver.get_solution()
        solution1 = game_solver.get_other_solution()
        solution2 = game_solver.get_other_solution()
        solutions = {solution, solution1, solution2}
        self.assertEqual(expected_grids, solutions)
        self.assertEqual(Grid.empty(), game_solver.get_other_solution())

        if __name__ == '__main__':
            unittest.main()
