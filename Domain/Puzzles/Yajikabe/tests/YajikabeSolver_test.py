from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Yajikabe.YajilkabeSolver import YajikabeSolver

____ = ''
_ = 0
X = 1


class YajikabeSolverTests(TestCase):
    def test_solution_5x5_expert_29jxz(self):
        """https://gridpuzzle.com/yajikabe/29jxz"""
        grid = Grid([
            ['1↓', ____, '4↓', ____, '1←'],
            [____, ____, ____, ____, ____],
            [____, '0↓', ____, '0↑', ____],
            [____, ____, ____, ____, ____],
            ['1↑', ____, ____, ____, '3↑'],
        ])

        game_solver = YajikabeSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [_, X, _, _, _],
            [X, X, X, _, X],
            [_, _, X, _, X],
            [_, _, X, X, X],
            [_, _, X, _, _],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_evil_0e1rg(self):
        """https://gridpuzzle.com/yajikabe/0e1rg"""
        grid = Grid([
            [____, '3→', ____, ____, ____, ____, '3←', ____],
            [____, ____, '2←', ____, ____, '1↓', ____, ____],
            [____, '2→', '1↑', ____, ____, '1→', '0↑', ____],
            [____, ____, ____, ____, ____, ____, ____, ____],
            [____, ____, '3→', ____, ____, '3←', ____, ____],
            [____, ____, ____, ____, ____, ____, ____, ____],
            ['3→', ____, '1←', ____, ____, '0→', ____, '2↑'],
            ['2→', '3↑', ____, ____, ____, ____, '2↑', '2←'],
        ])

        game_solver = YajikabeSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [_, _, X, X, X, _, _, _],
            [X, X, _, _, X, _, _, _],
            [X, _, _, _, X, _, _, X],
            [X, _, _, _, X, X, X, X],
            [X, _, _, X, X, _, X, _],
            [X, X, X, X, _, _, _, _],
            [_, X, _, X, X, _, _, _],
            [_, _, X, X, _, _, _, _]
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_evil_0kxvg(self):
        """https://gridpuzzle.com/yajikabe/0kxvg"""
        grid = Grid([
            [____, ____, ____, ____, '3↓', ____, '0→', ____, ____, '4↓'],
            [____, '1↑', ____, ____, ____, ____, ____, '4↓', ____, '4←'],
            [____, ____, '2↑', ____, ____, ____, ____, ____, ____, ____],
            ['4↓', ____, ____, ____, '2→', ____, ____, ____, '2↓', ____],
            [____, ____, ____, '0↑', ____, ____, '1↑', ____, ____, ____],
            ['4→', ____, ____, '2←', ____, '4↑', ____, ____, ____, '2↑'],
            [____, ____, ____, ____, ____, ____, ____, ____, ____, ____],
            [____, ____, '3↑', ____, ____, ____, ____, ____, ____, ____],
            [____, ____, ____, ____, ____, ____, '3↑', '5←', ____, ____],
            ['2→', ____, '1←', ____, '1←', ____, ____, ____, ____, ____],
        ])

        game_solver = YajikabeSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [X, X, X, _, _, _, _, _, _, _],
            [X, _, X, _, _, X, _, _, X, _],
            [X, X, _, _, _, X, X, X, X, X],
            [_, X, _, _, _, X, _, X, _, _],
            [X, X, _, _, X, X, _, X, X, X],
            [_, X, X, _, X, _, X, _, _, _],
            [X, X, _, X, X, X, X, X, X, X],
            [X, _, _, X, _, X, _, _, _, X],
            [X, X, X, X, _, X, _, _, _, _],
            [_, X, _, _, _, X, _, _, _, _],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12_evil_211nq5(self):
        """https://gridpuzzle.com/yajikabe/211nq5"""
        grid = Grid([
            [____, ____, ____, '5↓', ____, '1→', '2←', ____, '0→', ____, ____, ____],
            ['1↑', ____, ____, ____, ____, ____, ____, ____, ____, ____, ____, '6←'],
            [____, ____, ____, '0←', ____, ____, ____, ____, '0→', ____, ____, ____],
            [____, ____, '0←', '2→', ____, ____, ____, ____, '0→', '7↓', ____, ____],
            [____, ____, ____, '6→', ____, ____, ____, ____, '3→', ____, ____, ____],
            ['2↓', '2↑', ____, ____, ____, ____, ____, ____, ____, ____, '3↓', '6←'],
            [____, ____, ____, ____, '2↑', '0←', '2↑', '3↓', ____, ____, ____, ____],
            ['2↓', '2↑', ____, ____, ____, ____, ____, ____, ____, ____, '5←', '2↑'],
            ['7→', ____, ____, ____, ____, ____, ____, ____, ____, ____, ____, '7←'],
            [____, ____, '5→', ____, ____, ____, ____, ____, ____, '2→', ____, ____],
            [____, '5→', ____, ____, ____, ____, ____, ____, ____, ____, '6←', ____],
            [____, ____, ____, ____, '5↑', ____, ____, '5←', ____, ____, ____, ____]
        ])

        game_solver = YajikabeSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [X, X, _, _, _, _, _, X, _, _, _, _],
            [_, X, X, X, X, X, _, X, _, _, _, _],
            [_, _, _, _, _, X, X, X, _, _, _, _],
            [_, _, _, _, _, X, _, X, _, _, _, _],
            [_, _, _, _, _, X, X, X, _, X, X, X],
            [_, _, _, X, X, X, _, X, X, X, _, _],
            [_, _, _, _, _, _, _, _, _, X, X, X],
            [_, _, _, _, _, X, X, X, X, X, _, _],
            [_, _, X, X, X, X, _, X, _, X, X, _],
            [_, _, _, _, X, _, _, X, X, _, X, X],
            [X, _, _, X, X, X, _, _, X, X, _, _],
            [X, X, X, X, _, X, _, _, _, X, _, _],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12_evil_1nwe1k(self):
        """https://gridpuzzle.com/yajikabe/1nwe1k"""
        grid = Grid([
            [____, ____, ____, '3→', '0←', ____, ____, '3↓', '7↓', ____, ____, ____],
            [____, '5↓', ____, ____, ____, '3←', '3→', ____, ____, ____, '6←', ____],
            ['5↓', ____, ____, ____, ____, '3→', '1←', ____, ____, ____, ____, '5↓'],
            [____, ____, ____, ____, ____, ____, ____, ____, ____, ____, ____, ____],
            [____, ____, ____, '2↑', '2←', '3→', '2↓', '2↑', '5↓', ____, ____, ____],
            [____, '5→', ____, ____, ____, ____, ____, ____, ____, ____, '2↓', ____],
            [____, ____, '1←', ____, ____, ____, ____, ____, ____, '1→', ____, ____],
            [____, ____, ____, ____, '4↑', ____, ____, '2←', ____, ____, ____, ____],
            ['3↓', ____, ____, ____, ____, ____, ____, ____, ____, ____, ____, '8←'],
            [____, ____, ____, ____, '3←', '2↑', '2→', '3↑', ____, ____, ____, ____],
            [____, ____, ____, ____, ____, '4←', '2→', ____, ____, ____, ____, ____],
            [____, ____, '1→', ____, ____, '1→', '2↑', ____, ____, '9↑', ____, ____]
        ])

        game_solver = YajikabeSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [_, _, _, _, _, _, _, _, _, X, X, X],
            [_, _, X, X, X, _, _, X, X, X, _, _],
            [_, _, _, _, X, _, _, X, _, X, X, _],
            [X, X, X, X, X, _, _, _, X, X, _, X],
            [X, _, X, _, _, _, _, _, _, X, X, X],
            [_, _, X, X, _, _, _, _, X, X, _, X],
            [_, X, _, X, X, X, X, _, X, _, _, X],
            [_, X, _, X, _, _, _, _, X, X, _, X],
            [_, X, X, X, X, X, X, X, X, _, _, _],
            [X, X, _, X, _, _, _, _, X, X, _, _],
            [X, _, X, X, X, _, _, _, _, X, X, _],
            [X, _, _, _, _, _, _, _, _, _, X, _]
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
