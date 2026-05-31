from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import BoolVarT

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Island import Island
from PuzzleSolver.Board.IslandsGrid import IslandGrid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class DetourSolver(GameSolver):
    cell_empty = None

    def __init__(self, clues_grid: Grid, regions_grid: Grid):
        self._clues_grid = clues_grid
        self._regions = regions_grid.get_regions()
        self._island_grid: IslandGrid | None = None
        self._init_island_grid()
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._island_bridges_z3: dict[Position, dict[Direction, BoolVarT]] = {}
        self._flow_vars: dict[Position, dict[Direction, cp_model.IntVar]] = {}
        self._previous_solution: IslandGrid | None = None

    def _init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._clues_grid.columns_number)] for r in range(self._clues_grid.rows_number)]
        )

    def _init_solver(self):
        self._island_bridges_z3 = {
            island.position: {direction: self._model.new_bool_var(f"{island.position}_{direction}") for direction in Direction.orthogonal_directions()}
            for island in self._island_grid.islands.values()
        }
        n = self._island_grid.rows_number * self._island_grid.columns_number
        self._flow_vars = {
            position: {
                direction: self._model.new_int_var(0, n - 1, f"flow_{position}_{direction}")
                for direction in Direction.orthogonal_directions()
                if position.after(direction) in self._island_bridges_z3
            }
            for position in self._island_bridges_z3
        }
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if not self._model.Proto().variables:
            self._init_solver()

        status = self._solver.solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return IslandGrid.empty()

        self._init_island_grid()
        for position, direction_bridges in self._island_bridges_z3.items():
            for direction, bridges in direction_bridges.items():
                if self._solver.value(bridges) > 0:
                    self._island_grid[position].set_bridge_to_position(
                        self._island_grid[position].direction_position_bridges[direction][0], 1
                    )
                elif direction in self._island_grid[position].direction_position_bridges:
                    self._island_grid[position].direction_position_bridges.pop(direction)
            self._island_grid[position].set_bridges_count_according_to_directions_bridges()

        self._previous_solution = self._island_grid
        return self._island_grid

    def get_other_solution(self):
        literals_for_disjunction = []
        for island in self._previous_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                var = self._island_bridges_z3[island.position][direction]
                if value == 1:
                    literals_for_disjunction.append(var.negated())
                else:
                    literals_for_disjunction.append(var)
        self._model.add_bool_or(literals_for_disjunction)

        self._init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_opposite_bridges_constraints()
        self._add_bridges_sum_constraints()
        self._add_flow_constraints()
        self._add_clues_turn_regions_constraints()

    def _add_initial_constraints(self):
        constraints_border_up = [self._island_bridges_z3[Position(0, c)][Direction.up()] == 0 for c in range(self._island_grid.columns_number)]
        constraints_border_down = [
            self._island_bridges_z3[Position(self._island_grid.rows_number - 1, c)][Direction.down()] == 0 for c in range(self._island_grid.columns_number)
        ]
        constraints_border_right = [
            self._island_bridges_z3[Position(r, self._island_grid.columns_number - 1)][Direction.right()] == 0 for r in range(self._island_grid.rows_number)
        ]
        constraints_border_left = [self._island_bridges_z3[Position(r, 0)][Direction.left()] == 0 for r in range(self._island_grid.rows_number)]

        for constraint in constraints_border_down + constraints_border_up + constraints_border_right + constraints_border_left:
            self._model.add(constraint)

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._model.add(
                        self._island_bridges_z3[island.position][direction] ==
                        self._island_bridges_z3[island.direction_position_bridges[direction][0]][direction.opposite]
                    )
                else:
                    self._model.add(self._island_bridges_z3[island.position][direction] == 0)

    def _add_bridges_sum_constraints(self):
        for island in self._island_grid.islands.values():
            self._model.add(sum([self._island_bridges_z3[island.position][direction] for direction in Direction.orthogonal_directions()]) == 2)

    def _add_flow_constraints(self):
        n = self._island_grid.rows_number * self._island_grid.columns_number
        all_positions = set(self._island_bridges_z3.keys())
        source = Position(0, 0)

        for position, directions in self._flow_vars.items():
            for direction, flow_var in directions.items():
                bridge_var = self._island_bridges_z3[position][direction]
                self._model.add(flow_var <= (n - 1) * bridge_var)

        for position in all_positions:
            outgoing = []
            incoming = []
            for direction in Direction.orthogonal_directions():
                neighbor = position.after(direction)
                if neighbor in all_positions:
                    if direction in self._flow_vars[position]:
                        outgoing.append(self._flow_vars[position][direction])
                    opposite = direction.opposite
                    if opposite in self._flow_vars[neighbor]:
                        incoming.append(self._flow_vars[neighbor][opposite])
            if position == source:
                self._model.add(sum(outgoing) - sum(incoming) == n - 1)
            else:
                self._model.add(sum(incoming) - sum(outgoing) == 1)

    def _add_clues_turn_regions_constraints(self):
        for region in self._regions.values():
            self._add_clues_turn_region_constraints(region)

    def _add_clues_turn_region_constraints(self, region: frozenset[Position]):
        clues_in_region = [self._clues_grid[position] for position in region if self._clues_grid[position] != self.empty]
        if not clues_in_region:
            return
        turn_clue = max(clues_in_region)

        turn_variables = []
        for position in region:
            is_turn = self._create_turn_variable(position)
            turn_variables.append(is_turn)

        self._model.add(sum(turn_variables) == turn_clue)

    def _create_turn_variable(self, position: Position) -> BoolVarT:
        up = self._island_bridges_z3[position][Direction.up()]
        right = self._island_bridges_z3[position][Direction.right()]
        down = self._island_bridges_z3[position][Direction.down()]
        left = self._island_bridges_z3[position][Direction.left()]

        straight_vertical = self._model.new_bool_var("straight_vertical")
        self._model.add_bool_and([up, down]).only_enforce_if(straight_vertical)
        self._model.add_bool_or([up.negated(), down.negated()]).only_enforce_if(straight_vertical.negated())

        straight_horizontal = self._model.new_bool_var("straight_horizontal")
        self._model.add_bool_and([left, right]).only_enforce_if(straight_horizontal)
        self._model.add_bool_or([left.negated(), right.negated()]).only_enforce_if(straight_horizontal.negated())

        is_turn = self._model.new_bool_var("is_turn")
        self._model.add(is_turn + straight_vertical + straight_horizontal == 1)

        return is_turn
