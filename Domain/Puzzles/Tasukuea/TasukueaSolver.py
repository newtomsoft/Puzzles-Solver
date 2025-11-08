from z3 import Solver, Not, And, Bool, Implies, Or, sat, is_true, If, Sum, AtMost

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
        self._grid_z3: Grid = Grid.empty()
        self._solver = Solver()
        self._previous_solution: Grid | None = None
        # Lazy-built global square model structures
        self._square_selectors = None
        self._selector_areas = None
        self._coverage = None
        self._square_bounds = None
        self._squares_built = False

    def _init_solver(self):
        self._grid_z3 = Grid([[Bool(f"cell_{r}-{c}") for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.assertions():
            self._init_solver()

        solution, _ = self._ensure_all_white_connected()
        self._previous_solution = solution
        return solution

    def _ensure_all_white_connected(self):
        proposition_count = 0
        while self._solver.check() == sat:
            model = self._solver.model()
            proposition_count += 1
            current_grid = Grid([[is_true(model.eval(self._grid_z3.value(i, j))) for j in range(self._columns_number)] for i in range(self._rows_number)])
            white_shapes = current_grid.get_all_shapes(value=False)
            if len(white_shapes) == 1:
                return current_grid, proposition_count

            biggest_white_shapes = max(white_shapes, key=len)
            white_shapes.remove(biggest_white_shapes)
            for white_shape in white_shapes:
                in_all_with = And([Not(self._grid_z3[position]) for position in white_shape])
                around_all_black = And([self._grid_z3[position] for position in ShapeGenerator.around_shape(white_shape) if position in self._grid_z3])
                constraint = Not(And(around_all_black, in_all_with))
                self._solver.add(constraint)

        return Grid.empty(), proposition_count

    def get_other_solution(self):
        constraints = []
        for position, value in self._previous_solution:
            constraints.append(self._grid_z3[position] == value)
        self._solver.add(Not(And(constraints)))
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_all_squares_constraints()

    def _add_initial_constraints(self):
        for position, value in self._grid:
            if value != self.empty:
                self._solver.add(Not(self._grid_z3[position]))

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

        self._square_selectors = []  # list[Bool]
        self._selector_areas = dict()  # selector -> area
        self._coverage = dict()  # (r,c) -> list[Bool]
        self._square_bounds = []  # list of (selector, r0, c0, size)

        for size in range(1, max_size + 1):
            for r0 in range(0, rows - size + 1):
                for c0 in range(0, cols - size + 1):
                    selector = Bool(f"sq_{r0}_{c0}_{size}")
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
                            self._solver.add(Implies(selector, self._grid_z3[pos]))

        # Prune squares that aren't orthogonally adjacent to any clue
        clue_positions = [p for (p, v) in self._grid if v != self.empty]
        if clue_positions:
            for s, r0, c0, sz in self._square_bounds:
                r_min, r_max = r0, r0 + sz - 1
                c_min, c_max = c0, c0 + sz - 1
                adjacent_literals = []
                for p in clue_positions:
                    for nr, nc in ((p.r - 1, p.c), (p.r + 1, p.c), (p.r, p.c - 1), (p.r, p.c + 1)):
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if r_min <= nr <= r_max and c_min <= nc <= c_max:
                                adjacent_literals.append(True)
                if not adjacent_literals:
                    self._solver.add(Not(s))

        # Non-overlap on cells and coverage completeness
        for r in range(rows):
            for c in range(cols):
                key = (r, c)
                selectors = self._coverage.get(key, [])
                if selectors:
                    # If cell is black (True), must come from a selected square
                    self._solver.add(Implies(self._grid_z3[Position(r, c)], Or(selectors)))
                    # At most one square covers a cell
                    self._solver.add(AtMost(*(selectors + [1])))
                else:
                    # No square can cover this cell => force white (False)
                    self._solver.add(Not(self._grid_z3[Position(r, c)]))

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
                    self._solver.add(Not(And(s1, s2)))

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
            self._solver.add(False)
            return

        terms = [If(s, self._selector_areas[s], 0) for s in adjacent_selectors]
        if sum_squares_area != self.unknown:
            self._solver.add(Sum(terms) == sum_squares_area)
        else:
            # Unknown clue: only enforce a non-trivial bound
            self._solver.add(Sum(terms) > 0, Sum(terms) < self._rows_number * self._columns_number)