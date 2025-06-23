from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Yajilin.YajilinSolver import YajilinSolver

____ = ''


class YajilinSolverTests(TestCase):
    def test_solution_3x3_digit_0(self):
        grid = Grid([
            [____, ____, ____],
            [____, "0R", ____],
            [____, ____, ____],
        ])

        game_solver = YajilinSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' │  0R  │ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_0106r(self):
        #  https://gridpuzzle.com/yajilin/0106r
        grid = Grid([
            [____, ____, ____, ____, ____, '1L', ____, ____],
            [____, ____, ____, '0R', ____, ____, ____, ____],
            [____, '2R', ____, ____, ____, '1L', ____, ____],
            [____, ____, ____, ____, ____, ____, ____, ____],
            ['1U', ____, ____, ____, ____, '1L', '0D', ____],
            [____, ____, ____, '0R', ____, ____, ____, ____],
            [____, ____, ____, ____, ____, ____, ____, ____],
            ['0R', ____, ____, ____, ____, '0L', ____, ____]
        ])

        game_solver = YajilinSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ■  ┌────────┐  1L  ┌──┐ \n'
            ' ┌──┘  ■  0R  └─────┘  │ \n'
            ' │  2R  ┌──┐  ■  1L  ■  │ \n'
            ' └─────┘  │  ┌────────┘ \n'
            ' 1U  ■  ┌──┘  │  1L  0D  ■ \n'
            ' ┌─────┘  0R  └────────┐ \n'
            ' └──┐  ┌──┐  ┌─────┐  │ \n'
            ' 0R  └──┘  └──┘  0L  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12_1v8w6(self):
        #  https://gridpuzzle.com/yajilin/1v8w6
        grid = Grid([
            [____, ____, ____, ____, ____, ____, '0R', ____, ____, ____, ____, ____],
            [____, ____, ____, ____, '0L', ____, ____, ____, ____, ____, ____, ____],
            [____, '0L', ____, ____, '0L', '0R', ____, ____, ____, ____, ____, ____],
            [____, ____, ____, '0L', ____, ____, ____, ____, '0R', ____, '1L', ____],
            [____, ____, ____, ____, ____, ____, '0R', ____, ____, ____, ____, ____],
            [____, ____, ____, ____, ____, ____, '1L', ____, ____, ____, ____, ____],
            [____, ____, '0L', ____, ____, '0L', ____, ____, '0L', ____, '0L', ____],
            [____, ____, ____, ____, '0R', ____, ____, ____, ____, ____, ____, ____],
            [____, ____, '0L', ____, ____, ____, ____, ____, ____, ____, ____, ____],
            ['1U', ____, ____, ____, '0L', ____, ____, ____, '0R', ____, '0L', ____],
            [____, ____, ____, ____, ____, ____, '0R', ____, ____, ____, ____, ____],
            [____, ____, ____, ____, '0L', ____, ____, ____, ____, '1U', ____, ____]
        ])

        game_solver = YajilinSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐  ■  ┌─────┐  0R  ┌───────────┐ \n'
            ' │  └──┐  │  0L  └──┐  └──┐  ■  ┌──┘ \n'
            ' │  0L  └──┘  0L  0R  └──┐  └──┐  └──┐ \n'
            ' │  ┌──┐  0L  ┌──┐  ■  │  0R  │  1L  │ \n'
            ' └──┘  └─────┘  │  0R  └─────┘  ┌──┘ \n'
            ' ■  ┌─────┐  ┌──┘  1L  ┌─────┐  └──┐ \n'
            ' ┌──┘  0L  └──┘  0L  ┌──┘  0L  │  0L  │ \n'
            ' │  ┌─────┐  0R  ┌──┘  ┌─────┘  ┌──┘ \n'
            ' └──┘  0L  │  ■  │  ■  └─────┐  └──┐ \n'
            ' 1U  ┌─────┘  0L  └─────┐  0R  │  0L  │ \n'
            ' ┌──┘  ■  ┌─────┐  0R  └──┐  └──┐  │ \n'
            ' └────────┘  0L  └────────┘  1U  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
