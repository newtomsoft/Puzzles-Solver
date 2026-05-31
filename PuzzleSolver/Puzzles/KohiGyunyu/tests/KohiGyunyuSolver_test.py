import unittest
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Island import Island
from PuzzleSolver.Puzzles.KohiGyunyu.KohiGyunyuSolver import KohiGyunyuSolver

W = KohiGyunyuSolver.MILK
B = KohiGyunyuSolver.COFFEE
_ = '.'

class KohiGyunyuSolverTest(unittest.TestCase):
    def test_basic_3x3(self):
        grid_str = (
            ' ·  W  · \n'
            ' B  G  W \n'
            ' ·  B  · '
        )
        expected_solution_str = (
            ' ·  ╷  · \n'
            ' ╶──┼──╴ \n'
            ' ·  ╵  · '
        )
        solver = KohiGyunyuSolver(Grid.from_str(grid_str, type(Island)))
        solution = solver.get_solution()
        other_solution = solver.get_other_solution()
        self.assertEqual(str(solution), expected_solution_str)
        self.assertTrue(other_solution.is_empty())

    def test_6x6_3e17l(self):
        """https://gridpuzzle.com/kohi-gyunyu/3e17l"""
        grid_str = (
            ' ·  ·  W  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  · \n'
            ' B  ·  G  ·  W  · \n'
            ' ·  ·  ·  ·  ·  · \n'
            ' ·  W  ·  G  ·  B \n'
            ' B  ·  ·  ·  ·  · '
        )
        expected_solution_str = (
            ' ·  ·  ╷  ·  ·  · \n'
            ' ·  ·  │  ·  ·  · \n'
            ' ┌─────┴─────╴  · \n'
            ' │  ·  ·  ·  ·  · \n'
            ' │  ╶───────────╴ \n'
            ' ╵  ·  ·  ·  ·  · '
        )

        solver = KohiGyunyuSolver(Grid.from_str(grid_str, type(Island)))
        solution = solver.get_solution()
        self.assertEqual(str(solution), expected_solution_str)
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_7x7_1nwjr(self):
        """https://gridpuzzle.com/kohi-gyunyu/1nwjr"""
        grid_str = (
            ' ·  ·  W  ·  ·  W  · \n'
            ' B  ·  ·  B  ·  ·  W \n'
            ' ·  B  ·  ·  ·  G  · \n'
            ' ·  ·  ·  ·  ·  ·  · \n'
            ' ·  G  ·  B  ·  ·  · \n'
            ' ·  ·  B  ·  ·  B  · \n'
            ' ·  W  ·  ·  W  ·  W '
        )

        expected_solution_str = (
            ' ·  ·  ╶────────┐  · \n'
            ' ╶────────┐  ·  │  ╷ \n'
            ' ·  ╷  ·  │  ·  │  │ \n'
            ' ·  │  ·  │  ·  │  │ \n'
            ' ·  ├─────┘  ·  │  │ \n'
            ' ·  │  ╶────────┘  │ \n'
            ' ·  └──────────────┘ '
        )

        solver = KohiGyunyuSolver(Grid.from_str(grid_str, type(Island)))
        solution = solver.get_solution()
        self.assertEqual(str(solution), expected_solution_str)
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_9x9_0x41w(self):
        """https://gridpuzzle.com/kohi-gyunyu/0x41w"""
        grid_str = (
            ' .  .  .  .  .  .  .  B  . \n'
            ' B  .  .  G  .  B  .  .  . \n'
            ' .  .  .  .  .  .  .  B  . \n'
            ' .  W  .  W  .  B  .  .  . \n'
            ' .  .  .  .  .  .  .  .  . \n'
            ' .  .  .  W  .  G  .  B  . \n'
            ' .  .  .  .  .  .  .  .  . \n'
            ' .  W  .  .  .  W  .  B  . \n'
            ' .  .  .  W  .  .  .  .  W '
        )

        expected_solution_str = (
            ' ·  ·  ·  ·  ·  ·  ·  ╷  · \n'
            ' ╶────────┬─────┐  ·  │  · \n'
            ' ·  ·  ·  │  ·  │  ·  │  · \n'
            ' ·  ┌─────┘  ·  ╵  ·  │  · \n'
            ' ·  │  ·  ·  ·  ·  ·  │  · \n'
            ' ·  │  ·  ┌─────┬─────┤  · \n'
            ' ·  │  ·  │  ·  │  ·  │  · \n'
            ' ·  ╵  ·  │  ·  ╵  ·  ╵  · \n'
            ' ·  ·  ·  └──────────────╴ '
        )

        solver = KohiGyunyuSolver(Grid.from_str(grid_str, type(Island)))
        solution = solver.get_solution()
        other_solution = solver.get_other_solution()
        self.assertEqual(str(solution), expected_solution_str)
        self.assertTrue(other_solution.is_empty())

    def test_12x12_1y6nd(self):
        """https://gridpuzzle.com/kohi-gyunyu/1y6nd"""
        grid_str = (
            ' B  .  B  .  .  .  .  .  .  .  .  B \n'
            ' .  .  .  .  .  .  .  .  .  .  .  . \n'
            ' G  .  W  .  G  .  .  .  B  .  .  . \n'
            ' .  .  .  .  .  .  .  .  .  W  .  G \n'
            ' W  .  .  W  .  .  G  .  W  .  .  . \n'
            ' .  .  .  .  .  .  .  B  .  .  G  . \n'
            ' B  .  .  .  G  .  B  .  .  .  .  . \n'
            ' .  .  .  .  .  .  .  B  .  .  .  . \n'
            ' .  .  .  .  .  .  .  .  .  .  .  W \n'
            ' B  .  .  .  W  .  .  .  .  .  .  . \n'
            ' .  .  .  .  .  .  B  .  W  .  W  . \n'
            ' B  .  .  .  W  .  .  .  .  W  .  . '
        )

        expected_solution_str = (
           ' ╷  ·  ╶──────────────────────────┐ \n'
           ' │  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  │ \n'
           ' │  ·  ╶─────────────────╴  ·  ·  │ \n'
           ' │  ·  ·  ·  ·  ·  ·  ·  ·  ╶─────┤ \n'
           ' ╵  ·  ·  ╶────────┬─────╴  ·  ·  │ \n'
           ' ·  ·  ·  ·  ·  ·  │  ┌────────┐  │ \n'
           ' ┌───────────┐  ·  │  │  ·  ·  │  │ \n'
           ' │  ·  ·  ·  │  ·  │  ╵  ·  ·  │  │ \n'
           ' │  ·  ·  ·  │  ·  │  ·  ·  ·  │  ╵ \n'
           ' │  ·  ·  ·  │  ·  │  ·  ·  ·  │  · \n'
           ' │  ·  ·  ·  │  ·  ╵  ·  ╶─────┘  · \n'
           ' ╵  ·  ·  ·  └──────────────╴  ·  · '
        )

        solver = KohiGyunyuSolver(Grid.from_str(grid_str, type(Island)))
        solution = solver.get_solution()
        other_solution = solver.get_other_solution()
        self.assertEqual(str(solution), expected_solution_str)
        self.assertTrue(other_solution.is_empty())

    def test_15x15_0806w(self):
        """https://gridpuzzle.com/kohi-gyunyu/0806w"""
        grid_str = (
            " .  B  .  .  W  .  B  .  G  .  .  .  W  .  B \n"
            " .  .  .  .  .  W  .  .  .  .  .  .  .  W  . \n"
            " B  .  .  .  .  .  B  .  .  G  .  W  .  .  . \n"
            " .  .  .  .  .  B  .  .  .  .  .  .  .  G  . \n"
            " .  .  .  .  G  .  .  .  .  .  .  W  .  .  . \n"
            " G  .  .  .  .  .  B  .  .  .  B  .  .  .  . \n"
            " .  .  .  .  B  .  .  .  B  .  .  W  .  .  . \n"
            " .  .  .  .  .  .  B  .  .  B  .  .  B  .  . \n"
            " .  .  .  .  .  B  .  .  W  .  B  .  .  B  . \n"
            " W  .  .  .  B  .  .  .  .  B  .  .  B  .  G \n"
            " .  .  .  .  .  .  .  .  W  .  G  .  .  W  . \n"
            " .  G  .  .  B  .  .  .  .  .  .  .  .  .  . \n"
            " .  .  .  W  .  G  .  .  W  .  .  W  .  .  W \n"
            " .  .  .  .  .  .  .  .  .  .  .  .  .  .  . \n"
            " .  W  .  W  .  .  G  .  .  W  .  .  W  .  W "
        )
        expected_solution_str = (
            ' ·  ╷  ·  ·  ╷  ·  ╶─────────────────╴  ·  ╷ \n'
            ' ·  │  ·  ·  │  ╶───────────────────────┐  │ \n'
            ' ╷  │  ·  ·  │  ·  ╶──────────────╴  ·  │  │ \n'
            ' │  │  ·  ·  │  ╶───────────────────────┤  │ \n'
            ' │  │  ·  ·  ├────────────────────┐  ·  │  │ \n'
            ' │  │  ·  ·  │  ·  ╶───────────┐  │  ·  │  │ \n'
            ' │  │  ·  ·  ├───────────╴  ·  │  ╵  ·  │  │ \n'
            ' │  │  ·  ·  │  ·  ┌────────┐  │  ·  ╷  │  │ \n'
            ' │  │  ·  ·  │  ╷  │  ·  ╷  │  │  ·  │  ╵  │ \n'
            ' ╵  │  ·  ·  ╵  │  │  ·  │  ╵  │  ·  └─────┤ \n'
            ' ·  │  ·  ·  ·  │  │  ·  └─────┴────────╴  │ \n'
            ' ·  ├────────╴  │  │  ·  ·  ·  ·  ·  ·  ·  │ \n'
            ' ·  │  ·  ╶─────┘  │  ·  ╶─────────────────┘ \n'
            ' ·  │  ·  ·  ·  ·  │  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  └─────╴  ·  ·  └───────────────────────╴ '
        )

        solver = KohiGyunyuSolver(Grid.from_str(grid_str, type(Island)))
        solution = solver.get_solution()
        self.assertEqual(str(solution), expected_solution_str)
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_18x18_08nvw(self):
        """https://gridpuzzle.com/kohi-gyunyu/08nvw"""
        grid_str = (
            ' B  .  W  .  .  .  B  .  .  G  .  .  .  .  W  .  .  W \n'
            ' .  W  .  .  .  .  .  .  B  .  .  .  .  .  .  B  .  . \n'
            ' .  .  G  .  .  .  B  .  .  .  B  .  .  .  .  .  .  G \n'
            ' .  .  .  .  .  .  .  B  .  W  .  W  .  .  W  .  .  . \n'
            ' .  .  .  .  .  B  .  .  .  .  B  .  .  B  .  .  .  G \n'
            ' G  .  .  .  .  .  B  .  .  G  .  .  B  .  .  .  .  . \n'
            ' .  G  .  W  .  .  .  G  .  .  W  .  .  .  W  .  .  W \n'
            ' .  .  .  .  .  .  W  .  .  .  .  W  .  .  .  .  .  . \n'
            ' .  .  .  W  .  G  .  .  .  .  .  .  .  .  .  .  .  W \n'
            ' .  B  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . \n'
            ' .  .  .  .  .  .  .  .  .  .  .  .  B  .  .  .  .  B \n'
            ' .  .  .  W  .  .  .  .  .  .  .  .  .  .  .  .  .  . \n'
            ' W  .  W  .  .  .  .  .  .  .  .  W  .  .  .  .  .  G \n'
            ' .  .  .  .  .  .  .  W  .  .  .  .  .  .  .  .  .  . \n'
            ' W  .  .  .  .  B  .  .  .  .  G  .  .  B  .  .  B  . \n'
            ' .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . \n'
            ' .  .  .  .  .  B  .  .  .  B  .  .  .  .  .  B  .  . \n'
            ' W  .  .  .  .  .  W  .  G  .  .  B  .  .  .  .  B  . '
        )
        expected_solution_str = (
            ' ╷  ·  ╷  ·  ·  ·  ╶───────────────────────╴  ·  ·  ╷ \n'
            ' │  ╷  │  ·  ·  ·  ·  ·  ┌────────────────────╴  ·  │ \n'
            ' │  │  ├───────────┐  ·  │  ·  ╶────────────────────┘ \n'
            ' │  │  │  ·  ·  ·  │  ╷  │  ┌──────────────╴  ·  ·  · \n'
            ' │  │  │  ·  ·  ╷  │  │  │  │  ╶────────────────────┐ \n'
            ' │  │  │  ·  ·  │  ╵  │  │  ├────────╴  ·  ·  ·  ·  │ \n'
            ' │  │  │  ╷  ·  │  ·  │  │  │  ┌───────────╴  ·  ·  │ \n'
            ' │  │  │  │  ·  │  ╷  │  │  │  │  ╷  ·  ·  ·  ·  ·  │ \n'
            ' │  │  │  ├─────┤  │  │  │  │  │  │  ·  ·  ·  ·  ·  ╵ \n'
            ' │  ╵  │  │  ·  │  │  │  │  │  │  │  ·  ·  ·  ·  ·  · \n'
            ' │  ·  │  │  ·  │  │  │  │  │  │  │  ╶──────────────┐ \n'
            ' │  ·  │  ╵  ·  │  │  │  │  │  │  │  ·  ·  ·  ·  ·  │ \n'
            ' ╵  ·  ╵  ·  ·  │  │  │  │  │  │  └─────────────────┘ \n'
            ' ·  ·  ·  ·  ·  │  │  ╵  │  │  │  ·  ·  ·  ·  ·  ·  · \n'
            ' ╷  ·  ·  ·  ·  │  │  ·  │  │  └─────────────────╴  · \n'
            ' │  ·  ·  ·  ·  │  │  ·  │  │  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' │  ·  ·  ·  ·  ╵  │  ·  │  └─────────────────╴  ·  · \n'
            ' └─────────────────┴─────┴───────────────────────╴  · '
        )

        solver = KohiGyunyuSolver(Grid.from_str(grid_str, type(Island)))
        solution = solver.get_solution()
        self.assertEqual(str(solution), expected_solution_str)
        self.assertTrue(solver.get_other_solution().is_empty())


    def test_20x20_0zp5r(self):
        """https://gridpuzzle.com/kohi-gyunyu/0zp5r"""
        grid_str = (
            ' .  .  B  .  G  .  W  .  B  .  .  B  .  .  .  .  .  .  .  B  \n'
            ' .  .  .  .  .  .  .  .  .  .  W  .  W  .  .  .  .  .  .  .  \n'
            ' .  .  .  .  .  .  .  .  .  .  .  W  .  .  W  .  .  .  .  .  \n'
            ' .  .  .  B  .  .  .  .  G  .  W  .  W  .  .  .  .  .  .  G  \n'
            ' .  .  .  .  .  .  .  .  .  B  .  G  .  .  B  .  G  .  W  .  \n'
            ' .  .  .  .  W  .  .  .  B  .  .  .  .  .  .  .  .  .  .  .  \n'
            ' .  .  .  .  .  .  .  .  .  .  .  B  .  .  .  .  W  .  .  .  \n'
            ' W  .  .  .  G  .  .  .  .  .  B  .  .  .  B  .  .  .  .  W  \n'
            ' .  B  .  G  .  .  B  .  .  .  .  .  B  .  .  .  .  B  .  .  \n'
            ' .  .  .  .  .  B  .  G  .  .  .  B  .  .  B  .  B  .  B  .  \n'
            ' .  B  .  .  .  .  .  .  .  W  .  .  G  .  .  B  .  .  .  W  \n'
            ' .  .  .  .  .  W  .  W  .  .  .  .  .  .  .  .  G  .  W  .  \n'
            ' .  .  .  .  .  .  .  .  .  .  .  W  .  .  .  G  .  .  .  .  \n'
            ' .  W  .  W  .  .  .  .  B  .  .  .  W  .  .  .  .  .  .  .  \n'
            ' W  .  W  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  \n'
            ' .  B  .  G  .  W  .  .  G  .  .  .  .  .  .  .  .  .  .  .  \n'
            ' G  .  B  .  B  .  .  .  .  .  .  G  .  .  .  W  .  .  .  .  \n'
            ' .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  W  .  .  W  \n'
            ' B  .  .  W  .  .  .  .  .  .  .  .  .  .  B  .  .  .  .  .  \n'
            ' .  .  .  .  .  .  .  .  .  W  .  B  .  B  .  G  .  .  .  W  \n'
        )
        expected_solution_str = (
            ' ·  ·  ╶───────────╴  ·  ╷  ·  ·  ╶───────────────────────┐ \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  │  ·  ┌─────╴  ·  ·  ·  ·  ·  ·  │ \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  │  ·  │  ┌────────╴  ·  ·  ·  ·  │ \n'
            ' ·  ·  ·  ╶──────────────┼─────┘  │  ╶────────────────────┤ \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  │  ╶─────┤  ·  ·  ┌─────┬─────╴  │ \n'
            ' ·  ·  ·  ·  ╷  ·  ·  ·  ╵  ·  ·  │  ·  ·  │  ·  │  ·  ·  │ \n'
            ' ·  ·  ·  ·  │  ·  ·  ·  ·  ·  ·  ╵  ·  ·  │  ·  ╵  ·  ·  │ \n'
            ' ╶───────────┼─────────────────╴  ·  ·  ·  ╵  ·  ·  ·  ·  ╵ \n'
            ' ·  ┌─────┐  │  ·  ╶─────────────────┬──────────────╴  ·  · \n'
            ' ·  │  ·  │  │  ╶─────┬───────────╴  │  ·  ┌─────┬─────╴  · \n'
            ' ·  ╵  ·  │  │  ·  ·  │  ·  ┌────────┤  ·  │  ╷  │  ·  ·  ╷ \n'
            ' ·  ·  ·  │  │  ╶─────┘  ·  │  ·  ·  │  ·  │  │  ├─────╴  │ \n'
            ' ·  ·  ·  │  │  ·  ·  ·  ·  │  ·  ╷  │  ·  │  │  │  ·  ·  │ \n'
            ' ·  ╶─────┘  │  ·  ·  ·  ╷  │  ·  │  ╵  ·  │  │  │  ·  ·  │ \n'
            ' ┌─────╴  ·  │  ·  ·  ·  │  │  ·  │  ·  ·  │  │  │  ·  ·  │ \n'
            ' │  ╶─────┐  │  ╶────────┘  │  ·  │  ·  ·  │  │  │  ·  ·  │ \n'
            ' ├─────╴  │  ╵  ·  ·  ·  ·  │  ·  │  ·  ·  │  ╵  │  ·  ·  │ \n'
            ' │  ·  ·  │  ·  ·  ·  ·  ·  │  ·  │  ·  ·  │  ·  └────────┘ \n'
            ' ╵  ·  ·  ╵  ·  ·  ·  ·  ·  │  ·  │  ·  ·  ╵  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  ╵  ·  ╵  ·  ╶─────────────────╴ '
        )

        solver = KohiGyunyuSolver(Grid.from_str(grid_str, type(Island)))
        solution = solver.get_solution()
        self.assertEqual(str(solution), expected_solution_str)
        self.assertTrue(solver.get_other_solution().is_empty())
