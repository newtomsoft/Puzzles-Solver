from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver

class GeradewegSolver(GameSolver):
    _used_directions = [Direction.right(), Direction.down()]

    def __init__(self, grid: Grid):
        self._input_grid = grid
        self._island_grid: IslandGrid | None = None
        self._rows_number = self._input_grid.rows_number
        self._columns_number = self._input_grid.columns_number
        self._solver = cp_model.CpSolver()
        self._solver.parameters.max_time_in_seconds = 120.0
        self._grid_vars: dict[tuple[Position, Direction], cp_model.IntVar] = {}
        self._previous_solution: IslandGrid | None = None
        self._model: cp_model.CpModel | None = None
        self._init_island_grid()

    def _init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._input_grid.columns_number)] for r in
             range(self._input_grid.rows_number)])

    def _build_model(self):
        self._model = cp_model.CpModel()
        self._grid_vars = {}
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                position = Position(r, c)
                for direction in Direction.orthogonal_directions():
                    self._grid_vars[(position, direction)] = self._model.new_bool_var(f"{position}_{direction}")
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if self._model is None:
            self._build_model()
        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        proposition_count = 0
        while True:
            status = self._solver.solve(self._model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                return IslandGrid.empty(), proposition_count

            proposition_count += 1
            self._init_island_grid()
            for r in range(self._rows_number):
                for c in range(self._columns_number):
                    position = Position(r, c)
                    for direction in Direction.orthogonal_directions():
                        neighbor = position.after(direction)
                        if neighbor not in self._island_grid.islands:
                            continue
                        bridges_number = self._solver.value(self._grid_vars[(position, direction)])
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
                cell_constraints = []
                for position in positions:
                    for direction, (_, value) in self._island_grid[position].direction_position_bridges.items():
                        if value == 1:
                            cell_constraints.append(self._grid_vars[(position, direction)])
                        else:
                            cell_constraints.append(self._grid_vars[(position, direction)].Not())
                if cell_constraints:
                    self._model.add_bool_or([constraint.Not() for constraint in cell_constraints])
            self._init_island_grid()

    def get_other_solution(self):
        if self._previous_solution is None:
            return self.get_solution()
        if self._model is None:
            self._build_model()
        self._exclude_previous_solution()
        self._init_island_grid()
        return self.get_solution()

    def _exclude_previous_solution(self):
        previous_solution_constraints = []
        for island in self._previous_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                if value == 1:
                    previous_solution_constraints.append(self._grid_vars[(island.position, direction)])
                else:
                    previous_solution_constraints.append(self._grid_vars[(island.position, direction)].Not())
        if previous_solution_constraints:
            self._model.add_bool_or([constraint.Not() for constraint in previous_solution_constraints])

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_opposite_bridges_constraints()
        self._add_lengths_constraints()

    def _add_initial_constraints(self):
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                position = Position(r, c)
                bridges_count_vars = [self._grid_vars[(position, direction)] for direction in Direction.orthogonal_directions()]
                on_loop = self._model.new_bool_var(f"on_loop_{r}_{c}")
                self._model.add(sum(bridges_count_vars) == 2).only_enforce_if(on_loop)
                self._model.add(sum(bridges_count_vars) == 0).only_enforce_if(on_loop.Not())

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in Direction.orthogonal_directions():
                neighbor = island.position.after(direction)
                if neighbor in self._island_grid.islands:
                    self._model.add(self._grid_vars[(island.position, direction)] == self._grid_vars[(neighbor, direction.opposite)])
                else:
                    self._model.add(self._grid_vars[(island.position, direction)] == 0)

    def _add_lengths_constraints(self):
        for position, length in [(position, value) for position, value in self._input_grid if value > 0]:
            self._model.add(sum(self._grid_vars[(position, direction)] for direction in Direction.orthogonal_directions()) == 2)
            configs = []
            for direction in self._used_directions:
                config = self._length_constraint(position, length, direction)
                if config is not None:
                    configs.append(config)
            if configs:
                self._model.add_bool_or(configs)

    def _length_constraint(self, position: Position, length: int, direction: Direction):
        configs = []
        extremities = self._extremities_constraint(position, length, direction)
        if extremities is not None:
            configs.append(extremities)
        for before_offset in range(1, length):
            offset_config = self._offsets_constraint(position, length, direction, before_offset)
            if offset_config is not None:
                configs.append(offset_config)
        if not configs:
            return None
        return self._or_var(configs)

    def _extremities_constraint(self, position: Position, length: int, direction: Direction):
        other_direction = next(d for d in self._used_directions if d != direction)
        other_before = self._offsets_constraint(position, length, other_direction, 0)
        other_after = self._offsets_constraint(position, length, other_direction, length)
        before = self._offsets_constraint(position, length, direction, 0)
        after = self._offsets_constraint(position, length, direction, length)

        side_parts = [x for x in [other_before, other_after] if x is not None]
        side = self._or_var(side_parts) if side_parts else None

        configs = []
        if before is not None and side is not None:
            configs.append(self._and_var([before, side]))
        if after is not None and side is not None:
            configs.append(self._and_var([after, side]))
        if not configs:
            return None
        return self._or_var(configs)

    def _offsets_constraint(self, position: Position, length: int, direction: Direction, before_offset: int):
        after_offset = length - before_offset
        first_position = position.before(direction, before_offset)
        last_position = position.after(direction, after_offset)
        if first_position not in self._input_grid or last_position not in self._input_grid:
            return None
        between_positions = first_position.all_positions_between(last_position)
        literals = [
            self._grid_vars[(first_position, direction)],
            self._grid_vars[(first_position, direction.opposite)].Not(),
            self._grid_vars[(last_position, direction)].Not(),
            self._grid_vars[(last_position, direction.opposite)],
        ]
        for current_position in between_positions:
            literals.append(self._grid_vars[(current_position, direction)])
            literals.append(self._grid_vars[(current_position, direction.opposite)])
        return self._and_var(literals)

    def _and_var(self, literals: list):
        config = self._model.new_bool_var(f"and_{id(literals)}")
        self._model.add_bool_and(literals).only_enforce_if(config)
        self._model.add_bool_or([config] + [lit.Not() for lit in literals])
        return config

    def _or_var(self, literals: list):
        config = self._model.new_bool_var(f"or_{id(literals)}")
        self._model.add_bool_or(literals).only_enforce_if(config)
        for lit in literals:
            self._model.add_implication(lit, config)
        return config
