import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Grades.GradesSolver import GradesSolver

_ = GradesSolver.no_value


class GradesGameTests(TestCase):
    def test_solution_5x5_easy_3eqm2(self):
        """https://gridpuzzle.com/grades/3eqm2"""
        grid = Grid([
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
        ])
        clues = {'up': [1, 1, 1, 1, 2], 'down': [3, 1, 8, 6, 17], 'left': [2, 1, 1, 1, 1], 'right': [12, 8, 8, 1, 6]}

        expected_solution = Grid([
            [3, 0, 0, 0, 9],
            [0, 0, 8, 0, 0],
            [0, 0, 0, 0, 8],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 6, 0],
        ])
        game_solver = GradesSolver(grid, clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_evil_0x60r(self):
        """https://gridpuzzle.com/grades/0x60r"""
        grid = Grid([
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
        ])
        clues = {'up': [2, 1, 1, 1, 1], 'down': [17, 4, 8, 3, 1], 'left': [2, 0, 1, 1, 2], 'right': [7, 0, _, 8, 9]}

        expected_solution = Grid([
            [0, 4, 0, 3, 0],
            [0, 0, 0, 0, 0],
            [9, 0, 0, 0, 0],
            [0, 0, 8, 0, 0],
            [8, 0, 0, 0, 1],
        ])
        game_solver = GradesSolver(grid, clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_expert_08421(self):
        """https://gridpuzzle.com/grades/08421"""
        grid = Grid([
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
        ])
        clues = {'up': [3, 1, 2, _, 1, 2, 1, 3], 'down': [13, 1, 14, 5, 1, 5, 2, 11], 'left': [1, 3, 1, 2, 2, _, 1, 3], 'right': [3, 7, 7, 5, 10, 5, _, 11]}

        expected_solution = Grid([
            [0, 0, 0, 0, 0, 0, 0, 3],
            [0, 1, 0, 5, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 7],
            [4, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 8, 0, 0, 0, 2, 0],
            [5, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 4, 0, 0],
            [4, 0, 6, 0, 0, 0, 0, 1],
        ])
        game_solver = GradesSolver(grid, clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_evil_6d6rr(self):
        """https://gridpuzzle.com/grades/6d6rr"""
        grid = Grid([
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [4, _, _, _, _, _, _, 1],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
        ])
        clues = {'up': [3, 1, 1, 2, _, 2, 1, 2], 'down': [_, 9, 2, 9, 6, 8, 7, 10], 'left': [3, 1, 3, 0, _, 2, 2, 2], 'right': [11, 2, 9, 0, 2, 3, 16, 16]}

        expected_solution = Grid([
            [2, 0, 0, 0, 2, 0, 7, 0],
            [0, 0, 2, 0, 0, 0, 0, 0],
            [4, 0, 0, 0, 4, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 7, 0, 0, 0, 9],
            [0, 9, 0, 0, 0, 7, 0, 0],
        ])
        game_solver = GradesSolver(grid, clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_evil_0p1g2(self):
        """https://gridpuzzle.com/grades/0p1g2"""
        grid = Grid([
            [_, _, _, _, _, _, _,_, _, _],
            [_, _, _, _, _, _, _,_, _, _],
            [_, _, _, _, _, _, _,_, _, _],
            [_, _, _, _, _, _, _,_, _, _],
            [_, _, _, _, _, _, _,_, _, _],
            [_, _, _, _, _, _, _,_, _, _],
            [_, _, _, _, _, _, _,_, _, _],
            [_, _, _, _, _, _, _,_, _, _],
            [_, _, _, _, _, _, _,_, _, _],
            [6, _, _, _, _, _, _,_, _, 4],
        ])
        clues = {
            'up': [2, 2, _, _, 2, 1, 3, 1, 2, 3],
            'down': [8, 8, 5, 3, 18, 4, 16, _, 6, 16],
            'left': [1, 4, 1, 2, 2, 1, 1, 2, 1, 3],
            'right': [5, 18, 8, 9, 7, 9, 3, 8, 3, 17]
        }

        expected_solution = Grid([
            [0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
            [2, 0, 5, 0, 9, 0, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
            [0, 5, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 3, 0, 4],
            [0, 0, 0, 0, 9, 0, 0, 0, 0, 0],
            [0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 7, 0, 1, 0],
            [0, 0, 0, 3, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 7, 0, 0, 4],
        ])
        game_solver = GradesSolver(grid, clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
