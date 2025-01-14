from typing import Dict

from z3 import Solver, sat, Int, And, Not, Sum, ArithRef, Or

from Utils.Direction import Direction
from Utils.Grid import Grid
from Utils.IslandsGrid import IslandGrid
from Utils.Position import Position


class ShingokiGame:
    def __init__(self, grid: Grid):
        self.input_grid = grid
        self._island_grid = None
        self.init_island_grid()
        self._solver: Solver | None = None
        self._island_bridges_z3: Dict[Position, Dict[Direction, ArithRef]] = {}
        self._last_solution: IslandGrid | None = None

    def init_island_grid(self):
        self._island_grid = IslandGrid(Grid([[2 for _ in row] for row in self.input_grid.matrix]))

    def _init_solver(self):
        orthogonal_directions = [Direction.right(), Direction.down(), Direction.left(), Direction.up()]
        self._island_bridges_z3 = {island.position: {direction: Int(f"{island.position}_{direction}") for direction in orthogonal_directions} for island in
                                   self._island_grid.islands.values()}
        self._solver = Solver()
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if self._solver is None:
            self._init_solver()

        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> (Grid, int):
        proposition_count = 0
        while self._solver.check() == sat:
            model = self._solver.model()
            proposition_count += 1
            for position, direction_bridges in self._island_bridges_z3.items():
                for direction, bridges in direction_bridges.items():
                    if position.next(direction) not in self._island_bridges_z3:
                        continue
                    bridges_number = model.eval(bridges).as_long()
                    if bridges_number > 0:
                        self._island_grid[position].set_bridge(self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
                    elif position in self._island_grid and direction in self._island_grid[position].direction_position_bridges:
                        self._island_grid[position].direction_position_bridges.pop(direction)
                self._island_grid[position].set_bridges_count_according_to_directions_bridges()
            connected_positions = self._island_grid.get_connected_positions(exclude_without_bridge=True)
            if len(connected_positions) == 1:
                self._last_solution = self._island_grid
                return self._island_grid, proposition_count

            not_loop_constraints = []
            for positions in connected_positions:
                cell_constraints = []
                for position in positions:
                    for direction, (_, value) in self._island_grid[position].direction_position_bridges.items():
                        cell_constraints.append(self._island_bridges_z3[position][direction] == value)
                not_loop_constraints.append(Not(And(cell_constraints)))
            self._solver.add(And(not_loop_constraints))
            self.init_island_grid()

        return IslandGrid.empty(), proposition_count

    def get_other_solution(self):
        previous_solution_constraints = []
        for island in self._last_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                previous_solution_constraints.append(self._island_bridges_z3[island.position][direction] == value)
        self._solver.add(Not(And(previous_solution_constraints)))

        self.init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_opposite_bridges_constraints()
        self._add_bridges_sum_constraints()
        self._add_dots_count_constraints()

    def _add_initial_constraints(self):
        for _island_bridges_z3 in self._island_bridges_z3.values():
            for direction_bridges in _island_bridges_z3.values():
                self._solver.add(Or(direction_bridges == 0, direction_bridges == 1))

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._solver.add(self._island_bridges_z3[island.position][direction] == self._island_bridges_z3[island.direction_position_bridges[direction][0]][
                        direction.opposite])
                else:
                    self._solver.add(self._island_bridges_z3[island.position][direction] == 0)

    def _add_bridges_sum_constraints(self):
        for island in self._island_grid.islands.values():
            sum_constraint_0 = Sum(
                [self._island_bridges_z3[island.position][direction] for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]]) == 0
            sum_constraint_2 = Sum(
                [self._island_bridges_z3[island.position][direction] for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]]) == 2
            self._solver.add(Or(sum_constraint_0, sum_constraint_2))

    def _add_dots_count_constraints(self):
        for position, cell_value in self.input_grid:
            color, segments_count = self._convert_cell_value_to_color_and_segments_count(cell_value)
            if color == 'w':
                dot_count_constraints = []
                for first_part_count in range(1, segments_count):
                    second_part_count = segments_count - first_part_count
                    horizontal_positions = [position.next(Direction.left(), count) for count in reversed(range(1, first_part_count + 1))] + [position] + [position.next(Direction.right(), count) for count in range(1, second_part_count + 1)]
                    horizontal_constraints = []
                    if all(position in self._island_bridges_z3 for position in horizontal_positions):
                        horizontal_constraint = And([self._island_bridges_z3[position][Direction.left()] == 1 for position in horizontal_positions[1:first_part_count+1]] + [self._island_bridges_z3[position][Direction.right()] == 1 for position in horizontal_positions[first_part_count:-1]])
                        left_up_constraint, left_down_constraint, right_up_constraint, right_down_constraint = False, False, False, False
                        if Direction.up() in self._island_bridges_z3[horizontal_positions[0]]:
                            left_up_constraint = self._island_bridges_z3[horizontal_positions[0]][Direction.up()] == 1
                        if Direction.down() in self._island_bridges_z3[horizontal_positions[0]]:
                            left_down_constraint = self._island_bridges_z3[horizontal_positions[0]][Direction.down()] == 1
                        if Direction.up() in self._island_bridges_z3[horizontal_positions[-1]]:
                            right_up_constraint = self._island_bridges_z3[horizontal_positions[-1]][Direction.up()] == 1
                        if Direction.down() in self._island_bridges_z3[horizontal_positions[-1]]:
                            right_down_constraint = self._island_bridges_z3[horizontal_positions[-1]][Direction.down()] == 1
                        turn_constraint = And(Or(left_up_constraint, left_down_constraint), Or(right_up_constraint, right_down_constraint))
                        horizontal_constraints.append(And(horizontal_constraint, turn_constraint))

                    vertical_positions = [position.next(Direction.up(), count) for count in reversed(range(1, first_part_count + 1))] + [position] + [position.next(Direction.down(), count) for count in range(1, second_part_count + 1)]
                    vertical_constraints = []
                    if all(position in self._island_bridges_z3 for position in vertical_positions):
                        vertical_constraint = And([self._island_bridges_z3[position][Direction.up()] == 1 for position in vertical_positions[1:first_part_count+1]] + [self._island_bridges_z3[position][Direction.down()] == 1 for position in vertical_positions[first_part_count:-1]])
                        up_left_constraint, down_left_constraint, up_right_constraint, down_right_constraint = False, False, False, False
                        if Direction.left() in self._island_bridges_z3[vertical_positions[0]]:
                            up_left_constraint = self._island_bridges_z3[vertical_positions[0]][Direction.left()] == 1
                        if Direction.right() in self._island_bridges_z3[vertical_positions[0]]:
                            up_right_constraint = self._island_bridges_z3[vertical_positions[0]][Direction.right()] == 1
                        if Direction.left() in self._island_bridges_z3[vertical_positions[-1]]:
                            down_left_constraint = self._island_bridges_z3[vertical_positions[-1]][Direction.left()] == 1
                        if Direction.right() in self._island_bridges_z3[vertical_positions[-1]]:
                            down_right_constraint = self._island_bridges_z3[vertical_positions[-1]][Direction.right()] == 1
                        turn_constraint = And(Or(up_left_constraint, up_right_constraint), Or(down_left_constraint, down_right_constraint))
                        vertical_constraints.append(And(vertical_constraint, turn_constraint))
                    dot_count_constraints.append(Or(Or(horizontal_constraints), Or(vertical_constraints)))
                self._solver.add(Or(dot_count_constraints))

            if color == 'b':
                left_up_constraint, left_down_constraint, right_up_constraint, right_down_constraint = False, False, False, False
                if position.right in self._island_bridges_z3 and position.right.right in self._island_bridges_z3 and position.down in self._island_bridges_z3 and position.down.down in self._island_bridges_z3:
                    right_down_constraint = And(
                        self._island_bridges_z3[position][Direction.right()] == 1, self._island_bridges_z3[position.right][Direction.right()] == 1,
                        self._island_bridges_z3[position][Direction.down()] == 1, self._island_bridges_z3[position.down][Direction.down()] == 1)
                if position.left in self._island_bridges_z3 and position.left.left in self._island_bridges_z3 and position.down in self._island_bridges_z3 and position.down.down in self._island_bridges_z3:
                    left_down_constraint = And(
                        self._island_bridges_z3[position][Direction.left()] == 1, self._island_bridges_z3[position.left][Direction.left()] == 1,
                        self._island_bridges_z3[position][Direction.down()] == 1, self._island_bridges_z3[position.down][Direction.down()] == 1)
                if position.right in self._island_bridges_z3 and position.right.right in self._island_bridges_z3 and position.up in self._island_bridges_z3 and position.up.up in self._island_bridges_z3:
                    right_up_constraint = And(
                        self._island_bridges_z3[position][Direction.right()] == 1, self._island_bridges_z3[position.right][Direction.right()] == 1,
                        self._island_bridges_z3[position][Direction.up()] == 1, self._island_bridges_z3[position.up][Direction.up()] == 1)
                if position.left in self._island_bridges_z3 and position.left.left in self._island_bridges_z3 and position.up in self._island_bridges_z3 and position.up.up in self._island_bridges_z3:
                    left_up_constraint = And(
                        self._island_bridges_z3[position][Direction.left()] == 1, self._island_bridges_z3[position.left][Direction.left()] == 1,
                        self._island_bridges_z3[position][Direction.up()] == 1, self._island_bridges_z3[position.up][Direction.up()] == 1)
                self._solver.add(Or(right_down_constraint, left_down_constraint, right_up_constraint, left_up_constraint))

    @staticmethod
    def _convert_cell_value_to_color_and_segments_count(cell_value: str):
        if len(cell_value) != 2:
            return ' ', 0
        color = cell_value[0]
        segments_count = int(cell_value[1])
        return color, segments_count
