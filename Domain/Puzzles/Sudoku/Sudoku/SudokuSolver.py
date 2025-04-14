from Domain.Board.Grid import Grid
from Domain.Ports.SolverEngine import SolverEngine
from Domain.Puzzles.GameSolver import GameSolver
from Domain.Puzzles.Sudoku.SudokuBaseSolver import SudokuBaseSolver
from Utils.utils import is_perfect_square


class SudokuSolver(SudokuBaseSolver, GameSolver):
    def __init__(self, grid: Grid, solver_engine: SolverEngine):
        super().__init__(grid, solver_engine)
        if not is_perfect_square(self.rows_number) and self.rows_number != 6 and self.rows_number != 12:
            raise ValueError("Sudoku subgrid must have size n x n or 3x2 or 4x3")
        self._init_sub_squares()

    def _add_specific_constraints(self):
        self._add_distinct_in_sub_squares_constraints()


