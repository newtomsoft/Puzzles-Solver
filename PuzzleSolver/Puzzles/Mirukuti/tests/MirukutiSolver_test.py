import unittest
from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Island import Island
from PuzzleSolver.Board.IslandsGrid import IslandGrid
from PuzzleSolver.Puzzles.Mirukuti.MirukutiSolver import MirukutiSolver

W = MirukutiSolver.MILK
B = MirukutiSolver.COOKIE
_ = '.'

class MirukutiSolverTest(unittest.TestCase):
    def test_5x5_31n1r(self):
        """https://gridpuzzle.com/mirukuti/31n1r"""
        grid_str = (
            ' W  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  W \n'
            ' ·  B  ·  B  · \n'
            ' W  B  ·  ·  · \n'
            ' W  ·  ·  W  W '
        )
        expected_solution_str = (
            ' W  ·  ·  ·  · \n'
            ' │  ·  ·  ·  W \n'
            ' ├──B  ·  B──┤ \n'
            ' W  B  ·  ·  │ \n'
            ' W──┴─────W  W '
        )

        solver = MirukutiSolver(Grid.from_str(grid_str, type(Island)))
        solution = solver.get_solution()
        self.assertEqual(str(solution), expected_solution_str)
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_6x6_314z0(self):
        """https://gridpuzzle.com/mirukuti/314z0"""
        grid_str = (
            ' ·  ·  W  W  ·  · \n'
            ' ·  B  ·  ·  ·  B \n'
            ' W  ·  ·  ·  ·  W \n'
            ' ·  ·  ·  ·  ·  · \n'
            ' ·  B  ·  ·  B  · \n'
            ' W  ·  W  W  ·  W '
        )

        expected_solution_str = (
            ' ·  ·  W  W  ·  · \n'
            ' ·  B──┤  ├─────B \n'
            ' W  ·  │  │  ·  W \n'
            ' │  ·  │  │  ·  │ \n'
            ' ├──B  │  │  B──┤ \n'
            ' W  ·  W  W  ·  W '
        )

        solver = MirukutiSolver(Grid.from_str(grid_str, type(Island)))
        solution = solver.get_solution()
        self.assertEqual(str(solution), expected_solution_str)
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_7x7_gridpuzzle_example(self):
        grid_str = (
            ' ·  ·  W  ·  ·  ·  W \n'
            ' ·  B  ·  W  ·  ·  · \n'
            ' ·  ·  ·  ·  B  ·  · \n'
            ' ·  ·  ·  ·  ·  W  · \n'
            ' ·  ·  W  ·  B  ·  · \n'
            ' B  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  W  ·  W  W '
        )

        expected_solution_str = (
            ' ·  ·  W  ·  ·  ·  W \n'
            ' ·  B──┤  W  ·  ·  │ \n'
            ' ·  ·  │  │  B─────┤ \n'
            ' ·  ·  │  │  ·  W  │ \n'
            ' ·  ·  W  │  B──┤  │ \n'
            ' B────────┤  ·  │  │ \n'
            ' ·  ·  ·  W  ·  W  W '
        )

        solver = MirukutiSolver(Grid.from_str(grid_str, type(Island)))
        solution = solver.get_solution()
        self.assertEqual(str(solution), expected_solution_str)
        self.assertTrue(solver.get_other_solution().is_empty())


    def test_7x7_1npy9(self):
        """https://gridpuzzle.com/mirukuti/1npy9"""
        grid_str = (
            ' ·  ·  ·  ·  B  ·  · \n'
            ' ·  ·  W  ·  ·  ·  W \n'
            ' W  ·  ·  ·  W  ·  W \n'
            ' ·  W  ·  ·  ·  ·  · \n'
            ' B  ·  ·  ·  ·  ·  · \n'
            ' ·  W  ·  ·  B  ·  · \n'
            ' ·  ·  B  ·  ·  ·  W '
        )

        expected_solution_str = (
           ' ·  ·  ·  ·  B  ·  · \n'
           ' ·  ·  W─────┴─────W \n'
           ' W─────┬─────W  ·  W \n'
           ' ·  W  │  ·  ·  ·  │ \n'
           ' B──┤  │  ·  ·  ·  │ \n'
           ' ·  W  │  ·  B─────┤ \n'
           ' ·  ·  B  ·  ·  ·  W '
        )

        solver = MirukutiSolver(Grid.from_str(grid_str, type(Island)))
        solution = solver.get_solution()
        self.assertEqual(str(solution), expected_solution_str)
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_12x12_0yw62(self):
        """https://gridpuzzle.com/mirukuti/0yw62"""
        grid_str = (
            ' ·  W  ·  ·  ·  W  ·  ·  B  ·  W  · \n'
            ' ·  ·  B  ·  B  ·  W  ·  ·  W  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  B  ·  ·  · \n'
            ' ·  ·  W  ·  ·  ·  ·  ·  W  ·  ·  · \n'
            ' ·  ·  W  ·  B  W  ·  ·  W  ·  ·  · \n'
            ' B  ·  ·  ·  ·  ·  B  ·  ·  W  W  W \n'
            ' ·  ·  W  ·  ·  ·  ·  ·  ·  ·  B  · \n'
            ' ·  W  ·  ·  ·  W  B  ·  ·  ·  ·  · \n'
            ' W  W  ·  ·  ·  ·  W  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  B  ·  ·  ·  W  ·  W \n'
            ' ·  ·  ·  ·  B  ·  ·  ·  B  ·  ·  · \n'
            ' W  ·  ·  ·  ·  W  ·  ·  ·  ·  ·  W '
        )
        expected_solution_str = (
            ' ·  W──┬────────W  ·  ·  B  ·  W  · \n'
            ' ·  ·  B  ·  B  ·  W─────┴──W  │  · \n'
            ' ·  ·  ·  ·  │  ·  ·  ·  B─────┤  · \n'
            ' ·  ·  W─────┴───────────W  ·  │  · \n'
            ' ·  ·  W  ·  B  W──┬─────W  ·  │  · \n'
            ' B─────┤  ·  │  ·  B  ·  ·  W  W  W \n'
            ' ·  ·  W  ·  │  ·  ·  ·  ·  │  B──┤ \n'
            ' ·  W────────┴──W  B────────┤  ·  │ \n'
            ' W  W───────────┬──W  ·  ·  │  ·  │ \n'
            ' │  ·  ·  ·  ·  B  ·  ·  ·  W  ·  W \n'
            ' ├───────────B  ·  ·  ·  B  ·  ·  · \n'
            ' W  ·  ·  ·  ·  W────────┴────────W '
        )
        solver = MirukutiSolver(Grid.from_str(grid_str, type(Island)))
        solution = solver.get_solution()
        self.assertEqual(str(solution), expected_solution_str)
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_15x15_45gr5(self):
        """https://gridpuzzle.com/mirukuti/45gr5"""
        grid_str = (
            ' ·  ·  W  ·  ·  ·  W  W  ·  B  ·  ·  ·  ·  W \n'
            ' B  ·  ·  W  ·  W  ·  ·  W  ·  W  B  ·  ·  · \n'
            ' ·  ·  ·  ·  B  W  ·  ·  ·  ·  B  ·  ·  B  · \n'
            ' ·  ·  ·  B  ·  ·  ·  W  W  ·  W  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  B  ·  B  ·  ·  ·  ·  · \n'
            ' ·  ·  W  ·  ·  W  ·  W  ·  ·  ·  ·  ·  W  · \n'
            ' W  ·  ·  ·  ·  W  ·  ·  W  ·  W  ·  W  ·  W \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  B  ·  B  · \n'
            ' ·  ·  ·  ·  ·  B  ·  ·  ·  ·  W  ·  W  ·  · \n'
            ' W  ·  ·  B  ·  ·  W  ·  ·  B  ·  ·  B  ·  · \n'
            ' ·  W  ·  ·  ·  ·  ·  ·  ·  W  W  ·  ·  ·  · \n'
            ' ·  ·  B  W  ·  ·  ·  ·  ·  W  B  ·  ·  ·  · \n'
            ' ·  W  ·  ·  W  ·  B  W  ·  ·  ·  ·  W  ·  · \n'
            ' W  ·  ·  B  B  W  ·  ·  W  W  ·  ·  ·  ·  W \n'
            ' W  ·  ·  ·  ·  ·  W  B  ·  ·  ·  ·  ·  ·  · '
        )
        expected_solution_str = (
            ' ·  ·  W  ·  ·  ·  W  W  ·  B  ·  ·  ·  ·  W \n'
            ' B─────┤  W──┬──W  │  │  W──┴──W  B  ·  ·  │ \n'
            ' ·  ·  │  ·  B  W  │  ├────────B  │  ·  B──┤ \n'
            ' ·  ·  │  B─────┤  │  W  W──┬──W  │  ·  ·  │ \n'
            ' ·  ·  │  ·  ·  │  ├──B  ·  B  ·  │  ·  ·  │ \n'
            ' ·  ·  W  ·  ·  W  │  W───────────┴─────W  │ \n'
            ' W────────┬─────W  │  ·  W──┬──W  ·  W  ·  W \n'
            ' ·  ·  ·  │  ·  ·  │  ·  ·  │  ·  B──┤  B  · \n'
            ' ·  ·  ·  │  ·  B  │  ·  ·  │  W  ·  W  │  · \n'
            ' W  ·  ·  B  ·  │  W  ·  ·  B  ├─────B  │  · \n'
            ' │  W───────────┴───────────W  W  ·  ·  │  · \n'
            ' ├─────B  W────────┬────────W  B  ·  ·  │  · \n'
            ' │  W─────┬──W  ·  B  W────────┴─────W  │  · \n'
            ' W  ·  ·  B  B  W─────┬──W  W───────────┴──W \n'
            ' W───────────┴─────W  B  ·  ·  ·  ·  ·  ·  · '
        )
        solver = MirukutiSolver(Grid.from_str(grid_str, type(Island)))
        solution = solver.get_solution()
        self.assertEqual(str(solution), expected_solution_str)
        self.assertTrue(solver.get_other_solution().is_empty())
