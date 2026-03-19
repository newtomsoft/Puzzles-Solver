from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class YinYangSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number < 6:
            raise ValueError("Yin Yang grid must be at least 6x6")

        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._solver.parameters.max_time_in_seconds = 120.0  # Fail fast if stuck
        self._grid_vars = {}
        self._previous_solution = None

        self._init_model()

    def _init_model(self):
        for pos in self._grid.get_positions():
            self._grid_vars[pos] = self._model.new_bool_var(f"cell_{pos.r}_{pos.c}")

        self._add_constraints()

    def _add_constraints(self):
        self._add_initial_values_constraints()
        self._add_no_solid_square_constraints()
        self._add_checkerboard_constraints()
        self._add_connectivity_constraints()

    def _add_initial_values_constraints(self):
        for pos, val in self._grid:
            if val == 1:  # White
                self._model.add(self._grid_vars[pos] == 1)
            elif val == 0:  # Black
                self._model.add(self._grid_vars[pos] == 0)

    def _add_no_solid_square_constraints(self):
        # 2x2 Constraints (No solid square)
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                cells = [
                    self._grid_vars[Position(r, c)],
                    self._grid_vars[Position(r + 1, c)],
                    self._grid_vars[Position(r, c + 1)],
                    self._grid_vars[Position(r + 1, c + 1)],
                ]
                self._model.add(sum(cells) > 0)
                self._model.add(sum(cells) < 4)

    def _add_checkerboard_constraints(self):
        # Forbidden: 1 0 / 0 1 and 0 1 / 1 0
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                self._model.add_forbidden_assignments(
                    [
                        self._grid_vars[Position(r, c)],
                        self._grid_vars[Position(r, c + 1)],
                        self._grid_vars[Position(r + 1, c)],
                        self._grid_vars[Position(r + 1, c + 1)],
                    ],
                    [(1, 0, 0, 1), (0, 1, 1, 0)],
                )

    def _add_connectivity_constraints(self):
        # 1. Border transitions constraint (extremely powerful for Yin-Yang)
        border_cells = []
        for pos in self._grid.edge_up_positions():
            border_cells.append(self._grid_vars[pos])
        for pos in self._grid.edge_right_positions()[1:]:
            border_cells.append(self._grid_vars[pos])
        for pos in reversed(self._grid.edge_down_positions()[:-1]):
            border_cells.append(self._grid_vars[pos])
        for pos in reversed(self._grid.edge_left_positions()[1:-1]):
            border_cells.append(self._grid_vars[pos])

        transitions = []
        for i in range(len(border_cells)):
            c1 = border_cells[i]
            c2 = border_cells[(i + 1) % len(border_cells)]
            diff = self._model.new_bool_var(f"diff_border_{i}")
            self._model.add(c1 != c2).only_enforce_if(diff)
            self._model.add(c1 == c2).only_enforce_if(diff.Not())
            transitions.append(diff)
        self._model.add(sum(transitions) == 2)

        # 2. Connectivity for BOTH colors
        for color in [0, 1]:
            self._add_color_connectivity(color)

    def _add_color_connectivity(self, color):
        num_cells = self.rows_number * self.columns_number
        ranks = {}
        is_root = {}
        for pos in self._grid.get_positions():
            ranks[pos] = self._model.new_int_var(0, num_cells - 1, f"color_{color}_rank_{pos.r}_{pos.c}")
            is_root[pos] = self._model.new_bool_var(f"is_root_color_{color}_{pos.r}_{pos.c}")

        # Root for each color can be restricted to the border to speed up search
        border_positions = self._grid.edges_positions()
        self._model.add(sum(is_root[pos] for pos in border_positions) == 1)

        for pos in set(self._grid.get_positions()) - border_positions:
            self._model.add(is_root[pos] == 0)

        for pos in self._grid.get_positions():
            u_is_color = self._grid_vars[pos] if color == 1 else self._grid_vars[pos].Not()
            u_rank = ranks[pos]
            u_is_root = is_root[pos]

            # Root must be of the correct color and have rank 0
            self._model.add(u_is_color == 1).only_enforce_if(u_is_root)
            self._model.add(u_rank == 0).only_enforce_if(u_is_root)

            # Each non-root cell of this color must have at least one neighbor of same color with lower rank
            # This prevents cycles and ensures connectivity.
            has_parent = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = pos.r + dr, pos.c + dc
                if 0 <= nr < self.rows_number and 0 <= nc < self.columns_number:
                    v_pos = Position(nr, nc)
                    v_is_color = self._grid_vars[v_pos] if color == 1 else self._grid_vars[v_pos].Not()
                    v_rank = ranks[v_pos]

                    p = self._model.new_bool_var(f"p_color_{color}_{pos}_{v_pos}")
                    self._model.add(v_is_color == 1).only_enforce_if(p)
                    self._model.add(v_rank < u_rank).only_enforce_if(p)
                    has_parent.append(p)

            # If u is this color and not root, it must have a parent
            self._model.add_bool_or(has_parent).only_enforce_if([u_is_color, u_is_root.Not()])

    def get_solution(self) -> Grid:
        status = self._solver.solve(self._model)
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            solution_grid = self._build_grid_from_solution()
            self._previous_solution = solution_grid
            return solution_grid
        else:
            return Grid.empty()

    def get_other_solution(self):
        if self._previous_solution is None:
            return self.get_solution()

        constraints = []
        for pos, val in self._previous_solution:
            if val == 1:
                constraints.append(self._grid_vars[pos].Not())
            else:
                constraints.append(self._grid_vars[pos])

        self._model.add_bool_or(constraints)

        return self.get_solution()

    def _build_grid_from_solution(self) -> Grid:
        data = [[0 for _ in range(self.columns_number)] for _ in range(self.rows_number)]
        for pos in self._grid.get_positions():
            val = self._solver.value(self._grid_vars[pos])
            data[pos.r][pos.c] = int(val)
        return Grid(data)
