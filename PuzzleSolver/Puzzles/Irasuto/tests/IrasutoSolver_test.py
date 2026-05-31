import unittest
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Irasuto.IrasutoSolver import IrasutoSolver

_ = None
w = 'w'
b = 'b'

class IrasutoSolverTests(unittest.TestCase):
    def test_solve_3x3_white(self):
        clues_grid = Grid([
            [3, _, _],
            [_, 4, _],
            [2, _, _]
        ])
        colors_grid = Grid([
            [w, w, w],
            [w, w, w],
            [w, w, w]
        ])

        expected_solution = Grid([
            [w, w, w],
            [w, w, w],
            [w, w, b]
        ])

        solver = IrasutoSolver(clues_grid, colors_grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solve_3x3_black(self):
        clues_grid = Grid([
            [3, _, _],
            [_, 4, _],
            [2, _, _]
        ])
        colors_grid = Grid([
            [b, w, w],
            [w, b, w],
            [b, w, w]
        ])

        expected_solution = Grid([
            [b, b, b],
            [b, b, b],
            [b, b, w]
        ])

        solver = IrasutoSolver(clues_grid, colors_grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solve_4x4_0y7x2(self):
        clues_grid = Grid([
            [1, _, _, 2],
            [_, 2, 1, _],
            [_, _, _, _],
            [2, _, _, 0]
        ])
        colors_grid = Grid([
            [w, w, w, b],
            [w, b, b, w],
            [w, w, w, w],
            [w, w, w, b]
        ])

        expected_solution = Grid([
            [w, b, b, b],
            [w, b, b, w],
            [b, b, w, w],
            [w, w, w, b]
        ])

        solver = IrasutoSolver(clues_grid, colors_grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solve_4x4_31p20(self):
        clues_grid = Grid([
            [0, 1, _, 0],
            [0, 0, 2, _],
            [_, 1, _, 1],
            [1, _, _, 1]
        ])
        colors_grid = Grid([
            [b, b, w, w],
            [w, w, b, w],
            [w, b, w, w],
            [w, w, w, b]
        ])

        expected_solution = Grid([
            [b, b, b, w],
            [w, w, b, b],
            [b, b, w, w],
            [w, w, b, b]
        ])

        solver = IrasutoSolver(clues_grid, colors_grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solve_10x10_1mm76_evil(self):
        clues_grid = Grid([
            [_, _, _, 2, _, _, 2, _, _, 1],
            [_, 5, _, _, _, _, _, 3, _, _],
            [2, _, _, _, 4, _, _, _, _, 3],
            [_, 1, _, 5, _, _, _, _, _, _],
            [_, _, 0, _, _, 2, _, _, _, _],
            [_, 1, _, 3, 6, _, _, 4, _, 3],
            [_, _, _, _, _, _, _, _, _, _],
            [2, _, 1, _, _, 4, _, _, 6, _],
            [_, 4, _, 0, _, _, 9, _, _, _],
            [_, _, 1, _, _, _, _, 1, _, 0]
        ])
        colors_grid = Grid([
            [w, w, w, w, w, w, b, w, w, w],
            [w, b, w, w, w, w, w, w, w, w],
            [b, w, w, w, b, w, w, w, w, w],
            [w, b, w, w, w, w, w, w, w, w],
            [w, w, b, w, w, w, w, w, w, w],
            [w, b, w, w, b, w, w, w, w, w],
            [w, w, w, w, w, w, w, w, w, w],
            [w, w, w, w, w, w, w, w, b, w],
            [w, w, w, w, w, w, w, w, w, w],
            [w, w, w, w, w, w, w, b, w, b]
        ])

        expected_solution = Grid([
            [w, b, w, w, w, b, b, b, w, w],
            [b, b, b, b, b, w, w, w, w, b],
            [b, w, b, b, b, b, w, b, w, w],
            [b, b, w, w, w, w, w, b, b, w],
            [w, w, b, w, b, w, w, b, b, w],
            [b, b, w, w, b, b, w, w, b, w],
            [b, w, b, w, b, b, w, w, b, w],
            [w, w, w, b, b, w, w, w, b, b],
            [w, w, b, w, b, w, w, w, b, w],
            [b, w, w, b, b, w, b, b, w, b]
        ])

        solver = IrasutoSolver(clues_grid, colors_grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solve_15x15_211gwy_evil(self):
        clues_grid = Grid([
            [2, _, _, 3, _, _, 3, _, 2, _, _, 2, _, _, 1],
            [_, 4, _, _, _, 0, _, _, _, 1, _, _, _, 3, _],
            [2, _, _, 2, 4, _, _, _, _, _, 3, 4, _, _, 1],
            [_, 2, _, _, _, 6, _, _, _, 3, _, _, _, 1, _],
            [_, _, _, _, _, _, 1, _, 3, _, _, _, _, _, _],
            [0, _, 1, _, _, 5, _, 5, _, 3, _, _, 2, _, 3],
            [5, _, _, _, _, _, 4, _, 2, _, _, _, _, _, 0],
            [_, _, _, 7, _, _, _, 4, _, _, _, 6, _, _, _],
            [_, _, _, _, 3, _, _, _, _, _, 9, _, _, _, _],
            [2, _, _, 2, _, 3, _, 2, _, 2, _, 0, _, _, 2],
            [_, 5, _, 1, _, _, _, 3, _, _, _, 1, _, 1, _],
            [_, 2, _, _, _, _, 2, _, 3, _, _, _, _, 1, _],
            [2, _, _, _, 3, _, _, _, _, _, 2, _, _, _, 2],
            [_, _, 0, _, _, _, 1, _, 3, _, _, _, 3, _, _],
            [0, _, 0, 0, _, _, 0, _, 0, _, _, 0, 1, _, 0]
        ])
        colors_grid = Grid([
            [w, w, w, b, w, w, b, w, b, w, w, b, w, w, b],
            [w, w, w, w, w, w, w, w, w, b, w, w, w, b, w],
            [b, w, w, b, b, w, w, w, w, w, w, w, w, w, w],
            [w, b, w, w, w, b, w, w, w, b, w, w, w, w, w],
            [w, w, w, w, w, w, w, w, b, w, w, w, w, w, w],
            [w, w, b, w, w, b, w, b, w, b, w, w, w, w, b],
            [w, w, w, w, w, w, w, w, b, w, w, w, w, w, w],
            [w, w, w, w, w, w, w, w, w, w, w, b, w, w, w],
            [w, w, w, w, w, w, w, w, w, w, b, w, w, w, w],
            [b, w, w, b, w, w, w, w, w, b, w, w, w, w, w],
            [w, w, w, b, w, w, w, b, w, w, w, w, w, w, w],
            [w, b, w, w, w, w, w, w, w, w, w, w, w, w, w],
            [w, w, w, w, w, w, w, w, w, w, w, w, w, w, b],
            [w, w, w, w, w, w, b, w, b, w, w, w, w, w, w],
            [b, w, b, w, w, w, w, w, w, w, w, b, b, w, w]
        ])

        expected_solution = Grid([
            [w, w, b, b, b, b, b, w, b, b, b, b, w, b, b],
            [w, w, w, w, b, w, b, b, w, b, w, w, b, b, w],
            [b, b, b, b, b, b, w, b, b, w, w, w, w, b, w],
            [w, b, b, w, b, b, b, b, b, b, w, w, b, w, b],
            [b, w, w, b, w, b, w, b, b, w, b, w, w, w, b],
            [w, b, b, w, b, b, w, b, w, b, b, b, w, b, b],
            [w, w, w, w, w, b, w, b, b, b, w, b, w, b, w],
            [w, w, w, w, w, b, w, w, w, w, w, b, b, b, b],
            [b, w, b, w, w, b, w, b, b, b, b, b, b, b, b],
            [b, w, b, b, b, w, w, w, w, b, b, w, b, b, w],
            [b, w, w, b, w, w, b, b, b, w, b, w, b, w, w],
            [w, b, w, b, w, w, w, b, w, w, w, w, b, w, w],
            [w, b, b, w, w, b, b, w, b, w, w, b, w, b, b],
            [w, b, w, b, b, w, b, w, b, b, b, w, w, w, b],
            [b, w, b, w, b, b, w, b, w, b, w, b, b, b, w]
        ])

        solver = IrasutoSolver(clues_grid, colors_grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
