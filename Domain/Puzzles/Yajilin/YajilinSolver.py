from typing import Dict

from z3 import ArithRef, Solver, Not, And, Or, Int, sat, Bool, Implies, is_true

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Puzzles.GameSolver import GameSolver


class YajilinSolver(GameSolver):
    direction_map = {
        'R': Direction.right(),
        'D': Direction.down(),
        'L': Direction.left(),
        'U': Direction.up()
    }

    def __init__(self, grid: Grid):
        self.input_grid = grid
        self._island_grid: IslandGrid | None = None
        self._init_island_grid()
        self._solver = Solver()
        self._island_bridges_z3: Dict[Position, Dict[Direction, ArithRef]] = {}
        self._previous_solution: IslandGrid | None = None

    def _init_island_grid(self):
        self._island_grid = IslandGrid([[Island(Position(r, c), 2) for c in range(self.input_grid.columns_number)] for r in range(self.input_grid.rows_number)])
        for position in [position for position, value in self.input_grid if value != '']:
            [self._island_grid[position].set_bridge_to_position(neighbor, 0) for neighbor in position.neighbors()]
            self._island_grid[position].set_bridges_count_according_to_directions_bridges()
            for neighbor in position.neighbors():
                if neighbor not in self._island_grid:
                    continue
                self._island_grid[neighbor].set_bridge_to_position(position, 0)

    def _init_solver(self):
        self._island_bridges_z3 = {island.position: {direction: Int(f"{island.position}_{direction}") for direction in Direction.orthogonals()} for island in
                                   self._island_grid.islands.values() if island.bridges_count > 0}
        for position in [position for position, _ in self.input_grid if position not in self._island_bridges_z3]:
            neighbors = self.input_grid.neighbors_positions(position)
            for neighbor in [neighbor for neighbor in neighbors if neighbor in self._island_bridges_z3]:
                direction = neighbor.direction_to(position)
                self._solver.add(self._island_bridges_z3[neighbor][direction] == 0)

        self._black_cells_z3 = {position: Bool(f'p{position}') for position, _ in self.input_grid if position in self._island_bridges_z3}
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
                for direction, bridges_number in [(direction, model.eval(bridges).as_long()) for direction, bridges in direction_bridges.items() if
                                                  position.after(direction) in self._island_bridges_z3]:
                    self._island_grid[position].set_bridge_to_position(self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
                self._island_grid[position].set_bridges_count_according_to_directions_bridges()

            connected_positions = self._island_grid.get_connected_positions(exclude_without_bridge=True)
            if len(connected_positions) == 1:
                for position, value in [(position, value) for position, value in self.input_grid if value != '']:
                    self._island_grid.set_value(position, value)
                for position, var in self._black_cells_z3.items():
                    if is_true(model.eval(var)):
                        self._island_grid.set_value(position, '■')

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
        for island in [island for island in self._previous_solution.islands.values() if island.position in self._island_bridges_z3]:
            for direction, (_, value) in island.direction_position_bridges.items():
                previous_solution_constraints.append(self._island_bridges_z3[island.position][direction] == value)
        self._solver.add(Not(And(previous_solution_constraints)))

        self._init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_walls_around_digit_constraints()
        self._add_black_cell_constraints()
        self._add_no_adjacent_black_constraint()
        self._add_opposite_bridges_constraints()
        self._add_bridges_sum_constraints()

    def _add_initial_constraints(self):
        constraints = [Or(direction_bridges == 0, direction_bridges == 1) for _island_bridges_z3 in self._island_bridges_z3.values() for direction_bridges in
                       _island_bridges_z3.values()]
        self._solver.add(constraints)
        constraints_border_up = [self._island_bridges_z3[Position(0, c)][Direction.up()] == 0 for c in range(self._island_grid.columns_number) if
                                 Position(0, c) in self._island_bridges_z3]
        constraints_border_down = [self._island_bridges_z3[Position(self._island_grid.rows_number - 1, c)][Direction.down()] == 0 for c in
                                   range(self._island_grid.columns_number) if Position(self._island_grid.rows_number - 1, c) in self._island_bridges_z3]
        constraints_border_right = [self._island_bridges_z3[Position(r, self._island_grid.columns_number - 1)][Direction.right()] == 0 for r in
                                    range(self._island_grid.rows_number) if Position(r, self._island_grid.columns_number - 1) in self._island_bridges_z3]
        constraints_border_left = [self._island_bridges_z3[Position(r, 0)][Direction.left()] == 0 for r in range(self._island_grid.rows_number) if
                                   Position(r, 0) in self._island_bridges_z3]
        self._solver.add(constraints_border_down + constraints_border_up + constraints_border_right + constraints_border_left)

    def _add_opposite_bridges_constraints(self):
        for island in [island for island in self._island_grid.islands.values() if island.position in self._island_bridges_z3]:
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                position_bridges = island.direction_position_bridges.get(direction)
                if position_bridges is not None:
                    other_position, _ = position_bridges
                    if other_position not in self._island_bridges_z3:
                        continue
                    self._solver.add(self._island_bridges_z3[island.position][direction] == self._island_bridges_z3[other_position][direction.opposite])
                else:
                    self._solver.add(self._island_bridges_z3[island.position][direction] == 0)

    def _add_black_cell_constraints(self):
        for position, blacks_count_direction in [(position, value) for position, value in self.input_grid if value != '']:
            blacks_count = int(blacks_count_direction[0])
            direction = YajilinSolver.direction_map[blacks_count_direction[1]]
            concerned_positions = self.input_grid.all_positions_at(position, direction)
            self._solver.add(sum([self._black_cells_z3[concerned_position] for concerned_position in concerned_positions if
                                  concerned_position in self._island_bridges_z3.keys()]) == blacks_count)

    def _add_bridges_sum_constraints(self):
        for position in [position for position, value in self.input_grid if value == '']:
            bridges_count_0 = sum(
                [self._island_bridges_z3[position][direction] for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]]) == 0
            bridges_count_2 = sum(
                [self._island_bridges_z3[position][direction] for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]]) == 2
            black_cell = self._black_cells_z3[position]
            path_cell = Not(black_cell)
            self._solver.add(Implies(black_cell, bridges_count_0))
            self._solver.add(Implies(path_cell, bridges_count_2))

    def _add_no_adjacent_black_constraint(self):
        for position in [position for position, value in self.input_grid if value == '']:
            for neighbor_position in self.input_grid.neighbors_positions(position):
                if neighbor_position not in self._island_bridges_z3:
                    continue
                self._solver.add(Implies(self._black_cells_z3[position], Not(self._black_cells_z3[neighbor_position])))

    def _add_walls_around_digit_constraints(self):
        for position in [position for position, value in self.input_grid if value != '']:
            neighbors = self.input_grid.neighbors_positions(position)
            for neighbor in [neighbor for neighbor in neighbors if neighbor in self._island_bridges_z3]:
                direction = neighbor.direction_to(position)
                self._solver.add(self._island_bridges_z3[neighbor][direction] == 0)
