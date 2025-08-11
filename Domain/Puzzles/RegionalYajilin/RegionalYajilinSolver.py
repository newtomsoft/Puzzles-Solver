from typing import Dict

from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class RegionalYajilinSolver(GameSolver):
    def __init__(self, blacks_count_grid: Grid, regions_grid: Grid):
        self._regions_grid = regions_grid
        self._positions_by_region_id = regions_grid.get_regions()
        self._blacks_count_grid = blacks_count_grid
        self._island_grid: IslandGrid | None = None
        self._init_island_grid()
        self._model = cp_model.CpModel()
        self._island_bridges_vars: Dict[Position, Dict[Direction, cp_model.IntVar]] = {}
        self._black_cells_vars: Dict[Position, cp_model.IntVar] = {}
        self._previous_solution: IslandGrid | None = None

    def _init_island_grid(self):
        self._island_grid = IslandGrid([[Island(Position(r, c), 2) for c in range(self._regions_grid.columns_number)] for r in range(self._regions_grid.rows_number)])

    def _init_model(self):
        self._island_bridges_vars = {
            island.position: {direction: self._model.NewIntVar(0, 1, f"{island.position}_{direction}") for direction in Direction.orthogonals()}
            for island in self._island_grid.islands.values() if island.bridges_count > 0
        }

        for position in [position for position, _ in self._regions_grid if position not in self._island_bridges_vars]:
            neighbors = self._regions_grid.neighbors_positions(position)
            for neighbor in [neighbor for neighbor in neighbors if neighbor in self._island_bridges_vars]:
                direction = neighbor.direction_to(position)
                self._model.Add(self._island_bridges_vars[neighbor][direction] == 0)

        self._black_cells_vars = {position: self._model.NewBoolVar(f"p{position}") for position, _ in self._regions_grid if position in self._island_bridges_vars}
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if not self._island_bridges_vars:
            self._init_model()

        return self._ensure_all_islands_connected()[0]

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        proposition_count = 0
        solver = cp_model.CpSolver()

        while True:
            status = solver.Solve(self._model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                return IslandGrid.empty(), proposition_count

            proposition_count += 1

            for position, direction_bridges in self._island_bridges_vars.items():
                for direction, var in direction_bridges.items():
                    next_pos = position.after(direction)
                    if next_pos in self._island_bridges_vars:
                        bridges_number = solver.Value(var)
                        self._island_grid[position].set_bridge_to_position(self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
                self._island_grid[position].set_bridges_count_according_to_directions_bridges()

            connected_positions = self._island_grid.get_connected_positions(exclude_without_bridge=True)
            if len(connected_positions) == 1:
                for position, var in self._black_cells_vars.items():
                    if solver.BooleanValue(var):
                        self._island_grid.set_value(position, '■')

                self._previous_solution = self._island_grid
                return self._island_grid, proposition_count

            for positions in connected_positions:
                vars_list = []
                for position in positions:
                    for direction, (_, value) in self._island_grid[position].direction_position_bridges.items():
                        var = self._island_bridges_vars[position][direction]
                        vars_list.append((var, value))
                if vars_list:
                    self._add_no_good_constraint(vars_list)

            self._init_island_grid()

    def get_other_solution(self):
        if self._previous_solution is None:
            return self.get_solution()
        if self._previous_solution.is_empty():
            return Grid.empty()

        vars_list = []
        for island in [island for island in self._previous_solution.islands.values() if island.position in self._island_bridges_vars]:
            for direction, (_, value) in island.direction_position_bridges.items():
                vars_list.append((self._island_bridges_vars[island.position][direction], value))
        if vars_list:
            self._add_no_good_constraint(vars_list)

        self._init_island_grid()
        return self.get_solution()

    def _add_no_good_constraint(self, vars_list):
        matches = []
        for var, value in vars_list:
            if value == 1:
                matches.append(var)
            else:
                one_minus = self._model.NewIntVar(0, 1, f"one_minus_prev_{var.Name()}")
                self._model.Add(one_minus + var == 1)
                matches.append(one_minus)
        self._model.Add(sum(matches) <= len(matches) - 1)

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_black_cell_constraints()
        self._add_no_adjacent_black_constraint()
        self._add_opposite_bridges_constraints()
        self._add_bridges_sum_constraints()

    def _add_initial_constraints(self):
        for c in range(self._island_grid.columns_number):
            pos = Position(0, c)
            if pos in self._island_bridges_vars:
                self._model.Add(self._island_bridges_vars[pos][Direction.up()] == 0)
        for c in range(self._island_grid.columns_number):
            pos = Position(self._island_grid.rows_number - 1, c)
            if pos in self._island_bridges_vars:
                self._model.Add(self._island_bridges_vars[pos][Direction.down()] == 0)
        for r in range(self._island_grid.rows_number):
            pos = Position(r, self._island_grid.columns_number - 1)
            if pos in self._island_bridges_vars:
                self._model.Add(self._island_bridges_vars[pos][Direction.right()] == 0)
        for r in range(self._island_grid.rows_number):
            pos = Position(r, 0)
            if pos in self._island_bridges_vars:
                self._model.Add(self._island_bridges_vars[pos][Direction.left()] == 0)

    def _add_opposite_bridges_constraints(self):
        for island in [island for island in self._island_grid.islands.values() if island.position in self._island_bridges_vars]:
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                position_bridges = island.direction_position_bridges.get(direction)
                if position_bridges is not None:
                    other_position, _ = position_bridges
                    if other_position not in self._island_bridges_vars:
                        continue
                    self._model.Add(self._island_bridges_vars[island.position][direction] == self._island_bridges_vars[other_position][direction.opposite])
                else:
                    self._model.Add(self._island_bridges_vars[island.position][direction] == 0)

    def _add_black_cell_constraints(self):
        for position, blacks_count in [(position, value) for position, value in self._blacks_count_grid if value >= 0]:
            region_id = next(region_id for region_id, positions in self._positions_by_region_id.items() if position in positions)
            region_positions = self._positions_by_region_id[region_id]
            vars_in_region = [self._black_cells_vars[position] for position in region_positions if position in self._island_bridges_vars.keys()]
            if vars_in_region:
                self._model.Add(sum(vars_in_region) == blacks_count)

    def _add_bridges_sum_constraints(self):
        for position in [position for position, _ in self._regions_grid]:
            if position not in self._island_bridges_vars:
                continue
            sum_dirs = sum([self._island_bridges_vars[position][direction] for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]])
            black_cell = self._black_cells_vars[position]
            self._model.Add(sum_dirs == 0).OnlyEnforceIf(black_cell)
            self._model.Add(sum_dirs == 2).OnlyEnforceIf(black_cell.Not())

    def _add_no_adjacent_black_constraint(self):
        for position in [position for position, _ in self._regions_grid]:
            if position not in self._black_cells_vars:
                continue
            for neighbor_position in self._regions_grid.neighbors_positions(position):
                if neighbor_position not in self._island_bridges_vars or neighbor_position not in self._black_cells_vars:
                    continue
                self._model.AddBoolOr([self._black_cells_vars[position].Not(), self._black_cells_vars[neighbor_position].Not()])
