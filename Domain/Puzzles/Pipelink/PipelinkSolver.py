from z3 import Solver, Not, And, Or, sat, Bool, is_true

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class PipelinkSolver(GameSolver):
    def __init__(self, grid: Grid):
        self.input_grid = grid
        self._rows_number, self._columns_number = grid.rows_number, grid.columns_number
        self._island_grid: IslandGrid | None = None
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution: IslandGrid

    def _init_island_grid(self):
        self._island_grid = IslandGrid([[Island(Position(r, c), 2) for c in range(self._columns_number)] for r in range(self._rows_number)])

    def _init_solver(self):
        self._grid_z3 = Grid(
            [[{direction: Bool(f"{direction}_{r}-{c}") for direction in Direction.orthogonals()} for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.assertions():
            self._init_solver()

        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        propositions_count = 0
        while self._solver.check() == sat:
            self._init_island_grid()
            model = self._solver.model()
            propositions_count += 1
            for position, direction_bridges in self._grid_z3:
                for direction, bridges in direction_bridges.items():
                    bridges_number = 1 if is_true(model.eval(bridges)) else 0
                    if bridges_number > 0:
                        self._island_grid[position].set_bridge_to_position(self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
                    elif position in self._island_grid and direction in self._island_grid[position].direction_position_bridges:
                        self._island_grid[position].direction_position_bridges.pop(direction)
                self._island_grid[position].set_bridges_count_according_to_directions_bridges()
            connected_positions = self._island_grid.get_linear_connected_positions(exclude_without_bridge=True)
            if len(connected_positions) == 1:
                self._previous_solution = self._island_grid
                return self._island_grid, propositions_count

            biggest_connected_positions = max(connected_positions, key=len)
            connected_positions.remove(biggest_connected_positions)
            for positions in connected_positions:
                not_loop_constraints = []
                cell_constraints = []
                for position in positions:
                    directions_with_bridge = self._island_grid[position].direction_position_bridges.keys()
                    for direction in directions_with_bridge:
                        cell_constraints.append(self._grid_z3[position][direction])
                    directions_without_bridge = [direction for direction in Direction.orthogonals() if direction not in directions_with_bridge]
                    for direction in directions_without_bridge:
                        cell_constraints.append(Not(self._grid_z3[position][direction]))
                not_loop_constraints.append(Not(And(cell_constraints)))
                self._solver.add(And(not_loop_constraints))

        return IslandGrid.empty(), propositions_count

    def get_other_solution(self):
        constraints = []
        for position, island in self._previous_solution:
            constraints += [self._grid_z3[position][direction] == (island.direction_position_bridges.get(direction, [0,0])[1] == 1) for direction in Direction.orthogonals()]
        self._solver.add(Not(And(constraints)))
        return self.get_solution()

    def _add_constraints(self):
        self._add_initials_constraints()
        self._add_opposite_constraints()
        self._add_bridges_sum_constraints()

    def _add_initials_constraints(self):
        for position in self._grid_z3.edge_up_positions():
            self._solver.add(Not(self._grid_z3[position][Direction.up()]))
        for position in self._grid_z3.edge_down_positions():
            self._solver.add(Not(self._grid_z3[position][Direction.down()]))
        for position in self._grid_z3.edge_left_positions():
            self._solver.add(Not(self._grid_z3[position][Direction.left()]))
        for position in self._grid_z3.edge_right_positions():
            self._solver.add(Not(self._grid_z3[position][Direction.right()]))

        for position, island in [(position, island) for position, island in self.input_grid if not island.has_no_bridge()]:
            for direction, (_, bridges) in island.direction_position_bridges.items():
                self._solver.add(self._grid_z3[position][direction] == (bridges == 1))

    def _add_opposite_constraints(self):
        for position, _ in self._grid_z3:
            if position.up in self._grid_z3:
                self._solver.add(self._grid_z3[position][Direction.up()] == self._grid_z3[position.up][Direction.down()])
            if position.down in self._grid_z3:
                self._solver.add(self._grid_z3[position][Direction.down()] == self._grid_z3[position.down][Direction.up()])
            if position.left in self._grid_z3:
                self._solver.add(self._grid_z3[position][Direction.left()] == self._grid_z3[position.left][Direction.right()])
            if position.right in self._grid_z3:
                self._solver.add(self._grid_z3[position][Direction.right()] == self._grid_z3[position.right][Direction.left()])

    def _add_bridges_sum_constraints(self):
        for position, _ in self._grid_z3:
            sum_constraint_2 = sum(
                [self._grid_z3[position][direction] for direction in Direction.orthogonals()]) == 2
            sum_constraint_4 = sum(
                [self._grid_z3[position][direction] for direction in Direction.orthogonals()]) == 4
            self._solver.add(Or(sum_constraint_2, sum_constraint_4))
