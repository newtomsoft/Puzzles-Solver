from z3 import Solver, ArithRef, Int, sat, Or, And, Not

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position


class GeradewegSolver:
    _used_directions = [Direction.right(), Direction.down()]

    def __init__(self, grid: Grid):
        self._input_grid = grid
        self._island_grid: IslandGrid | None = None
        self._rows_number = self._input_grid.rows_number
        self._columns_number = self._input_grid.columns_number
        self._init_island_grid()
        self._solver = Solver()
        self._island_bridges_z3: dict[Position, dict[Direction, ArithRef]] = {}
        self._previous_solution: IslandGrid | None = None

    def _init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._input_grid.columns_number)] for r in
             range(self._input_grid.rows_number)])

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
        self._add_lengths_constraints()

    def _add_initial_constraints(self):
        for position, directions_bridges in self._island_bridges_z3.items():
            bridges_count_vars = list(directions_bridges.values())
            self._solver.add(Or(sum(bridges_count_vars) == 2, sum(bridges_count_vars) == 0))
            for direction_bridges in directions_bridges.values():
                self._solver.add(And(direction_bridges >= 0, direction_bridges <= 1))

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._solver.add(self._island_bridges_z3[island.position][direction] ==
                                     self._island_bridges_z3[island.direction_position_bridges[direction][0]][direction.opposite])
                else:
                    self._solver.add(self._island_bridges_z3[island.position][direction] == 0)

    def _add_lengths_constraints(self):
        for position, length in [(position, value) for position, value in self._input_grid if value > 0]:
            self._solver.add(sum(self._island_bridges_z3[position][direction] for direction in Direction.orthogonal_directions()) == 2)
            constraints = []
            for direction in self._used_directions:
                constraints.append(self._length_constraint(position, length, direction))
            self._solver.add(Or(constraints))

    def _length_constraint(self, position: Position, length: int, direction: Direction):
        constraints = [self._extremities_constraint(position, length, direction)]

        for before_offset in range(1, length):
            constraints.append(self._offsets_constraint(position, length, direction, before_offset))
        return Or(constraints)

    def _extremities_constraint(self, position: Position, length: int, direction: Direction):
        constraints = []
        other_direction = next(other_direction for other_direction in self._used_directions if other_direction != direction)
        other_direction_before_constraints = self._offsets_constraint(position, length, other_direction, 0)
        other_direction_after_constraints = self._offsets_constraint(position, length, other_direction, length)
        before_constraints = self._offsets_constraint(position, length, direction, 0)
        constraints.append(And(before_constraints, Or(other_direction_before_constraints, other_direction_after_constraints)))
        after_constraints = self._offsets_constraint(position, length, direction, length)
        constraints.append(And(after_constraints, Or(other_direction_before_constraints, other_direction_after_constraints)))
        return Or(constraints)

    def _offsets_constraint(self, position: Position, length: int, direction: Direction, before_offset: int):
        after_offset = length - before_offset
        first_position = position.before(direction, before_offset)
        last_position = position.after(direction, after_offset)
        if first_position not in self._input_grid or last_position not in self._input_grid:
            return False
        between_positions = first_position.all_positions_between(last_position)
        current_constraints = [
            self._island_bridges_z3[first_position][direction] == 1,
            self._island_bridges_z3[first_position][direction.opposite] == 0,
            self._island_bridges_z3[last_position][direction] == 0,
            self._island_bridges_z3[last_position][direction.opposite] == 1
        ]
        for current_position in between_positions:
            current_constraints.append(self._island_bridges_z3[current_position][direction] == 1)
            current_constraints.append(self._island_bridges_z3[current_position][direction.opposite] == 1)
        return And(current_constraints)
