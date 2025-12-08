from typing import Collection

from z3 import Bool, Solver, Not, And, sat, is_true, Sum, ArithRef

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class MitiSolver(GameSolver):

    def __init__(self, dots_positions: Collection[Position], size: int):
        self._dots_positions = dots_positions
        self._rows_number = size
        self._columns_number = size
        self._init_island_grid()
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution: IslandGrid

    def _init_island_grid(self):
        self._island_grid = IslandGrid([[Island(Position(r, c), 2) for c in range(self._columns_number)] for r in range(self._rows_number)])

    def _init_solver(self):
        self._grid_z3 = Grid(
            [[{direction: Bool(f"{direction}_{r}-{c}") for direction in Direction.orthogonal_directions()} for c in range(self._columns_number)] for r in
             range(self._rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.assertions():
            self._init_solver()

        solution, _ = self._ensure_all_islands_grouped()
        return solution

    def _ensure_all_islands_grouped(self) -> tuple[IslandGrid, int]:
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

            connected_positions = self._island_grid.compute_linear_connected_positions()
            if len(connected_positions) == 1:
                self._previous_solution = self._island_grid
                return self._island_grid, propositions_count

            for loop in connected_positions:
                self._exclude_positions_values_together(loop)

        return IslandGrid.empty(), propositions_count

    def _exclude_positions_values_together(self, positions: set[Position]):
        constraints = []
        for position in positions:
            constraints += [
                self._grid_z3[position][direction] == (self._island_grid[position].direction_position_bridges.get(direction, [0, 0])[1] == 1) for
                direction in Direction.orthogonal_directions()
            ]
        self._solver.add(Not(And(constraints)))

    def get_other_solution(self):
        self._exclude_positions_values_together(self._previous_solution.get_positions())
        return self.get_solution()

    def _add_constraints(self):
        self._add_initials_constraints()
        self._add_opposite_constraints()
        self._add_bridges_sum_constraints()
        self._add_dots_constraints()
        self._add_not_edge_dots_constraints()
        self._add_not_inside_dots_constraints()

    def _add_initials_constraints(self):
        for position in self._grid_z3.edge_up_positions():
            self._solver.add(Not(self._grid_z3[position][Direction.up()]))
        for position in self._grid_z3.edge_down_positions():
            self._solver.add(Not(self._grid_z3[position][Direction.down()]))
        for position in self._grid_z3.edge_left_positions():
            self._solver.add(Not(self._grid_z3[position][Direction.left()]))
        for position in self._grid_z3.edge_right_positions():
            self._solver.add(Not(self._grid_z3[position][Direction.right()]))

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
        for _, value in self._grid_z3:
            self._solver.add(sum([value[direction] for direction in Direction.orthogonal_directions()]) == 2)

    def _add_dots_constraints(self):
        for dot_position in self._dots_positions:
            self._add_dot_constraints(dot_position)

    def _add_dot_constraints(self, dot_position: Position):
        neighbors_positions = dot_position.straddled_neighbors()
        in_grid_neighbors_positions = [pos for pos in neighbors_positions if pos in self._grid_z3]
        if len(in_grid_neighbors_positions) == 2:
            pos0, pos1 = in_grid_neighbors_positions
            direction = pos0.direction_to(pos1)
            self._solver.add(Not(self._grid_z3[pos0][direction]))
            return

        connected_cells_count_var = self._connected_cells_count_var(in_grid_neighbors_positions)
        self._solver.add(connected_cells_count_var == 1)

    def _add_not_edge_dots_constraints(self):
        empty_edge_positions = self._get_empty_edge_positions()
        for position in empty_edge_positions:
            pos0, pos1 = [neighbor for neighbor in position.straddled_neighbors() if neighbor in self._grid_z3]
            direction = pos0.direction_to(pos1)
            self._solver.add(self._grid_z3[pos0][direction])

    def _add_not_inside_dots_constraints(self):
        empty_inside_positions = self._get_empty_inside_positions()
        for position in empty_inside_positions:
            self._add_not_inside_dot_constraints(position)

    def _add_not_inside_dot_constraints(self, position):
        positions = [neighbor for neighbor in position.straddled_neighbors() if neighbor in self._grid_z3]
        neighbors_connection_count_var = self._connected_cells_count_var(positions)
        self._solver.add(neighbors_connection_count_var >= 2)

    def _get_empty_edge_positions(self) -> set[Position]:
        first_position = Position(-0.5, -0.5)
        positions = set()
        for c in range(1, self._columns_number):
            positions.add(first_position + Position(0, c))
            positions.add(first_position + Position(self._rows_number, c))

        for r in range(1, self._rows_number):
            positions.add(first_position + Position(r, 0))
            positions.add(first_position + Position(r, self._columns_number))

        positions -= set(self._dots_positions)
        return positions

    def _get_empty_inside_positions(self):
        first_position = Position(-0.5, -0.5)
        positions = set()
        for r in range(1, self._rows_number):
            for c in range(1, self._columns_number):
                positions.add(first_position + Position(r, c))

        positions -= set(self._dots_positions)
        return positions

    def _connected_cells_count_var(self, in_grid_neighbors_positions: list[Position]) -> ArithRef:
        paires = [(in_grid_neighbors_positions[i], in_grid_neighbors_positions[(i + 1) % 4]) for i in range(4)]
        constraints = []
        for pos0, pos1 in paires:
            direction = pos0.direction_to(pos1)
            constraints.append(self._grid_z3[pos0][direction])
        return Sum(constraints)
