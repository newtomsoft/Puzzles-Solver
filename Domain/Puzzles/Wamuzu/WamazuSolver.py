from z3 import Solver, ArithRef, Int, sat, Or, And, Not

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position


class WamazuSolver:
    def __init__(self, grid: Grid):
        self._input_grid = grid
        self._connections_number = sum(1 for row in grid for cell in row if cell == 1) // 2
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
            island.position: {direction: Int(f"{island.position}_{direction}") for direction in Direction.orthogonals()}
            for island in self._island_grid.islands.values()
        }
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if not self._solver.assertions():
            self._init_solver()

        solution, _ = self._ensure_no_loop()
        return solution

    def _ensure_no_loop(self) -> tuple[IslandGrid, int]:
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
            loop_positions = self._island_grid.get_loop_positions()
            if len(loop_positions) == 0:
                self._previous_solution = self._island_grid
                return self._island_grid, proposition_count

            to_exclude_loop_constraints = []
            for island in [self._island_grid.islands[position] for position in loop_positions]:
                for direction, (_, value) in island.direction_position_bridges.items():
                    to_exclude_loop_constraints.append(self._island_bridges_z3[island.position][direction] == value)
            self._solver.add(Not(And(to_exclude_loop_constraints)))
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
        self._add_turn_constraints()

    def _add_initial_constraints(self):
        for position in [position for position, value in self._input_grid if value == 1]:
            bridges = self._island_bridges_z3[position]
            bridges_count_vars = list(bridges.values())
            self._solver.add(sum(bridges_count_vars) == 1)
            for direction_bridges in bridges.values():
                self._solver.add(And(direction_bridges >= 0, direction_bridges <= 1))

        for position in [position for position, value in self._input_grid if value != 1]:
            bridges = self._island_bridges_z3[position]
            self._solver.add(Or(
                And(bridges[Direction.right()] == 0, bridges[Direction.down()] == 0, bridges[Direction.left()] == 1, bridges[Direction.up()] == 1),
                And(bridges[Direction.left()] == 0, bridges[Direction.up()] == 0, bridges[Direction.right()] == 1, bridges[Direction.down()] == 1),
                And(bridges[Direction.down()] == 0, bridges[Direction.left()] == 0, bridges[Direction.up()] == 1, bridges[Direction.right()] == 1),
                And(bridges[Direction.up()] == 0, bridges[Direction.right()] == 0, bridges[Direction.down()] == 1, bridges[Direction.left()] == 1)
            ))
            for direction_bridges in bridges.values():
                self._solver.add(And(direction_bridges >= 0, direction_bridges <= 1))

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._solver.add(self._island_bridges_z3[island.position][direction] ==
                                     self._island_bridges_z3[island.direction_position_bridges[direction][0]][direction.opposite])
                else:
                    self._solver.add(self._island_bridges_z3[island.position][direction] == 0)

    def _add_turn_constraints(self):
        pass
