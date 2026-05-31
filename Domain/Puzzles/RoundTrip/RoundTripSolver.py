from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class RoundTripSolver(GameSolver):
    cell_empty = None

    def __init__(self, grid: Grid, clues: dict[Direction, list[int]]):
        self.input_grid = grid
        self._rows_number, self._columns_number = grid.rows_number, grid.columns_number
        self._clues = clues
        self._island_grid: IslandGrid | None = None
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_vars: dict[Position, dict[Direction, cp_model.BoolVar]] | None = None
        self._previous_solution: IslandGrid | None = None
        self._initialized = False

    def _init_solver(self):
        self._grid_vars = {}
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                pos = Position(r, c)
                self._grid_vars[pos] = {
                    direction: self._model.new_bool_var(f"{direction}_{r}-{c}")
                    for direction in Direction.orthogonal_directions()
                }
        self._add_constraints()
        self._initialized = True

    def get_solution(self) -> Grid:
        if not self._initialized:
            self._init_solver()

        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        propositions_count = 0
        while True:
            status = self._solver.solve(self._model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                return IslandGrid.empty(), propositions_count

            propositions_count += 1
            island_grid = self._extract_island_grid()
            connected_positions = island_grid.compute_linear_connected_positions(exclude_without_bridge=True)
            if len(connected_positions) == 1:
                self._previous_solution = island_grid
                return island_grid, propositions_count

            biggest_connected_positions = max(connected_positions, key=len)
            connected_positions.remove(biggest_connected_positions)
            for positions in connected_positions:
                blocking_vars = []
                for position in positions:
                    directions_with_bridge = [
                        direction
                        for direction in Direction.orthogonal_directions()
                        if island_grid[position].bridges_number(direction) == 1
                    ]
                    for direction in directions_with_bridge:
                        blocking_vars.append(self._grid_vars[position][direction].Not())
                    directions_without_bridge = [
                        direction
                        for direction in Direction.orthogonal_directions()
                        if island_grid[position].bridges_number(direction) == 0
                    ]
                    for direction in directions_without_bridge:
                        blocking_vars.append(self._grid_vars[position][direction])
                self._model.add_bool_or(blocking_vars)

    def _extract_island_grid(self) -> IslandGrid:
        island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._columns_number)] for r in range(self._rows_number)]
        )
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                pos = Position(r, c)
                for direction in Direction.orthogonal_directions():
                    if self._solver.boolean_value(self._grid_vars[pos][direction]):
                        neighbor_pos = pos.after(direction)
                        island_grid[pos].set_bridge_to_position(neighbor_pos, 1)
                island_grid[pos].set_bridges_count_according_to_directions_bridges()
        return island_grid

    def get_other_solution(self):
        blocking_vars = []
        for position, island in self._previous_solution:
            for direction in Direction.orthogonal_directions():
                if island.bridges_number(direction) == 1:
                    blocking_vars.append(self._grid_vars[position][direction].Not())
                else:
                    blocking_vars.append(self._grid_vars[position][direction])
        self._model.add_bool_or(blocking_vars)
        return self.get_solution()

    def _add_constraints(self):
        self._add_initials_constraints()
        self._add_opposite_constraints()
        self._add_bridges_sum_constraints()
        self._add_clues_segments_length_constraints()

    def _add_initials_constraints(self):
        for position in self.input_grid.edge_up_positions():
            self._model.add(self._grid_vars[position][Direction.up()] == 0)
        for position in self.input_grid.edge_down_positions():
            self._model.add(self._grid_vars[position][Direction.down()] == 0)
        for position in self.input_grid.edge_left_positions():
            self._model.add(self._grid_vars[position][Direction.left()] == 0)
        for position in self.input_grid.edge_right_positions():
            self._model.add(self._grid_vars[position][Direction.right()] == 0)

        for position, island in self.input_grid:
            if not island.has_no_bridge():
                for direction, (_, bridges) in island.direction_position_bridges.items():
                    self._model.add(self._grid_vars[position][direction] == (bridges == 1))

    def _add_opposite_constraints(self):
        for position in self._grid_vars:
            if position.up in self._grid_vars:
                self._model.add(
                    self._grid_vars[position][Direction.up()] == self._grid_vars[position.up][Direction.down()]
                )
            if position.down in self._grid_vars:
                self._model.add(
                    self._grid_vars[position][Direction.down()] == self._grid_vars[position.down][Direction.up()]
                )
            if position.left in self._grid_vars:
                self._model.add(
                    self._grid_vars[position][Direction.left()] == self._grid_vars[position.left][Direction.right()]
                )
            if position.right in self._grid_vars:
                self._model.add(
                    self._grid_vars[position][Direction.right()] == self._grid_vars[position.right][Direction.left()]
                )

    def _add_bridges_sum_constraints(self):
        for position in self._grid_vars:
            vars_ = [self._grid_vars[position][direction] for direction in Direction.orthogonal_directions()]
            degree = sum(vars_)
            b0 = self._model.new_bool_var(f"deg0_{position.r}_{position.c}")
            b2 = self._model.new_bool_var(f"deg2_{position.r}_{position.c}")
            b4 = self._model.new_bool_var(f"deg4_{position.r}_{position.c}")
            self._model.add(degree == 0).only_enforce_if(b0)
            self._model.add(degree == 2).only_enforce_if(b2)
            self._model.add(degree == 4).only_enforce_if(b4)
            self._model.add(sum([b0, b2, b4]) == 1)

    def _add_clues_segments_length_constraints(self):
        directions__range_line__positions_func = [
            (Direction.right(), range(self._rows_number), lambda r: [Position(r, c) for c in range(self._columns_number)]),
            (Direction.left(), range(self._rows_number), lambda r: [Position(r, c) for c in reversed(range(self._columns_number))]),
            (Direction.down(), range(self._columns_number), lambda c: [Position(r, c) for r in range(self._rows_number)]),
            (Direction.up(), range(self._columns_number), lambda c: [Position(r, c) for r in reversed(range(self._rows_number))])
        ]

        for direction, range_line, positions_func in directions__range_line__positions_func:
            for i in range_line:
                positions = positions_func(i)
                if (clue_size := self._clues[direction][i]) == self.empty:
                    continue
                self._add_clue_segment_length_constraint(direction, clue_size, positions)

    def _add_clue_segment_length_constraint(self, direction: Direction, clue_size: int, positions: list[Position]):
        if clue_size == 0:
            for position in positions:
                self._model.add(self._grid_vars[position][direction] == 0)
            return

        n = len(positions)
        bridges_count = clue_size - 1
        vars_in_line = [self._grid_vars[position][direction] for position in positions]

        if bridges_count == 0:
            # Equivalent to Z3's Or(And(lens_var[0..i-1] == 0, lens_var[i] == 0))
            # which simplifies to vars_in_line[0] == 0
            self._model.add(vars_in_line[0] == 0)
            return

        select_vars = []
        # lens_var[i] is only defined when there is at least one position after i,
        # and it can reach bridges_count only while i <= n - 1 - bridges_count
        for i in range(n - bridges_count):
            sel = self._model.new_bool_var(f"sel_{direction}_{positions[i]}_{i}")
            select_vars.append(sel)
            # prefix must be 0
            for j in range(i):
                self._model.add(vars_in_line[j] <= 1 - sel)
            # segment of bridges_count consecutive ones
            for k in range(bridges_count):
                self._model.add(vars_in_line[i + k] >= sel)
            # cell right after the segment must be 0
            if i + bridges_count < n:
                self._model.add(vars_in_line[i + bridges_count] <= 1 - sel)

        self._model.add(sum(select_vars) == 1)
