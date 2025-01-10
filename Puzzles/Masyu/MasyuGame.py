from typing import Dict

from z3 import Solver, sat, Int, And, Not, ArithRef, Or, Sum

from Utils.Direction import Direction
from Utils.Grid import Grid
from Utils.IslandsGrid import IslandGrid
from Utils.Position import Position


class MasyuGame:
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
        if self._solver.check() != sat:
            return IslandGrid.empty()
        model = self._solver.model()
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
        self._last_solution = self._island_grid
        if not self._island_grid.are_all_islands_connected(exclude_without_bridge=True):
            return self.get_other_solution()
        return self._island_grid

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
        self._add_circles_constraints()

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

    def _add_circles_constraints(self):
        for position, value in self.input_grid:
            if value == 'w':
                horizontal_constraint = False
                vertical_constraint = False
                if position.left in self._island_bridges_z3 and position.right in self._island_bridges_z3:
                    horizontal_constraint = And(self._island_bridges_z3[position][Direction.left()] == 1, self._island_bridges_z3[position][Direction.right()] == 1)
                    turn0_constraint = False
                    turn1_constraint = False
                    turn2_constraint = False
                    turn3_constraint = False
                    if Direction.up() in self._island_bridges_z3[position.left]:
                        turn0_constraint = self._island_bridges_z3[position.left][Direction.up()] == 1
                    if Direction.down() in self._island_bridges_z3[position.left]:
                        turn1_constraint = self._island_bridges_z3[position.left][Direction.down()] == 1
                    if Direction.up() in self._island_bridges_z3[position.right]:
                        turn2_constraint = self._island_bridges_z3[position.right][Direction.up()] == 1
                    if Direction.down() in self._island_bridges_z3[position.right]:
                        turn3_constraint = self._island_bridges_z3[position.right][Direction.down()] == 1
                    turn_constraint = Or(turn0_constraint, turn1_constraint, turn2_constraint, turn3_constraint)
                    horizontal_constraint = And(horizontal_constraint, turn_constraint)
                if position.up in self._island_bridges_z3 and position.down in self._island_bridges_z3:
                    vertical_constraint = And(self._island_bridges_z3[position][Direction.up()] == 1, self._island_bridges_z3[position][Direction.down()] == 1)
                    turn0_constraint = False
                    turn1_constraint = False
                    turn2_constraint = False
                    turn3_constraint = False
                    if Direction.left() in self._island_bridges_z3[position.up]:
                        turn0_constraint = self._island_bridges_z3[position.up][Direction.left()] == 1
                    if Direction.right() in self._island_bridges_z3[position.up]:
                        turn1_constraint = self._island_bridges_z3[position.up][Direction.right()] == 1
                    if Direction.left() in self._island_bridges_z3[position.down]:
                        turn2_constraint = self._island_bridges_z3[position.down][Direction.left()] == 1
                    if Direction.right() in self._island_bridges_z3[position.down]:
                        turn3_constraint = self._island_bridges_z3[position.down][Direction.right()] == 1
                    turn_constraint = Or(turn0_constraint, turn1_constraint, turn2_constraint, turn3_constraint)
                    vertical_constraint = And(vertical_constraint, turn_constraint)
                self._solver.add(Or(horizontal_constraint, vertical_constraint))
            if value == 'b':
                right_down_constraint = False
                left_down_constraint = False
                right_up_constraint = False
                left_up_constraint = False
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