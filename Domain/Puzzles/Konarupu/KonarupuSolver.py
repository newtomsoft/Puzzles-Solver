﻿from z3 import Solver, Not, And, Int, sat, Or, Sum, BoolRef

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
        self._solver = Solver()
        self._island_bridges_z3: dict[Position, dict[Direction, any]] = {}
        self._previous_solution: IslandGrid | None = None

    def _init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self.input_grid.columns_number + 1)] for r in range(self.input_grid.rows_number + 1)])

    def _init_solver(self):
        self._island_bridges_z3 = {island.position: {direction: Int(f"{island.position}_{direction}") for direction in Direction.orthogonals()} for island in
                                   self._island_grid.islands.values()}
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if not self._solver.assertions():
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
        self._add_numbers_constraints()

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
        for island in self._island_grid.islands.values():
            sum0_constraint = sum([self._island_bridges_z3[island.position][direction] for direction in
                                   [Direction.right(), Direction.down(), Direction.left(), Direction.up()]]) == 0
            sum2_constraint = sum([self._island_bridges_z3[island.position][direction] for direction in
                                   [Direction.right(), Direction.down(), Direction.left(), Direction.up()]]) == 2
            self._solver.add(Or(sum0_constraint, sum2_constraint))

    def _add_numbers_constraints(self):
        for position, number in [(position, number) for position, number in self.input_grid if number != _]:
            up_left_no_turn_constraint = self.corner_no_turn_constraint(self._island_bridges_z3[position])
            down_left_no_turn_constraint = self.corner_no_turn_constraint(self._island_bridges_z3[position.down])
            down_right_no_turn_constraint = self.corner_no_turn_constraint(self._island_bridges_z3[position.down_right])
            up_right_no_turn_constraint = self.corner_no_turn_constraint(self._island_bridges_z3[position.right])

            self._solver.add(
                Sum(up_left_no_turn_constraint, down_left_no_turn_constraint, down_right_no_turn_constraint, up_right_no_turn_constraint) == 4 - number
            )

    def corner_no_turn_constraint(self, corner_directions_var: dict[Direction, int]) -> BoolRef:
        corner_vertical = self.vertical_constraint(corner_directions_var)
        corner_horizontal = self.horizontal_constraint(corner_directions_var)
        corner_empty = self.empty_constraint(corner_directions_var)
        return Or(corner_vertical, corner_horizontal, corner_empty)

    @staticmethod
    def vertical_constraint(directions_var: dict[Direction, int]) -> BoolRef:
        return And(directions_var[Direction.down()] == 1, directions_var[Direction.up()] == 1)

    @staticmethod
    def horizontal_constraint(directions_var: dict[Direction, int]) -> BoolRef:
        return And(directions_var[Direction.left()] == 1, directions_var[Direction.right()] == 1)

    @staticmethod
    def empty_constraint(dir_var: dict[Direction, int]) -> BoolRef:
        return And(dir_var[Direction.left()] == 0, dir_var[Direction.right()] == 0, dir_var[Direction.up()] == 0, dir_var[Direction.down()] == 0)
