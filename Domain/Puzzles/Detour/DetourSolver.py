from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import BoolVarT

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class DetourSolver(GameSolver):
    empty = None

    def __init__(self, clues_grid: Grid, regions_grid: Grid):
        self._clues_grid = clues_grid
        self._regions = regions_grid.get_regions()
        self._island_grid: IslandGrid | None = None
        self._init_island_grid()
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._island_bridges_z3: dict[Position, dict[Direction, BoolVarT]] = {}
        self._previous_solution: IslandGrid | None = None

    def _init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._clues_grid.columns_number)] for r in range(self._clues_grid.rows_number)]
        )

    def _init_solver(self):
        self._island_bridges_z3 = {
            island.position: {direction: self._model.NewBoolVar(f"{island.position}_{direction}") for direction in Direction.orthogonal_directions()}
            for island in self._island_grid.islands.values()
        }
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if not self._model.Proto().variables:
            self._init_solver()

        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        proposition_count = 0
        while self._solver.Solve(self._model) == cp_model.OPTIMAL:
            proposition_count += 1
            for position, direction_bridges in self._island_bridges_z3.items():
                for direction, bridges in direction_bridges.items():
                    if position.after(direction) not in self._island_bridges_z3:
                        continue
                    bridges_number = self._solver.Value(bridges)
                    if bridges_number > 0:
                        self._island_grid[position].set_bridge_to_position(
                            self._island_grid[position].direction_position_bridges[direction][0], bridges_number
                        )
                    elif position in self._island_grid and direction in self._island_grid[position].direction_position_bridges:
                        self._island_grid[position].direction_position_bridges.pop(direction)
                self._island_grid[position].set_bridges_count_according_to_directions_bridges()

            connected_positions = self._island_grid.get_connected_positions(exclude_without_bridge=False)
            if len(connected_positions) == 1:
                self._previous_solution = self._island_grid
                return self._island_grid, proposition_count

            for positions in connected_positions:
                literals_for_this_component = []
                for position in positions:
                    for direction, (_, value) in self._island_grid[position].direction_position_bridges.items():
                        var = self._island_bridges_z3[position][direction]
                        if value == 1:
                            literals_for_this_component.append(var.Not())
                        else:
                            literals_for_this_component.append(var)
                self._model.AddBoolOr(literals_for_this_component)
            self._init_island_grid()

        return IslandGrid.empty(), proposition_count

    def get_other_solution(self):
        literals_for_disjunction = []
        for island in self._previous_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                var = self._island_bridges_z3[island.position][direction]
                if value == 1:
                    literals_for_disjunction.append(var.Not())
                else:
                    literals_for_disjunction.append(var)
        self._model.AddBoolOr(literals_for_disjunction)

        self._init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_opposite_bridges_constraints()
        self._add_bridges_sum_constraints()
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
            self._model.Add(constraint)

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._model.Add(
                        self._island_bridges_z3[island.position][direction] ==
                        self._island_bridges_z3[island.direction_position_bridges[direction][0]][direction.opposite]
                    )
                else:
                    self._model.Add(self._island_bridges_z3[island.position][direction] == 0)

    def _add_bridges_sum_constraints(self):
        for island in self._island_grid.islands.values():
            self._model.Add(sum([self._island_bridges_z3[island.position][direction] for direction in Direction.orthogonal_directions()]) == 2)

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

        self._model.Add(sum(turn_variables) == turn_clue)

    def _create_turn_variable(self, position: Position) -> BoolVarT:
        up = self._island_bridges_z3[position][Direction.up()]
        right = self._island_bridges_z3[position][Direction.right()]
        down = self._island_bridges_z3[position][Direction.down()]
        left = self._island_bridges_z3[position][Direction.left()]

        turn_up_right = self._model.NewBoolVar("turn_up_right")
        self._model.AddBoolAnd([up, right, down.Not(), left.Not()]).OnlyEnforceIf(turn_up_right)
        self._model.AddBoolOr([up.Not(), right.Not(), down, left]).OnlyEnforceIf(turn_up_right.Not())

        turn_right_down = self._model.NewBoolVar("turn_right_down")
        self._model.AddBoolAnd([right, down, left.Not(), up.Not()]).OnlyEnforceIf(turn_right_down)
        self._model.AddBoolOr([right.Not(), down.Not(), left, up]).OnlyEnforceIf(turn_right_down.Not())

        turn_down_left = self._model.NewBoolVar("turn_down_left")
        self._model.AddBoolAnd([down, left, up.Not(), right.Not()]).OnlyEnforceIf(turn_down_left)
        self._model.AddBoolOr([down.Not(), left.Not(), up, right]).OnlyEnforceIf(turn_down_left.Not())

        turn_left_up = self._model.NewBoolVar("turn_left_up")
        self._model.AddBoolAnd([left, up, right.Not(), down.Not()]).OnlyEnforceIf(turn_left_up)
        self._model.AddBoolOr([left.Not(), up.Not(), right, down]).OnlyEnforceIf(turn_left_up.Not())

        is_turn = self._model.NewBoolVar("is_turn")
        self._model.AddBoolOr([turn_up_right, turn_right_down, turn_down_left, turn_left_up]).OnlyEnforceIf(is_turn)
        self._model.AddBoolAnd([turn_up_right.Not(), turn_right_down.Not(), turn_down_left.Not(), turn_left_up.Not()]).OnlyEnforceIf(is_turn.Not())

        return is_turn
