from typing import Dict

from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import CpModel, CpSolverSolutionCallback, FEASIBLE, OPTIMAL

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver
from Utils.ShapeGenerator import ShapeGenerator


class MoonsunSolver(GameSolver):
    white = 'w'
    black = 'b'
    no_circle = None

    def __init__(self, circle_grid: Grid, regions_grid: Grid):
        self._circle_grid = circle_grid
        self._regions_grid = regions_grid
        self._regions = regions_grid.get_regions()
        self._island_grid: IslandGrid | None = None
        self._init_island_grid()
        self._model = CpModel()
        self._solver = cp_model.CpSolver()
        self._island_bridges_z3: Dict[Position, Dict[Direction, Var]] = {}
        self._previous_solution: IslandGrid | None = None
        self._solver_initialized = False

    def _init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._circle_grid.columns_number)] for r in range(self._circle_grid.rows_number)])

    def _init_solver(self):
        self._island_bridges_z3 = {island.position: {direction: self._model.NewIntVar(0, 1, f"{island.position}_{direction}") for direction in Direction.orthogonals()} for island in
                                   self._island_grid.islands.values()}
        self._add_constraints()
        self._solver_initialized = True

    def get_solution(self) -> IslandGrid:
        if not self._solver_initialized:
            self._init_solver()

        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        proposition_count = 0
        while self._solver.Solve(self._model) in [FEASIBLE, OPTIMAL]:
            proposition_count += 1
            for position, direction_bridges in self._island_bridges_z3.items():
                for direction, bridges in direction_bridges.items():
                    if position.after(direction) not in self._island_bridges_z3:
                        continue
                    bridges_number = self._solver.Value(bridges)
                    if bridges_number > 0:
                        self._island_grid[position].set_bridge_to_position(
                            self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
                    elif position in self._island_grid and direction in self._island_grid[position].direction_position_bridges:
                        self._island_grid[position].direction_position_bridges.pop(direction)
                self._island_grid[position].set_bridges_count_according_to_directions_bridges()

            connected_positions = self._island_grid.get_connected_positions(exclude_without_bridge=True)
            if len(connected_positions) == 1:
                self._previous_solution = self._island_grid
                return self._island_grid, proposition_count

            for i, positions in enumerate(connected_positions):
                cell_constraints = []
                for position in positions:
                    for direction, (_, value) in self._island_grid[position].direction_position_bridges.items():
                        b = self._model.NewBoolVar(f'constraint_{i}_{position}_{direction}')
                        self._model.Add(self._island_bridges_z3[position][direction] != value).OnlyEnforceIf(b)
                        self._model.Add(self._island_bridges_z3[position][direction] == value).OnlyEnforceIf(b.Not())
                        cell_constraints.append(b)
                if cell_constraints:
                    self._model.AddBoolOr(cell_constraints)
            self._init_island_grid()

        return IslandGrid.empty(), proposition_count

    def get_other_solution(self):
        previous_solution_constraints = []
        for island in self._previous_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                b = self._model.NewBoolVar(f'other_solution_{island.position}_{direction}')
                self._model.Add(self._island_bridges_z3[island.position][direction] != value).OnlyEnforceIf(b)
                self._model.Add(self._island_bridges_z3[island.position][direction] == value).OnlyEnforceIf(b.Not())
                previous_solution_constraints.append(b)
        if previous_solution_constraints:
            self._model.AddBoolOr(previous_solution_constraints)

        self._init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_opposite_bridges_constraints()
        self._add_bridges_sum_constraints()
        self._add_single_path_by_region_constraints()
        self._add_all_same_color_in_region_crossed_constraints()
        self._add_all_regions_crossed_constraints()
        self._add_alternating_black_and_withe_constraints()

    def _add_initial_constraints(self):
        for c in range(self._island_grid.columns_number):
            self._model.Add(self._island_bridges_z3[Position(0, c)][Direction.up()] == 0)
            self._model.Add(self._island_bridges_z3[Position(self._island_grid.rows_number - 1, c)][Direction.down()] == 0)
        for r in range(self._island_grid.rows_number):
            self._model.Add(self._island_bridges_z3[Position(r, self._island_grid.columns_number - 1)][Direction.right()] == 0)
            self._model.Add(self._island_bridges_z3[Position(r, 0)][Direction.left()] == 0)

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._model.Add(
                        self._island_bridges_z3[island.position][direction] == self._island_bridges_z3[island.direction_position_bridges[direction][0]][
                            direction.opposite])
                else:
                    self._model.Add(self._island_bridges_z3[island.position][direction] == 0)

    def _add_bridges_sum_constraints(self):
        for island in self._island_grid.islands.values():
            s = self._model.NewIntVar(0, 4, f'sum_{island.position}')
            self._model.Add(s == sum(self._island_bridges_z3[island.position][direction] for direction in Direction.orthogonals()))
            self._model.AddAllowedAssignments([s], [(0,), (2,)])

    def _add_single_path_by_region_constraints(self):
        for region_positions in self._regions.values():
            region_edges_positions = [position for position in ShapeGenerator.edges(region_positions) if position in self._island_bridges_z3]
            out_directions = []
            for pos in region_edges_positions:
                out_directions += [self._island_bridges_z3[pos][dir] for dir in Direction.orthogonals() if pos.after(dir) not in region_positions and pos.after(dir) in self._island_bridges_z3]
            self._model.Add(sum(out_directions) == 2)  # 1 for in and 1 for out

    def _add_all_regions_crossed_constraints(self):
        for region in self._regions.values():
            self._add_regions_crossed_constraints(region)

    def _add_regions_crossed_constraints(self, region: frozenset[Position]):
        sum_for_positions_constraints = []
        for position in region:
            crossed = self._model.NewBoolVar(f"crossed_{position}")
            self._model.Add(sum(self._island_bridges_z3[position][direction] for direction in Direction.orthogonals()) == 2).OnlyEnforceIf(crossed)
            self._model.Add(sum(self._island_bridges_z3[position][direction] for direction in Direction.orthogonals()) != 2).OnlyEnforceIf(crossed.Not())
            sum_for_positions_constraints.append(crossed)
        self._model.AddBoolOr(sum_for_positions_constraints)

    def _add_alternating_black_and_withe_constraints(self):
        colors_regions = {}
        for region_id, region in self._regions.items():
            color_region = self._model.NewIntVar(1, 2, f"color_region_{region_id}")
            colors_regions[region_id] = color_region

        for region_id, region in self._regions.items():
            for pos in [pos for pos in region if self._circle_grid[pos] == self.white]:
                crossed = self._model.NewBoolVar(f"crossed_{pos}")
                self._model.Add(sum(self._island_bridges_z3[pos][direction] for direction in Direction.orthogonals()) == 2).OnlyEnforceIf(crossed)
                self._model.Add(sum(self._island_bridges_z3[pos][direction] for direction in Direction.orthogonals()) != 2).OnlyEnforceIf(crossed.Not())
                self._model.Add(colors_regions[region_id] == 1).OnlyEnforceIf(crossed)
            for pos in [pos for pos in region if self._circle_grid[pos] == self.black]:
                crossed = self._model.NewBoolVar(f"crossed_{pos}")
                self._model.Add(sum(self._island_bridges_z3[pos][direction] for direction in Direction.orthogonals()) == 2).OnlyEnforceIf(crossed)
                self._model.Add(sum(self._island_bridges_z3[pos][direction] for direction in Direction.orthogonals()) != 2).OnlyEnforceIf(crossed.Not())
                self._model.Add(colors_regions[region_id] == 2).OnlyEnforceIf(crossed)

            for position in region:
                for neighbors_position in [pos for pos in self._circle_grid.neighbors_positions(position) if pos not in region]:
                    neighbor_region_id = self._regions_grid[neighbors_position]
                    direction = position.direction_to(neighbors_position)
                    linked = self._island_bridges_z3[position][direction]
                    self._model.Add(colors_regions[neighbor_region_id] != colors_regions[region_id]).OnlyEnforceIf(linked)

        white_regions = []
        for region_id in colors_regions:
            is_white = self._model.NewBoolVar(f"is_white_{region_id}")
            self._model.Add(colors_regions[region_id] == 1).OnlyEnforceIf(is_white)
            self._model.Add(colors_regions[region_id] != 1).OnlyEnforceIf(is_white.Not())
            white_regions.append(is_white)
        self._model.Add(sum(white_regions) == len(colors_regions) // 2)

    def _add_all_same_color_in_region_crossed_constraints(self):
        for region_id, region in self._regions.items():
            self._add_same_color_in_region_crossed_constraints(region_id, region)

    def _add_same_color_in_region_crossed_constraints(self, region_id, region):
        white_positions = [position for position in region if self._circle_grid[position] == self.white]
        black_positions = [position for position in region if self._circle_grid[position] == self.black]

        if not white_positions and not black_positions:
            return

        is_white_region = self._model.NewBoolVar(f"is_white_region_{region_id}")
        is_black_region = self._model.NewBoolVar(f"is_black_region_{region_id}")

        if not white_positions:
            self._model.Add(is_black_region == 1)
            self._model.Add(is_white_region == 0)
        elif not black_positions:
            self._model.Add(is_white_region == 1)
            self._model.Add(is_black_region == 0)
        else:
            self._model.Add(is_white_region + is_black_region == 1)

        for pos in white_positions:
            s = sum(self._island_bridges_z3[pos][d] for d in Direction.orthogonals())
            self._model.Add(s == 2).OnlyEnforceIf(is_white_region)
            self._model.Add(s == 0).OnlyEnforceIf(is_black_region)

        for pos in black_positions:
            s = sum(self._island_bridges_z3[pos][d] for d in Direction.orthogonals())
            self._model.Add(s == 2).OnlyEnforceIf(is_black_region)
            self._model.Add(s == 0).OnlyEnforceIf(is_white_region)
