from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import BoolVarT

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class BalanceLoopSolver(GameSolver):
    empty = None
    white = 'w'
    black = 'b'

    def __init__(self, clues_grid: Grid):
        self._clues_grid = clues_grid
        self._island_grid: IslandGrid | None = None
        self._init_island_grid()
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._island_bridges_vars: dict[Position, dict[Direction, BoolVarT]] = {}
        self._previous_solution: IslandGrid | None = None

    def _init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._clues_grid.columns_number)] for r in range(self._clues_grid.rows_number)])

    def _init_solver(self):
        self._model = cp_model.CpModel()
        self._island_bridges_vars = {island.position: {direction: self._model.new_bool_var(f"{island.position}_{direction}") for direction in Direction.orthogonal_directions()} for island in
                                     self._island_grid.islands.values()}
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if not self._island_bridges_vars:
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
                        self._island_grid[position].set_bridge_to_position(self._island_grid[position].direction_position_bridges[direction][0], 1)
                    elif position in self._island_grid and direction in self._island_grid[position].direction_position_bridges:
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
        self._add_dots_constraints()

    def _add_initial_constraints(self):
        constraints_border_up = [self._island_bridges_vars[Position(0, c)][Direction.up()] == 0 for c in range(self._island_grid.columns_number)]
        constraints_border_down = [self._island_bridges_vars[Position(self._island_grid.rows_number - 1, c)][Direction.down()] == 0 for c in
                                   range(self._island_grid.columns_number)]
        constraints_border_right = [self._island_bridges_vars[Position(r, self._island_grid.columns_number - 1)][Direction.right()] == 0 for r in
                                    range(self._island_grid.rows_number)]
        constraints_border_left = [self._island_bridges_vars[Position(r, 0)][Direction.left()] == 0 for r in range(self._island_grid.rows_number)]
        for constraint in constraints_border_down + constraints_border_up + constraints_border_right + constraints_border_left:
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
        for position, value in self._clues_grid:
            bridge_vars = [self._island_bridges_vars[position][direction] for direction in Direction.orthogonal_directions()]
            if value != self.empty:
                self._model.add(sum(bridge_vars) == 2)
                continue

            is_used = self._model.new_bool_var(f"u_{position.r}_{position.c}")
            self._model.add(sum(bridge_vars) == 2).only_enforce_if(is_used)
            self._model.add(sum(bridge_vars) == 0).only_enforce_if(is_used.negated())

    def _add_dots_constraints(self):
        for position, cell_value in [(position, value) for position, value in self._clues_grid if value != self.empty]:
            color, segments_count = self._convert_cell_value_to_color_and_segments_count(cell_value)
            match segments_count:
                case 0:
                    all_options_vars = self._compute_options_vars_without_segments_length(position, color)
                    self._model.add_bool_or(all_options_vars)
                case 2:
                    all_options_vars = self._compute_options_vars(position, segments_count, color)
                    self._model.add_bool_or(all_options_vars)
                    self._not_loop_turn2_constraint(position)
                case _:
                    all_options_vars = self._compute_options_vars(position, segments_count, color)
                    self._model.add_bool_or(all_options_vars)

    def _compute_options_vars(self, position: Position, segments_count: int, color: str) -> list[BoolVarT]:
        all_options = []
        all_options.extend(self._not_turn_options_vars(position, segments_count, color))
        all_options.extend(self._turn_options_vars(position, segments_count, color))
        return all_options

    def _not_turn_options_vars(self, position: Position, segments_count: int, color: str) -> list[BoolVarT]:
        options = []
        if color == self.white:
            first_part_count = segments_count // 2
            second_part_count = segments_count - first_part_count
            options.extend(self._vertical_options_vars(position, first_part_count, second_part_count))
            options.extend(self._horizontal_options_vars(position, first_part_count, second_part_count))
        else:
            for first_part_count in range(1, segments_count):
                second_part_count = segments_count - first_part_count
                if second_part_count == first_part_count:
                    continue
                options.extend(self._vertical_options_vars(position, first_part_count, second_part_count))
                options.extend(self._horizontal_options_vars(position, first_part_count, second_part_count))
        return options

    def _build_shape_var(self, name: str, conditions: list, end_conditions_lists: list[list[BoolVarT]]) -> BoolVarT | None:
        if any(not lst for lst in end_conditions_lists):
            return None
        shape_var = self._model.new_bool_var(name)
        for cond in conditions:
            self._model.add(cond).only_enforce_if(shape_var)
        for lst in end_conditions_lists:
            self._model.add_bool_or(lst).only_enforce_if(shape_var)
        return shape_var

    def _vertical_options_vars(self, position: Position, first_part_count: int, second_part_count: int) -> list[BoolVarT]:
        vertical_positions = (
                [position.after(Direction.up(), count) for count in reversed(range(1, first_part_count + 1))] +
                [position] +
                [position.after(Direction.down(), count) for count in range(1, second_part_count + 1)]
        )
        if not all(pos in self._island_bridges_vars for pos in vertical_positions):
            return []

        conditions = []
        for pos in vertical_positions[1:first_part_count + 1]:
            conditions.append(self._island_bridges_vars[pos][Direction.up()] == 1)
        for pos in vertical_positions[first_part_count:-1]:
            conditions.append(self._island_bridges_vars[pos][Direction.down()] == 1)

        top_conditions = []
        if Direction.left() in self._island_bridges_vars[vertical_positions[0]]:
            top_conditions.append(self._island_bridges_vars[vertical_positions[0]][Direction.left()])
        if Direction.right() in self._island_bridges_vars[vertical_positions[0]]:
            top_conditions.append(self._island_bridges_vars[vertical_positions[0]][Direction.right()])

        bottom_conditions = []
        if Direction.left() in self._island_bridges_vars[vertical_positions[-1]]:
            bottom_conditions.append(self._island_bridges_vars[vertical_positions[-1]][Direction.left()])
        if Direction.right() in self._island_bridges_vars[vertical_positions[-1]]:
            bottom_conditions.append(self._island_bridges_vars[vertical_positions[-1]][Direction.right()])

        shape_var = self._build_shape_var(f"v_no_turn_{position}_{first_part_count}_{second_part_count}", conditions, [top_conditions, bottom_conditions])
        return [shape_var] if shape_var is not None else []

    def _horizontal_options_vars(self, position: Position, first_part_count: int, second_part_count: int) -> list[BoolVarT]:
        horizontal_positions = (
                [position.after(Direction.left(), count) for count in reversed(range(1, first_part_count + 1))] +
                [position] +
                [position.after(Direction.right(), count) for count in range(1, second_part_count + 1)]
        )
        if not all(pos in self._island_bridges_vars for pos in horizontal_positions):
            return []

        conditions = []
        for pos in horizontal_positions[1:first_part_count + 1]:
            conditions.append(self._island_bridges_vars[pos][Direction.left()] == 1)
        for pos in horizontal_positions[first_part_count:-1]:
            conditions.append(self._island_bridges_vars[pos][Direction.right()] == 1)

        left_conditions = []
        if Direction.up() in self._island_bridges_vars[horizontal_positions[0]]:
            left_conditions.append(self._island_bridges_vars[horizontal_positions[0]][Direction.up()])
        if Direction.down() in self._island_bridges_vars[horizontal_positions[0]]:
            left_conditions.append(self._island_bridges_vars[horizontal_positions[0]][Direction.down()])

        right_conditions = []
        if Direction.up() in self._island_bridges_vars[horizontal_positions[-1]]:
            right_conditions.append(self._island_bridges_vars[horizontal_positions[-1]][Direction.up()])
        if Direction.down() in self._island_bridges_vars[horizontal_positions[-1]]:
            right_conditions.append(self._island_bridges_vars[horizontal_positions[-1]][Direction.down()])

        shape_var = self._build_shape_var(f"h_no_turn_{position}_{first_part_count}_{second_part_count}", conditions, [left_conditions, right_conditions])
        return [shape_var] if shape_var is not None else []

    def _turn_options_vars(self, position: Position, segments_count: int, color: str) -> list[BoolVarT]:
        options = []
        if color == self.white:
            first_part_count = segments_count // 2
            second_part_count = segments_count - first_part_count
            options.extend(self._turn_right_down_options_vars(position, first_part_count, second_part_count))
            options.extend(self._turn_right_up_options_vars(position, first_part_count, second_part_count))
            options.extend(self._turn_left_down_options_vars(position, first_part_count, second_part_count))
            options.extend(self._turn_left_up_options_vars(position, first_part_count, second_part_count))
        else:
            for first_part_count in range(1, segments_count):
                second_part_count = segments_count - first_part_count
                if second_part_count == first_part_count:
                    continue
                options.extend(self._turn_right_down_options_vars(position, first_part_count, second_part_count))
                options.extend(self._turn_right_up_options_vars(position, first_part_count, second_part_count))
                options.extend(self._turn_left_down_options_vars(position, first_part_count, second_part_count))
                options.extend(self._turn_left_up_options_vars(position, first_part_count, second_part_count))
        return options

    def _turn_right_down_options_vars(self, position: Position, first_part_count: int, second_part_count: int) -> list[BoolVarT]:
        right_down_positions = (
                [position.after(Direction.right(), count) for count in reversed(range(1, first_part_count + 1))] +
                [position] +
                [position.after(Direction.down(), count) for count in range(1, second_part_count + 1)]
        )
        if not all(pos in self._island_bridges_vars for pos in right_down_positions):
            return []

        conditions = []
        for pos in right_down_positions[1:first_part_count + 1]:
            conditions.append(self._island_bridges_vars[pos][Direction.right()] == 1)
        for pos in right_down_positions[first_part_count:-1]:
            conditions.append(self._island_bridges_vars[pos][Direction.down()] == 1)

        top_conditions = []
        if Direction.up() in self._island_bridges_vars[right_down_positions[0]]:
            top_conditions.append(self._island_bridges_vars[right_down_positions[0]][Direction.up()])
        if Direction.down() in self._island_bridges_vars[right_down_positions[0]]:
            top_conditions.append(self._island_bridges_vars[right_down_positions[0]][Direction.down()])

        bottom_conditions = []
        if Direction.left() in self._island_bridges_vars[right_down_positions[-1]]:
            bottom_conditions.append(self._island_bridges_vars[right_down_positions[-1]][Direction.left()])
        if Direction.right() in self._island_bridges_vars[right_down_positions[-1]]:
            bottom_conditions.append(self._island_bridges_vars[right_down_positions[-1]][Direction.right()])

        shape_var = self._build_shape_var(f"rd_turn_{position}_{first_part_count}_{second_part_count}", conditions, [top_conditions, bottom_conditions])
        return [shape_var] if shape_var is not None else []

    def _turn_right_up_options_vars(self, position: Position, first_part_count: int, second_part_count: int) -> list[BoolVarT]:
        right_up_positions = (
                [position.after(Direction.right(), count) for count in reversed(range(1, first_part_count + 1))] +
                [position] +
                [position.after(Direction.up(), count) for count in range(1, second_part_count + 1)]
        )
        if not all(pos in self._island_bridges_vars for pos in right_up_positions):
            return []

        conditions = []
        for pos in right_up_positions[1:first_part_count + 1]:
            conditions.append(self._island_bridges_vars[pos][Direction.right()] == 1)
        for pos in right_up_positions[first_part_count:-1]:
            conditions.append(self._island_bridges_vars[pos][Direction.up()] == 1)

        top_conditions = []
        if Direction.up() in self._island_bridges_vars[right_up_positions[0]]:
            top_conditions.append(self._island_bridges_vars[right_up_positions[0]][Direction.up()])
        if Direction.down() in self._island_bridges_vars[right_up_positions[0]]:
            top_conditions.append(self._island_bridges_vars[right_up_positions[0]][Direction.down()])

        bottom_conditions = []
        if Direction.left() in self._island_bridges_vars[right_up_positions[-1]]:
            bottom_conditions.append(self._island_bridges_vars[right_up_positions[-1]][Direction.left()])
        if Direction.right() in self._island_bridges_vars[right_up_positions[-1]]:
            bottom_conditions.append(self._island_bridges_vars[right_up_positions[-1]][Direction.right()])

        shape_var = self._build_shape_var(f"ru_turn_{position}_{first_part_count}_{second_part_count}", conditions, [top_conditions, bottom_conditions])
        return [shape_var] if shape_var is not None else []

    def _turn_left_down_options_vars(self, position: Position, first_part_count: int, second_part_count: int) -> list[BoolVarT]:
        left_down_positions = (
                [position.after(Direction.left(), count) for count in reversed(range(1, first_part_count + 1))] +
                [position] +
                [position.after(Direction.down(), count) for count in range(1, second_part_count + 1)]
        )
        if not all(pos in self._island_bridges_vars for pos in left_down_positions):
            return []

        conditions = []
        for pos in left_down_positions[1:first_part_count + 1]:
            conditions.append(self._island_bridges_vars[pos][Direction.left()] == 1)
        for pos in left_down_positions[first_part_count:-1]:
            conditions.append(self._island_bridges_vars[pos][Direction.down()] == 1)

        top_conditions = []
        if Direction.up() in self._island_bridges_vars[left_down_positions[0]]:
            top_conditions.append(self._island_bridges_vars[left_down_positions[0]][Direction.up()])
        if Direction.down() in self._island_bridges_vars[left_down_positions[0]]:
            top_conditions.append(self._island_bridges_vars[left_down_positions[0]][Direction.down()])

        bottom_conditions = []
        if Direction.left() in self._island_bridges_vars[left_down_positions[-1]]:
            bottom_conditions.append(self._island_bridges_vars[left_down_positions[-1]][Direction.left()])
        if Direction.right() in self._island_bridges_vars[left_down_positions[-1]]:
            bottom_conditions.append(self._island_bridges_vars[left_down_positions[-1]][Direction.right()])

        shape_var = self._build_shape_var(f"ld_turn_{position}_{first_part_count}_{second_part_count}", conditions, [top_conditions, bottom_conditions])
        return [shape_var] if shape_var is not None else []

    def _turn_left_up_options_vars(self, position: Position, first_part_count: int, second_part_count: int) -> list[BoolVarT]:
        left_up_positions = (
                [position.after(Direction.left(), count) for count in reversed(range(1, first_part_count + 1))] +
                [position] +
                [position.after(Direction.up(), count) for count in range(1, second_part_count + 1)]
        )
        if not all(pos in self._island_bridges_vars for pos in left_up_positions):
            return []

        conditions = []
        for pos in left_up_positions[1:first_part_count + 1]:
            conditions.append(self._island_bridges_vars[pos][Direction.left()] == 1)
        for pos in left_up_positions[first_part_count:-1]:
            conditions.append(self._island_bridges_vars[pos][Direction.up()] == 1)

        top_conditions = []
        if Direction.up() in self._island_bridges_vars[left_up_positions[0]]:
            top_conditions.append(self._island_bridges_vars[left_up_positions[0]][Direction.up()])
        if Direction.down() in self._island_bridges_vars[left_up_positions[0]]:
            top_conditions.append(self._island_bridges_vars[left_up_positions[0]][Direction.down()])

        bottom_conditions = []
        if Direction.left() in self._island_bridges_vars[left_up_positions[-1]]:
            bottom_conditions.append(self._island_bridges_vars[left_up_positions[-1]][Direction.left()])
        if Direction.right() in self._island_bridges_vars[left_up_positions[-1]]:
            bottom_conditions.append(self._island_bridges_vars[left_up_positions[-1]][Direction.right()])

        shape_var = self._build_shape_var(f"lu_turn_{position}_{first_part_count}_{second_part_count}", conditions, [top_conditions, bottom_conditions])
        return [shape_var] if shape_var is not None else []

    @staticmethod
    def _convert_cell_value_to_color_and_segments_count(cell_value: str):
        if cell_value is None:
            return ' ', 0
        if len(cell_value) < 2:
            return ' ', 0
        color = cell_value[0]
        segments_count = int(cell_value.replace(color, ''))
        return color, segments_count

    def _not_loop_turn2_constraint(self, position):
        if position.up_right in self._island_bridges_vars:
            self._model.add_bool_or([
                self._island_bridges_vars[position][Direction.right()].negated(),
                self._island_bridges_vars[position][Direction.up()].negated(),
                self._island_bridges_vars[position.up_right][Direction.left()].negated(),
                self._island_bridges_vars[position.up_right][Direction.down()].negated(),
            ])

        if position.down_right in self._island_bridges_vars:
            self._model.add_bool_or([
                self._island_bridges_vars[position][Direction.right()].negated(),
                self._island_bridges_vars[position][Direction.down()].negated(),
                self._island_bridges_vars[position.down_right][Direction.left()].negated(),
                self._island_bridges_vars[position.down_right][Direction.up()].negated(),
            ])

        if position.up_left in self._island_bridges_vars:
            self._model.add_bool_or([
                self._island_bridges_vars[position][Direction.left()].negated(),
                self._island_bridges_vars[position][Direction.up()].negated(),
                self._island_bridges_vars[position.up_left][Direction.right()].negated(),
                self._island_bridges_vars[position.up_left][Direction.down()].negated(),
            ])

        if position.down_left in self._island_bridges_vars:
            self._model.add_bool_or([
                self._island_bridges_vars[position][Direction.left()].negated(),
                self._island_bridges_vars[position][Direction.down()].negated(),
                self._island_bridges_vars[position.down_left][Direction.right()].negated(),
                self._island_bridges_vars[position.down_left][Direction.up()].negated(),
            ])

    def _compute_options_vars_without_segments_length(self, position: Position, color: str) -> list[BoolVarT]:
        segments_length_vars = []
        for direction in Direction.orthogonal_directions():
            segment_length_var = self._compute_direction_segment_length_var(position, direction)
            if segment_length_var is None:
                continue
            segments_length_vars.append(segment_length_var)

        pairs = [(i, j) for i in range(len(segments_length_vars)) for j in range(i + 1, len(segments_length_vars))]
        options = []
        if color == self.white:
            for i, j in pairs:
                option = self._model.new_bool_var(f"seg_eq_{position}_{i}_{j}")
                self._model.add(segments_length_vars[i] == segments_length_vars[j]).only_enforce_if(option)
                self._model.add(segments_length_vars[i] > 0).only_enforce_if(option)
                options.append(option)
        else:
            for i, j in pairs:
                option = self._model.new_bool_var(f"seg_neq_{position}_{i}_{j}")
                self._model.add(segments_length_vars[i] != segments_length_vars[j]).only_enforce_if(option)
                self._model.add(segments_length_vars[i] > 0).only_enforce_if(option)
                self._model.add(segments_length_vars[j] > 0).only_enforce_if(option)
                options.append(option)
        return options

    def _compute_direction_segment_length_var(self, position: Position, direction: Direction):
        positions = [position]
        positions_in_direction = self._clues_grid.all_positions_in_direction(position, direction)
        if not positions_in_direction:
            return None
        positions.extend(positions_in_direction)

        n = len(positions) - 1
        segment_len = self._model.new_int_var(0, n, f"seg_len_{position}_{direction}")

        consecutive = []
        for i in range(n):
            cvar = self._model.new_bool_var(f"consec_{position}_{direction}_{i}")
            consecutive.append(cvar)

        self._model.add(consecutive[0] == self._island_bridges_vars[positions[0]][direction])
        for i in range(1, n):
            self._model.add(consecutive[i] <= consecutive[i - 1])
            self._model.add(consecutive[i] <= self._island_bridges_vars[positions[i]][direction])
            self._model.add(consecutive[i - 1] + self._island_bridges_vars[positions[i]][direction] <= 1 + consecutive[i])

        self._model.add(segment_len == sum(consecutive))
        return segment_len
