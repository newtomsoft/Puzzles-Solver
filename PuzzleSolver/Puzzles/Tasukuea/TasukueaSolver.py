from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class TasukueaSolver(GameSolver):
    cell_empty = None
    unknown = '?'

    def __init__(self, grid: Grid):
        super().__init__()
        self._grid = grid
        self._rows_number = self._grid.rows_number
        self._columns_number = self._grid.columns_number
        self._grid_var: Grid = Grid.empty()
        self._model = cp_model.CpModel()
        self._initialized = False
        self._previous_solution: Grid | None = None
        self._square_selectors = None
        self._selector_areas = None
        self._coverage = {}
        self._square_bounds = []
        self._squares_built = False

    def _init_solver(self):
        self._grid_var = Grid([[self._model.new_bool_var(f"cell_{r}_{c}") for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])
        self._add_constraints()
        self._initialized = True

    def get_solution(self) -> Grid:
        if not self._initialized:
            self._init_solver()

        status = self._solver.solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()

        solution = Grid([[None] * self._columns_number for _ in range(self._rows_number)])
        for position, var in self._grid_var:
            solution[position] = bool(self._solver.value(var))
        self._previous_solution = solution
        return solution

    def get_other_solution(self):
        if self._previous_solution is not None:
            diff_literals = []
            for position, value in self._previous_solution:
                var = self._grid_var[position]
                diff_literals.append(var if value is False else var.negated())
            self._model.add_bool_or(diff_literals)
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_all_squares_constraints()
        self._add_white_connectivity_constraint()

    def _add_initial_constraints(self):
        for position, value in self._grid:
            if value != self.cell_empty:
                self._model.add(self._grid_var[position] == 0)

    def _add_white_connectivity_constraint(self):
        total_cells = self._rows_number * self._columns_number
        self._rank_vars = Grid([[self._model.new_int_var(0, total_cells - 1, f"rank_{r}_{c}") for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])
        is_root_vars = []
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                pos = Position(r, c)
                is_root = self._model.new_bool_var(f"is_root_{r}_{c}")
                is_root_vars.append(is_root)
                is_white = self._grid_var[pos].negated()
                self._model.add(is_root <= is_white)
                self._model.add(self._rank_vars[pos] == 0).OnlyEnforceIf(is_root)
        self._model.add(sum(is_root_vars) == 1)
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                pos = Position(r, c)
                is_white = self._grid_var[pos].negated()
                is_root = is_root_vars[r * self._columns_number + c]
                parent_literals = []
                for neighbor in self._grid_var.neighbors_positions(pos):
                    parent = self._model.new_bool_var(f"parent_{r}_{c}_{neighbor.r}_{neighbor.c}")
                    self._model.add(self._grid_var[neighbor] == 0).OnlyEnforceIf(parent)
                    self._model.add(self._rank_vars[neighbor] < self._rank_vars[pos]).OnlyEnforceIf(parent)
                    parent_literals.append(parent)
                if parent_literals:
                    self._model.add_bool_or(parent_literals).OnlyEnforceIf([is_white, is_root.negated()])

    def _add_all_squares_constraints(self):
        self._build_square_model()
        for position, sum_squares_area in [(position, value) for position, value in self._grid if value != self.cell_empty]:
            self._add_squares_no_adjacent_constraint(position, sum_squares_area)

    def _build_square_model(self):
        if self._squares_built:
            return
        rows = self._rows_number
        cols = self._columns_number
        max_size = min(rows, cols)

        self._square_selectors = []
        self._selector_areas = dict()
        self._coverage = dict()

        for size in range(1, max_size + 1):
            for r0 in range(0, rows - size + 1):
                for c0 in range(0, cols - size + 1):
                    selector = self._model.new_bool_var(f"sq_{r0}_{c0}_{size}")
                    area = size * size
                    self._square_selectors.append(selector)
                    self._selector_areas[selector] = area
                    self._square_bounds.append((selector, r0, c0, size))

                    for r in range(r0, r0 + size):
                        for c in range(c0, c0 + size):
                            pos = Position(r, c)
                            key = (r, c)
                            if key not in self._coverage:
                                self._coverage[key] = []
                            self._coverage[key].append(selector)
                            self._model.add_implication(selector, self._grid_var[pos])

        clue_positions = [p for (p, v) in self._grid if v != self.cell_empty]
        if clue_positions:
            for s, r0, c0, sz in self._square_bounds:
                r_min, r_max = r0, r0 + sz - 1
                c_min, c_max = c0, c0 + sz - 1
                adjacent_found = False
                for p in clue_positions:
                    for neighbor in self._grid.neighbors_positions(p, mode='orthogonal'):
                        if r_min <= neighbor.r <= r_max and c_min <= neighbor.c <= c_max:
                            adjacent_found = True
                            break
                    if adjacent_found:
                        break
                if not adjacent_found:
                    self._model.add(s == 0)

        for position, var in self._grid_var:
            key = (position.r, position.c)
            selectors = self._coverage.get(key, [])
            if selectors:
                self._model.add_bool_or(selectors + [var.negated()])
                self._model.add_at_most_one(selectors)
            else:
                self._model.add(var == 0)

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
                    self._model.add_bool_or([s1.negated(), s2.negated()])

        self._squares_built = True

    def _add_squares_no_adjacent_constraint(self, position: Position, sum_squares_area: int):
        adjacent_positions = list(self._grid.neighbors_positions(position, mode='orthogonal'))
        adjacent_selectors = set()
        for p in adjacent_positions:
            for s in self._coverage.get((p.r, p.c), []):
                adjacent_selectors.add(s)

        if not adjacent_selectors:
            self._model.add(False)
            return

        terms = [s * self._selector_areas[s] for s in adjacent_selectors]
        if sum_squares_area != self.unknown:
            self._model.add(sum(terms) == int(sum_squares_area))
        else:
            self._model.add(sum(terms) >= 1)
            self._model.add(sum(terms) <= self._rows_number * self._columns_number - 1)
