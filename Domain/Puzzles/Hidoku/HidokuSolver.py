from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class HidokuSolver(GameSolver):
    empty = None

    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows_number = self._grid.rows_number
        self._columns_number = self._grid.columns_number
        self._model = cp_model.CpModel()
        self._grid_var = Grid.empty()
        self._previous_solution = Grid.empty()
        self.position_value_min = next((p for p, v in self._grid if v == 1), None)
        self.position_value_max = next((p for p, v in self._grid if v == self._rows_number * self._columns_number), None)
        self._init_model()

    def _init_model(self):
        self._grid_var = Grid(
            [[self._model.NewIntVar(1, self._rows_number * self._columns_number, f"grid_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)]
        )
        self._add_constraints()

    def get_solution(self) -> Grid:
        solver = cp_model.CpSolver()
        status = solver.Solve(self._model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            return self._compute_solution(solver)

        return Grid.empty()

    def get_other_solution(self) -> Grid:
        if self._previous_solution.is_empty():
            return Grid.empty()

        # Add constraint to forbid previous solution
        bool_vars = []
        for position, value in self._previous_solution:
            var = self._grid_var[position]
            # b <=> var != value
            # We enforce b is true if var != value
            # Actually we want "At least one cell differs".
            # So we create b_i for each cell. b_i is true if cell_i != old_value_i.
            # And we enforce Or(b_1, b_2, ...).

            b = self._model.NewBoolVar(f"diff_{position}")
            # If b is true, then var != value
            self._model.Add(var != value).OnlyEnforceIf(b)
            # If b is false, then var == value
            self._model.Add(var == value).OnlyEnforceIf(b.Not())
            bool_vars.append(b)

        self._model.AddBoolOr(bool_vars)

        return self.get_solution()

    def _compute_solution(self, solver) -> Grid:
        self._previous_solution = Grid(
            [
                [solver.Value(self._grid_var[Position(r, c)]) for c in range(self._columns_number)]
                for r in range(self._rows_number)
            ]
        )
        return self._previous_solution

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_distinct_number_constraints()
        self._add_neighbors_constraints()

    def _add_initial_constraints(self):
        for position, value in self._grid:
            if value == self.empty:
                self._model.Add(self._grid_var[position] > 1)
                self._model.Add(self._grid_var[position] < self._rows_number * self._columns_number)
            else:
                self._model.Add(self._grid_var[position] == value)

    def _add_distinct_number_constraints(self):
        self._model.AddAllDifferent(list(self._grid_var.values))

    def _add_neighbors_constraints(self):
        for position, value in self._grid_var:
            neighbors_values = self._grid_var.neighbors_values(position, "diagonal")
            if position != self.position_value_min:
                # Predecessor existence: Or(value == neighbor + 1)
                bools = []
                for neighbor_value in neighbors_values:
                    # b <=> value == neighbor + 1
                    b = self._model.NewBoolVar(f"pred_{position}")
                    self._model.Add(value == neighbor_value + 1).OnlyEnforceIf(b)
                    self._model.Add(value != neighbor_value + 1).OnlyEnforceIf(b.Not())
                    bools.append(b)
                self._model.AddBoolOr(bools)

            if position != self.position_value_max:
                # Successor existence: Or(value == neighbor - 1)
                bools = []
                for neighbor_value in neighbors_values:
                    # b <=> value == neighbor - 1
                    b = self._model.NewBoolVar(f"succ_{position}")
                    self._model.Add(value == neighbor_value - 1).OnlyEnforceIf(b)
                    self._model.Add(value != neighbor_value - 1).OnlyEnforceIf(b.Not())
                    bools.append(b)
                self._model.AddBoolOr(bools)
