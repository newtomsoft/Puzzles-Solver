from collections import defaultdict

from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.LinearPathGrid import LinearPathGrid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class NumberChainSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._start_position = Position(0, 0)
        self._end_position = Position(self._grid.rows_number - 1, self._grid.columns_number - 1)
        self._start_value = self._grid[self._start_position]
        self._end_value = self._grid[self._end_position]
        self._previous_solution: Grid | None = None
        self._blocked_patterns: list[list[tuple[Position, int]]] = []

    def get_solution(self) -> Grid:
        self._blocked_patterns = []
        return self._compute_solution()

    def get_other_solution(self) -> Grid:
        if self._previous_solution is not None:
            self._blocked_patterns.append([(position, value) for position, value in self._previous_solution if value > 0])
        return self._compute_solution()

    def _compute_solution(self) -> Grid:
        while True:
            model = cp_model.CpModel()

            grid_vars = Grid([
                [model.new_int_var(-self._end_value, self._end_value, f"grid_{r}_{c}") for c in range(self.columns_number)]
                for r in range(self.rows_number)
            ])
            pos_bools = Grid([
                [model.new_bool_var(f"pos_{r}_{c}") for c in range(self.columns_number)]
                for r in range(self.rows_number)
            ])

            for (position, var) in grid_vars:
                b = pos_bools[position]
                model.Add(var >= 1).OnlyEnforceIf(b)
                model.Add(var <= 0).OnlyEnforceIf(b.Not())

            self._add_initial_constraints(model, grid_vars)
            self._add_way_cells_count_constraint(model, pos_bools)
            self._add_way_distinct_cells_constraint(model, grid_vars)
            self._add_neighbors_count_constraints(model, pos_bools, grid_vars)

            for block in self._blocked_patterns:
                if not block:
                    continue
                lits = []
                for position, value in block:
                    v = grid_vars[position]
                    eq_lit = model.new_bool_var(f"block_eq_{position.r}_{position.c}")
                    model.Add(v == value).OnlyEnforceIf(eq_lit)
                    model.Add(v != value).OnlyEnforceIf(eq_lit.Not())
                    lits.append(eq_lit)
                model.Add(sum(lits) <= len(lits) - 1)

            solver = cp_model.CpSolver()
            status = solver.Solve(model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                return Grid.empty()

            matrix_number = [
                [solver.Value(grid_vars.value(i, j)) for j in range(self.columns_number)]
                for i in range(self.rows_number)
            ]
            attempt = Grid(matrix_number)

            attempt_bool = Grid([[matrix_number[i][j] > 0 for j in range(self.columns_number)] for i in range(self.rows_number)])
            attempt_bool.set_value(self._end_position, 2)
            linear_path_grid = LinearPathGrid.from_grid_and_checkpoints(
                attempt_bool, {1: self._start_position, 2: self._end_position}
            )
            if linear_path_grid == Grid.empty():
                self._blocked_patterns.append([(position, value) for position, value in attempt if value > 0])
                continue

            self._previous_solution = attempt
            return linear_path_grid

    def _add_initial_constraints(self, model: cp_model.CpModel, grid_vars: Grid):
        model.Add(grid_vars[self._start_position] == self._start_value)
        model.Add(grid_vars[self._end_position] == self._end_value)

    def _add_neighbors_count_constraints(self, model: cp_model.CpModel, pos_bools: Grid, grid_vars: Grid):
        start_neighbors_count = sum(pos_bools.neighbors_values(self._start_position))
        model.Add(start_neighbors_count >= 1)

        end_neighbors_count = sum(pos_bools.neighbors_values(self._end_position))
        model.Add(end_neighbors_count >= 1)

        for position, _ in self._grid:
            if position == self._start_position or position == self._end_position:
                continue
            neighbors_count = sum(pos_bools.neighbors_values(position))
            model.Add(neighbors_count >= 2).OnlyEnforceIf(pos_bools[position])

    def _add_way_cells_count_constraint(self, model: cp_model.CpModel, pos_bools: Grid):
        all_bools = [b for _, b in pos_bools]
        model.Add(sum(all_bools) == self._end_value)

    def _add_way_distinct_cells_constraint(self, model: cp_model.CpModel, grid_vars: Grid):
        values_to_positions = defaultdict(list)
        for position, value in [(position, value) for position, value in self._grid if value > 0]:
            values_to_positions[value].append(position)

        for value, positions in values_to_positions.items():
            if len(positions) == 1:
                model.Add(grid_vars[positions[0]] == value)
                continue
            selectors = []
            for index, position in enumerate(positions):
                sel = model.new_bool_var(f"pick_{value}_{position.r}_{position.c}")
                v = grid_vars[position]
                model.Add(v == value).OnlyEnforceIf(sel)
                model.Add(v == -index).OnlyEnforceIf(sel.Not())
                selectors.append(sel)
            model.Add(sum(selectors) == 1)
