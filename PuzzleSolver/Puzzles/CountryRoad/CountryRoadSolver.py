from ortools.sat.python import cp_model

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.GridMask import is_outside_region, resolve_outside
from PuzzleSolver.Board.Island import Island
from PuzzleSolver.Board.IslandsGrid import IslandGrid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver
from Utils.ShapeGenerator import ShapeGenerator


class CountryRoadSolver(GameSolver):
    def __init__(self, clues_grid: Grid, regions_grid: Grid):
        super().__init__()
        self._clues_grid = clues_grid
        self._outside = resolve_outside(clues_grid)
        self._regions = regions_grid.get_regions()
        self._rows_number = self._clues_grid.rows_number
        self._columns_number = self._clues_grid.columns_number
        self._init_island_grid()
        self._model = cp_model.CpModel()
        self._island_bridges_var: dict[Position, dict[Direction, cp_model.BoolVarT]] = {}
        self._previous_solution: IslandGrid | None = None
        self._initialized = False

    def _init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._clues_grid.columns_number)] for r in range(self._clues_grid.rows_number)])

    def _init_solver(self):
        self._island_bridges_var = {
            island.position: {direction: self._model.new_bool_var(f"{island.position}_{direction}") for direction in Direction.orthogonal_directions()}
            for island in self._island_grid.islands.values()
        }
        self._add_constraints()
        self._initialized = True

    def get_solution(self) -> IslandGrid:
        if not self._initialized:
            self._init_solver()

        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _extract_island_grid(self) -> IslandGrid:
        island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._columns_number)] for r in range(self._rows_number)])
        for position, direction_bridges in self._island_bridges_var.items():
            for direction, var in direction_bridges.items():
                if position.after(direction) not in self._island_bridges_var:
                    continue
                bridges_number = self._solver.value(var)
                if bridges_number > 0:
                    island_grid[position].set_bridge_to_position(
                        island_grid[position].direction_position_bridges[direction][0], bridges_number)
                elif position in island_grid and direction in island_grid[position].direction_position_bridges:
                    island_grid[position].direction_position_bridges.pop(direction)
            island_grid[position].set_bridges_count_according_to_directions_bridges()
        return island_grid

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        proposition_count = 0
        while True:
            status = self._solver.solve(self._model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                return IslandGrid.empty(), proposition_count

            proposition_count += 1
            island_grid = self._extract_island_grid()
            connected_positions = island_grid.get_connected_positions(exclude_without_bridge=True)
            if len(connected_positions) == 1:
                self._previous_solution = island_grid
                return island_grid, proposition_count

            biggest = max(connected_positions, key=len)
            connected_positions.remove(biggest)
            for positions in connected_positions:
                blocking_vars = []
                for position in positions:
                    for direction in Direction.orthogonal_directions():
                        neighbor = position.after(direction)
                        if neighbor not in self._island_bridges_var:
                            continue
                        var = self._island_bridges_var[position][direction]
                        if self._solver.value(var) == 1:
                            blocking_vars.append(var.Not())
                        else:
                            blocking_vars.append(var)
                if blocking_vars:
                    self._model.add_bool_or(blocking_vars)

    def get_other_solution(self):
        if self._previous_solution is None:
            return self.get_solution()

        blocking_vars = []
        for island in self._previous_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                var = self._island_bridges_var[island.position][direction]
                if value == 1:
                    blocking_vars.append(var.Not())
                else:
                    blocking_vars.append(var)
        if blocking_vars:
            self._model.add_bool_or(blocking_vars)

        self._init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_crossed_cell_by_region_numbers_constraints()
        self._add_single_path_by_region_constraints()
        self._add_no_adjacent_empty_cell_between_regions_constraints()
        self._add_opposite_bridges_constraints()

    def _add_initial_constraints(self):
        for position, directions_bridges in self._island_bridges_var.items():
            bridges_count_vars = list(directions_bridges.values())
            s = self._model.new_int_var(0, 4, f"sum_{position.r}_{position.c}")
            self._model.add(s == sum(bridges_count_vars))
            if (position.r, position.c) in self._outside:
                self._model.add_allowed_assignments([s], [(0,)])
                for var in bridges_count_vars:
                    self._model.add(var == 0)
            else:
                self._model.add_allowed_assignments([s], [(0,), (2,)])

    def _add_crossed_cell_by_region_numbers_constraints(self):
        numbers_by_position = {position: number for position, number in self._clues_grid if number is not None}
        for region_id, positions in self._regions.items():
            if is_outside_region(positions, self._outside):
                continue
            for position in [position for position in positions if position in numbers_by_position]:
                number = numbers_by_position[position]
                if number is not None:
                    region_positions = self._regions[region_id]
                    all_bridges_number_for_region = []
                    for bridges in [self._island_bridges_var[position] for position in region_positions]:
                        all_bridges_number_for_region += list(bridges.values())
                    self._model.add(sum(all_bridges_number_for_region) == number * 2)

    def _add_single_path_by_region_constraints(self):
        for region_positions in self._regions.values():
            if is_outside_region(region_positions, self._outside):
                continue
            region_edges_positions = [position for position in ShapeGenerator.edges(region_positions) if position in self._island_bridges_var]
            out_directions = []
            for pos in region_edges_positions:
                out_directions += [self._island_bridges_var[pos][direction] for direction in Direction.orthogonal_directions() if pos.after(direction) not in region_positions and pos.after(direction) in self._island_bridges_var]
            self._model.add(sum(out_directions) == 2)

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    neighbor_pos = island.direction_position_bridges[direction][0]
                    self._model.add(self._island_bridges_var[island.position][direction] == self._island_bridges_var[neighbor_pos][direction.opposite])
                else:
                    self._model.add(self._island_bridges_var[island.position][direction] == 0)

    def _add_no_adjacent_empty_cell_between_regions_constraints(self):
        for region_positions in self._regions.values():
            if is_outside_region(region_positions, self._outside):
                continue
            for position in region_positions:
                if (position.r, position.c) in self._outside:
                    continue
                neighbors_positions = [
                    neighbor
                    for neighbor in self._clues_grid.neighbors_positions(position)
                    if neighbor not in region_positions and (neighbor.r, neighbor.c) not in self._outside
                ]
                for neighbor_position in neighbors_positions:
                    sum_neighbor = sum(self._island_bridges_var[neighbor_position][direction] for direction in Direction.orthogonal_directions())
                    sum_position = sum(self._island_bridges_var[position][direction] for direction in Direction.orthogonal_directions())
                    self._model.add(sum_neighbor + sum_position >= 1)
