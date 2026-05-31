from ortools.sat.python import cp_model

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Island import Island
from PuzzleSolver.Board.IslandsGrid import IslandGrid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class IchimagaSolver(GameSolver):
    Empty = None

    def __init__(self, grid: Grid):
        self._input_grid = grid
        self._island_grid: IslandGrid | None = None
        self.init_island_grid()
        self._model = cp_model.CpModel()
        self._cp_solver = cp_model.CpSolver()
        self._island_bridges_z3: dict[Position, dict[Direction, cp_model.IntVar]] = {}
        self._previous_solution: IslandGrid | None = None
        self._solver_initialized = False

    def init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._input_grid.columns_number)] for r in range(self._input_grid.rows_number)]
        )

    def _init_solver(self):
        self._island_bridges_z3 = {
            island.position: {direction: self._model.NewIntVar(0, 1, f"{island.position}_{direction}") for direction in Direction.orthogonal_directions()}
            for island in self._island_grid.islands.values()
        }
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if not self._solver_initialized:
            self._init_solver()
            self._solver_initialized = True

        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        proposition_count = 0
        while self._cp_solver.Solve(self._model) in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            proposition_count += 1
            for position, direction_bridges in self._island_bridges_z3.items():
                for direction, bridges in direction_bridges.items():
                    if position.after(direction) not in self._island_bridges_z3:
                        continue
                    bridges_number = self._cp_solver.Value(bridges)
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
                eq_bools = []
                for i, position in enumerate(positions):
                    for direction, (_, value) in self._island_grid[position].direction_position_bridges.items():
                        b = self._model.NewBoolVar(f'eq_conn_{i}_{position}_{direction}')
                        var = self._island_bridges_z3[position][direction]
                        self._model.Add(var == value).OnlyEnforceIf(b)
                        self._model.Add(var != value).OnlyEnforceIf(b.Not())
                        eq_bools.append(b)
                self._model.Add(sum(eq_bools) <= len(eq_bools) - 1)
            self.init_island_grid()

        return IslandGrid.empty(), proposition_count

    def get_other_solution(self):
        eq_bools = []
        for island in self._previous_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                var = self._island_bridges_z3[island.position][direction]
                b = self._model.NewBoolVar(f'prev_eq_{island.position}_{direction}')
                self._model.Add(var == value).OnlyEnforceIf(b)
                self._model.Add(var != value).OnlyEnforceIf(b.Not())
                eq_bools.append(b)
        self._model.Add(sum(eq_bools) <= len(eq_bools) - 1)

        self.init_island_grid()
        return self.get_solution()

    def get_stats(self) -> dict:
        return {
            "num_conflicts": self._cp_solver.NumConflicts(),
            "num_branches": self._cp_solver.NumBranches(),
            "wall_time": self._cp_solver.WallTime(),
        }

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_opposite_bridges_constraints()
        self._add_links_constraints()

    def _add_initial_constraints(self):
        for position, value in self._input_grid:
            bridges_var = list(self._island_bridges_z3[position].values())
            if value == self.Empty:
                b0 = self._model.NewBoolVar(f'sum0_{position}')
                b2 = self._model.NewBoolVar(f'sum2_{position}')
                self._model.Add(sum(bridges_var) == 0).OnlyEnforceIf(b0)
                self._model.Add(sum(bridges_var) != 0).OnlyEnforceIf(b0.Not())
                self._model.Add(sum(bridges_var) == 2).OnlyEnforceIf(b2)
                self._model.Add(sum(bridges_var) != 2).OnlyEnforceIf(b2.Not())
                self._model.AddBoolOr([b0, b2])
            else:
                self._model.Add(sum(bridges_var) == value)

            for bridge_var in bridges_var:
                self._model.Add(bridge_var >= 0)
                self._model.Add(bridge_var <= 1)

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._model.Add(
                        self._island_bridges_z3[island.position][direction] ==
                        self._island_bridges_z3[island.direction_position_bridges[direction][0]][direction.opposite])
                else:
                    self._model.Add(self._island_bridges_z3[island.position][direction] == 0)

    def _add_links_constraints(self):
        for position in [position for position, value in self._input_grid if value != self.Empty]:
            sum_linked_bools = self._get_connected_neighbors_boolvars(position)
            self._model.Add(sum(sum_linked_bools) == self._input_grid[position])

    def _get_connected_neighbors_boolvars(self, value_pos: Position):
        bool_vars = []
        for other_value_pos in [pos for pos, value in self._input_grid if value != self.Empty and pos != value_pos]:
            if value_pos.r == other_value_pos.r:
                direction = Direction.right() if other_value_pos.c > value_pos.c else Direction.left()
                b = self._straight_connection_boolvar(value_pos, other_value_pos, direction, f's_{value_pos}_{other_value_pos}')
                if b is not None:
                    bool_vars.append(b)
            elif value_pos.c == other_value_pos.c:
                direction = Direction.down() if other_value_pos.r > value_pos.r else Direction.up()
                b = self._straight_connection_boolvar(value_pos, other_value_pos, direction, f's_{value_pos}_{other_value_pos}')
                if b is not None:
                    bool_vars.append(b)
            else:
                hor_turn_pos = Position(value_pos.r, other_value_pos.c)
                vert_turn_pos = Position(other_value_pos.r, value_pos.c)
                hor_direction = Direction.right() if other_value_pos.c > value_pos.c else Direction.left()
                vert_direction = Direction.down() if other_value_pos.r > value_pos.r else Direction.up()

                b_hor = self._to_other_value_boolvar(value_pos, other_value_pos, hor_turn_pos, hor_direction, vert_direction, f'h_{value_pos}_{other_value_pos}')
                b_vert = self._to_other_value_boolvar(value_pos, other_value_pos, vert_turn_pos, vert_direction, hor_direction, f'v_{value_pos}_{other_value_pos}')

                if b_hor is not None:
                    bool_vars.append(b_hor)
                if b_vert is not None:
                    bool_vars.append(b_vert)

        return bool_vars

    def _pairs_to_boolvar(self, pairs, name: str):
        eq_bools = []
        for i, (var, val) in enumerate(pairs):
            b = self._model.NewBoolVar(f'{name}_eq_{i}')
            self._model.Add(var == val).OnlyEnforceIf(b)
            self._model.Add(var != val).OnlyEnforceIf(b.Not())
            eq_bools.append(b)
        b_all = self._model.NewBoolVar(f'{name}_all')
        for eb in eq_bools:
            self._model.AddImplication(b_all, eb)
        self._model.AddBoolOr([b_all] + [eb.Not() for eb in eq_bools])
        return b_all

    def _straight_connection_boolvar(self, start, end, direction, suffix: str):
        pairs = [(self._island_bridges_z3[start][direction], 1)]
        current = start.after(direction)
        while current != end:
            if current not in self._input_grid or self._input_grid[current] != self.Empty:
                return None
            pairs.append((self._island_bridges_z3[current][direction], 1))
            current = current.after(direction)
        return self._pairs_to_boolvar(pairs, suffix)

    def _to_other_value_boolvar(self, value_pos, other_value_pos, turn_position, first_direction, second_direction, suffix: str):
        pairs = [(self._island_bridges_z3[value_pos][first_direction], 1)]
        current_position = value_pos.after(first_direction)
        while self._input_grid[current_position] == self.Empty and current_position in self._input_grid and current_position != turn_position:
            pairs.append((self._island_bridges_z3[current_position][first_direction], 1))
            current_position = current_position.after(first_direction)
        if current_position not in self._input_grid or self._input_grid[current_position] != self.Empty:
            return None

        pairs.append((self._island_bridges_z3[current_position][second_direction], 1))
        current_position = current_position.after(second_direction)
        while self._input_grid[current_position] == self.Empty and current_position != other_value_pos:
            pairs.append((self._island_bridges_z3[current_position][second_direction], 1))
            current_position = current_position.after(second_direction)
        if current_position != other_value_pos:
            return None

        return self._pairs_to_boolvar(pairs, suffix)
