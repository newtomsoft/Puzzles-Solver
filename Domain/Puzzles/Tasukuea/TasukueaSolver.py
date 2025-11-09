from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver
from Utils.ShapeGenerator import ShapeGenerator


class TasukueaSolver(GameSolver):
    empty = None
    unknown = '?'

    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows_number = self._grid.rows_number
        self._columns_number = self._grid.columns_number
        # Keep the same attribute name to minimize downstream changes
        self._grid_var: Grid = Grid.empty()  # actually CP-SAT BoolVars
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._initialized = False
        self._previous_solution: Grid | None = None
        # Lazy-built global square model structures
        self._square_selectors = None
        self._selector_areas = None
        self._coverage = None
        self._square_bounds = None
        self._squares_built = False

    def _init_solver(self):
        # Create BoolVars for each cell
        self._grid_var = Grid([[self._model.NewBoolVar(f"cell_{r}-{c}") for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])
        self._add_constraints()
        self._initialized = True

    def get_solution(self) -> Grid:
        if not self._initialized:
            self._init_solver()

        solution, _ = self._ensure_all_white_connected()
        self._previous_solution = solution
        return solution

    def _ensure_all_white_connected(self):
        proposition_count = 0
        while True:
            status = self._solver.Solve(self._model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                break
            proposition_count += 1
            current_grid = Grid([[bool(self._solver.Value(self._grid_var.value(i, j))) for j in range(self._columns_number)] for i in range(self._rows_number)])
            white_shapes = current_grid.get_all_shapes(value=False)
            if len(white_shapes) == 1:
                return current_grid, proposition_count

            biggest_white_shapes = max(white_shapes, key=len)
            white_shapes.remove(biggest_white_shapes)
            for white_shape in white_shapes:
                # Cut: not (all W white and all boundary black)
                # Encode as clause: (OR w in W: w==1) OR (OR b in B: b==0)
                w_literals = [self._grid_var[position] for position in white_shape]
                boundary_positions = [position for position in ShapeGenerator.around_shape(white_shape) if position in self._grid_var]
                b_literals = [self._grid_var[position].Not() for position in boundary_positions]
                self._model.AddBoolOr(w_literals + b_literals)

        return Grid.empty(), proposition_count

    def get_other_solution(self):
        # Forbid the previous full assignment: at least one cell differs
        if self._previous_solution is not None:
            diff_literals = []
            for position, value in self._previous_solution:
                var = self._grid_var[position]
                diff_literals.append(var if value is False else var.Not())
            self._model.AddBoolOr(diff_literals)
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_all_squares_constraints()

    def _add_initial_constraints(self):
        for position, value in self._grid:
            if value != self.empty:
                # Clue cells are forced to white (False)
                self._model.Add(self._grid_var[position] == 0)

    def _add_all_squares_constraints(self):
        # Build the global square model once
        self._build_square_model()
        # Add per-clue sum constraints only
        for position, sum_squares_area in [(position, value) for position, value in self._grid if value != self.empty]:
            self._add_squares_no_adjacent_constraint(position, sum_squares_area)

    def _build_square_model(self):
        if self._squares_built:
            return
        rows = self._rows_number
        cols = self._columns_number
        max_size = min(rows, cols)

        self._square_selectors = []  # list[BoolVar]
        self._selector_areas = dict()  # selector -> area
        self._coverage = dict()  # (r,c) -> list[BoolVar]
        self._square_bounds = []  # list of (selector, r0, c0, size)

        for size in range(1, max_size + 1):
            for r0 in range(0, rows - size + 1):
                for c0 in range(0, cols - size + 1):
                    selector = self._model.NewBoolVar(f"sq_{r0}_{c0}_{size}")
                    area = size * size
                    self._square_selectors.append(selector)
                    self._selector_areas[selector] = area
                    self._square_bounds.append((selector, r0, c0, size))

                    # selector => all cells inside are True
                    for r in range(r0, r0 + size):
                        for c in range(c0, c0 + size):
                            pos = Position(r, c)
                            key = (r, c)
                            if key not in self._coverage:
                                self._coverage[key] = []
                            self._coverage[key].append(selector)
                            self._model.AddImplication(selector, self._grid_var[pos])

        # Prune squares that aren't orthogonally adjacent to any clue
        clue_positions = [p for (p, v) in self._grid if v != self.empty]
        if clue_positions:
            for s, r0, c0, sz in self._square_bounds:
                r_min, r_max = r0, r0 + sz - 1
                c_min, c_max = c0, c0 + sz - 1
                adjacent_found = False
                for p in clue_positions:
                    for nr, nc in ((p.r - 1, p.c), (p.r + 1, p.c), (p.r, p.c - 1), (p.r, p.c + 1)):
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if r_min <= nr <= r_max and c_min <= nc <= c_max:
                                adjacent_found = True
                                break
                    if adjacent_found:
                        break
                if not adjacent_found:
                    self._model.Add(s == 0)

        # Non-overlap on cells and coverage completeness
        for r in range(rows):
            for c in range(cols):
                key = (r, c)
                selectors = self._coverage.get(key, [])
                var = self._grid_var[Position(r, c)]
                if selectors:
                    # If cell is black (True), it must come from a selected square: var => Or(selectors)
                    self._model.AddBoolOr(selectors + [var.Not()])
                    # At most one square covers a cell
                    self._model.AddAtMostOne(selectors)
                else:
                    # No square can cover this cell => force white (False)
                    self._model.Add(var == 0)

        # Forbid orthogonal edge-touching between distinct squares (diagonal touching allowed)
        n = len(self._square_bounds)
        for i in range(n):
            s1, r1, c1, sz1 = self._square_bounds[i]
            r1_min, r1_max = r1, r1 + sz1 - 1
            c1_min, c1_max = c1, c1 + sz1 - 1
            for j in range(i + 1, n):
                s2, r2, c2, sz2 = self._square_bounds[j]
                r2_min, r2_max = r2, r2 + sz2 - 1
                c2_min, c2_max = c2, c2 + sz2 - 1
                horizontal_touch = (c1_max + 1 == c2_min or c2_max + 1 == c1_min) and not (r1_max < r2_min or r2_max < r1_min)
                vertical_touch = (r1_max + 1 == r2_min or r2_max + 1 == r1_min) and not (c1_max < c2_min or c2_max < c1_min)
                if horizontal_touch or vertical_touch:
                    # Not(s1 and s2)
                    self._model.AddBoolOr([s1.Not(), s2.Not()])

        self._squares_built = True

    def _add_squares_no_adjacent_constraint(self, position: Position, sum_squares_area: int):
        # Using the globally built structures, compute the set of square selectors
        # that are adjacent (via an orthogonal neighbor cell) to this clue position.
        adjacent_positions = list(self._grid.neighbors_positions(position, mode='orthogonal'))
        adjacent_selectors = set()
        for p in adjacent_positions:
            for s in self._coverage.get((p.r, p.c), []):
                adjacent_selectors.add(s)

        if not adjacent_selectors:
            # Impossible to satisfy this clue
            self._model.Add(False)
            return

        terms = [s * self._selector_areas[s] for s in adjacent_selectors]
        if sum_squares_area != self.unknown:
            self._model.Add(sum(terms) == int(sum_squares_area))
        else:
            # Unknown clue: only enforce a non-trivial bound (strict inequalities -> use >= / <=)
            self._model.Add(sum(terms) >= 1)
            self._model.Add(sum(terms) <= self._rows_number * self._columns_number - 1)