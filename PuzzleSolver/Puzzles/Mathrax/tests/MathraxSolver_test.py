import unittest
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Mathrax.MathraxSolver import MathraxSolver

_ = 0

class MathraxSolverTest(unittest.TestCase):
    def _check_solve(self, name, matrix, constraints, expected_matrix):
        grid = Grid(matrix)
        solver = MathraxSolver(grid, constraints)
        solution = solver.get_solution()

        # self.assertEqual(solution.matrix, expected_matrix)

        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution, f"More than one solution for {name}")

    def test_solve_4x4_29pg5(self):
        # https://gridpuzzle.com/mathrax/29pg5
        matrix = [
            [4, _, _, 1],
            [_, _, _, 4],
            [2, _, _, _],
            [1, _, _, 2]
        ]
        constraints = [
            {'pos': (0, 0), 'op': '+', 'val': 6},
            {'pos': (1, 0), 'op': '+', 'val': 4},
            {'pos': (2, 2), 'op': '+', 'val': 6}
        ]
        expected_matrix = [
            [4, 3, 2, 1],
            [3, 2, 1, 4],
            [2, 1, 4, 3],
            [1, 4, 3, 2]
        ]
        self._check_solve("4x4_29pg5", matrix, constraints, expected_matrix)

    def test_solve_5x5_08nvw(self):
        # https://gridpuzzle.com/mathrax/08nvw
        matrix = [
            [_, _, _, 2, 3],
            [_, 1, 5, _, _],
            [_, _, _, _, _],
            [_, _, 1, 5, _],
            [5, _, 2, 4, 1]
        ]
        constraints = [
            {'pos': (2, 2), 'op': 'O'},
            {'pos': (3, 1), 'op': '+', 'val': 4},
            {'pos': (3, 2), 'op': '-', 'val': 3}
        ]
        expected_matrix = [
            [1, 5, 4, 2, 3],
            [4, 1, 5, 3, 2],
            [2, 4, 3, 1, 5],
            [3, 2, 1, 5, 4],
            [5, 3, 2, 4, 1]
        ]
        self._check_solve("5x5_08nvw", matrix, constraints, expected_matrix)

    def test_solve_6x6_01vq2(self):
        # https://gridpuzzle.com/mathrax/01vq2
        matrix = [
            [_, 3, _, _, _, 1],
            [_, _, 6, _, 1, 3],
            [_, 4, _, _, 3, _],
            [5, _, 3, 1, _, _],
            [1, 5, 2, _, _, _],
            [_, _, _, _, _, _]
        ]
        constraints = [
            {'pos': (1, 2), 'op': '-', 'val': 4},
            {'pos': (1, 4), 'op': '+', 'val': 6},
            {'pos': (2, 3), 'op': '-', 'val': 2},
            {'pos': (3, 1), 'op': '+', 'val': 8},
            {'pos': (3, 3), 'op': '+', 'val': 7},
            {'pos': (4, 0), 'op': 'O'},
            {'pos': (4, 2), 'op': '-', 'val': 2},
            {'pos': (4, 4), 'op': 'E'}
        ]
        expected_matrix = [
            [2, 3, 4, 6, 5, 1],
            [4, 2, 6, 5, 1, 3],
            [6, 4, 1, 2, 3, 5],
            [5, 6, 3, 1, 4, 2],
            [1, 5, 2, 3, 6, 4],
            [3, 1, 5, 4, 2, 6]
        ]
        self._check_solve("6x6_01vq2", matrix, constraints, expected_matrix)

    def test_solve_7x7_0d5xr(self):
        # https://gridpuzzle.com/mathrax/0d5xr
        matrix = [
            [_, _, _, 7, _, 3, _],
            [7, 5, _, _, _, _, _],
            [6, _, 4, _, _, _, _],
            [_, 2, _, 3, 1, 4, 6],
            [_, _, 2, _, 4, _, 7],
            [_, _, _, _, 2, _, 5],
            [_, 1, _, _, 7, _, 2]
        ]
        constraints = [
            {'pos': (0, 0), 'op': '-', 'val': 3},
            {'pos': (1, 5), 'op': '+', 'val': 5},
            {'pos': (2, 5), 'op': '+', 'val': 7},
            {'pos': (3, 0), 'op': '-', 'val': 1},
            {'pos': (3, 5), 'op': '+', 'val': 11},
            {'pos': (4, 4), 'op': '-', 'val': 3}
        ]
        expected_matrix = [
            [2, 4, 5, 7, 6, 3, 1],
            [7, 5, 1, 6, 3, 2, 4],
            [6, 7, 4, 2, 5, 1, 3],
            [5, 2, 7, 3, 1, 4, 6],
            [3, 6, 2, 1, 4, 5, 7],
            [1, 3, 6, 4, 2, 7, 5],
            [4, 1, 3, 5, 7, 6, 2]
        ]
        self._check_solve("7x7_0d5xr", matrix, constraints, expected_matrix)

    def test_solve_9x9_0ww9g(self):
        # https://gridpuzzle.com/mathrax/0ww9g
        matrix = [
            [_, _, _, _, _, _, _, _, _],
            [_, _, 4, _, _, 3, _, _, _],
            [9, _, 2, _, _, _, _, _, _],
            [5, _, _, _, _, _, 4, 6, _],
            [_, 4, 8, _, 3, _, 6, 1, _],
            [_, _, 5, 8, _, _, _, _, _],
            [_, _, _, _, _, 9, 7, _, _],
            [_, _, _, _, _, _, _, _, 2],
            [_, _, _, _, 1, _, _, _, 3]
        ]
        constraints = [
            {'pos': (0, 4), 'op': '-', 'val': 4},
            {'pos': (1, 6), 'op': '+', 'val': 13},
            {'pos': (2, 2), 'op': '-', 'val': 1},
            {'pos': (2, 6), 'op': 'E'},
            {'pos': (4, 7), 'op': 'O'},
            {'pos': (6, 0), 'op': '+', 'val': 12},
            {'pos': (7, 1), 'op': 'O'}
        ]
        expected_matrix = [
            [4, 8, 3, 2, 7, 6, 1, 9, 5],
            [8, 1, 4, 7, 2, 3, 9, 5, 6],
            [9, 3, 2, 6, 5, 7, 8, 4, 1],
            [5, 2, 7, 3, 9, 1, 4, 6, 8],
            [2, 4, 8, 9, 3, 5, 6, 1, 7],
            [1, 6, 5, 8, 4, 2, 3, 7, 9],
            [3, 5, 6, 1, 8, 9, 7, 2, 4],
            [7, 9, 1, 4, 6, 8, 5, 3, 2],
            [6, 7, 9, 5, 1, 4, 2, 8, 3]
        ]
        self._check_solve("9x9_0ww9g", matrix, constraints, expected_matrix)
        
    def test_solve_9x9_plus_size_9(self):
        # https://gridpuzzle.com/mathrax-plus/size-9
        matrix = [[0 for _ in range(9)] for _ in range(9)]
        constraints = [
            {'pos': (0, 7), 'op': '*', 'val': 4},
            {'pos': (1, 0), 'op': 'O'},
            {'pos': (1, 5), 'op': '-', 'val': 2},
            {'pos': (1, 6), 'op': '+', 'val': 9},
            {'pos': (2, 1), 'op': '-', 'val': 6},
            {'pos': (3, 5), 'op': '-', 'val': 3},
            {'pos': (3, 6), 'op': '+', 'val': 16},
            {'pos': (3, 7), 'op': '-', 'val': 4},
            {'pos': (4, 2), 'op': '-', 'val': 1},
            {'pos': (5, 0), 'op': 'O'},
            {'pos': (5, 4), 'op': '+', 'val': 15},
            {'pos': (5, 5), 'op': '-', 'val': 7},
            {'pos': (5, 6), 'op': '-', 'val': 4},
            {'pos': (5, 7), 'op': '-', 'val': 3},
            {'pos': (6, 1), 'op': '-', 'val': 3},
            {'pos': (6, 7), 'op': 'O'},
            {'pos': (7, 2), 'op': '+', 'val': 9},
            {'pos': (7, 5), 'op': '-', 'val': 2}
        ]
        expected_matrix = [
            [4, 6, 5, 9, 8, 3, 7, 2, 1],
            [5, 1, 9, 8, 3, 7, 6, 4, 2],
            [9, 7, 8, 1, 2, 4, 5, 3, 6],
            [7, 2, 1, 6, 4, 5, 9, 8, 3],
            [2, 9, 3, 5, 1, 6, 8, 7, 4],
            [3, 5, 4, 2, 7, 9, 1, 6, 8],
            [1, 3, 7, 4, 6, 8, 2, 5, 9],
            [8, 4, 6, 7, 9, 2, 3, 1, 5],
            [6, 8, 2, 3, 5, 1, 4, 9, 7]
        ]
        self._check_solve("9x9_plus_size_9", matrix, constraints, expected_matrix)

    def test_solve_9x9_plus_8dmz5(self):
        # https://gridpuzzle.com/mathrax-plus/8dmz5
        matrix = [[0 for _ in range(9)] for _ in range(9)]
        constraints = [
            {'pos': (0, 0), 'op': '+', 'val': 6},
            {'pos': (0, 1), 'op': '/', 'val': 2},
            {'pos': (1, 2), 'op': '-', 'val': 5},
            {'pos': (1, 4), 'op': '-', 'val': 4},
            {'pos': (1, 7), 'op': '+', 'val': 7},
            {'pos': (2, 4), 'op': '+', 'val': 8},
            {'pos': (3, 3), 'op': '-', 'val': 2},
            {'pos': (4, 1), 'op': '-', 'val': 2},
            {'pos': (4, 2), 'op': '-', 'val': 1},
            {'pos': (4, 4), 'op': '+', 'val': 11},
            {'pos': (4, 5), 'op': '+', 'val': 10},
            {'pos': (4, 6), 'op': 'O'},
            {'pos': (5, 6), 'op': 'O'},
            {'pos': (6, 7), 'op': '-', 'val': 1},
            {'pos': (7, 1), 'op': '+', 'val': 6},
            {'pos': (7, 3), 'op': '+', 'val': 13}
        ]
        expected_matrix = [
            [5, 4, 2, 9, 1, 8, 6, 7, 3],
            [2, 1, 8, 4, 9, 3, 7, 6, 5],
            [4, 8, 9, 3, 7, 5, 2, 1, 6],
            [7, 6, 5, 2, 3, 1, 8, 9, 4],
            [8, 2, 7, 5, 4, 9, 3, 1, 6],
            [3, 9, 4, 6, 2, 7, 1, 5, 8],
            [6, 7, 1, 8, 5, 4, 9, 3, 2],
            [9, 3, 6, 7, 8, 2, 5, 4, 1],
            [1, 5, 3, 1, 6, 2, 4, 8, 7]
        ]
        self._check_solve("9x9_plus_8dmz5", matrix, constraints, expected_matrix)

if __name__ == '__main__':
    unittest.main()
