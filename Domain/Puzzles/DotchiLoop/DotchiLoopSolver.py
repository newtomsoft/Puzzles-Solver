from z3 import Solver, Not, And, Int, sat, Or, ArithRef

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position

_ = 0
B = 1
W = 2


class DotchiLoopSolver:
    def __init__(self, region_grid: Grid[int], value_grid: Grid[int]):
        self._region_grid = region_grid
        self._value_grid = value_grid
        self._rows_number = self._region_grid.rows_number
        self._columns_number = self._region_grid.columns_number
        self._solver = Solver()
        self._island_grid: IslandGrid | None = None
        self.init_island_grid()
        self._solver = Solver()
        self._island_bridges_z3: dict[Position, dict[Direction, ArithRef]] = {}
        self._previous_solution: IslandGrid | None = None

    def init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._value_grid.columns_number)] for r in range(self._value_grid.rows_number)])

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
        self._add_cell_color_constraints()
        self._add_same_cross_type_by_region_constraints()

    def _add_initial_constraints(self):
        for position, direction_bridges in self._island_bridges_z3.items():
            bridges_count_vars = list(direction_bridges.values())
            self._solver.add(Or(sum(bridges_count_vars) == 2, sum(bridges_count_vars) == 0))
            for bridges in direction_bridges.values():
                self._solver.add(And(bridges >= 0, bridges <= 1))

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._solver.add(self._island_bridges_z3[island.position][direction] ==
                                     self._island_bridges_z3[island.direction_position_bridges[direction][0]][direction.opposite])
                else:
                    self._solver.add(self._island_bridges_z3[island.position][direction] == 0)

    def _add_cell_color_constraints(self):
        for position, value in [(position, value) for position, value in self._value_grid if value != _]:
            if value == B:
                for direction in Direction.orthogonal_directions():
                    self._solver.add(self._island_bridges_z3[position][direction] == 0)
            if value == W:
                self._solver.add(sum(self._island_bridges_z3[position].values()) == 2)

    def _add_same_cross_type_by_region_constraints(self):
        for positions in self._region_grid.get_regions().values():
            cross_line_constraints = []
            cross_turn_constraints = []
            for pos in [pos for pos in positions if self._value_grid[pos] == W]:
                hor = And(self._island_bridges_z3[pos][Direction.right()] == 1, self._island_bridges_z3[pos][Direction.left()] == 1)
                ver = And(self._island_bridges_z3[pos][Direction.down()] == 1, self._island_bridges_z3[pos][Direction.up()] == 1)
                cross_line_constraints.append(Or(hor, ver))

                turn1 = And(self._island_bridges_z3[pos][Direction.right()] == 1, self._island_bridges_z3[pos][Direction.down()] == 1)
                turn2 = And(self._island_bridges_z3[pos][Direction.right()] == 1, self._island_bridges_z3[pos][Direction.up()] == 1)
                turn3 = And(self._island_bridges_z3[pos][Direction.left()] == 1, self._island_bridges_z3[pos][Direction.down()] == 1)
                turn4 = And(self._island_bridges_z3[pos][Direction.left()] == 1, self._island_bridges_z3[pos][Direction.up()] == 1)
                cross_turn_constraints.append(Or(turn1, turn2, turn3, turn4))

            self._solver.add(Or(And(cross_line_constraints), And(cross_turn_constraints)))