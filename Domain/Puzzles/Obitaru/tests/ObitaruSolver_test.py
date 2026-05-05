import unittest

from Domain.Board.Grid import Grid
from Domain.Puzzles.Obitaru.ObitaruSolver import ObitaruSolver, ObitaruCell

_ = None
W = ObitaruSolver.white


class ObitaruSolverTests(unittest.TestCase):
    def test_obitaru_5x5_easy_37py9(self):
        """https://gridpuzzle.com/obitaru/37py9"""
        grid = Grid[ObitaruCell]([
            [_, W, _, _, W],
            [W, _, W, _, _],
            [_, _, _, 2, _],
            [_, _, _, _, _],
            [_, _, W, _, _],
        ])
        
        expected_solution = (
            ' ·  ┌────────┐ \n'
            ' ┌──┼──┐  ·  │ \n'
            ' │  │  │  ·  │ \n'
            ' │  └──┼─────┘ \n'
            ' └─────┘  ·  · '
        )
        solver = ObitaruSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_obitaru_5x5_no_blacks(self):
        grid = Grid([
            [W, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
        ])
        
        expected_solution = (
            ' ┌────────┐  · \n'
            ' │  ·  ·  │  · \n'
            ' │  ·  ·  │  · \n'
            ' └────────┘  · \n'
            ' ·  ·  ·  ·  · '
        )
        solver = ObitaruSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, str(solution))

    def test_obitaru_7x7_evil_15770(self):
        """https://gridpuzzle.com/obitaru/15770"""
        grid = Grid([
            [_, W, W, W, W, W, _],
            [W, _, _, W, _, _, W],
            [W, 8, _, W, _, 9, W],
            [W, _, _, W, _, _, W],
            [W, W, W, W, W, W, W],
            [W, W, _, W, _, 10, W],
            [W, W, W, W, W, W, W],
        ])
        
        expected_solution = (
            ' ┌─────┐  ┌────────┐ \n'
            ' │  ·  │  │  ·  ·  │ \n'
            ' │  ·  │  │  ·  ·  │ \n'
            ' │  ·  │  └────────┘ \n'
            ' └─────┘  ┌────────┐ \n'
            ' ┌─────┐  │  ·  ·  │ \n'
            ' └─────┘  └────────┘ '
        )
        
        solver = ObitaruSolver(grid)
        solver._solver.parameters.max_time_in_seconds = 120
        solution = solver.get_solution()
        self.assertEqual(expected_solution, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_obitaru_8x8_evil_1g0zk(self):
        """https://gridpuzzle.com/obitaru/1g0zk"""
        grid = Grid([
            [W, _, W, W, _, _, _, _],
            [W, W, W, _, 8, _, W, _],
            [_, W, W, _, W, W, W, W],
            [W, _, W, W, W, _, W, _],
            [W, 16, W, _, _, W, _, _],
            [W, _, W, W, _, W, W, W],
            [W, W, W, W, _, _, W, W],
            [_, _, W, W, W, W, _, _],
        ])
        
        expected_solution = (
            ' ┌─────┐  ┌────────┐  · \n'
            ' └─────┘  │  ·  ·  │  · \n'
            ' ┌────────┼────────┼──┐ \n'
            ' │  ·  ┌──┼─────┐  │  │ \n'
            ' │  ·  │  │  ·  │  │  │ \n'
            ' │  ·  │  └─────┼──┘  │ \n'
            ' └─────┼────────┼─────┘ \n'
            ' ·  ·  └────────┘  ·  · '
        )
        
        solver = ObitaruSolver(grid)
        solver._solver.parameters.max_time_in_seconds = 180
        solution = solver.get_solution()
        self.assertEqual(expected_solution, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
