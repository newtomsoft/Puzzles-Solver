import unittest
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Mobiriti.MobiritiSolver import MobiritiSolver

_ = None
w = MobiritiSolver.white
b = MobiritiSolver.black

class MobiritiSolverTests(unittest.TestCase):
    def test_solve_5x5_3jnr9_easy(self):
        """https://gridpuzzle.com/mobiriti/3jnr9"""
        clues_grid = Grid([
            [_, 2, _, _, _],
            [1, _, 1, 3, _],
            [1, _, 3, _, _],
            [_, 3, _, _, _],
            [_, _, 3, _, 1]
        ])

        expected_solution = Grid([
            [w, w, w, b, w],
            [w, b, w, w, w],
            [w, w, w, w, b],
            [b, w, w, b, b],
            [b, w, w, w, w],
        ])

        solver = MobiritiSolver(clues_grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())

    def test_solve_5x5_0xz68_evil(self):
        # https://gridpuzzle.com/mobiriti/0xz68
        clues_grid = Grid([
            [_, _, _, _, _],
            [_, 1, _, 5, _],
            [_, 1, _, _, _],
            [_, _, _, 4, 1],
            [_, _, _, _, _]
        ])
        
        solver = MobiritiSolver(clues_grid)
        solution = solver.get_solution()
        print(f"\nSolution 0xz68:\n{solution}")

    def test_solve_10x10_0gwjg_hard(self):
        # https://gridpuzzle.com/mobiriti/0gwjg
        clues_grid = Grid([
            [_, _, _, 2, _, _, _, _, _, _],
            [_, _, _, _, _, 2, _, _, _, _],
            [_, 2, _, _, _, _, 3, _, _, _],
            [_, _, _, _, 4, _, _, 3, _, _],
            [_, _, _, _, _, _, 3, _, _, 3],
            [2, _, _, 2, _, _, _, _, _, _],
            [_, _, 3, _, _, 5, _, _, _, _],
            [_, _, _, 4, _, _, _, _, 5, _],
            [_, _, _, _, 2, _, _, _, _, _],
            [_, _, _, _, _, _, 5, _, _, _]
        ])
        
        solver = MobiritiSolver(clues_grid)
        solution = solver.get_solution()
        print(f"\nSolution 0gwjg:\n{solution}")

if __name__ == '__main__':
    unittest.main()
