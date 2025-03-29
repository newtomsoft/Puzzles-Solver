import unittest

from parameterized import parameterized

from Domain.Board.Grid import Grid
from Lits.LitsSolver import LitsSolver
from Lits.LitsType import LitsType
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine


class LitsSolverTest(unittest.TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_get_solution_region_too_small(self):
        grid = Grid([
            [1, 1, 1]
        ])
        with self.assertRaises(ValueError) as context:
            LitsSolver(grid, self.get_solver_engine())

        self.assertEqual("The grid must have at least 4 cells per region", str(context.exception))

    @parameterized.expand([
        ("I horizontal", Grid([
            [1, 1, 1, 1],
            [2, 2, 2, 2],
            [2, 2, 2, 2]
        ]), Grid([
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]).get_regions()[1],
         LitsType.I.value),
        ("I vertical", Grid([
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0]
        ]), Grid([
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0]
        ]).get_regions()[1],
         LitsType.I.value),
        ("L horizontal down left", Grid([
            [1, 1, 1, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 0]
        ]), Grid([
            [1, 1, 1, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 0]
        ]).get_regions()[1],
         LitsType.L.value),
        ("L horizontal down right", Grid([
            [1, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 0]
        ]), Grid([
            [1, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 0]
        ]).get_regions()[1],
         LitsType.L.value),
        ("L horizontal up left", Grid([
            [1, 0, 0, 0, 0],
            [1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ]), Grid([
            [1, 0, 0, 0, 0],
            [1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ]).get_regions()[1],
         LitsType.L.value),
        ("L horizontal up right", Grid([
            [0, 0, 0, 0],
            [0, 0, 1, 0],
            [1, 1, 1, 0],
        ]), Grid([
            [0, 0, 0, 0],
            [0, 0, 1, 0],
            [1, 1, 1, 0],
        ]).get_regions()[1],
         LitsType.L.value),
        ("L vertical down left", Grid([
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 1, 1]
        ]), Grid([
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 1, 1]
        ]).get_regions()[1],
         LitsType.L.value),
        ("L vertical down right", Grid([
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 1, 0, 0]
        ]), Grid([
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 1, 0, 0]
        ]).get_regions()[1],
         LitsType.L.value),
        ("L vertical up left", Grid([
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1]
        ]), Grid([
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1]
        ]).get_regions()[1],
         LitsType.L.value),
        ("L vertical up right", Grid([
            [1, 1, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0]
        ]), Grid([
            [1, 1, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0]
        ]).get_regions()[1],
         LitsType.L.value),
        ("T horizontal down", Grid([
            [1, 1, 1, ''],
            ['', 1, '', ''],
            ['', '', '', '']
        ]), Grid([
            [1, 1, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0]
        ]).get_regions()[1],
         LitsType.T.value),
        ("T horizontal up", Grid([
            [0, 0, 0, 0],
            [0, 1, 0, 0],
            [1, 1, 1, 0]
        ]), Grid([
            [0, 0, 0, 0],
            [0, 1, 0, 0],
            [1, 1, 1, 0]
        ]).get_regions()[1],
         LitsType.T.value),
        ("T vertical right", Grid([
            [1, 0, 0],
            [1, 1, 0],
            [1, 0, 0],
            [0, 0, 0]
        ]), Grid([
            [1, 0, 0],
            [1, 1, 0],
            [1, 0, 0],
            [0, 0, 0]
        ]).get_regions()[1],
         LitsType.T.value),
        ("T vertical left", Grid([
            [0, 0, 1],
            [0, 1, 1],
            [0, 0, 1],
            [0, 0, 0]
        ]), Grid([
            [0, 0, 1],
            [0, 1, 1],
            [0, 0, 1],
            [0, 0, 0]
        ]).get_regions()[1],
         LitsType.T.value),
        ("S horizontal left", Grid([
            [1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]), Grid([
            [1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]).get_regions()[1],
         LitsType.S.value),
        ("S horizontal right", Grid([
            [0, 0, 1, 1],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]), Grid([
            [0, 0, 1, 1],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]).get_regions()[1],
         LitsType.S.value),
        ("S vertical left", Grid([
            [0, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1]
        ]), Grid([
            [0, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1]
        ]).get_regions()[1],
         LitsType.S.value),
        ("S vertical right", Grid([
            [0, 0, 0, 0],
            [0, 1, 0, 0],
            [1, 1, 0, 0],
            [1, 0, 0, 0]
        ]), Grid([
            [0, 0, 0, 0],
            [0, 1, 0, 0],
            [1, 1, 0, 0],
            [1, 0, 0, 0]
        ]).get_regions()[1],
         LitsType.S.value),
    ])
    def test_get_solution_region(self, name, input_grid, expected_solution_region, expected_lits_value):
        solution = LitsSolver(input_grid, self.get_solver_engine()).get_solution()
        self.assertNotEqual(Grid.empty(), solution)
        tested_region_positions = input_grid.get_regions().get(1)
        solution_region1 = frozenset([position for position in solution.get_regions().get(expected_lits_value) if position in tested_region_positions])
        self.assertEqual(expected_solution_region, solution_region1)

    def test_get_solution_when_square_forced(self):
        input_grid = Grid([
            [1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2],
        ])
        lits_solver = LitsSolver(input_grid, self.get_solver_engine())
        solution = lits_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_get_solution_when_same_lits_shape(self):
        input_grid = Grid([
            [1, 1, 1],
            [1, 1, 2],
            [2, 2, 2],
        ])
        lits_solver = LitsSolver(input_grid, self.get_solver_engine())
        solution = lits_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_6x6_normal(self):
        input_grid = Grid([
            [1, 1, 2, 2, 3, 3],
            [1, 4, 2, 2, 2, 3],
            [1, 4, 4, 4, 2, 3],
            [1, 2, 2, 2, 2, 2],
            [1, 2, 2, 5, 2, 5],
            [1, 5, 5, 5, 5, 5],
        ])
        expected_solution = Grid([
            [0, 0, 0, 0, 1, 1],
            [0, 1, 0, 0, 0, 1],
            [2, 1, 1, 1, 0, 1],
            [2, 0, 0, 3, 3, 3],
            [2, 0, 0, 0, 3, 0],
            [2, 0, 2, 2, 2, 2],
        ])
        lits_solver = LitsSolver(input_grid, self.get_solver_engine())
        solution = lits_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = lits_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_hard(self):
        input_grid = Grid([
            [1, 1, 2, 2, 2, 3],
            [1, 2, 2, 2, 3, 3],
            [1, 4, 4, 4, 4, 3],
            [1, 5, 4, 5, 3, 3],
            [5, 5, 5, 5, 6, 6],
            [6, 6, 6, 6, 6, 6],
        ])
        expected_solution = Grid([
            [1, 1, 3, 3, 3, 2],
            [1, 0, 0, 3, 0, 2],
            [1, 0, 1, 1, 1, 2],
            [0, 0, 1, 0, 0, 2],
            [2, 2, 2, 2, 0, 1],
            [0, 0, 0, 1, 1, 1],
        ])
        lits_solver = LitsSolver(input_grid, self.get_solver_engine())
        solution = lits_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = lits_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_hard(self):
        input_grid = Grid([
            [1, 1, 1, 1, 2, 2, 2, 2],
            [3, 3, 3, 3, 4, 4, 2, 2],
            [3, 5, 5, 3, 3, 4, 4, 4],
            [5, 5, 6, 3, 3, 7, 4, 4],
            [6, 6, 6, 6, 6, 7, 7, 4],
            [8, 8, 8, 8, 6, 7, 7, 9],
            [6, 6, 6, 6, 6, 6, 9, 9],
            [6, 10, 10, 10, 10, 10, 9, 9],
        ])
        expected_solution = Grid([
            [2, 2, 2, 2, 0, 3, 3, 3],
            [0, 0, 0, 3, 0, 0, 3, 0],
            [0, 4, 4, 3, 3, 1, 1, 1],
            [4, 4, 0, 3, 0, 4, 0, 1],
            [0, 0, 0, 0, 1, 4, 4, 0],
            [2, 2, 2, 2, 1, 0, 4, 1],
            [0, 0, 0, 0, 1, 1, 0, 1],
            [0, 2, 2, 2, 2, 0, 1, 1]
        ])
        lits_solver = LitsSolver(input_grid, self.get_solver_engine())
        solution = lits_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = lits_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)        

    def test_solution_10x10_hard(self):
        input_grid = Grid([
            [1, 2, 2, 2, 3, 4, 4, 4, 4, 4],
            [1, 1, 2, 3, 3, 3, 5, 6, 6, 4],
            [1, 2, 2, 3, 5, 5, 5, 5, 6, 6],
            [1, 7, 2, 2, 8, 5, 5, 5, 6, 6],
            [1, 7, 2, 2, 8, 9, 9, 9, 6, 6],
            [1, 7, 2, 8, 8, 8, 8, 9, 9, 10],
            [7, 7, 7, 8, 11, 8, 8, 12, 10, 10],
            [13, 13, 7, 11, 11, 8, 12, 12, 10, 10],
            [13, 7, 7, 11, 8, 8, 12, 14, 10, 14],
            [13, 7, 7, 11, 12, 12, 12, 14, 14, 14]
        ])
        expected_solution = Grid([
            [3, 0, 0, 0, 3, 0, 2, 2, 2, 2],
            [3, 3, 1, 3, 3, 3, 4, 0, 0, 0],
            [3, 0, 1, 0, 0, 0, 4, 4, 1, 1],
            [0, 2, 1, 1, 0, 0, 0, 4, 0, 1],
            [0, 2, 0, 0, 4, 1, 1, 1, 0, 1],
            [0, 2, 0, 4, 4, 0, 0, 1, 0, 3],
            [0, 2, 0, 4, 0, 0, 0, 4, 3, 3],
            [1, 1, 0, 1, 1, 0, 4, 4, 0, 3],
            [1, 0, 0, 1, 0, 0, 4, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 1, 1, 1]
        ])
        lits_solver = LitsSolver(input_grid, self.get_solver_engine())
        solution = lits_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = lits_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_15x15_hard(self):
        input_grid = Grid([
            [1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5, 6, 6],
            [1, 7, 8, 8, 2, 2, 9, 9, 3, 4, 4, 4, 5, 5, 6],
            [7, 7, 8, 8, 8, 10, 9, 9, 11, 11, 12, 12, 12, 5, 6],
            [7, 7, 8, 8, 10, 10, 9, 9, 11, 11, 12, 12, 13, 5, 6],
            [7, 14, 14, 10, 10, 10, 15, 15, 16, 11, 11, 12, 13, 13, 6],
            [17, 14, 14, 14, 15, 15, 15, 16, 16, 16, 18, 18, 13, 13, 6],
            [17, 14, 14, 19, 19, 19, 20, 20, 16, 18, 18, 18, 13, 6, 6],
            [17, 21, 21, 19, 19, 20, 20, 20, 22, 22, 18, 18, 23, 23, 6],
            [17, 17, 21, 21, 19, 24, 20, 22, 22, 25, 25, 25, 23, 23, 6],
            [26, 26, 21, 21, 27, 24, 24, 22, 22, 22, 25, 25, 23, 28, 28],
            [26, 26, 27, 27, 27, 24, 24, 29, 29, 30, 30, 30, 30, 28, 28],
            [31, 26, 31, 27, 32, 24, 29, 29, 33, 33, 34, 34, 30, 35, 28],
            [31, 31, 31, 31, 32, 32, 29, 29, 33, 34, 34, 34, 36, 35, 35],
            [37, 31, 31, 32, 32, 32, 32, 38, 33, 33, 34, 36, 36, 36, 35],
            [37, 37, 37, 32, 38, 38, 38, 38, 38, 38, 36, 36, 36, 35, 35]
        ])
        expected_solution = Grid([
            [1, 1, 1, 4, 4, 0, 1, 1, 1, 4, 4, 0, 0, 0, 0],
            [1, 0, 0, 0, 4, 4, 3, 0, 1, 0, 4, 4, 1, 1, 0],
            [3, 0, 1, 1, 1, 0, 3, 3, 4, 0, 0, 3, 0, 1, 0],
            [3, 3, 1, 0, 4, 4, 3, 0, 4, 4, 3, 3, 0, 1, 0],
            [3, 0, 3, 4, 4, 0, 1, 0, 0, 4, 0, 3, 0, 4, 0],
            [2, 3, 3, 0, 1, 1, 1, 3, 3, 3, 1, 1, 4, 4, 2],
            [2, 0, 3, 0, 3, 0, 3, 0, 3, 0, 1, 0, 4, 0, 2],
            [2, 1, 1, 3, 3, 0, 3, 3, 1, 0, 1, 0, 1, 1, 2],
            [2, 0, 1, 0, 3, 2, 3, 0, 1, 3, 3, 3, 1, 0, 2],
            [4, 0, 1, 0, 0, 2, 0, 1, 1, 0, 3, 0, 1, 0, 3],
            [4, 4, 3, 3, 3, 2, 0, 4, 0, 2, 2, 2, 2, 3, 3],
            [0, 4, 0, 3, 0, 2, 4, 4, 1, 1, 0, 4, 0, 0, 3],
            [2, 2, 2, 2, 1, 0, 4, 0, 1, 0, 4, 4, 0, 1, 1],
            [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 4, 0, 1, 0, 1],
            [1, 1, 1, 0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 0, 1]
        ])
        lits_solver = LitsSolver(input_grid, self.get_solver_engine())
        solution = lits_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = lits_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_20x20_hard(self):
        input_grid = Grid([
            [1, 1, 2, 2, 3, 3, 3, 3, 3, 4, 5, 6, 7, 7, 7, 8, 8, 8, 9, 9],
            [1, 2, 2, 2, 10, 10, 10, 11, 3, 4, 5, 6, 6, 12, 7, 7, 9, 8, 9, 9],
            [1, 2, 10, 10, 10, 10, 11, 11, 3, 4, 5, 5, 6, 12, 12, 12, 9, 8, 9, 13],
            [2, 2, 10, 14, 14, 14, 15, 11, 3, 4, 5, 6, 6, 6, 12, 12, 9, 9, 9, 13],
            [2, 16, 10, 10, 10, 14, 15, 15, 17, 17, 5, 6, 18, 6, 12, 9, 9, 19, 9, 13],
            [2, 16, 20, 20, 20, 14, 14, 15, 17, 17, 5, 18, 18, 21, 21, 19, 19, 19, 22, 13],
            [2, 16, 16, 20, 23, 24, 15, 15, 25, 17, 5, 18, 5, 21, 21, 19, 19, 22, 22, 13],
            [2, 16, 16, 16, 23, 24, 24, 25, 25, 5, 5, 5, 5, 21, 21, 19, 26, 26, 22, 13],
            [2, 27, 27, 23, 23, 24, 24, 25, 25, 25, 5, 28, 28, 28, 21, 19, 26, 26, 26, 13],
            [27, 27, 27, 29, 23, 23, 24, 24, 24, 30, 31, 31, 28, 28, 28, 32, 32, 26, 26, 13],
            [33, 33, 29, 29, 29, 23, 34, 30, 30, 30, 31, 31, 31, 28, 32, 32, 32, 32, 35, 35],
            [33, 33, 33, 36, 29, 30, 34, 30, 37, 37, 38, 38, 31, 39, 39, 35, 35, 35, 35, 35],
            [40, 40, 33, 36, 36, 30, 34, 30, 37, 38, 38, 38, 38, 39, 39, 35, 41, 41, 42, 42],
            [40, 33, 33, 33, 36, 30, 34, 30, 37, 43, 38, 44, 39, 39, 35, 35, 35, 41, 42, 42],
            [40, 40, 40, 33, 36, 30, 30, 30, 43, 43, 44, 44, 39, 45, 45, 35, 41, 41, 41, 42],
            [40, 46, 47, 33, 36, 36, 30, 30, 43, 43, 44, 39, 39, 48, 45, 45, 45, 45, 49, 42],
            [50, 46, 47, 47, 51, 51, 43, 43, 43, 44, 44, 52, 48, 48, 53, 45, 54, 54, 49, 42],
            [50, 46, 47, 46, 46, 51, 55, 55, 55, 55, 52, 52, 48, 48, 53, 53, 54, 49, 49, 42],
            [50, 46, 46, 46, 46, 51, 51, 56, 55, 52, 52, 52, 53, 53, 53, 54, 54, 54, 49, 42],
            [50, 50, 46, 46, 51, 51, 51, 56, 56, 56, 52, 42, 42, 42, 42, 42, 42, 42, 42, 42]
        ])
        expected_solution = Grid([
            [1, 1, 0, 0, 2, 2, 2, 2, 0, 2, 0, 4, 0, 4, 4, 0, 1, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 3, 0, 2, 0, 4, 4, 0, 4, 4, 0, 1, 0, 0],
            [1, 0, 1, 1, 0, 0, 3, 3, 0, 2, 0, 0, 4, 1, 1, 0, 0, 1, 0, 2],
            [2, 0, 1, 0, 1, 1, 0, 3, 0, 2, 0, 0, 0, 0, 1, 0, 4, 4, 0, 2],
            [2, 0, 1, 0, 0, 1, 0, 1, 0, 3, 0, 0, 4, 0, 1, 4, 4, 0, 0, 2],
            [2, 0, 3, 3, 3, 1, 0, 1, 3, 3, 0, 4, 4, 0, 4, 0, 0, 0, 3, 2],
            [2, 1, 0, 3, 0, 0, 1, 1, 0, 3, 0, 4, 0, 4, 4, 1, 1, 3, 3, 0],
            [0, 1, 1, 1, 0, 0, 0, 4, 4, 0, 1, 1, 1, 4, 0, 1, 0, 0, 3, 0],
            [0, 3, 0, 4, 4, 0, 1, 0, 4, 4, 1, 0, 0, 3, 0, 1, 4, 4, 0, 0],
            [3, 3, 3, 0, 4, 4, 1, 1, 1, 0, 0, 0, 3, 3, 3, 0, 0, 4, 4, 0],
            [0, 0, 1, 1, 1, 0, 2, 0, 0, 0, 1, 1, 1, 0, 2, 2, 2, 2, 0, 0],
            [0, 0, 0, 0, 1, 0, 2, 0, 1, 1, 3, 0, 1, 0, 0, 1, 0, 0, 0, 0],
            [2, 0, 3, 0, 2, 0, 2, 0, 1, 0, 3, 3, 0, 4, 0, 1, 0, 1, 0, 3],
            [2, 3, 3, 3, 2, 0, 2, 0, 1, 0, 3, 0, 4, 4, 1, 1, 0, 1, 3, 3],
            [2, 0, 0, 0, 2, 4, 4, 0, 3, 0, 1, 1, 4, 0, 0, 0, 1, 1, 0, 3],
            [2, 0, 3, 0, 2, 0, 4, 4, 3, 3, 1, 0, 0, 4, 3, 3, 3, 0, 2, 0],
            [0, 0, 3, 3, 1, 1, 0, 0, 3, 0, 1, 0, 4, 4, 0, 3, 0, 0, 2, 0],
            [1, 0, 3, 0, 0, 1, 2, 2, 2, 2, 3, 0, 4, 0, 1, 0, 3, 0, 2, 0],
            [1, 0, 0, 4, 4, 1, 0, 1, 0, 0, 3, 3, 1, 1, 1, 3, 3, 3, 2, 0],
            [1, 1, 4, 4, 0, 0, 0, 1, 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        lits_solver = LitsSolver(input_grid, self.get_solver_engine())
        solution = lits_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = lits_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
