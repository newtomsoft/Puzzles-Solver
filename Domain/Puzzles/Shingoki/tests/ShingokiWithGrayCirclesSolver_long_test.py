import unittest

from Domain.Board.Grid import Grid
from Domain.Puzzles.Shingoki.ShingokiSolver import ShingokiSolver

# region
__ = ' '
W0 = 'w0'
W2 = 'w2'
W3 = 'w3'
W4 = 'w4'
B0 = 'b0'
B2 = 'b2'
B3 = 'b3'
B4 = 'b4'
B5 = 'b5'
B6 = 'b6'
B7 = 'b7'
B8 = 'b8'
G0 = 'g0'
G2 = 'g2'
G3 = 'g3'
G4 = 'g4'
G5 = 'g5'
G6 = 'g6'
G7 = 'g7'
# endregion


# region
__ = ' '
W0 = 'w0'
W2 = 'w2'
W3 = 'w3'
W4 = 'w4'
B0 = 'b0'
B2 = 'b2'
B3 = 'b3'
B4 = 'b4'
B5 = 'b5'
B6 = 'b6'
B7 = 'b7'
B8 = 'b8'
G0 = 'g0'
G2 = 'g2'
G3 = 'g3'
G4 = 'g4'
G5 = 'g5'
G6 = 'g6'
G7 = 'g7'


# endregion

class ShingokiWithGrayCirclesSolverLongTests(unittest.TestCase):
    # @unittest.skip("temporarily disabled - fails intermittently")  # todo reactive test
    def test_solution_12x12_all_colors_undefined_segment_len(self):
        grid = Grid([
            [B8, __, G0, __, __, __, __, __, __, G3, __, B7],
            [__, __, __, __, __, W2, W0, __, __, __, __, __],
            [__, __, __, W0, __, __, __, __, B0, __, __, __],
            [__, __, B6, __, __, __, __, __, __, W0, __, __],
            [__, W0, __, __, __, __, __, __, __, __, W0, __],
            [__, __, __, B5, __, __, __, __, B5, __, __, __],
            [W2, __, __, __, __, W0, G7, __, __, __, __, W2],
            [__, __, W0, __, __, __, __, __, __, B2, __, __],
            [__, __, __, __, __, __, __, __, __, __, __, __],
            [__, __, __, __, W3, __, __, B2, __, __, __, __],
            [G4, W3, __, __, __, __, __, __, __, __, G4, G0],
            [__, __, __, __, __, G4, G6, __, __, __, __, __]
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──────────────┐  ┌──┐  ┌────────┐ \n'
            ' │  ·  ·  ·  ·  │  │  └──┘  ·  ·  │ \n'
            ' │  ·  ┌────────┘  └──┐  ┌──┐  ·  │ \n'
            ' └──┐  └──────────────┘  │  │  ·  │ \n'
            ' ·  │  ·  ┌──────────────┘  └─────┘ \n'
            ' ┌──┘  ·  └───────────┐  ┌────────┐ \n'
            ' │  ·  ┌───────────┐  │  │  ·  ·  │ \n'
            ' └──┐  │  ·  ·  ·  │  │  └──┐  ┌──┘ \n'
            ' ·  │  │  ·  ·  ·  │  └─────┘  │  · \n'
            ' ┌──┘  └────────┐  └──┐  ·  ·  │  · \n'
            ' └────────┐  ·  │  ┌──┘  ·  ·  └──┐ \n'
            ' ·  ·  ·  └─────┘  └──────────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
