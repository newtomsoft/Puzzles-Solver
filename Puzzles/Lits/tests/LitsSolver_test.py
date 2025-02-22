import unittest

from parameterized import parameterized

from Lits.LitsSolver import LitsSolver
from Lits.LitsType import LitsType
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine
from Utils.Grid import Grid


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

    def test_get_solution_region_4_not_compliant(self):
        grid = Grid([
            [1, 1, 1, 2],
            [2, 2, 2, 2],
            [2, 2, 1, 2]
        ])
        with self.assertRaises(ValueError) as context:
            LitsSolver(grid, self.get_solver_engine())

        self.assertEqual("The regions must have all cells connected", str(context.exception))

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


# todo ajouter tests 8x8 10x10 15x15 20x20

if __name__ == '__main__':
    unittest.main()
