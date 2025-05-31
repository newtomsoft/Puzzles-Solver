from typing import Dict

from z3 import ArithRef, Solver, Not, And, Or, Int, sat, Bool

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class KoburinSolver(GameSolver):
    def __init__(self, grid: Grid):
        self.input_grid = grid
        self._island_grid: IslandGrid | None = None
        self._init_island_grid()
        self._solver = Solver()
        self._island_bridges_z3: Dict[Position, Dict[Direction, ArithRef]] = {}
        self._previous_solution: IslandGrid | None = None

    def _init_island_grid(self):
        self._island_grid = IslandGrid([[Island(Position(r, c), 2) for c in range(self.input_grid.columns_number)] for r in range(self.input_grid.rows_number)])
        for position in [position for position, value in self.input_grid if value >= 0]:
            [self._island_grid[position].set_bridge(neighbor, 0) for neighbor in position.neighbors()]
            self._island_grid[position].set_bridges_count_according_to_directions_bridges()
            for neighbor in position.neighbors():
                if neighbor not in self._island_grid:
                    continue
                self._island_grid[neighbor].set_bridge(position, 0)

    def _init_solver(self):
        self._island_bridges_z3 = {island.position: {direction: Int(f"{island.position}_{direction}") for direction in Direction.orthogonals()} for island in self._island_grid.islands.values() if self.input_grid[island.position] < 0}
        for position in [position for position, _ in self.input_grid if position not in self._island_bridges_z3]:
            neighbors = self.input_grid.neighbors_positions(position)
            for neighbor in [neighbor for neighbor in neighbors if neighbor in self._island_bridges_z3]:
                direction = neighbor.direction_to(position)
                self._solver.add(self._island_bridges_z3[neighbor][direction] == 0)

        self._set_walls_around_digit()

        self._black_cells_z3 = {position: Bool for position, _ in self.input_grid if position in self._island_bridges_z3}

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
                for direction, bridges_number in [(direction, model.eval(bridges).as_long()) for direction, bridges in direction_bridges.items() if position.after(direction) in self._island_bridges_z3]:
                    if bridges_number > 0:
                        self._island_grid[position].set_bridge(self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
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
        for island in [island for island in self._previous_solution.islands.values() if island.position in self._island_bridges_z3]:
            for direction, (_, value) in island.direction_position_bridges.items():
                previous_solution_constraints.append(self._island_bridges_z3[island.position][direction] == value)
        self._solver.add(Not(And(previous_solution_constraints)))

        self._init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self.add_black_cell_constraints()
        self._add_opposite_bridges_constraints()
        self._add_bridges_sum_constraints()

    def _add_initial_constraints(self):
        constraints = [Or(direction_bridges == 0, direction_bridges == 1) for _island_bridges_z3 in self._island_bridges_z3.values() for direction_bridges in _island_bridges_z3.values()]
        self._solver.add(constraints)
        constraints_border_up = [self._island_bridges_z3[Position(0, c)][Direction.up()] == 0 for c in range(self._island_grid.columns_number) if Position(0, c) in self._island_bridges_z3]
        constraints_border_down = [self._island_bridges_z3[Position(self._island_grid.rows_number - 1, c)][Direction.down()] == 0 for c in range(self._island_grid.columns_number) if Position(self._island_grid.rows_number - 1, c) in self._island_bridges_z3]
        constraints_border_right = [self._island_bridges_z3[Position(r, self._island_grid.columns_number - 1)][Direction.right()] == 0 for r in range(self._island_grid.rows_number) if Position(r, self._island_grid.columns_number - 1) in self._island_bridges_z3]
        constraints_border_left = [self._island_bridges_z3[Position(r, 0)][Direction.left()] == 0 for r in range(self._island_grid.rows_number) if Position(r, 0) in self._island_bridges_z3]
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

    def _add_bridges_sum_constraints(self):
        for island in [island for island in self._island_grid.islands.values() if island.position in self._island_bridges_z3]:
            sum_constraint_2 = sum([self._island_bridges_z3[island.position][direction] for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]]) == 2
            sum_constraint_0 = sum([self._island_bridges_z3[island.position][direction] for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]]) == 0
            self._solver.add(Or(sum_constraint_2, sum_constraint_0))

    def add_black_cell_constraints(self):
        for position, value in [(position, value) for position, value in self.input_grid if value >= 0]:
            neighbors = self.input_grid.neighbors_positions(position)
            constraints = []
            for neighbor in neighbors:
                if neighbor not in self._island_bridges_z3:
                    continue
                direction = neighbor.direction_to(position)
                constraints.append(self._island_bridges_z3[neighbor][direction] == 0)
            if constraints:
                self._solver.add(Or(constraints))
            else:
                self._solver.add(self._black_cells_z3[position] == False)

    def _set_walls_around_digit(self):
        for position in [position for position, value in self.input_grid if value >= 0]:
            neighbors = self.input_grid.neighbors_positions(position)
            for neighbor in [neighbor for neighbor in neighbors if neighbor in self._island_bridges_z3]:
                direction = neighbor.direction_to(position)
                self._solver.add(self._island_bridges_z3[neighbor][direction] == 0)
