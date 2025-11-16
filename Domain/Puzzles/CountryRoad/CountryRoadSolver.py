from z3 import Solver, Not, And, Or, Int, sat, Sum

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
        self._solver = Solver()
        self._previous_solution: IslandGrid | None = None

    def _init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._numbers_grid.columns_number)] for r in range(self._numbers_grid.rows_number)])

    def _init_solver(self):
        self._island_bridges_z3 = {
            island.position: {direction: Int(f"{island.position}_{direction}") for direction in Direction.orthogonal_directions()}
            for island in self._island_grid.islands.values()
        }
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if not self._solver.assertions():
            self._init_solver()

        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        proposition_count = 0
        while self._solver.check() == sat:
            model = self._solver.model()
            proposition_count += 1
            for position, direction_bridges in self._island_bridges_z3.items():
                for direction, bridges in direction_bridges.items():
                    if position.after(direction) not in self._island_bridges_z3:
                        continue
                    bridges_number = model.eval(bridges).as_long()
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

            not_loop_constraints = []
            for positions in connected_positions:
                cell_constraints = []
                for position in positions:
                    for direction, (_, value) in self._island_grid[position].direction_position_bridges.items():
                        cell_constraints.append(self._island_bridges_z3[position][direction] == value)
                not_loop_constraints.append(Not(And(cell_constraints)))
            self._solver.add(And(not_loop_constraints))
            self._init_island_grid()

        return IslandGrid.empty(), proposition_count

    def get_other_solution(self):
        previous_solution_constraints = []
        for island in self._previous_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                previous_solution_constraints.append(self._island_bridges_z3[island.position][direction] == value)
        self._solver.add(Not(And(previous_solution_constraints)))

        self._init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_crossed_cell_by_region_numbers_constraints()
        self._add_single_path_by_region_constraints()
        self._add_no_adjacent_empty_cell_between_regions_constraints()
        self._add_opposite_bridges_constraints()

    def _add_initial_constraints(self):
        for position, directions_bridges in self._island_bridges_z3.items():
            bridges_count_vars = list(directions_bridges.values())
            self._solver.add(Or(sum(bridges_count_vars) == 2, sum(bridges_count_vars) == 0))
            for direction_bridges in directions_bridges.values():
                self._solver.add(And(direction_bridges >= 0, direction_bridges <= 1))

    def _add_crossed_cell_by_region_numbers_constraints(self):
        numbers_by_position = {position: number for position, number in self._numbers_grid if number is not None}
        for region_id, positions in self._regions.items():
            for position in [position for position in positions if position in numbers_by_position]:
                number = numbers_by_position[position]
                if number is not None:
                    region_positions = self._regions[region_id]
                    all_bridges_number_for_region = []
                    for bridges in [self._island_bridges_z3[position] for position in region_positions]:
                        all_bridges_number_for_region += list(bridges.values())
                    self._solver.add(Sum(all_bridges_number_for_region) == number * 2)  # 2 bridges per island

    def _add_single_path_by_region_constraints(self):
        for region_positions in self._regions.values():
            region_edges_positions = [position for position in ShapeGenerator.edges(region_positions) if position in self._island_bridges_z3]
            out_directions = []
            for pos in region_edges_positions:
                out_directions += [self._island_bridges_z3[pos][dir] for dir in Direction.orthogonal_directions() if pos.after(dir) not in region_positions and pos.after(dir) in self._island_bridges_z3]
            self._solver.add(sum(out_directions) == 2)  # 1 for in and 1 for out

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._solver.add(self._island_bridges_z3[island.position][direction] ==
                                     self._island_bridges_z3[island.direction_position_bridges[direction][0]][direction.opposite])
                else:
                    self._solver.add(self._island_bridges_z3[island.position][direction] == 0)

    def _add_no_adjacent_empty_cell_between_regions_constraints(self):
        for region_positions in self._regions.values():
            for position in region_positions:
                neighbors_positions = [position for position in self._numbers_grid.neighbors_positions(position) if position not in region_positions]
                for neighbor_position in neighbors_positions:
                    self._solver.add(Or(sum([self._island_bridges_z3[neighbor_position][direction] for direction in Direction.orthogonal_directions()]) > 0,
                                        sum([self._island_bridges_z3[position][direction] for direction in Direction.orthogonal_directions()]) > 0))