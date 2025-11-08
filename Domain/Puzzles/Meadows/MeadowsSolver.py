from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class MeadowsSolver(GameSolver):
    empty = None

    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows_number = self._grid.rows_number
        self._columns_number = self._grid.columns_number
        self._model = cp_model.CpModel()
        self._vars: Grid | None = None
        self._previous_solution: Grid | None = None

    def _init_model(self):
        # Determine domain bounds from given numbers
        given_values = [value for _, value in self._grid if value is not self.empty]
        if not given_values:
            # No numbers? empty grid has no solution in this puzzle definition
            return
        min_value = min(given_values)
        max_value = max(given_values)

        # Create IntVar grid
        self._vars = Grid([[self._model.NewIntVar(min_value, max_value, f"cell_{r}_{c}") for c in range(self._columns_number)]
                           for r in range(self._rows_number)])

        # Fix given cells
        for position, value in self._grid:
            if value is not self.empty:
                self._model.Add(self._vars[position] == value)

        # Add shape constraints
        self._add_all_shapes_are_squares_constraints()

    def get_solution(self) -> Grid:
        if self._vars is None:
            self._init_model()
        if self._vars is None:
            return Grid.empty()

        solver = cp_model.CpSolver()
        status = solver.Solve(self._model)
        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            return Grid.empty()

        solution = Grid([[solver.Value(self._vars.value(i, j)) for j in range(self._columns_number)] for i in range(self._rows_number)])
        self._previous_solution = solution
        return solution

    def get_other_solution(self):
        # Ensure we have a first solution
        if self._previous_solution is None:
            first = self.get_solution()
            self._previous_solution = first
            return first
        if self._previous_solution.is_empty():
            return Grid.empty()

        # Add constraint: at least one cell differs from previous solution
        eq_bools: list[cp_model.BoolVar] = []
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                prev_val = self._previous_solution.value(r, c)
                b_eq = self._model.NewBoolVar(f"eq_prev_{r}_{c}")
                var = self._vars.value(r, c)
                self._model.Add(var == prev_val).OnlyEnforceIf(b_eq)
                # Not equal when b_eq is false
                # Encode var != prev_val as (var <= prev_val - 1) OR (var >= prev_val + 1)
                b_le = self._model.NewBoolVar(f"le_prev_{r}_{c}")
                b_ge = self._model.NewBoolVar(f"ge_prev_{r}_{c}")
                self._model.Add(var <= prev_val - 1).OnlyEnforceIf(b_le)
                self._model.Add(var >= prev_val + 1).OnlyEnforceIf(b_ge)
                # If b_eq is false, at least one of b_le or b_ge must be true
                self._model.AddBoolOr([b_le, b_ge, b_eq])
                eq_bools.append(b_eq)
        # Not all equal
        self._model.Add(sum(eq_bools) <= self._rows_number * self._columns_number - 1)

        solver = cp_model.CpSolver()
        status = solver.Solve(self._model)
        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            return Grid.empty()

        solution = Grid([[solver.Value(self._vars.value(i, j)) for j in range(self._columns_number)] for i in range(self._rows_number)])
        self._previous_solution = solution
        return solution

    def _add_all_shapes_are_squares_constraints(self):
        for position, value in [(position, value) for position, value in self._grid if value is not self.empty]:
            self._add_square_constraint(position, value)

    def _add_square_constraint(self, position: Position, cell_value: int):
        rows = self._rows_number
        cols = self._columns_number
        pr, pc = position.r, position.c

        # Pre-filled cells different from this value
        fixed_other = [pos for pos, val in self._grid if val is not None and val != cell_value]

        min_size = 1
        max_size = min(rows, cols)

        candidates: list[cp_model.IntVar] = []
        pos_to_selectors: dict[tuple[int, int], list[cp_model.BoolVar]] = {}

        for size in range(min_size, max_size + 1):
            r0_min = max(0, position.r - size + 1)
            c0_min = max(0, position.c - size + 1)
            r0_max = min(position.r, rows - size)
            c0_max = min(position.c, cols - size)
            if r0_min > r0_max or c0_min > c0_max:
                continue

            for r0 in range(r0_min, r0_max + 1):
                r1 = r0 + size - 1
                if not (r0 <= pr <= r1):
                    continue
                for c0 in range(c0_min, c0_max + 1):
                    c1 = c0 + size - 1
                    if not (c0 <= pc <= c1):
                        continue

                    conflict = False
                    for p in fixed_other:
                        if r0 <= p.r <= r1 and c0 <= p.c <= c1:
                            conflict = True
                            break
                    if conflict:
                        continue

                    if not (r0 <= position.r <= r1 and c0 <= position.c <= c1):
                        continue

                    selector = self._model.NewBoolVar(f"sq_{cell_value}_{pr}_{pc}_{r0}_{c0}_{size}")

                    # Inside cells equal to the value when selector is true
                    for r in range(r0, r1 + 1):
                        for c in range(c0, c1 + 1):
                            pos = Position(r, c)
                            self._model.Add(self._vars[pos] == cell_value).OnlyEnforceIf(selector)
                            pos_to_selectors.setdefault((r, c), []).append(selector)

                    candidates.append(selector)

        if not candidates:
            # Impossible: no candidate squares; force infeasibility
            self._model.Add(False)
            return

        # Exactly one candidate selected
        self._model.AddExactlyOne(candidates)

        # Coverage constraints: if a cell equals this value, it must be covered by one of the selected candidates
        covered_positions = set(pos_to_selectors.keys())
        for r in range(rows):
            for c in range(cols):
                key = (r, c)
                var = self._vars.value(r, c)
                if key in covered_positions:
                    # Create b_eq: channel var == cell_value without using reified != directly
                    b_eq = self._model.NewBoolVar(f"eq_{cell_value}_{r}_{c}")
                    self._model.Add(var == cell_value).OnlyEnforceIf(b_eq)
                    # Not equal when b_eq is false via two bounds
                    b_le = self._model.NewBoolVar(f"le_{cell_value}_{r}_{c}")
                    b_ge = self._model.NewBoolVar(f"ge_{cell_value}_{r}_{c}")
                    self._model.Add(var <= cell_value - 1).OnlyEnforceIf(b_le)
                    self._model.Add(var >= cell_value + 1).OnlyEnforceIf(b_ge)
                    # If not equal then at least one of b_le or b_ge holds
                    self._model.AddBoolOr([b_le, b_ge, b_eq])
                    # b_eq -> Or(selectors)
                    self._model.AddBoolOr(pos_to_selectors[key] + [b_eq.Not()])
                else:
                    # Can never be part of this square
                    self._model.Add(var != cell_value)
