from z3 import Solver, Not, And, Int, sat, ArithRef, Or, Sum, If

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class IchimagaSolver(GameSolver):
    Empty = None

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
            island.position: {direction: Int(f"{island.position}_{direction}") for direction in Direction.orthogonal_directions()}
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
        for position, value in self._input_grid:
            bridges_var = list(self._island_bridges_z3[position].values())
            if value == self.Empty:
                self._solver.add(Or(sum(bridges_var) == 0, sum(bridges_var) == 2))
            else:
                self._solver.add(sum(bridges_var) == value)

            for bridge_var in bridges_var:
                self._solver.add(And(bridge_var >= 0, bridge_var <= 1))

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
        for position in [position for position, value in self._input_grid if value != self.Empty]:
            sum_linked_values_constraints = Sum(self._get_connected_neighbors_constraints(position))
            self._solver.add(sum_linked_values_constraints == self._input_grid[position])

    def _get_connected_neighbors_constraints(self, value_pos: Position):
        constraints = []
        for other_value_pos in [pos for pos, value in self._input_grid if value != self.Empty and pos != value_pos]:
            if value_pos.r == other_value_pos.r:
                direction = Direction.right() if other_value_pos.c > value_pos.c else Direction.left()
                constraint = self._straight_connection_constraint(value_pos, other_value_pos, direction)
                if constraint is not False:
                    constraints.append(If(constraint, 1, 0))
            elif value_pos.c == other_value_pos.c:
                direction = Direction.down() if other_value_pos.r > value_pos.r else Direction.up()
                constraint = self._straight_connection_constraint(value_pos, other_value_pos, direction)
                if constraint is not False:
                    constraints.append(If(constraint, 1, 0))
            else:
                hor_turn_pos = Position(value_pos.r, other_value_pos.c)
                vert_turn_pos = Position(other_value_pos.r, value_pos.c)
                hor_direction = Direction.right() if other_value_pos.c > value_pos.c else Direction.left()
                vert_direction = Direction.down() if other_value_pos.r > value_pos.r else Direction.up()

                hor_first_constraint = self._to_other_value_constraint(value_pos, other_value_pos, hor_turn_pos, hor_direction, vert_direction)
                vert_first_constraints = self._to_other_value_constraint(value_pos, other_value_pos, vert_turn_pos, vert_direction, hor_direction)
                
                if hor_first_constraint is not False:
                    constraints.append(If(hor_first_constraint, 1, 0))
                if vert_first_constraints is not False:
                    constraints.append(If(vert_first_constraints, 1, 0))

        return constraints

    def _straight_connection_constraint(self, start, end, direction):
        constraints = [self._island_bridges_z3[start][direction] == 1]
        current = start.after(direction)
        while current != end:
            if current not in self._input_grid or self._input_grid[current] != self.Empty:
                return False
            constraints.append(self._island_bridges_z3[current][direction] == 1)
            current = current.after(direction)
        return And(constraints)

    def _to_other_value_constraint(self, value_pos, other_value_pos, turn_position, first_direction, second_direction):
        constraints = [self._island_bridges_z3[value_pos][first_direction] == 1]
        current_position = value_pos.after(first_direction)
        while self._input_grid[current_position] == self.Empty and current_position in self._input_grid and current_position != turn_position:
            constraints.append(self._island_bridges_z3[current_position][first_direction] == 1)
            current_position = current_position.after(first_direction)
        if current_position not in self._input_grid or self._input_grid[current_position] != self.Empty:
            return False

        constraints.append(self._island_bridges_z3[current_position][second_direction] == 1)
        current_position = current_position.after(second_direction)
        while self._input_grid[current_position] == self.Empty and current_position != other_value_pos:
            constraints.append(self._island_bridges_z3[current_position][second_direction] == 1)
            current_position = current_position.after(second_direction)
        if current_position != other_value_pos:
            return False

        return And(constraints) if len(constraints) > 1 else constraints[0]
