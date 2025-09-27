from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver

_ = ''


class KonarupuSolver(GameSolver):
    def __init__(self, grid: Grid):
        self.input_grid = grid
        self._island_grid: IslandGrid | None = None
        self._init_island_grid()
        self._model = cp_model.CpModel()
        self._island_bridges_vars: dict[Position, dict[Direction, any]] = {}
        self._previous_solution: IslandGrid | None = None
        self._solver = cp_model.CpSolver()

    def _init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self.input_grid.columns_number + 1)] for r in
             range(self.input_grid.rows_number + 1)])

    def _init_solver(self):
        self._island_bridges_vars = {
            island.position: {
                direction: self._model.NewIntVar(0, 1, f"{island.position}_{direction}")
                for direction in Direction.orthogonals()
            }
            for island in self._island_grid.islands.values()
        }
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if not self._island_bridges_vars:
            self._init_solver()

        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> (Grid, int):
        proposition_count = 0
        while True:
            status = self._solver.Solve(self._model)
            if status != cp_model.FEASIBLE and status != cp_model.OPTIMAL:
                break

            proposition_count += 1
            for position, direction_bridges in self._island_bridges_vars.items():
                for direction, bridges in direction_bridges.items():
                    if position.after(direction) not in self._island_bridges_vars:
                        continue
                    bridges_number = self._solver.Value(bridges)
                    if bridges_number > 0:
                        self._island_grid[position].set_bridge_to_position(
                            self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
                    elif position in self._island_grid and direction in self._island_grid[
                        position].direction_position_bridges:
                        self._island_grid[position].direction_position_bridges.pop(direction)
                self._island_grid[position].set_bridges_count_according_to_directions_bridges()

            connected_positions = self._island_grid.get_connected_positions(exclude_without_bridge=True)
            if len(connected_positions) == 1:
                self._previous_solution = self._island_grid
                return self._island_grid, proposition_count

            for positions in connected_positions:
                bool_constraints = []
                for position in positions:
                    for direction, (_, value) in self._island_grid[position].direction_position_bridges.items():
                        b = self._model.NewBoolVar(f'b_{position}_{direction}')
                        var = self._island_bridges_vars[position][direction]
                        self._model.Add(var == value).OnlyEnforceIf(b)
                        self._model.Add(var != value).OnlyEnforceIf(b.Not())
                        bool_constraints.append(b)
                self._model.AddBoolOr([b.Not() for b in bool_constraints])
            self._init_island_grid()

        return IslandGrid.empty(), proposition_count

    def get_other_solution(self):
        bool_constraints = []
        for island in self._previous_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                b = self._model.NewBoolVar(f'b_other_{island.position}_{direction}')
                var = self._island_bridges_vars[island.position][direction]
                self._model.Add(var == value).OnlyEnforceIf(b)
                self._model.Add(var != value).OnlyEnforceIf(b.Not())
                bool_constraints.append(b)
        self._model.AddBoolOr([b.Not() for b in bool_constraints])

        self._init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_opposite_bridges_constraints()
        self._add_bridges_sum_constraints()
        self._add_numbers_constraints()

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in Direction.orthogonals():
                neighbor_pos = island.position.after(direction)
                if neighbor_pos in self._island_grid.islands:
                    self._model.Add(self._island_bridges_vars[island.position][direction] ==
                                    self._island_bridges_vars[neighbor_pos][direction.opposite])
                else:
                    self._model.Add(self._island_bridges_vars[island.position][direction] == 0)

    def _add_bridges_sum_constraints(self):
        for island in self._island_grid.islands.values():
            bridges = list(self._island_bridges_vars[island.position].values())
            sum_var = self._model.NewIntVar(0, 8, f'sum_{island.position}')
            self._model.Add(sum_var == sum(bridges))

            is_zero = self._model.NewBoolVar(f'is_zero_{island.position}')
            is_two = self._model.NewBoolVar(f'is_two_{island.position}')

            self._model.Add(sum_var == 0).OnlyEnforceIf(is_zero)
            self._model.Add(sum_var != 0).OnlyEnforceIf(is_zero.Not())

            self._model.Add(sum_var == 2).OnlyEnforceIf(is_two)
            self._model.Add(sum_var != 2).OnlyEnforceIf(is_two.Not())

            self._model.AddBoolOr([is_zero, is_two])

    def _add_numbers_constraints(self):
        for position, number in [(pos, num) for pos, num in self.input_grid if num != _]:
            corners = [position, position.down, position.down_right, position.right]
            corner_vars = [self.corner_no_turn_constraint(self._island_bridges_vars[c]) for c in corners]
            self._model.Add(sum(corner_vars) == 4 - number)

    def corner_no_turn_constraint(self, corner_directions_var: dict[Direction, cp_model.IntVar]):
        no_turn_bool = self._model.NewBoolVar('')
        corner_vertical = self.vertical_constraint(corner_directions_var)
        corner_horizontal = self.horizontal_constraint(corner_directions_var)
        corner_empty = self.empty_constraint(corner_directions_var)
        self._model.AddBoolOr([corner_vertical, corner_horizontal, corner_empty]).OnlyEnforceIf(no_turn_bool)
        self._model.AddBoolAnd([corner_vertical.Not(), corner_horizontal.Not(), corner_empty.Not()]).OnlyEnforceIf(
            no_turn_bool.Not())
        return no_turn_bool

    def vertical_constraint(self, directions_var: dict[Direction, cp_model.IntVar]):
        v_bool = self._model.NewBoolVar('')
        self._model.Add(directions_var[Direction.down()] + directions_var[Direction.up()] == 2).OnlyEnforceIf(v_bool)
        self._model.Add(directions_var[Direction.down()] + directions_var[Direction.up()] != 2).OnlyEnforceIf(
            v_bool.Not())
        return v_bool

    def horizontal_constraint(self, directions_var: dict[Direction, cp_model.IntVar]):
        h_bool = self._model.NewBoolVar('')
        self._model.Add(directions_var[Direction.left()] + directions_var[Direction.right()] == 2).OnlyEnforceIf(h_bool)
        self._model.Add(directions_var[Direction.left()] + directions_var[Direction.right()] != 2).OnlyEnforceIf(
            h_bool.Not())
        return h_bool

    def empty_constraint(self, dir_var: dict[Direction, cp_model.IntVar]):
        e_bool = self._model.NewBoolVar('')
        all_dirs = list(dir_var.values())
        self._model.Add(sum(all_dirs) == 0).OnlyEnforceIf(e_bool)
        self._model.Add(sum(all_dirs) != 0).OnlyEnforceIf(e_bool.Not())
        return e_bool