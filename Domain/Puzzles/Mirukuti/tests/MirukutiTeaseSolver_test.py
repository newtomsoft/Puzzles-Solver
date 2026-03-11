import unittest
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Puzzles.Mirukuti.MirukutiTeaseSolver import MirukutiTeaseSolver

class MirukutiTeaseSolverTest(unittest.TestCase):
    def test_solve_5x5_31n6d(self):
        #https://gridpuzzle.com/mirukuti-tease/31n6d
        grid_str = (
            " W  ·  ·  W  B \n"
            " ·  ·  ·  ·  · \n"
            " ·  B  W  ·  · \n"
            " B  ·  ·  B  · \n"
            " ·  W  ·  ·  B "
        )
        
        expected = (
            " W──┬─────W  B \n"
            " ·  │  ·  ·  │ \n"
            " ·  B  W─────┤ \n"
            " B──┬─────B  │ \n"
            " ·  W  ·  ·  B "
        )
        
        solver = MirukutiTeaseSolver(Grid.from_str(grid_str, type(Island)))
        solution = solver.get_solution()
        self.assertEqual(str(solution), expected)
        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solve_7x7_1nwdr(self):
        # 7x7: https://gridpuzzle.com/mirukuti-tease/1nwdr
        grid_str = (
            " B  ·  W  ·  ·  ·  · \n"
            " ·  W  ·  ·  ·  ·  B \n"
            " ·  W  W  ·  ·  ·  · \n"
            " ·  ·  ·  ·  B  ·  · \n"
            " ·  W  B  ·  ·  ·  · \n"
            " B  ·  ·  ·  ·  ·  · \n"
            " W  ·  ·  ·  ·  W  · "
        )
        
        expected = (
            " B  ·  W  ·  ·  ·  · \n"
            " ├──W  ├───────────B \n"
            " │  W  W  ·  ·  ·  · \n"
            " │  ├────────B  ·  · \n"
            " │  W  B  ·  ·  ·  · \n"
            " B  ·  │  ·  ·  ·  · \n"
            " W─────┴────────W  · "
        )
        
        solver = MirukutiTeaseSolver(Grid.from_str(grid_str, type(Island)))
        solution = solver.get_solution()
        self.assertEqual(str(solution), expected)
        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solve_12x12_2985z(self):
        # https://gridpuzzle.com/mirukuti-tease/2985z
        grid_str = (
            " B  ·  ·  ·  ·  ·  B  ·  B  ·  ·  B \n"
            " ·  ·  ·  ·  W  ·  W  ·  ·  ·  ·  · \n"
            " ·  ·  ·  ·  ·  ·  ·  ·  ·  W  ·  · \n"
            " W  ·  ·  W  ·  B  W  ·  ·  W  W  B \n"
            " ·  ·  W  ·  ·  ·  ·  W  W  ·  ·  · \n"
            " ·  ·  B  B  ·  B  ·  ·  ·  B  ·  · \n"
            " ·  W  ·  ·  ·  ·  W  B  ·  ·  ·  B \n"
            " ·  ·  ·  ·  ·  B  ·  ·  B  W  ·  · \n"
            " W  ·  ·  W  ·  ·  ·  W  ·  ·  ·  · \n"
            " B  ·  ·  B  ·  ·  ·  ·  ·  ·  ·  · \n"
            " ·  W  ·  ·  W  ·  ·  B  ·  ·  ·  B \n"
            " ·  ·  B  ·  ·  B  W  ·  B  W  ·  · "
        )

        expected = (
            " B────────┬────────B  ·  B  ·  ·  B \n"
            " ·  ·  ·  │  W──┬──W  ·  │  ·  ·  │ \n"
            " ·  ·  ·  │  ·  │  ·  ·  │  W─────┤ \n"
            " W  ·  ·  W  ·  B  W─────┴──W  W  B \n"
            " │  ·  W──┬───────────W  W  ·  │  · \n"
            " ├─────B  B  ·  B────────┴──B  │  · \n"
            " │  W  ·  ·  ·  ·  W  B────────┴──B \n"
            " │  │  ·  ·  ·  B  │  ·  B  W  ·  · \n"
            " W  │  ·  W─────┤  │  W──┤  │  ·  · \n"
            " B──┴─────B  ·  │  │  ·  │  │  ·  · \n"
            " ·  W──┬─────W  │  ├──B  │  ├─────B \n"
            " ·  ·  B  ·  ·  B  W  ·  B  W  ·  · "
        )

        solver = MirukutiTeaseSolver(Grid.from_str(grid_str, type(Island)))
        solution = solver.get_solution()
        self.assertEqual(str(solution).strip(), expected.strip())
        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solve_15x15_0810w(self):
        # https://gridpuzzle.com/mirukuti-tease/0810w
        grid_str = (
            " W  ·  ·  ·  ·  W  ·  ·  ·  B  ·  W  ·  W  · \n"
            " ·  ·  B  ·  ·  ·  ·  W  ·  ·  ·  ·  B  ·  B \n"
            " W  W  B  ·  ·  ·  ·  ·  ·  B  B  ·  ·  ·  B \n"
            " B  ·  B  ·  ·  ·  ·  ·  B  ·  ·  ·  ·  ·  B \n"
            " ·  ·  ·  ·  ·  W  ·  B  ·  ·  ·  ·  B  ·  · \n"
            " B  ·  ·  ·  B  W  B  ·  ·  ·  B  ·  ·  ·  · \n"
            " ·  W  ·  B  ·  ·  ·  ·  W  ·  ·  W  ·  ·  · \n"
            " ·  ·  ·  ·  W  ·  ·  ·  W  W  ·  W  ·  ·  · \n"
            " ·  ·  ·  B  W  ·  ·  B  ·  ·  ·  ·  ·  W  · \n"
            " ·  ·  ·  B  ·  ·  ·  ·  ·  ·  ·  B  ·  ·  B \n"
            " ·  ·  W  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n"
            " ·  ·  ·  B  ·  W  ·  ·  ·  ·  B  ·  ·  W  · \n"
            " ·  W  ·  ·  ·  B  ·  ·  ·  ·  W  ·  ·  W  · \n"
            " W  ·  ·  W  W  B  ·  ·  W  B  ·  B  ·  ·  · \n"
            " ·  B  W  ·  ·  ·  ·  ·  ·  W  B  ·  ·  ·  B "
        )

        expected = (
            " W  ·  ·  ·  ·  W  ·  ·  ·  B  ·  W  ·  W  · \n"
            " ├─────B  ·  ·  │  ·  W─────┤  ·  │  B──┴──B \n"
            " W  W  B────────┤  ·  ·  ·  B  B──┴────────B \n"
            " B──┴──B  ·  ·  │  ·  ·  B──────────────┬──B \n"
            " ·  ·  ·  ·  ·  W  ·  B───────────┬──B  │  · \n"
            " B─────┬─────B  W  B─────┬─────B  │  ·  │  · \n"
            " ·  W  │  B  ·  │  ·  ·  W  ·  ·  W  ·  │  · \n"
            " ·  │  │  ├──W  │  ·  ·  W  W──┬──W  ·  │  · \n"
            " ·  │  │  B  W  ├─────B  │  ·  │  ·  ·  W  · \n"
            " ·  │  │  B──┤  │  ·  ·  │  ·  │  B─────┬──B \n"
            " ·  │  W  ·  │  │  ·  ·  │  ·  │  ·  ·  │  · \n"
            " ·  ├─────B  │  W  ·  ·  │  ·  B  ·  ·  W  · \n"
            " ·  W  ·  ·  │  B────────┤  ·  W  ·  ·  W  · \n"
            " W──┬─────W  W  B  ·  ·  W  B──┴──B  ·  │  · \n"
            " ·  B  W────────┴───────────W  B────────┴──B "
        )

        solver = MirukutiTeaseSolver(Grid.from_str(grid_str, type(Island)))
        solution = solver.get_solution()
        self.assertEqual(str(solution).strip(), expected.strip())
        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

if __name__ == '__main__':
    unittest.main()
