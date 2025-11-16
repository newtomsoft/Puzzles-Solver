from z3 import ArithRef, Solver, Not, And, Or, Int, sat, Implies, Sum

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
        self._solver = Solver()
        self._island_bridges_z3: dict[Position, dict[Direction, ArithRef]] = {}
        self._previous_solution: IslandGrid | None = None

    def _init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._clues_grid.columns_number)] for r in range(self._clues_grid.rows_number)])

    def _init_solver(self):
        self._island_bridges_z3 = {island.position: {direction: Int(f"{island.position}_{direction}") for direction in Direction.orthogonal_directions()} for island in
                                   self._island_grid.islands.values()}
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
                        self._island_grid[position].set_bridge_to_position(self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
                    elif position in self._island_grid and direction in self._island_grid[position].direction_position_bridges:
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
        self._add_opposite_bridges_constraints()
        self._add_bridges_sum_constraints()
        self._add_dots_constraints()

    def _add_initial_constraints(self):
        constraints = [Or(direction_bridges == 0, direction_bridges == 1) for _island_bridges_z3 in self._island_bridges_z3.values() for direction_bridges in
                       _island_bridges_z3.values()]
        self._solver.add(constraints)
        constraints_border_up = [self._island_bridges_z3[Position(0, c)][Direction.up()] == 0 for c in range(self._island_grid.columns_number)]
        constraints_border_down = [self._island_bridges_z3[Position(self._island_grid.rows_number - 1, c)][Direction.down()] == 0 for c in
                                   range(self._island_grid.columns_number)]
        constraints_border_right = [self._island_bridges_z3[Position(r, self._island_grid.columns_number - 1)][Direction.right()] == 0 for r in
                                    range(self._island_grid.rows_number)]
        constraints_border_left = [self._island_bridges_z3[Position(r, 0)][Direction.left()] == 0 for r in range(self._island_grid.rows_number)]
        self._solver.add(constraints_border_down + constraints_border_up + constraints_border_right + constraints_border_left)

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._solver.add(
                        self._island_bridges_z3[island.position][direction] == self._island_bridges_z3[island.direction_position_bridges[direction][0]][
                            direction.opposite])
                else:
                    self._solver.add(self._island_bridges_z3[island.position][direction] == 0)

    def _add_bridges_sum_constraints(self):
        for position, value in self._clues_grid:
            sum2_constraint = sum([self._island_bridges_z3[position][direction] for direction in Direction.orthogonal_directions()]) == 2
            if value != self.empty:
                self._solver.add(sum2_constraint)
                continue

            sum0_constraint = sum([self._island_bridges_z3[position][direction] for direction in Direction.orthogonal_directions()]) == 0
            self._solver.add(Or(sum2_constraint, sum0_constraint))

    def _add_dots_constraints(self):
        for position, cell_value in [(position, value) for position, value in self._clues_grid if value != self.empty]:
            color, segments_count = self._convert_cell_value_to_color_and_segments_count(cell_value)
            match segments_count:
                case 0:
                    constraints = self._compute_constraints_without_segments_length(position, color)
                    self._solver.add(Or(constraints))
                case 2:
                    constraints = self._compute_constraints(position, segments_count, color)
                    self._solver.add(Or(constraints))
                    self._solver.add(self._not_loop_turn2_constraint(position))
                case _:
                    constraints = self._compute_constraints(position, segments_count, color)
                    self._solver.add(Or(constraints))

    def _not_turn_constraints(self, position: Position, segments_count: int, color: str):
        if color == self.white:
            first_part_count = segments_count // 2
            second_part_count = segments_count - first_part_count
            vertical_constraints = self._vertical_constraints(position, first_part_count, second_part_count)
            horizontal_constraints = self._horizontal_constraints(position, first_part_count, second_part_count)
            return [Or(Or(vertical_constraints), Or(horizontal_constraints))]

        # color black
        white_constraints = []
        for first_part_count in range(1, segments_count):
            second_part_count = segments_count - first_part_count
            if second_part_count == first_part_count:
                continue
            vertical_constraints = self._vertical_constraints(position, first_part_count, second_part_count)
            horizontal_constraints = self._horizontal_constraints(position, first_part_count, second_part_count)
            white_constraints.append(Or(Or(vertical_constraints), Or(horizontal_constraints)))
        return white_constraints

    def _vertical_constraints(self, position: Position, first_part_count: int, second_part_count: int):
        vertical_positions = (
                [position.after(Direction.up(), count) for count in reversed(range(1, first_part_count + 1))] +
                [position] +
                [position.after(Direction.down(), count) for count in range(1, second_part_count + 1)]
        )
        vertical_constraints = []
        if all(position in self._island_bridges_z3 for position in vertical_positions):
            first_constraint_vertical = And(
                [self._island_bridges_z3[position][Direction.up()] == 1 for position in vertical_positions[1:first_part_count + 1]]
                + [self._island_bridges_z3[position][Direction.down()] == 1 for position in vertical_positions[first_part_count:-1]]
            )
            up_left_constraint = down_left_constraint = up_right_constraint = down_right_constraint = False
            if Direction.left() in self._island_bridges_z3[vertical_positions[0]]:
                up_left_constraint = self._island_bridges_z3[vertical_positions[0]][Direction.left()] == 1
            if Direction.right() in self._island_bridges_z3[vertical_positions[0]]:
                up_right_constraint = self._island_bridges_z3[vertical_positions[0]][Direction.right()] == 1
            if Direction.left() in self._island_bridges_z3[vertical_positions[-1]]:
                down_left_constraint = self._island_bridges_z3[vertical_positions[-1]][Direction.left()] == 1
            if Direction.right() in self._island_bridges_z3[vertical_positions[-1]]:
                down_right_constraint = self._island_bridges_z3[vertical_positions[-1]][Direction.right()] == 1
            second_constraint = And(Or(up_left_constraint, up_right_constraint), Or(down_left_constraint, down_right_constraint))
            vertical_constraints.append(And(first_constraint_vertical, second_constraint))
        return vertical_constraints

    def _horizontal_constraints(self, position: Position, first_part_count: int, second_part_count: int):
        horizontal_positions = (
                [position.after(Direction.left(), count) for count in reversed(range(1, first_part_count + 1))] +
                [position] +
                [position.after(Direction.right(), count) for count in range(1, second_part_count + 1)]
        )
        horizontal_constraints = []
        if all(position in self._island_bridges_z3 for position in horizontal_positions):
            first_constraint_horizontal = And(
                [self._island_bridges_z3[position][Direction.left()] == 1 for position in horizontal_positions[1:first_part_count + 1]]
                + [self._island_bridges_z3[position][Direction.right()] == 1 for position in horizontal_positions[first_part_count:-1]]
            )
            left_up_constraint = left_down_constraint = right_up_constraint = right_down_constraint = False
            if Direction.up() in self._island_bridges_z3[horizontal_positions[0]]:
                left_up_constraint = self._island_bridges_z3[horizontal_positions[0]][Direction.up()] == 1
            if Direction.down() in self._island_bridges_z3[horizontal_positions[0]]:
                left_down_constraint = self._island_bridges_z3[horizontal_positions[0]][Direction.down()] == 1
            if Direction.up() in self._island_bridges_z3[horizontal_positions[-1]]:
                right_up_constraint = self._island_bridges_z3[horizontal_positions[-1]][Direction.up()] == 1
            if Direction.down() in self._island_bridges_z3[horizontal_positions[-1]]:
                right_down_constraint = self._island_bridges_z3[horizontal_positions[-1]][Direction.down()] == 1
            second_constraint = And(Or(left_up_constraint, left_down_constraint), Or(right_up_constraint, right_down_constraint))
            horizontal_constraints.append(And(first_constraint_horizontal, second_constraint))
        return horizontal_constraints

    def _turn_constraints(self, position: Position, segments_count: int, color: str):
        if color == self.white:
            first_part_count = segments_count // 2
            second_part_count = segments_count - first_part_count
            right_down_constraints = self._turn_right_down_constraints(position, first_part_count, second_part_count)
            right_up_constraints = self._turn_right_up_constraints(position, first_part_count, second_part_count)
            left_down_constraints = self._turn_left_down_constraints(position, first_part_count, second_part_count)
            left_up_constraints = self._turn_left_up_constraints(position, first_part_count, second_part_count)
            return [Or(Or(right_down_constraints), Or(right_up_constraints), Or(left_down_constraints), Or(left_up_constraints))]

        # color black
        turn_constraints = []
        for first_part_count in range(1, segments_count):
            second_part_count = segments_count - first_part_count
            if second_part_count == first_part_count:
                continue
            right_down_constraints = self._turn_right_down_constraints(position, first_part_count, second_part_count)
            right_up_constraints = self._turn_right_up_constraints(position, first_part_count, second_part_count)
            left_down_constraints = self._turn_left_down_constraints(position, first_part_count, second_part_count)
            left_up_constraints = self._turn_left_up_constraints(position, first_part_count, second_part_count)
            turn_constraints.append(Or(Or(right_down_constraints), Or(right_up_constraints), Or(left_down_constraints), Or(left_up_constraints)))
        return turn_constraints

    def _turn_right_down_constraints(self, position: Position, first_part_count: int, second_part_count: int):
        right_down_positions = (
                [position.after(Direction.right(), count) for count in reversed(range(1, first_part_count + 1))] +
                [position] +
                [position.after(Direction.down(), count) for count in range(1, second_part_count + 1)]
        )
        right_down_constraints = []
        if all(position in self._island_bridges_z3 for position in right_down_positions):
            first_constraint_right_down = And(
                [self._island_bridges_z3[position][Direction.right()] == 1 for position in right_down_positions[1:first_part_count + 1]] + [
                    self._island_bridges_z3[position][Direction.down()] == 1 for position in right_down_positions[first_part_count:-1]])
            right_up_constraint = right_down_constraint = down_right_constraint = down_left_constraint = False
            if Direction.up() in self._island_bridges_z3[right_down_positions[0]]:
                right_up_constraint = self._island_bridges_z3[right_down_positions[0]][Direction.up()] == 1
            if Direction.down() in self._island_bridges_z3[right_down_positions[0]]:
                right_down_constraint = self._island_bridges_z3[right_down_positions[0]][Direction.down()] == 1
            if Direction.left() in self._island_bridges_z3[right_down_positions[-1]]:
                down_left_constraint = self._island_bridges_z3[right_down_positions[-1]][Direction.left()] == 1
            if Direction.right() in self._island_bridges_z3[right_down_positions[-1]]:
                down_right_constraint = self._island_bridges_z3[right_down_positions[-1]][Direction.right()] == 1
            second_constraint = And(Or(right_up_constraint, right_down_constraint), Or(down_left_constraint, down_right_constraint))
            right_down_constraints.append(And(first_constraint_right_down, second_constraint))
        return right_down_constraints

    def _turn_right_up_constraints(self, position: Position, first_part_count: int, second_part_count: int):
        right_up_positions = (
                [position.after(Direction.right(), count) for count in reversed(range(1, first_part_count + 1))] +
                [position] +
                [position.after(Direction.up(), count) for count in range(1, second_part_count + 1)]
        )
        right_up_constraints = []
        if all(position in self._island_bridges_z3 for position in right_up_positions):
            first_constraint_right_up = And(
                [self._island_bridges_z3[position][Direction.right()] == 1 for position in right_up_positions[1:first_part_count + 1]] + [
                    self._island_bridges_z3[position][Direction.up()] == 1 for position in right_up_positions[first_part_count:-1]])
            right_up_constraint = right_down_constraint = up_right_constraint = up_left_constraint = False
            if Direction.up() in self._island_bridges_z3[right_up_positions[0]]:
                right_up_constraint = self._island_bridges_z3[right_up_positions[0]][Direction.up()] == 1
            if Direction.down() in self._island_bridges_z3[right_up_positions[0]]:
                right_down_constraint = self._island_bridges_z3[right_up_positions[0]][Direction.down()] == 1
            if Direction.left() in self._island_bridges_z3[right_up_positions[-1]]:
                up_left_constraint = self._island_bridges_z3[right_up_positions[-1]][Direction.left()] == 1
            if Direction.right() in self._island_bridges_z3[right_up_positions[-1]]:
                up_right_constraint = self._island_bridges_z3[right_up_positions[-1]][Direction.right()] == 1
            second_constraint = And(Or(right_up_constraint, right_down_constraint), Or(up_left_constraint, up_right_constraint))
            right_up_constraints.append(And(first_constraint_right_up, second_constraint))
        return right_up_constraints

    def _turn_left_down_constraints(self, position: Position, first_part_count: int, second_part_count: int):
        left_down_positions = (
                [position.after(Direction.left(), count) for count in reversed(range(1, first_part_count + 1))] +
                [position] +
                [position.after(Direction.down(), count) for count in range(1, second_part_count + 1)]
        )
        left_down_constraints = []
        if all(position in self._island_bridges_z3 for position in left_down_positions):
            first_constraint_left_down = And(
                [self._island_bridges_z3[position][Direction.left()] == 1 for position in left_down_positions[1:first_part_count + 1]] + [
                    self._island_bridges_z3[position][Direction.down()] == 1 for position in left_down_positions[first_part_count:-1]])
            left_up_constraint = left_down_constraint = down_left_constraint = down_right_constraint = False
            if Direction.up() in self._island_bridges_z3[left_down_positions[0]]:
                left_up_constraint = self._island_bridges_z3[left_down_positions[0]][Direction.up()] == 1
            if Direction.down() in self._island_bridges_z3[left_down_positions[0]]:
                left_down_constraint = self._island_bridges_z3[left_down_positions[0]][Direction.down()] == 1
            if Direction.left() in self._island_bridges_z3[left_down_positions[-1]]:
                down_left_constraint = self._island_bridges_z3[left_down_positions[-1]][Direction.left()] == 1
            if Direction.right() in self._island_bridges_z3[left_down_positions[-1]]:
                down_right_constraint = self._island_bridges_z3[left_down_positions[-1]][Direction.right()] == 1
            second_constraint = And(Or(left_up_constraint, left_down_constraint), Or(down_left_constraint, down_right_constraint))
            left_down_constraints.append(And(first_constraint_left_down, second_constraint))
        return left_down_constraints

    def _turn_left_up_constraints(self, position: Position, first_part_count: int, second_part_count: int):
        left_up_positions = (
                [position.after(Direction.left(), count) for count in reversed(range(1, first_part_count + 1))] +
                [position] +
                [position.after(Direction.up(), count) for count in range(1, second_part_count + 1)]
        )
        left_up_constraints = []
        if all(position in self._island_bridges_z3 for position in left_up_positions):
            first_constraint_left_up = And(
                [self._island_bridges_z3[position][Direction.left()] == 1 for position in left_up_positions[1:first_part_count + 1]] + [
                    self._island_bridges_z3[position][Direction.up()] == 1 for position in left_up_positions[first_part_count:-1]])
            left_up_constraint = left_down_constraint = up_left_constraint = up_right_constraint = False
            if Direction.up() in self._island_bridges_z3[left_up_positions[0]]:
                left_up_constraint = self._island_bridges_z3[left_up_positions[0]][Direction.up()] == 1
            if Direction.down() in self._island_bridges_z3[left_up_positions[0]]:
                left_down_constraint = self._island_bridges_z3[left_up_positions[0]][Direction.down()] == 1
            if Direction.left() in self._island_bridges_z3[left_up_positions[-1]]:
                up_left_constraint = self._island_bridges_z3[left_up_positions[-1]][Direction.left()] == 1
            if Direction.right() in self._island_bridges_z3[left_up_positions[-1]]:
                up_right_constraint = self._island_bridges_z3[left_up_positions[-1]][Direction.right()] == 1
            second_constraint = And(Or(left_up_constraint, left_down_constraint), Or(up_left_constraint, up_right_constraint))
            left_up_constraints.append(And(first_constraint_left_up, second_constraint))
        return left_up_constraints

    def _compute_constraints(self, position: Position, segments_count: int, color: str):
        not_turn_constraints = self._not_turn_constraints(position, segments_count, color)
        turn_constraints = self._turn_constraints(position, segments_count, color)
        constraints = not_turn_constraints + turn_constraints
        return constraints

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
        constraints = []

        if position.up_right in self._island_bridges_z3:
            right_up_constraint = And(self._island_bridges_z3[position][Direction.right()] == 1, self._island_bridges_z3[position][Direction.up()] == 1)
            then_right_up_constraint = Not(
                And(self._island_bridges_z3[position.up_right][Direction.left()] == 1, self._island_bridges_z3[position.up_right][Direction.down()] == 1))
            constraints.append(Implies(right_up_constraint, then_right_up_constraint))

        if position.down_right in self._island_bridges_z3:
            right_down_constraint = And(self._island_bridges_z3[position][Direction.right()] == 1, self._island_bridges_z3[position][Direction.down()] == 1)
            then_right_down_constraint = Not(
                And(self._island_bridges_z3[position.down_right][Direction.left()] == 1, self._island_bridges_z3[position.down_right][Direction.up()] == 1))
            constraints.append(Implies(right_down_constraint, then_right_down_constraint))

        if position.up_left in self._island_bridges_z3:
            left_up_constraint = And(self._island_bridges_z3[position][Direction.left()] == 1, self._island_bridges_z3[position][Direction.up()] == 1)
            then_left_up_constraint = Not(
                And(self._island_bridges_z3[position.up_left][Direction.right()] == 1, self._island_bridges_z3[position.up_left][Direction.down()] == 1))
            constraints.append(Implies(left_up_constraint, then_left_up_constraint))

        if position.down_left in self._island_bridges_z3:
            left_down_constraint = And(self._island_bridges_z3[position][Direction.left()] == 1, self._island_bridges_z3[position][Direction.down()] == 1)
            then_left_down_constraint = Not(
                And(self._island_bridges_z3[position.down_left][Direction.right()] == 1, self._island_bridges_z3[position.down_left][Direction.up()] == 1))
            constraints.append(Implies(left_down_constraint, then_left_down_constraint))

        return And(constraints)

    def _compute_constraints_without_segments_length(self, position: Position, color: str):
        segments_length_var = []
        for direction in Direction.orthogonal_directions():
            segment_length_var = self._compute_direction_constraints(position, direction)
            if segment_length_var is None:
                continue
            segments_length_var.append(segment_length_var)

        pairs = [(i, j) for i in range(len(segments_length_var)) for j in range(i + 1, len(segments_length_var))]
        if color == self.white:
            return [And(segments_length_var[i] == segments_length_var[j], segments_length_var[i] > 0) for i, j in pairs]

        # color black
        return [And( segments_length_var[i] != segments_length_var[j], segments_length_var[i] > 0, segments_length_var[j] > 0) for i, j in pairs]

    def _compute_direction_constraints(self, position: Position, direction: Direction) -> ArithRef | None:
        positions = [position]
        positions_in_direction = self._clues_grid.all_positions_in_direction(position, direction)
        if len(positions_in_direction) == 0:
            return None
        positions.extend(positions_in_direction)

        consecutive_bridges_constraints = []
        previous_bridge_constraint = None
        for position in positions[:-1]:
            current_bridge_var = self._island_bridges_z3[position][direction]
            if previous_bridge_constraint is not None:
                current_bridge_condition_constraint = And(previous_bridge_constraint, current_bridge_var == 1)
                consecutive_bridges_constraints.append(current_bridge_condition_constraint)
            else:
                current_bridge_condition_constraint = current_bridge_var == 1
                consecutive_bridges_constraints.append(current_bridge_condition_constraint)
            previous_bridge_constraint = current_bridge_condition_constraint

        return Sum(consecutive_bridges_constraints)
