from z3 import Solver, Int, Not, And

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class TatamibariSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._initial_grid = grid
        self._rows_number = grid.rows_number
        self._columns_number = grid.columns_number
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        """Compute a solution for the current puzzle instance.
        Simple implementation: initialize solver if needed and return computed solution (or empty grid).
        """
        if not self._solver.assertions():
            self._init_solver()
        solution = self._compute_solution()
        self._previous_solution = solution
        return solution

    def get_other_solution(self) -> Grid:
        """Compute a different solution than the previous one, if any.
        Exclude the previous model from the solver and call compute again.
        If no previous solution exists, compute the first one.
        """
        if self._previous_solution is None:
            return self.get_solution()
        # Exclude the exact previous assignment of region ids if a model exists
        # We can only exclude based on current z3 vars; if _grid_z3 is not ready, initialize
        if not self._solver.assertions():
            self._init_solver()
        # Build a clause that forbids all cells to match their previous values simultaneously.
        equalities = []
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                try:
                    v = self._previous_solution.value(r, c)
                except Exception:
                    v = None
                if v is not None:
                    equalities.append(self._grid_z3.value(r, c) == v)
        if equalities:
            self._solver.add(Not(And(equalities)))
        # Compute another solution (will return empty until _compute_solution is fully implemented)
        return self._compute_solution()

    def _init_solver(self):
        """Initialize z3 variables and add base constraints.
        For now, create placeholder z3 variables and hook constraints scaffolding.
        """
        # Create an Int grid for future region ids or labels
        self._grid_z3 = Grid([[Int(f"cell_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()

    def _compute_solution(self) -> Grid:
        """Extract a Grid from the z3 model and return it as a Grid of ints.
        If the problem is unsatisfiable, return an empty Grid.
        """
        if self._grid_z3 is None:
            return Grid.empty()
        from z3 import sat
        check_result = self._solver.check()
        if check_result == sat:
            model = self._solver.model()
            solution = []
            for r in range(self._rows_number):
                row_vals = []
                for c in range(self._columns_number):
                    v = model.eval(self._grid_z3.value(r, c))
                    # Convert z3 IntNumRef to Python int; fallback to 0 if something unexpected
                    try:
                        row_vals.append(int(str(v)))
                    except Exception:
                        try:
                            row_vals.append(int(v.as_long()))
                        except Exception:
                            row_vals.append(0)
                solution.append(row_vals)
            return Grid(solution)
        return Grid.empty()

    def _add_constraints(self):
        """Add all constraints to the solver.
        For now, only call scaffolding methods without implementing their logic.
        """
        self._add_grid_bounds_constraints()
        self._add_symbols_placement_constraints()
        self._add_region_shape_constraints()
        self._add_unique_symbol_per_region_constraints()
        self._add_no_four_corners_shared_constraint()

    # ---- Constraints scaffolding methods (no implementation yet) ----
    def _add_grid_bounds_constraints(self):
        # Constrain each cell Int variable to a valid region id domain.
        # Since each region must contain exactly one symbol, there cannot be more regions than symbols.
        # Therefore, we bound region ids to [1, symbols_count], where symbols_count >= 1.
        if self._grid_z3 is None:
            return
        # Count symbols in the initial grid
        symbols_count = 0
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                val = self._initial_grid.value(r, c)
                if val in ['+', '-', '|']:
                    symbols_count += 1
        # Ensure at least one admissible id to keep domain non-empty even on malformed inputs
        max_id = symbols_count if symbols_count > 0 else 1
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                v = self._grid_z3.value(r, c)
                self._solver.add(And(v >= 1, v <= max_id))

    def _add_symbols_placement_constraints(self):
        pass

    def _add_region_shape_constraints(self):
        pass

    def _add_unique_symbol_per_region_constraints(self):
        # Each region must contain exactly one symbol. With region ids in _grid_z3 as Ints,
        # we can ensure uniqueness by forbidding two different symbol cells from sharing the same region id.
        # Collect positions of symbol cells grouped by their symbol type.
        if self._grid_z3 is None:
            return
        plus_cells = []
        minus_cells = []
        pipe_cells = []
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                val = self._initial_grid.value(r, c)
                if val == '+':
                    plus_cells.append((r, c))
                elif val == '-':
                    minus_cells.append((r, c))
                elif val == '|':
                    pipe_cells.append((r, c))
        # For any pair of symbol cells with different symbol types, enforce different region ids
        def add_all_pairs_diff(a, b):
            for (r1, c1) in a:
                for (r2, c2) in b:
                    self._solver.add(self._grid_z3.value(r1, c1) != self._grid_z3.value(r2, c2))
        add_all_pairs_diff(plus_cells, minus_cells)
        add_all_pairs_diff(plus_cells, pipe_cells)
        add_all_pairs_diff(minus_cells, pipe_cells)
        # Note: Ensuring at least one symbol per region and that symbol cells in same region share the same type
        # will be handled by other constraints (e.g., region construction constraints). This method only enforces
        # the uniqueness aspect required here.

    def _add_no_four_corners_shared_constraint(self):
        pass

