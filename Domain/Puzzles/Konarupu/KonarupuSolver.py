from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import BoolVarT

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver

_ = ''


class KonarupuSolver(GameSolver):
    def __init__(self, grid: Grid):
        self.input_grid = grid
        self._island_grid: IslandGrid | None = None
        self._init_island_grid()
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._island_bridges_vars: dict[Position, dict[Direction, BoolVarT]] = {}
        self._previous_solution: IslandGrid | None = None

    def _init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self.input_grid.columns_number + 1)] for r in range(self.input_grid.rows_number + 1)])

    def _init_solver(self):
        self._island_bridges_vars = {island.position: {direction: self._model.new_bool_var(f"{island.position}_{direction}") for direction in Direction.orthogonal_directions()} for island in
                                     self._island_grid.islands.values()}
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if not self._model.Proto().variables:
            self._init_solver()

        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        proposition_count = 0
        while True:
            status = self._solver.solve(self._model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                return IslandGrid.empty(), proposition_count

            proposition_count += 1
            for position, direction_bridges in self._island_bridges_vars.items():
                for direction, bridges_var in direction_bridges.items():
                    if position.after(direction) not in self._island_bridges_vars:
                        continue
                    is_bridge = self._solver.boolean_value(bridges_var)
                    if is_bridge:
                        self._island_grid[position].set_bridge_to_position(
                            self._island_grid[position].direction_position_bridges[direction][0], 1)
                    elif direction in self._island_grid[position].direction_position_bridges:
                        self._island_grid[position].direction_position_bridges.pop(direction)
                self._island_grid[position].set_bridges_count_according_to_directions_bridges()

            connected_positions = self._island_grid.get_connected_positions(exclude_without_bridge=True)
            if len(connected_positions) == 1:
                self._previous_solution = self._island_grid
                return self._island_grid, proposition_count

            block_literals = []
            for position, direction_bridges in self._island_bridges_vars.items():
                for direction, bridges_var in direction_bridges.items():
                    if position.after(direction) not in self._island_bridges_vars:
                        continue
                    is_bridge = self._solver.boolean_value(bridges_var)
                    if is_bridge:
                        block_literals.append(bridges_var.negated())
                    else:
                        block_literals.append(bridges_var)
            self._model.add_bool_or(block_literals)

            for positions in connected_positions:
                comp_literals = []
                for position in positions:
                    for direction, (_, value) in self._island_grid[position].direction_position_bridges.items():
                        var = self._island_bridges_vars[position][direction]
                        if value == 1:
                            comp_literals.append(var.negated())
                        else:
                            comp_literals.append(var)
                self._model.add_bool_or(comp_literals)

            self._init_island_grid()

    def get_other_solution(self):
        literals_for_disjunction = []
        for island in self._previous_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                var = self._island_bridges_vars[island.position][direction]
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
        self._add_numbers_constraints()

    def _add_initial_constraints(self):
        constraints = []
        constraints += [self._island_bridges_vars[Position(0, c)][Direction.up()] == 0 for c in range(self._island_grid.columns_number)]
        constraints += [self._island_bridges_vars[Position(self._island_grid.rows_number - 1, c)][Direction.down()] == 0 for c in
                        range(self._island_grid.columns_number)]
        constraints += [self._island_bridges_vars[Position(r, self._island_grid.columns_number - 1)][Direction.right()] == 0 for r in
                        range(self._island_grid.rows_number)]
        constraints += [self._island_bridges_vars[Position(r, 0)][Direction.left()] == 0 for r in range(self._island_grid.rows_number)]
        for constraint in constraints:
            self._model.add(constraint)

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._model.add(
                        self._island_bridges_vars[island.position][direction] == self._island_bridges_vars[island.direction_position_bridges[direction][0]][
                            direction.opposite])
                else:
                    self._model.add(self._island_bridges_vars[island.position][direction] == 0)

    def _add_bridges_sum_constraints(self):
        for island in self._island_grid.islands.values():
            b = self._island_bridges_vars[island.position]
            bridge_sum = sum([b[direction] for direction in Direction.orthogonal_directions()])
            self._model.add(bridge_sum != 1)
            self._model.add(bridge_sum != 3)
            self._model.add(bridge_sum != 4)

    def _add_numbers_constraints(self):
        for position, number in [(position, number) for position, number in self.input_grid if number != _]:
            up_left_no_turn = self._create_no_turn_var(position, self._island_bridges_vars[position])
            down_left_no_turn = self._create_no_turn_var(position.down, self._island_bridges_vars[position.down])
            down_right_no_turn = self._create_no_turn_var(position.down_right, self._island_bridges_vars[position.down_right])
            up_right_no_turn = self._create_no_turn_var(position.right, self._island_bridges_vars[position.right])
            self._model.add(up_left_no_turn + down_left_no_turn + down_right_no_turn + up_right_no_turn == 4 - number)

    def _create_no_turn_var(self, position: Position, corner_directions_var: dict[Direction, BoolVarT]) -> BoolVarT:
        up = corner_directions_var[Direction.up()]
        down = corner_directions_var[Direction.down()]
        left = corner_directions_var[Direction.left()]
        right = corner_directions_var[Direction.right()]

        vertical = self._model.new_bool_var(f"vertical_{position}")
        self._model.add_bool_and([up, down]).only_enforce_if(vertical)
        self._model.add_bool_or([up.negated(), down.negated()]).only_enforce_if(vertical.negated())

        horizontal = self._model.new_bool_var(f"horizontal_{position}")
        self._model.add_bool_and([left, right]).only_enforce_if(horizontal)
        self._model.add_bool_or([left.negated(), right.negated()]).only_enforce_if(horizontal.negated())

        empty = self._model.new_bool_var(f"empty_{position}")
        self._model.add_bool_and([up.negated(), down.negated(), left.negated(), right.negated()]).only_enforce_if(empty)
        self._model.add_bool_or([up, down, left, right]).only_enforce_if(empty.negated())

        no_turn = self._model.new_bool_var(f"no_turn_{position}")
        self._model.add_bool_or([vertical, horizontal, empty]).only_enforce_if(no_turn)
        self._model.add_bool_and([vertical.negated(), horizontal.negated(), empty.negated()]).only_enforce_if(no_turn.negated())

        return no_turn
