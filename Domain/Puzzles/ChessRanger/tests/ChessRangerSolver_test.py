import unittest

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.ChessRanger.ChessRangerSolver import ChessRangerSolver


class ChessRangerSolverTests(unittest.TestCase):
    def test_solve_simple_rook_capture(self):
        # R . P
        # . . .
        # . . .
        # Rook at (0,0) captures Pawn at (0,2)
        grid_data = [
            ['R', None, 'P'],
            [None, None, None],
            [None, None, None]
        ]
        grid = Grid(grid_data)
        solver = ChessRangerSolver(grid)
        solution = solver.get_solution()

        self.assertIsNotNone(solution)
        self.assertEqual(len(solution), 1)
        self.assertEqual(solution[0], (Position(0, 0), Position(0, 2)))

    def test_solve_two_step_capture(self):
        # R . P . P
        # R captures P1, then P2? No, R moves to P1's spot.
        # R at (0,0). P1 at (0,2). P2 at (0,4).
        # Move 1: R(0,0) -> P1(0,2). Board: . . R . P
        # Move 2: R(0,2) -> P2(0,4). Board: . . . . R
        grid_data = [
            ['R', None, 'P', None, 'P']
        ]
        grid = Grid(grid_data)
        solver = ChessRangerSolver(grid)
        solution = solver.get_solution()

        self.assertIsNotNone(solution)
        self.assertEqual(len(solution), 2)
        self.assertEqual(solution[0], (Position(0, 0), Position(0, 2)))
        self.assertEqual(solution[1], (Position(0, 2), Position(0, 4)))

    def test_knight_move(self):
        # N . .
        # . . P
        grid_data = [
            ['N', None, None],
            [None, None, 'P']
        ]
        grid = Grid(grid_data)
        solver = ChessRangerSolver(grid)
        solution = solver.get_solution()

        self.assertEqual(len(solution), 1)
        self.assertEqual(solution[0], (Position(0, 0), Position(1, 2)))

    def test_bishop_move(self):
        # B . .
        # . P .
        # . . P
        # B(0,0) -> P(1,1) -> P(2,2)
        grid_data = [
            ['B', None, None],
            [None, 'P', None],
            [None, None, 'P']
        ]
        grid = Grid(grid_data)
        solver = ChessRangerSolver(grid)
        solution = solver.get_solution()

        self.assertEqual(len(solution), 2)
        self.assertEqual(solution[0], (Position(0, 0), Position(1, 1)))
        self.assertEqual(solution[1], (Position(1, 1), Position(2, 2)))

    def test_cannot_jump(self):
        # R P P
        # Rook cannot capture the second pawn directly
        grid_data = [
            ['R', 'P', 'P']
        ]
        grid = Grid(grid_data)
        solver = ChessRangerSolver(grid)
        # R->P1, then R->P2
        solution = solver.get_solution()
        self.assertEqual(len(solution), 2)
        self.assertEqual(solution[0], (Position(0, 0), Position(0, 1)))
        self.assertEqual(solution[1], (Position(0, 1), Position(0, 2)))

    def test_no_solution(self):
        # R . .
        # . . .
        # . . P
        # Rook cannot reach P (diagonal)
        grid_data = [
            ['R', None, None],
            [None, None, None],
            [None, None, 'P']
        ]
        grid = Grid(grid_data)
        solver = ChessRangerSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(solution, [])

    def test_king_single_step(self):
        # K . P
        # King cannot reach P in one step
        grid_data = [
            ['K', None, 'P']
        ]
        grid = Grid(grid_data)
        solver = ChessRangerSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(solution, [])

        # K P
        grid_data_2 = [['K', 'P']]
        grid2 = Grid(grid_data_2)
        solver2 = ChessRangerSolver(grid2)
        sol2 = solver2.get_solution()
        self.assertEqual(len(sol2), 1)

if __name__ == '__main__':
    unittest.main()
