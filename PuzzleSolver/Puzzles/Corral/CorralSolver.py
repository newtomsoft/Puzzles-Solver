from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class CorralSolver(GameSolver):
    cell_empty = None

    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows = grid.rows_number
        self._cols = grid.columns_number
        self._cells_count = self._rows * self._cols
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._is_zero = [[self._model.new_bool_var(f"zero_{r}_{c}") for c in range(self._cols)] for r in range(self._rows)]
        self._is_root = [[self._model.new_bool_var(f"root_{r}_{c}") for c in range(self._cols)] for r in range(self._rows)]
        self._depth = [[self._model.new_int_var(0, self._cells_count, f"depth_{r}_{c}") for c in range(self._cols)] for r in range(self._rows)]
        self._region_value = [[self._model.new_int_var(0, self._cells_count, f"region_value_{r}_{c}") for c in range(self._cols)] for r in range(self._rows)]
        self._to_border_depth = [[self._model.new_int_var(0, self._cells_count, f"to_border_depth_{r}_{c}") for c in range(self._cols)] for r in range(self._rows)]
        self._initialized = False

    def get_solution(self) -> Grid:
        if not self._initialized:
            self._add_constraints()
            self._initialized = True

        status = self._solver.solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()

        matrix = []
        for r in range(self._rows):
            row = []
            for c in range(self._cols):
                if self._solver.boolean_value(self._is_zero[r][c]):
                    row.append(0)
                else:
                    row.append(None)
            matrix.append(row)

        return Grid(matrix)

    def get_other_solution(self) -> Grid:
        return Grid.empty()

    def _add_constraints(self):
        self._add_hint_constraints()
        self._add_connected_zero_component_constraints()
        self._add_hint_visibility_constraints()
        self._add_non_zero_regions_touch_border_constraints()
        self._add_non_zero_different_values_do_not_touch_constraints()

    def _add_hint_constraints(self):
        for position, value in self._grid:
            if value is not None:
                self._model.add(self._is_zero[position.r][position.c] == 1)

    def _add_connected_zero_component_constraints(self):
        root_vars = []
        for r in range(self._rows):
            for c in range(self._cols):
                root = self._is_root[r][c]
                is_zero = self._is_zero[r][c]
                depth = self._depth[r][c]

                self._model.add(root <= is_zero)
                self._model.add(depth == 0).only_enforce_if(is_zero.Not())
                self._model.add(depth == 0).only_enforce_if(root)

                neighbors = []
                if r > 0:
                    neighbors.append((r - 1, c))
                if r < self._rows - 1:
                    neighbors.append((r + 1, c))
                if c > 0:
                    neighbors.append((r, c - 1))
                if c < self._cols - 1:
                    neighbors.append((r, c + 1))

                outgoing_arcs = []
                for nr, nc in neighbors:
                    arc = self._model.new_bool_var(f"arc_{r}_{c}_to_{nr}_{nc}")
                    outgoing_arcs.append(arc)
                    self._model.add(arc <= is_zero)
                    self._model.add(arc <= self._is_zero[nr][nc])
                    self._model.add(depth == self._depth[nr][nc] + 1).only_enforce_if(arc)

                self._model.add(sum(outgoing_arcs) == is_zero - root)
                root_vars.append(root)

        self._model.add(sum(root_vars) == 1)

    def _add_hint_visibility_constraints(self):
        for position, value in self._grid:
            if value is None:
                continue

            r, c = position.r, position.c
            visible_zero_vars = [self._is_zero[r][c]]

            visible_zero_vars.extend(self._build_direction_visibility_vars(r, c, -1, 0))
            visible_zero_vars.extend(self._build_direction_visibility_vars(r, c, 1, 0))
            visible_zero_vars.extend(self._build_direction_visibility_vars(r, c, 0, -1))
            visible_zero_vars.extend(self._build_direction_visibility_vars(r, c, 0, 1))

            self._model.add(sum(visible_zero_vars) == value)

    def _build_direction_visibility_vars(self, start_r: int, start_c: int, dr: int, dc: int) -> list[cp_model.IntVar]:
        direction_visible_vars = []
        prefix_cells = []

        r, c = start_r + dr, start_c + dc
        while 0 <= r < self._rows and 0 <= c < self._cols:
            prefix_cells.append(self._is_zero[r][c])
            visible = self._model.new_bool_var(f"visible_{start_r}_{start_c}_{r}_{c}")

            for cell_is_zero in prefix_cells:
                self._model.add_implication(visible, cell_is_zero)

            self._model.add_bool_or([visible] + [cell_is_zero.Not() for cell_is_zero in prefix_cells])

            direction_visible_vars.append(visible)
            r += dr
            c += dc

        return direction_visible_vars

    def _add_non_zero_regions_touch_border_constraints(self):
        for r in range(self._rows):
            for c in range(self._cols):
                is_zero = self._is_zero[r][c]
                region_value = self._region_value[r][c]
                to_border_depth = self._to_border_depth[r][c]

                self._model.add(region_value == 0).only_enforce_if(is_zero)
                self._model.add(region_value >= 1).only_enforce_if(is_zero.Not())
                self._model.add(to_border_depth == 0).only_enforce_if(is_zero)

                neighbors = []
                if r > 0:
                    neighbors.append((r - 1, c))
                if r < self._rows - 1:
                    neighbors.append((r + 1, c))
                if c > 0:
                    neighbors.append((r, c - 1))
                if c < self._cols - 1:
                    neighbors.append((r, c + 1))

                arc_to_border_vars = []
                for nr, nc in neighbors:
                    self._model.add(self._region_value[r][c] == self._region_value[nr][nc]).only_enforce_if(
                        [self._is_zero[r][c].Not(), self._is_zero[nr][nc].Not()]
                    )

                    arc = self._model.new_bool_var(f"arc_to_border_{r}_{c}_to_{nr}_{nc}")
                    arc_to_border_vars.append(arc)
                    self._model.add(arc <= is_zero.Not())
                    self._model.add(arc <= self._is_zero[nr][nc].Not())
                    self._model.add(region_value == self._region_value[nr][nc]).only_enforce_if(arc)
                    self._model.add(to_border_depth == self._to_border_depth[nr][nc] + 1).only_enforce_if(arc)

                is_border = r == 0 or c == 0 or r == self._rows - 1 or c == self._cols - 1
                if is_border:
                    self._model.add(to_border_depth == 0).only_enforce_if(is_zero.Not())
                    self._model.add(sum(arc_to_border_vars) == 0).only_enforce_if(is_zero.Not())
                else:
                    self._model.add(sum(arc_to_border_vars) == 0).only_enforce_if(is_zero)
                    self._model.add(sum(arc_to_border_vars) == 1).only_enforce_if(is_zero.Not())

    def _add_non_zero_different_values_do_not_touch_constraints(self):
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1),
        ]

        for r in range(self._rows):
            for c in range(self._cols):
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < self._rows and 0 <= nc < self._cols):
                        continue

                    if (nr, nc) <= (r, c):
                        continue

                    self._model.add(self._region_value[r][c] == self._region_value[nr][nc]).only_enforce_if(
                        [self._is_zero[r][c].Not(), self._is_zero[nr][nc].Not()]
                    )
