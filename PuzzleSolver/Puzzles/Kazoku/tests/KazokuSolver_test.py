from unittest import TestCase
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.RegionsGrid import RegionsGrid
from PuzzleSolver.Puzzles.Kazoku.KazokuSolver import KazokuSolver

_ = None
C = KazokuSolver.Circle
U = KazokuSolver.Unknown

class KazokuSolverTests(TestCase):
    def test_kazoku_4n75p(self):
        """https://gridpuzzle.com/kazoku/4n75p"""
        numbers = Grid([
            [_, _, 1, _, _],
            [3, _, 0, _, 3],
            [_, _, 1, _, _],
            [_, _, _, _, _],
            [3, _, _, _, 1],
        ])
        circles = Grid([
            [_, C, _, C, _],
            [C, _, _, _, C],
            [C, _, C, _, C],
            [_, C, _, C, _],
            [C, _, C, _, C],
        ])

        expected_string = (
            '┌───┬─────┐\n'
            '│   ├─┬───┤\n'
            '│   ├─┤   │\n'
            '├───┴─┤   │\n'
            '│     ├───┤\n'
            '└─────┴───┘\n'
        )

        solver = KazokuSolver(numbers, circles)
        solution = solver.get_solution()
        other_solution = solver.get_other_solution()
        
        self.assertEqual(expected_string, str(solution))
        self.assertEqual(Grid.empty(), other_solution)

    def test_kazoku_lz47n(self):
        """https://gridpuzzle.com/kazoku/lz47n"""
        numbers = Grid([
            [_, U, _, _, _],
            [_, _, _, _, U],
            [_, _, U, _, 1],
            [_, 1, _, _, _],
            [_, _, _, _, _],
        ])
        circles = Grid([
            [_, _, C, C, _],
            [_, C, _, _, C],
            [C, _, C, _, _],
            [_, _, C, _, _],
            [C, _, _, C, _],
        ])

        expected_string = (
            '┌───┬─────┐\n'
            '│   │     │\n'
            '│   ├─┬───┤\n'
            '├───┤ │   │\n'
            '│   │ │   │\n'
            '└───┴─┴───┘\n'
        )

        solver = KazokuSolver(numbers, circles)
        solution = solver.get_solution()
        other_solution = solver.get_other_solution()
        
        self.assertEqual(expected_string, str(solution))
        self.assertEqual(Grid.empty(), other_solution)

    def test_kazoku_p6n1r(self):
        """https://gridpuzzle.com/kazoku/p6n1r"""
        numbers = Grid([
            [_, _, 0, _, _, U, _, _],
            [_, U, _, U, 0, _, 2, _],
            [_, _, _, _, _, _, _, _],
            [_, _, 3, _, _, U, _, _],
            [_, _, _, U, 0, _, _, _],
            [_, 4, _, _, _, _, 4, _],
            [_, _, _, _, _, _, _, _],
            [U, _, _, _, _, _, _, U],
        ])
        circles = Grid([
            [_, C, _, C, C, _, C, _],
            [C, _, C, _, _, C, _, C],
            [C, _, _, C, C, _, _, C],
            [_, C, _, _, _, _, C, _],
            [C, _, C, _, _, C, _, C],
            [_, C, _, C, C, _, C, _],
            [C, _, C, _, _, C, _, C],
            [_, C, _, C, C, _, C, _],
        ])

        expected_string = (
            '┌─┬─┬─┬─────────┐\n'
            '│ │ ├─┴─┬─┬─┬───┤\n'
            '│ ├─┴───┴─┤ │   │\n'
            '│ │       │ ├───┤\n'
            '│ ├─────┬─┤ │   │\n'
            '│ ├─────┴─┤ │   │\n'
            '│ │       │ │   │\n'
            '│ ├───────┴─┴───┤\n'
            '└─┴─────────────┘\n'
        )

        solver = KazokuSolver(numbers, circles)
        solution = solver.get_solution()
        other_solution = solver.get_other_solution()
        
        self.assertEqual(expected_string, str(solution))
        self.assertEqual(Grid.empty(), other_solution)

    def test_kazoku_nwrkk(self):
        """https://gridpuzzle.com/kazoku/nwrkk"""
        numbers = Grid([
            [_, _, _, _, 1, _, 3, _, _, _],
            [_, _, _, _, 1, U, _, _, _, _],
            [1, _, 1, _, _, _, 1, _, _, 1],
            [_, _, _, _, _, 1, _, _, _, _],
            [_, _, U, _, _, _, _, _, _, 2],
            [2, _, _, _, _, _, _, _, _, _],
            [_, _, _, U, _, _, _, 1, _, 1],
            [U, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, 1, _, _, _, 0, _],
            [U, _, _, _, _, _, _, 2, _, _],
        ])
        circles = Grid([
            [_, _, _, C, _, C, _, C, _, C],
            [_, _, _, _, _, _, _, C, _, _],
            [_, C, _, _, _, C, _, _, _, _],
            [_, _, C, _, C, _, C, _, _, C],
            [_, C, C, _, _, C, _, _, _, _],
            [_, _, _, _, C, _, _, C, _, C],
            [_, C, C, _, _, _, C, _, C, _],
            [C, _, _, C, _, _, _, _, _, C],
            [_, _, _, C, _, _, _, C, _, _],
            [_, C, _, _, _, _, C, _, C, C],
        ])
        expected_string = (
            '┌───┬───┬───┬───────┐\n'
            '│   │   ├─┬─┤       │\n'
            '│   │   │ │ ├─┬─────┤\n'
            '├───┴───┤ ├─┤ │     │\n'
            '│       │ │ │ ├─────┤\n'
            '├─────┬─┴─┴─┴─┤     │\n'
            '│     │       ├───┬─┤\n'
            '├─────┴─┬─────┴─┬─┤ │\n'
            '│       │       │ │ │\n'
            '├───────┴─────┬─┴─┴─┤\n'
            '└─────────────┴─────┘\n'
        )

        solver = KazokuSolver(numbers, circles)
        solution = solver.get_solution()
        other_solution = solver.get_other_solution()
        
        self.assertEqual(expected_string, str(solution))
        self.assertEqual(Grid.empty(), other_solution)

    def test_kazoku_1xnv9(self):
        """https://gridpuzzle.com/kazoku/1xnv9"""
        numbers = Grid([
            [2, _, _, _, _, _, _, _, _, _, _, 2],
            [_, _, _, _, _, _, 2, _, _, _, _, _],
            [_, _, _, 5, _, _, _, _, _, _, _, U],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [2, _, _, _, _, _, U, _, _, _, _, U],
            [_, U, _, _, _, _, _, _, _, 1, _, _],
            [_, _, _, _, _, _, _, _, _, 1, _, U],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, 2, _, _, _, _, _, _, _, _, _, _],
            [_, _, 1, _, _, _, U, _, 2, _, _, U],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, 2, _, _, _, _, 2, _, _, _, _, U],
        ])
        circles = Grid([
            [_, C, _, C, _, _, _, _, _, _, _, _],
            [C, _, C, _, C, _, _, C, C, _, C, C],
            [_, C, _, C, _, _, C, _, _, _, _, _],
            [C, _, C, C, _, _, _, C, _, C, _, _],
            [_, _, C, _, C, _, _, _, C, C, _, _],
            [_, _, _, _, _, _, C, _, _, _, C, C],
            [_, _, C, C, C, _, _, C, _, C, _, _],
            [_, C, _, _, _, _, _, _, C, _, C, _],
            [C, _, _, _, C, _, C, _, _, C, C, C],
            [_, C, _, _, _, C, _, _, _, _, C, _],
            [C, _, _, C, C, _, _, C, _, C, _, _],
            [_, C, _, _, _, _, _, _, _, _, C, C],
        ])
        expected_string = (
            '┌─┬─────────────────────┐\n'
            '│ ├───────────┬─────────┤\n'
            '│ ├─────┬─────┤         │\n'
            '│ │     │     ├─────────┤\n'
            '├─┤     │     │         │\n'
            '│ ├─────┴───┬─┴─────┬───┤\n'
            '│ │         ├─┬───┬─┤   │\n'
            '│ ├─────────┤ │   ├─┴───┤\n'
            '│ │         │ │   │     │\n'
            '│ ├─┬───────┤ │   │     │\n'
            '│ │ ├───────┴─┼───┴─────┤\n'
            '│ │ │         │         │\n'
            '└─┴─┴─────────┴─────────┘\n'
        )

        solver = KazokuSolver(numbers, circles)
        solution = solver.get_solution()
        other_solution = solver.get_other_solution()
        
        self.assertEqual(expected_string, str(solution))
        self.assertEqual(Grid.empty(), other_solution)

