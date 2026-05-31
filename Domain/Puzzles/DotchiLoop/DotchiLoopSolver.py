from ortools.sat.python import cp_model
from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver

_ = 0
B = 1
W = 2

class DotchiLoopSolver(GameSolver):
    def __init__(self, region_grid: Grid[int], value_grid: Grid[int]):
        self._region_grid = region_grid
        self._value_grid = value_grid
        self._rows_number = self._region_grid.rows_number
        self._columns_number = self._region_grid.columns_number
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._island_grid: IslandGrid | None = None
        self.init_island_grid()
        self._bridges_vars = {}
        self._previous_solution = None

    def init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._value_grid.columns_number)] for r in range(self._value_grid.rows_number)])

    def _init_solver(self):
        self._model = cp_model.CpModel()
        directions = Direction.orthogonal_directions()
        self._bridges_vars = {
            (r, c): {d: self._model.new_bool_var(f"b_{r}_{c}_{d}") for d in directions}
            for r in range(self._rows_number)
            for c in range(self._columns_number)
        }
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if not self._bridges_vars:
            self._init_solver()

        status = self._solver.solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return IslandGrid.empty()

        self._previous_solution = self._build_island_grid_from_solution()
        return self._previous_solution

    def _build_island_grid_from_solution(self) -> IslandGrid:
        directions = Direction.orthogonal_directions()
        island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._value_grid.columns_number)] for r in range(self._value_grid.rows_number)])
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                pos = Position(r, c)
                for d in directions:
                    val = self._solver.value(self._bridges_vars[r, c][d])
                    if val > 0:
                        island_grid[pos].set_bridge_to_position(island_grid[pos].direction_position_bridges[d][0], val)
                    elif d in island_grid[pos].direction_position_bridges:
                        island_grid[pos].direction_position_bridges.pop(d)
                island_grid[pos].set_bridges_count_according_to_directions_bridges()
        return island_grid

    def get_other_solution(self):
        if not self._previous_solution:
            return IslandGrid.empty()

        vars_list = []
        directions = Direction.orthogonal_directions()
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                pos = Position(r, c)
                for d in directions:
                    var = self._bridges_vars[r, c][d]
                    if d in self._previous_solution[pos].direction_position_bridges:
                        vars_list.append(var.negated())
                    else:
                        vars_list.append(var)
        self._model.add_bool_or(vars_list)
        return self.get_solution()

    def _add_constraints(self):
        directions = Direction.orthogonal_directions()
        right, down = Direction.right(), Direction.down()
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                pos = Position(r, c)
                for d in [right, down]:
                    n = pos.after(d)
                    if 0 <= n.r < self._rows_number and 0 <= n.c < self._columns_number:
                        self._model.add(self._bridges_vars[r, c][d] == self._bridges_vars[n.r, n.c][d.opposite])
                if r == 0: self._model.add(self._bridges_vars[r, c][Direction.up()] == 0)
                if r == self._rows_number - 1: self._model.add(self._bridges_vars[r, c][Direction.down()] == 0)
                if c == 0: self._model.add(self._bridges_vars[r, c][Direction.left()] == 0)
                if c == self._columns_number - 1: self._model.add(self._bridges_vars[r, c][Direction.right()] == 0)

                val = self._value_grid[r, c]
                vars_list = list(self._bridges_vars[r, c].values())
                if val == B:
                    for v in vars_list: self._model.add(v == 0)
                elif val == W:
                    self._model.add(sum(vars_list) == 2)
                else:
                    is_used = self._model.new_bool_var(f"u_{r}_{c}")
                    self._model.add(sum(vars_list) == 2).only_enforce_if(is_used)
                    self._model.add(sum(vars_list) == 0).only_enforce_if(is_used.negated())

        L_dir, R_dir = Direction.left(), Direction.right()
        for region_id, positions in self._region_grid.get_regions().items():
            white_pos = [p for p in positions if self._value_grid[p] == W]
            if not white_pos: continue
            is_st = self._model.new_bool_var(f"st_{region_id}")
            for p in white_pos:
                L, R = self._bridges_vars[p.r, p.c][L_dir], self._bridges_vars[p.r, p.c][R_dir]
                self._model.add(L == R).only_enforce_if(is_st)
                self._model.add(L != R).only_enforce_if(is_st.negated())

        self._add_connectivity_constraint()

    def _add_connectivity_constraint(self):
        total_cells = self._rows_number * self._columns_number
        directions = Direction.orthogonal_directions()
        rank_vars = [[self._model.new_int_var(0, total_cells - 1, f"rank_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)]
        has_any_bridge = [[self._model.new_bool_var(f"has_bridge_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)]
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                bridge_vars = list(self._bridges_vars[r, c].values())
                self._model.add(sum(bridge_vars) >= 1).only_enforce_if(has_any_bridge[r][c])
                self._model.add(sum(bridge_vars) == 0).only_enforce_if(has_any_bridge[r][c].negated())

        is_root_vars = []
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                is_root = self._model.new_bool_var(f"is_root_{r}_{c}")
                is_root_vars.append(is_root)
                self._model.add(is_root <= has_any_bridge[r][c])
                self._model.add(rank_vars[r][c] == 0).OnlyEnforceIf(is_root)

                parent_literals = []
                for d in directions:
                    delta = Position(0, 0).after(d)
                    nr, nc = r + delta.r, c + delta.c
                    if 0 <= nr < self._rows_number and 0 <= nc < self._columns_number:
                        parent = self._model.new_bool_var(f"parent_{r}_{c}_{d.value}")
                        self._model.add(self._bridges_vars[r, c][d] == 1).OnlyEnforceIf(parent)
                        self._model.add(rank_vars[nr][nc] < rank_vars[r][c]).OnlyEnforceIf(parent)
                        parent_literals.append(parent)
                if parent_literals:
                    self._model.add_bool_or(parent_literals).OnlyEnforceIf([has_any_bridge[r][c], is_root.negated()])

        self._model.add(sum(is_root_vars) == 1)
