﻿from z3 import Solver, Not, And, Int, sat, ArithRef, Or, Sum

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class KuroshiroSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._input_grid = grid
        self._island_grid: IslandGrid | None = None
        self.init_island_grid()
        self._solver = Solver()
        self._island_bridges_z3: dict[Position, dict[Direction, ArithRef]] = {}
        self._previous_solution: IslandGrid | None = None

    def init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._input_grid.columns_number)] for r in range(self._input_grid.rows_number)]
        )

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
                        self._island_grid[position].set_bridge_to_position(
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
        self._add_opposite_bridges_constraints()
        self._add_links_constraints()

    def _add_initial_constraints(self):
        for position, direction_bridges in self._island_bridges_z3.items():
            bridges_count_vars = list(direction_bridges.values())
            input_value = self._input_grid[position]
            is_circle = input_value in ['□', '■']
            constraint_sum = sum(bridges_count_vars) == 2 if is_circle else Or(sum(bridges_count_vars) == 2, sum(bridges_count_vars) == 0)
            self._solver.add(constraint_sum)
            for bridges in direction_bridges.values():
                self._solver.add(And(bridges >= 0, bridges <= 1))

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._solver.add(
                        self._island_bridges_z3[island.position][direction] ==
                        self._island_bridges_z3[island.direction_position_bridges[direction][0]][direction.opposite])
                else:
                    self._solver.add(self._island_bridges_z3[island.position][direction] == 0)

    def _add_links_constraints(self):
        for position, circle_value in [(position, value) for position, value in self._input_grid if value in ['□', '■']]:
            same_color_circles_linked_constraints = self._same_color_circles_linked_constraints(position, circle_value)
            other_color_circles_linked_constraints = self._other_color_circles_linked_constraints(position, circle_value)
            linked_circles_constraints = same_color_circles_linked_constraints + other_color_circles_linked_constraints
            self._solver.add(Sum(linked_circles_constraints) == 2)

    def _same_color_circles_linked_constraints(self, position: Position, circle_value: str) -> list:
        # it must have no turn between two circles of the same color
        or_constraints = []
        for direction in Direction.orthogonals():
            constraints = []
            found = None
            constraints.append(self._island_bridges_z3[position][direction] == 1)
            current_position = position.after(direction)
            while current_position in self._island_bridges_z3:
                if (value := self._input_grid[current_position]) == circle_value:
                    found = value
                    break
                constraints.append(self._island_bridges_z3[current_position][direction] == 1)
                current_position = current_position.after(direction)
            if found is None:
                continue
            or_constraints.append(And(constraints) if len(constraints) > 1 else constraints[0])
        return or_constraints if len(or_constraints) > 0 else [False]

    def _other_color_circles_linked_constraints(self, circle_pos: Position, circle_value: str):
        # it must have exactly 1 turn between two circles of different colors
        constraints = []
        other_color = '■' if circle_value == '□' else '□'
        for other_circle_pos in [pos for pos, value in self._input_grid if value == other_color and pos.r != circle_pos.r and pos.c != circle_pos.c]:
            hor_turn_pos = Position(circle_pos.r, other_circle_pos.c)
            vert_turn_pos = Position(other_circle_pos.r, circle_pos.c)
            hor_direction = Direction.right() if other_circle_pos.c > circle_pos.c else Direction.left()
            vert_direction = Direction.down() if other_circle_pos.r > circle_pos.r else Direction.up()

            hor_first_constraint = self._to_other_circle_constraint(circle_pos, other_circle_pos, hor_turn_pos, hor_direction, vert_direction)
            vert_first_constraints = self._to_other_circle_constraint(circle_pos, other_circle_pos, vert_turn_pos, vert_direction, hor_direction)
            constraints.append(Or(hor_first_constraint, vert_first_constraints))

        return constraints

    def _to_other_circle_constraint(self, circle_pos, other_circle_pos, turn_position, first_direction, second_direction):
        constraints = [self._island_bridges_z3[circle_pos][first_direction] == 1]
        current_position = circle_pos.after(first_direction)
        while self._input_grid[current_position] == '' and current_position != turn_position:
            constraints.append(self._island_bridges_z3[current_position][first_direction] == 1)
            current_position = current_position.after(first_direction)
        if self._input_grid[current_position] != '':
            return False

        constraints.append(self._island_bridges_z3[current_position][second_direction] == 1)
        current_position = current_position.after(second_direction)
        while self._input_grid[current_position] == '' and current_position != other_circle_pos:
            constraints.append(self._island_bridges_z3[current_position][second_direction] == 1)
            current_position = current_position.after(second_direction)
        if current_position != other_circle_pos:
            return False

        return And(constraints) if len(constraints) > 1 else constraints[0]
