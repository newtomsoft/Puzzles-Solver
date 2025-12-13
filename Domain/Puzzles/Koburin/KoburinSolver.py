from ortools.sat.cp_model_pb2 import CpSolverStatus
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import IntVar, CpModel, CpSolver

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
        self._model: CpModel = cp_model.CpModel()
        self._solver: CpSolver = CpSolver()
        self._initialized = False
        self._island_bridges_z3: dict[Position, dict[Direction, IntVar]] = {}
        self._black_cells_z3: dict[Position, IntVar] = {}
        self._previous_solution: IslandGrid | None = None

    def _init_island_grid(self):
        self._island_grid = IslandGrid([[Island(Position(r, c), 2) for c in range(self.input_grid.columns_number)] for r in range(self.input_grid.rows_number)])
        for position in [position for position, value in self.input_grid if value >= 0]:
            [self._island_grid[position].set_bridge_to_position(neighbor, 0) for neighbor in position.neighbors()]
            self._island_grid[position].set_bridges_count_according_to_directions_bridges()
            for neighbor in position.neighbors():
                if neighbor not in self._island_grid:
                    continue
                self._island_grid[neighbor].set_bridge_to_position(position, 0)

    def _init_solver(self):
        self._model = cp_model.CpModel()
        # Create BoolVars for bridges only on non-digit cells (bridges_count > 0 after init)
        self._island_bridges_z3 = {island.position: {direction: self._model.NewBoolVar(f"{island.position}_{direction}") for direction in Direction.orthogonal_directions()} for island in self._island_grid.islands.values() if island.bridges_count > 0}
        # Neighbors of digits or out-of-set positions cannot connect to them
        for position in [position for position, _ in self.input_grid if position not in self._island_bridges_z3]:
            neighbors = self.input_grid.neighbors_positions(position)
            for neighbor in [neighbor for neighbor in neighbors if neighbor in self._island_bridges_z3]:
                direction = neighbor.direction_to(position)
                self._model.Add(self._island_bridges_z3[neighbor][direction] == 0)

        self._set_walls_around_digit()
        self._black_cells_z3 = {position: self._model.NewBoolVar(f'p{position}') for position, _ in self.input_grid if position in self._island_bridges_z3}
        self._add_constraints()
        self._initialized = True

    @staticmethod
    def _is_feasible(status: CpSolverStatus) -> bool:
        return status in (cp_model.OPTIMAL, cp_model.FEASIBLE)

    def get_solution(self) -> IslandGrid:
        if not self._initialized:
            self._init_solver()

        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        proposition_count = 0
        while self._is_feasible(self._solver.Solve(self._model)):
            proposition_count += 1
            # Read model values into island grid
            for position, direction_bridges in self._island_bridges_z3.items():
                for direction, var in direction_bridges.items():
                    if position.after(direction) not in self._island_bridges_z3:
                        continue
                    bridges_number = self._solver.Value(var)
                    if bridges_number > 0:
                        self._island_grid[position].set_bridge_to_position(self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
                    elif position in self._island_grid and direction in self._island_grid[position].direction_position_bridges:
                        # Ensure we don't keep stale connections
                        self._island_grid[position].direction_position_bridges.pop(direction)
                self._island_grid[position].set_bridges_count_according_to_directions_bridges()

            connected_positions = self._island_grid.get_connected_positions(exclude_without_bridge=True)
            if len(connected_positions) == 1:
                for position, value in [(position, value) for position, value in self.input_grid if value >= 0]:
                    self._island_grid[position] = value
                for position, var in self._black_cells_z3.items():
                    if self._solver.Value(var) == 1:
                        self._island_grid[position] = '■'

                self._previous_solution = self._island_grid
                return self._island_grid, proposition_count

            # Add clause to forbid the current set of segments for each disconnected component (cut at least one)
            for positions in connected_positions:
                literals = []
                for position in positions:
                    for direction, (_, value) in self._island_grid[position].direction_position_bridges.items():
                        if value == 1:
                            literals.append(self._island_bridges_z3[position][direction])
                if literals:
                    # At least one active edge in the component must be turned off
                    self._model.AddBoolOr([lit.Not() for lit in literals])
            self._init_island_grid()

        return IslandGrid.empty(), proposition_count

    def get_other_solution(self):
        # Block the exact previous assignment of bridge variables
        literals = []
        for island in [island for island in self._previous_solution.islands.values() if island.position in self._island_bridges_z3]:
            for direction, (_, value) in island.direction_position_bridges.items():
                var = self._island_bridges_z3[island.position][direction]
                literals.append(var if value == 1 else var.Not())
        if literals:
            self._model.AddBoolOr([lit.Not() for lit in literals])

        self._init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_black_cell_constraints()
        self._add_no_adjacent_black_constraint()
        self._add_opposite_bridges_constraints()
        self._add_bridges_sum_constraints()

    def _add_initial_constraints(self):
        # Border constraints: no edges going outside the grid
        constraints_border_up = [self._model.Add(self._island_bridges_z3[Position(0, c)][Direction.up()] == 0) for c in range(self._island_grid.columns_number) if Position(0, c) in self._island_bridges_z3]
        constraints_border_down = [self._model.Add(self._island_bridges_z3[Position(self._island_grid.rows_number - 1, c)][Direction.down()] == 0) for c in range(self._island_grid.columns_number) if Position(self._island_grid.rows_number - 1, c) in self._island_bridges_z3]
        constraints_border_right = [self._model.Add(self._island_bridges_z3[Position(r, self._island_grid.columns_number - 1)][Direction.right()] == 0) for r in range(self._island_grid.rows_number) if Position(r, self._island_grid.columns_number - 1) in self._island_bridges_z3]
        constraints_border_left = [self._model.Add(self._island_bridges_z3[Position(r, 0)][Direction.left()] == 0) for r in range(self._island_grid.rows_number) if Position(r, 0) in self._island_bridges_z3]
        # The above add constraints directly; lists kept to mimic structure
        _ = constraints_border_up, constraints_border_down, constraints_border_right, constraints_border_left

    def _add_opposite_bridges_constraints(self):
        for island in [island for island in self._island_grid.islands.values() if island.position in self._island_bridges_z3]:
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                position_bridges = island.direction_position_bridges.get(direction)
                if position_bridges is not None:
                    other_position, _ = position_bridges
                    if other_position not in self._island_bridges_z3:
                        continue
                    self._model.Add(self._island_bridges_z3[island.position][direction] == self._island_bridges_z3[other_position][direction.opposite])
                else:
                    self._model.Add(self._island_bridges_z3[island.position][direction] == 0)

    def _add_black_cell_constraints(self):
        for position, blacks_count in [(position, value) for position, value in self.input_grid if value >= 0]:
            neighbors = self.input_grid.neighbors_positions(position)
            vars_list = [self._black_cells_z3[neighbor] for neighbor in neighbors if neighbor in self._island_bridges_z3.keys()]
            if vars_list:
                self._model.Add(sum(vars_list) == blacks_count)
            else:
                # No candidate black cells around the digit; digit must be 0
                self._model.Add(blacks_count == 0)

    def _add_bridges_sum_constraints(self):
        for position in [position for position, value in self.input_grid if value < 0]:
            vars_list = [self._island_bridges_z3[position][direction] for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]]
            s = sum(vars_list)
            black_cell = self._black_cells_z3[position]
            # If black then s == 0
            self._model.Add(s == 0).OnlyEnforceIf(black_cell)
            self._model.Add(s != 0).OnlyEnforceIf(black_cell.Not())
            # If path cell (not black) then s == 2
            self._model.Add(s == 2).OnlyEnforceIf(black_cell.Not())
            self._model.Add(s != 2).OnlyEnforceIf(black_cell)

    def _add_no_adjacent_black_constraint(self):
        for position in [position for position, value in self.input_grid if value < 0]:
            for neighbor_position in self.input_grid.neighbors_positions(position):
                if neighbor_position not in self._island_bridges_z3:
                    continue
                self._model.AddImplication(self._black_cells_z3[position], self._black_cells_z3[neighbor_position].Not())

    def _set_walls_around_digit(self):
        for position in [position for position, value in self.input_grid if value >= 0]:
            neighbors = self.input_grid.neighbors_positions(position)
            for neighbor in [neighbor for neighbor in neighbors if neighbor in self._island_bridges_z3]:
                direction = neighbor.direction_to(position)
                self._model.Add(self._island_bridges_z3[neighbor][direction] == 0)
