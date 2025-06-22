from z3 import *

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position


class MidLoopSolver:
    def __init__(self, grid_size: tuple[int, int], dots_positions: dict[int, Position]):
        self._input_grid = Grid([[0 for _ in range(grid_size[1])] for _ in range(grid_size[0])])
        self.dots_positions = dots_positions
        self._island_grid: IslandGrid | None = None
        self.rows_number = self._input_grid.rows_number
        self.columns_number = self._input_grid.columns_number
        self.init_island_grid()
        self._solver = Solver()
        self._island_bridges_z3: dict[Position, dict[Direction, ArithRef]] = {}
        self._previous_solution: IslandGrid | None = None

    def init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._input_grid.columns_number)] for r in range(self._input_grid.rows_number)])

    def _init_solver(self):
        self._island_bridges_z3 = {
            island.position: {direction: Int(f"{island.position}_{direction}") for direction in Direction.orthogonals()}
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
                        self._island_grid[position].set_bridge(
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
            self.init_island_grid()

        return IslandGrid.empty(), proposition_count

    def get_other_solution(self):
        previous_solution_constraints = []
        for island in self._previous_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                previous_solution_constraints.append(self._island_bridges_z3[island.position][direction] == value)
        self._solver.add(Not(And(previous_solution_constraints)))

        self.init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_minimal_edges_dot_constraints()
        self._add_symmetry_constraints()
        self._add_opposite_bridges_constraints()
        # self._add_dots_constraints()

    def _add_initial_constraints(self):
        for position, directions_bridges in self._island_bridges_z3.items():
            bridges_count_vars = list(directions_bridges.values())
            self._solver.add(Or(sum(bridges_count_vars) == 2, sum(bridges_count_vars) == 0))
            for direction_bridges in directions_bridges.values():
                self._solver.add(And(direction_bridges >= 0, direction_bridges <= 1))
        for position in self._input_grid.edge_up_positions():
            self._solver.add(self._island_bridges_z3[position][Direction.up()] == 0)
        for position in self._input_grid.edge_left_positions():
            self._solver.add(self._island_bridges_z3[position][Direction.left()] == 0)
        for position in self._input_grid.edge_down_positions():
            self._solver.add(self._island_bridges_z3[position][Direction.down()] == 0)
        for position in self._input_grid.edge_right_positions():
            self._solver.add(self._island_bridges_z3[position][Direction.right()] == 0)

    def _add_minimal_edges_dot_constraints(self):
        for dot_position in [position for position in self.dots_positions.values()
                             if self._input_grid.is_position_in_edge_up(position) or self._input_grid.is_position_in_edge_down(position)]:
            self._add_minimal_horizontal_bridge_constraints(dot_position)
        for dot_position in [position for position in self.dots_positions.values()
                             if self._input_grid.is_position_in_edge_left(position) or self._input_grid.is_position_in_edge_right(position)]:
            self._add_minimal_vertical_bridge_constraints(dot_position)

    def _add_minimal_horizontal_bridge_constraints(self, dot_position: Position):
        column = int(dot_position.c)
        is_cross_column = dot_position.c - column != 0
        if is_cross_column:
            position_left = Position(dot_position.r, column)
            position_right = position_left.right
            self._solver.add(self._island_bridges_z3[position_left][Direction.right()] == 1)
            self._solver.add(self._island_bridges_z3[position_right][Direction.left()] == 1)
            return

        self._solver.add(self._island_bridges_z3[dot_position][Direction.left()] == 1)
        self._solver.add(self._island_bridges_z3[dot_position][Direction.right()] == 1)
        self._solver.add(self._island_bridges_z3[dot_position][Direction.up()] == 0)
        self._solver.add(self._island_bridges_z3[dot_position][Direction.down()] == 0)

    def _add_minimal_vertical_bridge_constraints(self, dot_position):
        row = int(dot_position.r)
        is_cross_row = dot_position.r - row != 0
        if is_cross_row:
            position_up = Position(row, dot_position.c)
            position_down = position_up.down
            self._solver.add(self._island_bridges_z3[position_up][Direction.down()] == 1)
            self._solver.add(self._island_bridges_z3[position_down][Direction.up()] == 1)
            return

        self._solver.add(self._island_bridges_z3[dot_position][Direction.up()] == 1)
        self._solver.add(self._island_bridges_z3[dot_position][Direction.down()] == 1)
        self._solver.add(self._island_bridges_z3[dot_position][Direction.left()] == 0)
        self._solver.add(self._island_bridges_z3[dot_position][Direction.right()] == 0)

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._solver.add(self._island_bridges_z3[island.position][direction] ==
                                     self._island_bridges_z3[island.direction_position_bridges[direction][0]][direction.opposite])
                else:
                    self._solver.add(self._island_bridges_z3[island.position][direction] == 0)

    def _add_symmetry_constraints(self):
        for dot_position in self.dots_positions.values():
            row = int(dot_position.r)
            column = int(dot_position.c)
            if dot_position.r - row != 0:
                self._add_must_symetry_vertical_segment_constraint(dot_position)
            if dot_position.c - column != 0:
                self._add_must_symetry_horizontal_segment_constraint(dot_position)
    #         if dot_position.r - row == 0 and dot_position.c - column == 0:
    #             self._add_symetry_segment_constraint(dot_position)
    #
    # def _add_symetry_segment_constraint(self, dot_position: Position):
    #     vertical_constraint = self._symetry_vertical_segment_constraint(dot_position)
    #     horizontal_constraint = self._symetry_horizontal_segment_constraint(dot_position)
    #     self._solver.add(Or(vertical_constraint, horizontal_constraint))

    def _add_must_symetry_vertical_segment_constraint(self, dot_position: Position):
        constraint = self._symetry_vertical_segment_constraint(dot_position)
        self._solver.add(constraint)

    def _add_must_symetry_horizontal_segment_constraint(self, dot_position: Position):
        constraint = self._symetry_horizontal_segment_constraint(dot_position)
        self._solver.add(constraint)

    def _symetry_vertical_segment_constraint(self, dot_position: Position):
        row = int(dot_position.r)
        constraints = []
        if dot_position.r - row == 0:
            position_up = dot_position.up
            position_down = dot_position.down
            up_go_up = self._island_bridges_z3[position_up][Direction.up()] == 1
            down_go_down = self._island_bridges_z3[position_down][Direction.down()] == 1
            constraints.append(up_go_up == down_go_down)
            while (position_up := position_up.up) in self._input_grid and (position_down := position_down.down) in self._input_grid:
                up_go_down = self._island_bridges_z3[position_up][Direction.down()] == 1
                down_go_up = self._island_bridges_z3[position_down][Direction.up()] == 1
                up_go_down_and_down_go_up = And(up_go_down, down_go_up)
                up_go_up = self._island_bridges_z3[position_up][Direction.up()] == 1
                down_go_down = self._island_bridges_z3[position_down][Direction.down()] == 1
                constraints.append(Implies(up_go_down_and_down_go_up, up_go_up == down_go_down))
            return And(constraints)
        else:
            position_up = Position(row, dot_position.c)
            position_down = position_up.down
            up_go_up = self._island_bridges_z3[position_up][Direction.up()] == 1
            down_go_down = self._island_bridges_z3[position_down][Direction.down()] == 1
            constraints.append(up_go_up == down_go_down)
            while (position_up := position_up.up) in self._input_grid and (position_down := position_down.down) in self._input_grid:
                up_go_down = self._island_bridges_z3[position_up][Direction.down()] == 1
                down_go_up = self._island_bridges_z3[position_down][Direction.up()] == 1
                up_go_down_and_down_go_up = And(up_go_down, down_go_up)
                up_go_up = self._island_bridges_z3[position_up][Direction.up()] == 1
                down_go_down = self._island_bridges_z3[position_down][Direction.down()] == 1
                constraints.append(Implies(up_go_down_and_down_go_up, up_go_up == down_go_down))
            return And(constraints)

    def _symetry_horizontal_segment_constraint(self, dot_position: Position):
        return True

    #
    # def _add_dots_constraints(self):
    #     for position in self.dots_positions.values():
    #         row = int(position.r)
    #         column = int(position.c)
    #         if position.r - row != 0:
    #             self._add_dot_must_vertical_segment_constraint(position)
    #         if position.c - column != 0:
    #             self._add_dot_must_horizontal_segment_constraint(position)
    #
    # def _add_dot_must_horizontal_segment_constraint(self, dot_position):
    #     left_positions = self._input_grid.all_positions_left(dot_position)
    #     right_positions = self._input_grid.all_positions_right(dot_position)
    #     if len(left_positions) == 0 or len(right_positions) == 0:
    #         self._add_dot_not_row_segment_constraint(dot_position)
    #         return
    #     if len(left_positions) < len(right_positions):
    #         right_positions = right_positions[:len(left_positions)]
    #     elif len(right_positions) < len(left_positions):
    #         left_positions = left_positions[:len(right_positions)]
    #     for left_position, right_position in zip(left_positions, right_positions):
    #         self._solver.add(
    #             Implies(self._island_bridges_z3[left_position][Direction.right()] == 1, self._island_bridges_z3[right_position][Direction.left()] == 1))
    #
    # def _add_dot_must_vertical_segment_constraint(self, dot_position):
    #     up_positions = self._input_grid.all_positions_up(dot_position)
    #     down_positions = self._input_grid.all_positions_down(dot_position)
    #     if len(up_positions) == 0 or len(down_positions) == 0:
    #         self._add_dot_not_column_segment_constraint(dot_position)
    #         return
    #     if len(up_positions) < len(down_positions):
    #         down_positions = down_positions[:len(up_positions)]
    #     elif len(down_positions) < len(up_positions):
    #         up_positions = up_positions[:len(down_positions)]
    #     for up_position, down_position in zip(up_positions, down_positions):
    #         self._solver.add(Implies(self._island_bridges_z3[up_position][Direction.down()] == 1,
    #                                  self._island_bridges_z3[down_position][Direction.up()] == 1))
    #
    # def _add_dot_not_row_segment_constraint(self, position):
    #     if (neighbor_left := self._input_grid.neighbor_left(position)) is not None:
    #         self._solver.add(self._island_bridges_z3[neighbor_left][Direction.right()] == 0)
    #     if (neighbor_right := self._input_grid.neighbor_right(position)) is not None:
    #         self._solver.add(self._island_bridges_z3[neighbor_right][Direction.left()] == 0)
    #
    # def _add_dot_not_column_segment_constraint(self, position):
    #     if (neighbor_up := self._input_grid.neighbor_up(position)) is not None:
    #         self._solver.add(self._island_bridges_z3[neighbor_up][Direction.down()] == 0)
    #     if (neighbor_down := self._input_grid.neighbor_down(position)) is not None:
    #         self._solver.add(self._island_bridges_z3[neighbor_down][Direction.up()] == 0)
