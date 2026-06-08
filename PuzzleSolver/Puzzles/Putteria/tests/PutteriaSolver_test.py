import unittest

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Putteria.PutteriaSolver import PutteriaSolver

_ = PutteriaSolver.cell_empty
x = PutteriaSolver.cross
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

class PutteriaSolverTests(unittest.TestCase):
    def test_simple_multi_solutions_2x2(self):
        regions_grid = Grid([
            [1, 1],
            [2, 2],
        ])
        clues_grid = Grid([
            [_, _],
            [_, _],
        ])

        expected_solutions = {Grid([[_, 2], [2, _], ]), Grid([[2, _], [_, 2], ])}

        solver = PutteriaSolver(regions_grid, clues_grid)
        solutions = {solver.get_solution(), solver.get_other_solution()}
        self.assertEqual(expected_solutions, solutions)
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_with_crosses(self):
        regions_grid = Grid([
            [1, 1],
            [2, 2],
        ])

        clues_grid = Grid([
            [_, x],
            [_, _],
        ])

        expected = Grid([
            [2, _],
            [_, 2],
        ])

        solver = PutteriaSolver(regions_grid, clues_grid)
        solution = solver.get_solution()
        self.assertEqual(expected, solution)
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_unsolvable(self):
        regions_grid = Grid([
            [1, 2],
            [3, 3],
        ])
        clues_grid = Grid([
            [_, _],
            [_, _],
        ])

        solver = PutteriaSolver(regions_grid, clues_grid)
        solution = solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_gridpuzzle_219n8(self):
        """https://gridpuzzle.com/putteria/219n8"""
        regions_grid = Grid([
            [1, 1, 1, 2, 2],
            [3, 3, 3, 4, 4],
            [5, 6, 7, 7, 8],
            [5, 6, 6, 9, 8],
            [5, 6, 9, 9, 8],
        ])

        clues_grid = Grid([
            [_, _, 3, _, _],
            [_, _, _, 2, _],
            [_, _, 2, _, 3],
            [_, _, _, _, _],
            [3, _, _, _, _],
        ])

        expected = Grid([
            [_, _, 3, _, 2],
            [_, 3, _, 2, _],
            [_, _, 2, _, 3],
            [_, 4, _, 3, _],
            [3, _, _, _, _],
        ])

        solver = PutteriaSolver(regions_grid, clues_grid)
        solution = solver.get_solution()
        self.assertEqual(expected, solution)
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_9x9(self):
        regions_grid = Grid([
            [1, 1, 2, 2, 2, 3, 4, 4, 5],
            [1, 1, 2, 2, 2, 3, 3, 5, 5],
            [1, 6, 7, 3, 3, 3, 8, 8, 5],
            [1, 6, 7, 7, 9, 9, 8, 8, 5],
            [6, 6, 6, 6, A, 9, B, B, C],
            [D, D, D, D, A, E, F, B, C],
            [G, H, H, D, D, E, F, F, C],
            [G, G, H, I, I, I, J, J, J],
            [G, G, H, H, H, I, I, J, J],
        ])
        clues_grid = Grid([
            [x, _, _, _, x, x, _, 2, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, x, x],
            [_, x, _, _, _, x, x, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, x, _, _, _, _, _, _],
            [_, _, _, _, x, _, _, _, _],
            [_, _, _, x, x, x, _, _, _],
        ])
        
        expected = Grid([
            [_, _, _, _, _, _, _, 2, _],
            [_, _, _, _, 6, _, _, _, 5],
            [_, _, 3, _, _, 6, _, _, _],
            [6, _, _, _, 3, _, _, 4, _],
            [_, _, _, 6, _, _, 3, _, _],
            [_, 6, _, _, 2, _, _, _, 3],
            [5, _, _, _, _, 2, _, 3, _],
            [_, _, _, 5, _, _, _, _, _],
            [_, _, 6, _, _, _, _, 5, _],
        ])
        
        solver = PutteriaSolver(regions_grid, clues_grid)
        solution = solver.get_solution()
        self.assertEqual(expected, solution)
        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

if __name__ == '__main__':
    unittest.main()
