from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class SutoretoSolver(GameSolver):
    Empty = None
    Black = 'X'  # Black cell marker

    def __init__(self, grid: Grid):
        self.rows_number = len(grid.matrix)
        self.columns_number = len(grid.matrix[0]) if self.rows_number > 0 else 0
        self._clues = {}
        self._black_cells = set()
        
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                p = Position(r, c)
                val = grid[p]
                if val == self.Black:
                    self._black_cells.add(p)
                elif val is not self.Empty:
                    self._clues[p] = val

        self._solver = cp_model.CpSolver()
        self._model = None
        self._status = None

    def _init_model(self):
        self._model = cp_model.CpModel()
        # Sutoreto uses 1-9 like Str8ts, regardless of grid size
        min_val = 1
        max_val = 9
        
        # Create variables for each non-black cell
        self._vars = {}
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if Position(r, c) not in self._black_cells:
                    self._vars[(r, c)] = self._model.new_int_var(min_val, max_val, f'cell_{r}_{c}')
        
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._model is None:
            self._init_model()

        self._status = self._solver.solve(self._model)
        if self._status == cp_model.OPTIMAL or self._status == cp_model.FEASIBLE:
            return self._compute_solution()

        return Grid.empty()

    def get_other_solution(self) -> Grid:
        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return self.get_solution()

        # Store previous solution values
        prev_values = {}
        for (r, c), var in self._vars.items():
            prev_values[(r, c)] = self._solver.value(var)

        # Add constraint to exclude the previous solution
        diff_vars = []
        for (r, c), var in self._vars.items():
            diff_var = self._model.new_bool_var(f'diff_{r}_{c}')
            self._model.add(var != prev_values[(r, c)]).only_enforce_if(diff_var)
            diff_vars.append(diff_var)

        # At least one must be different
        self._model.add_bool_or(diff_vars)

        # Solve again
        new_status = self._solver.solve(self._model)
        if new_status == cp_model.OPTIMAL or new_status == cp_model.FEASIBLE:
            self._status = new_status
            return self._compute_solution()

        return Grid.empty()

    def _compute_solution(self) -> Grid:
        solution_matrix = [[self.Empty for _ in range(self.columns_number)] for _ in range(self.rows_number)]

        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = Position(r, c)
                if pos in self._black_cells:
                    solution_matrix[r][c] = self.Black
                elif (r, c) in self._vars:
                    solution_matrix[r][c] = self._solver.value(self._vars[(r, c)])

        return Grid(solution_matrix)

    def _add_constraints(self):
        self._add_clues_constraints()
        self._add_row_straights_constraints()
        self._add_column_straights_constraints()
        # Note: Unlike Str8ts, Sutoreto does NOT require all cells in a row/column to be different
        # Only the straights (segments) need to have unique consecutive values

    def _add_clues_constraints(self):
        for pos, val in self._clues.items():
            self._model.add(self._vars[(pos.r, pos.c)] == val)

    def _add_row_straights_constraints(self):
        """Each row segment (between black cells) must form a consecutive sequence"""
        for r in range(self.rows_number):
            segments = self._get_row_segments(r)
            for segment in segments:
                if len(segment) > 1:
                    self._add_straight_constraint(segment, is_row=True)

    def _add_column_straights_constraints(self):
        """Each column segment (between black cells) must form a consecutive sequence"""
        for c in range(self.columns_number):
            segments = self._get_column_segments(c)
            for segment in segments:
                if len(segment) > 1:
                    self._add_straight_constraint(segment, is_row=False)

    def _get_row_segments(self, row: int) -> list[list[tuple[int, int]]]:
        """Get segments of white cells in a row, separated by black cells"""
        segments = []
        current_segment = []
        for c in range(self.columns_number):
            if Position(row, c) in self._black_cells:
                if current_segment:
                    segments.append(current_segment)
                    current_segment = []
            else:
                current_segment.append((row, c))
        if current_segment:
            segments.append(current_segment)
        return segments

    def _get_column_segments(self, col: int) -> list[list[tuple[int, int]]]:
        """Get segments of white cells in a column, separated by black cells"""
        segments = []
        current_segment = []
        for r in range(self.rows_number):
            if Position(r, col) in self._black_cells:
                if current_segment:
                    segments.append(current_segment)
                    current_segment = []
            else:
                current_segment.append((r, col))
        if current_segment:
            segments.append(current_segment)
        return segments

    def _add_straight_constraint(self, segment: list[tuple[int, int]], is_row: bool):
        """Add constraint that cells in segment form a consecutive sequence (straight)"""
        if len(segment) <= 1:
            return

        vars_in_segment = [self._vars[pos] for pos in segment]
        n = len(vars_in_segment)

        # A straight of length n means: max - min = n - 1 and all values are different
        # We use: all_different + (max - min == n - 1)

        # All different
        self._model.add_all_different(vars_in_segment)

        # Create min and max variables
        min_var = self._model.new_int_var(1, 9, f'min_{"r" if is_row else "c"}_{segment[0]}')
        max_var = self._model.new_int_var(1, 9, f'max_{"r" if is_row else "c"}_{segment[0]}')

        # Min and max constraints
        for var in vars_in_segment:
            self._model.add(min_var <= var)
            self._model.add(max_var >= var)

        # max - min == n - 1
        self._model.add(max_var - min_var == n - 1)
