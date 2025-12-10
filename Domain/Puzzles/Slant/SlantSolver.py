from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.SlantGrid import SlantGrid
from Domain.Puzzles.GameSolver import GameSolver


class SlantSolver(GameSolver):
    empty = None

    def __init__(self, clues_grid: Grid):
        self._clues_grid = clues_grid
        self._rows_number = clues_grid.rows_number - 1
        self._columns_number = clues_grid.columns_number - 1
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_vars = SlantGrid.empty()
        self._previous_solution = SlantGrid.empty()

    def _init_solver(self):
        self._grid_vars = SlantGrid(
            [[self._model.NewBoolVar(f'cell_{r}_{c}') for c in range(self._columns_number)] for r in
             range(self._rows_number)])
        self._add_constraints()

    def get_solution(self) -> SlantGrid:
        if self._grid_vars == SlantGrid.empty() or not self._grid_vars.matrix:
            self._init_solver()

        self._previous_solution, _ = self._ensure_no_loop()
        return self._previous_solution

    def get_other_solution(self) -> SlantGrid:
        if self._previous_solution == SlantGrid.empty():
            return SlantGrid.empty()

        blocking_clause = []
        for position, val in self._previous_solution:
            blocking_clause.append(self._grid_vars[position].Not()) if val else blocking_clause.append(self._grid_vars[position])

        self._model.AddBoolOr(blocking_clause)
        return self.get_solution()

    def _ensure_no_loop(self) -> tuple[SlantGrid, int]:
        attempt_count = 0
        while self._solver.Solve(self._model) in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            attempt_count += 1
            current_grid = SlantGrid([[bool(self._solver.Value(self._grid_vars[r][c])) for c in range(self._columns_number)] for r in range(self._rows_number)])

            loops = current_grid.get_all_loops()
            if len(loops) == 0:
                return current_grid, attempt_count

            for loop in loops:
                loop_literals = []
                for position in loop:
                    if current_grid[position]:
                        loop_literals.append(self._grid_vars[position].Not())
                    else:
                        loop_literals.append(self._grid_vars[position])
                self._model.AddBoolOr(loop_literals)

        return SlantGrid.empty(), attempt_count

    def _add_constraints(self):
        self._add_clues_constraints()
        self._add_not_minimal_loop_constraint()

    def _add_clues_constraints(self):
        for position, clue in [(position, clue) for position, clue in self._clues_grid if clue != self.empty]:
            connections = []
            if (up_left := position.up_left) in self._grid_vars:
                connections.append(self._grid_vars[up_left])
            if (up := position.up) in self._grid_vars:
                connections.append(self._grid_vars[up].Not())
            if (left := position.left) in self._grid_vars:
                connections.append(self._grid_vars[left].Not())
            if position in self._grid_vars:
                connections.append(self._grid_vars[position])

            self._model.Add(sum(connections) == clue)

    def _add_not_minimal_loop_constraint(self):
        for position, value in [(pos, val) for pos, val in self._grid_vars if pos not in self._grid_vars.edge_down_positions() + self._grid_vars.edge_right_positions()]:
            up_left = self._grid_vars[position]
            up_right = self._grid_vars[position.right]
            down_left = self._grid_vars[position.down]
            down_right = self._grid_vars[position.down_right]

            self._model.AddBoolOr([up_left, up_right.Not(), down_left.Not(), down_right])
