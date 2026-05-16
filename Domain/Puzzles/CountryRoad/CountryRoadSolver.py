from ortools.sat.python.cp_model import CpModel, CpSolver

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver
from Utils.ShapeGenerator import ShapeGenerator


class CountryRoadSolver(GameSolver):
    def __init__(self, grid: Grid, regions_grid: Grid):
        self._numbers_grid = grid
        self._regions = regions_grid.get_regions()
        self._rows_number = self._numbers_grid.rows_number
        self._columns_number = self._numbers_grid.columns_number
        self._init_island_grid()
        self._model = CpModel()
        self._solver = CpSolver()
        self._island_bridges_ortools: dict[Position, dict[Direction, any]] = {}
        self._previous_solution: IslandGrid | None = None

    def _init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._numbers_grid.columns_number)] for r in range(self._numbers_grid.rows_number)])

    def _init_solver(self):
        self._model = CpModel()
        self._island_bridges_ortools = {
            island.position: {
                direction: self._model.new_bool_var(f"b_{island.position}_{direction}")
                for direction in Direction.orthogonal_directions()
            }
            for island in self._island_grid.islands.values()
        }
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        self._init_solver()
        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        proposition_count = 0

        while True:
            status = self._solver.solve(self._model)
            if status not in (4, 2):
                break

            proposition_count += 1
            for position, direction_bridges in self._island_bridges_ortools.items():
                island = self._island_grid[position]
                for direction, var in direction_bridges.items():
                    if position.after(direction) not in self._island_bridges_ortools:
                        continue
                    bridges_number = self._solver.value(var)
                    if bridges_number > 0:
                        island.set_bridge_to_position(
                            island.direction_position_bridges[direction][0], bridges_number)
                    elif direction in island.direction_position_bridges:
                        island.direction_position_bridges.pop(direction)
                island.set_bridges_count_according_to_directions_bridges()

            connected_positions = self._island_grid.get_connected_positions(exclude_without_bridge=True)
            if len(connected_positions) == 1:
                self._previous_solution = self._island_grid
                return self._island_grid, proposition_count

            for positions in connected_positions:
                component_vars = []
                for position in positions:
                    for direction, (_, _) in self._island_grid[position].direction_position_bridges.items():
                        component_vars.append(self._island_bridges_ortools[position][direction].negated())
                if component_vars:
                    self._model.add_bool_or(component_vars)

            self._init_island_grid()

        return IslandGrid.empty(), proposition_count

    def get_other_solution(self) -> IslandGrid:
        if not self._previous_solution:
            return IslandGrid.empty()

        previous_solution_constraints = []
        for island in self._previous_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                var = self._island_bridges_ortools[island.position][direction]
                if value > 0:
                    previous_solution_constraints.append(var.negated())
                else:
                    previous_solution_constraints.append(var)

        if previous_solution_constraints:
            self._model.add_bool_or(previous_solution_constraints)

        self._init_island_grid()
        return self._ensure_all_islands_connected()[0]

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_crossed_cell_by_region_numbers_constraints()
        self._add_single_path_by_region_constraints()
        self._add_no_adjacent_empty_cell_between_regions_constraints()
        self._add_opposite_bridges_constraints()

    def _add_initial_constraints(self):
        for directions_bridges in self._island_bridges_ortools.values():
            sum_bridges = sum(directions_bridges.values())
            self._model.add(sum_bridges != 1)
            self._model.add(sum_bridges != 3)
            self._model.add(sum_bridges != 4)

    def _add_crossed_cell_by_region_numbers_constraints(self):
        numbers_by_position = {position: number for position, number in self._numbers_grid if number is not None}
        for region_id, positions in self._regions.items():
            for position in [position for position in positions if position in numbers_by_position]:
                number = numbers_by_position[position]
                if number is not None:
                    region_positions = self._regions[region_id]
                    all_bridges_number_for_region = sum(
                        sum(self._island_bridges_ortools[pos].values())
                        for pos in region_positions
                    )
                    self._model.add(all_bridges_number_for_region == number * 2)

    def _add_single_path_by_region_constraints(self):
        for region_positions in self._regions.values():
            region_edges_positions = [position for position in ShapeGenerator.edges(region_positions) if position in self._island_bridges_ortools]
            out_directions = []
            for pos in region_edges_positions:
                out_directions += [self._island_bridges_ortools[pos][direction] for direction in Direction.orthogonal_directions() if pos.after(direction) not in region_positions and pos.after(direction) in self._island_bridges_ortools]
            self._model.add(sum(out_directions) == 2)

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if direction in island.direction_position_bridges:
                    neighbor_pos, _ = island.direction_position_bridges[direction]
                    self._model.add(self._island_bridges_ortools[island.position][direction] ==
                                    self._island_bridges_ortools[neighbor_pos][direction.opposite])
                else:
                    self._model.add(self._island_bridges_ortools[island.position][direction] == 0)

    def _add_no_adjacent_empty_cell_between_regions_constraints(self):
        for region_positions in self._regions.values():
            for position in region_positions:
                for neighbor_position in self._numbers_grid.neighbors_positions(position):
                    if neighbor_position in region_positions:
                        continue
                    self._model.add(
                        sum(self._island_bridges_ortools[neighbor_position].values()) +
                        sum(self._island_bridges_ortools[position].values()) >= 2
                    )
