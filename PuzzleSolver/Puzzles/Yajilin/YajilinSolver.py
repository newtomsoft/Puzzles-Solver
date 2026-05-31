from typing import Dict

from ortools.sat.python import cp_model

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Island import Island
from PuzzleSolver.Board.IslandsGrid import IslandGrid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


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
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._island_bridges_vars: Dict[Position, Dict[Direction, cp_model.IntVar]] = {}
        self._black_cells_vars: Dict[Position, cp_model.IntVar] = {}
        self._previous_solution: IslandGrid | None = None

    def _init_island_grid(self):
        self._island_grid = IslandGrid([[Island(Position(r, c), 2) for c in range(self.input_grid.columns_number)] for r in range(self.input_grid.rows_number)])
        for position, value in self.input_grid:
            if value != '':
                for neighbor in position.neighbors():
                    self._island_grid[position].set_bridge_to_position(neighbor, 0)
                self._island_grid[position].set_bridges_count_according_to_directions_bridges()
                for neighbor in position.neighbors():
                    if neighbor in self._island_grid:
                        self._island_grid[neighbor].set_bridge_to_position(position, 0)

    def _init_solver(self):
        self._island_bridges_vars = {pos: {direction: self._model.new_bool_var(f"bridge_{pos}_{direction}")
                                           for direction in Direction.orthogonal_directions()}
                                     for pos, _ in self.input_grid if self._island_grid[pos].bridges_count > 0}

        for pos, value in self.input_grid:
            if pos not in self._island_bridges_vars:
                for neighbor in pos.neighbors():
                    if neighbor in self._island_bridges_vars:
                        direction = neighbor.direction_to(pos)
                        self._model.add(self._island_bridges_vars[neighbor][direction] == 0)

        self._black_cells_vars = {pos: self._model.new_bool_var(f"black_{pos}")
                                  for pos, _ in self.input_grid if pos in self._island_bridges_vars}
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if not self._island_bridges_vars:
            self._init_solver()
        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        proposition_count = 0
        while self._solver.solve(self._model) in [cp_model.FEASIBLE, cp_model.OPTIMAL]:
            proposition_count += 1
            for position, direction_vars in self._island_bridges_vars.items():
                for direction, var in direction_vars.items():
                    if position.after(direction) in self._island_bridges_vars:
                        self._island_grid[position].set_bridge_to_position(position.after(direction), self._solver.value(var))
                self._island_grid[position].set_bridges_count_according_to_directions_bridges()

            connected_positions = self._island_grid.get_connected_positions(exclude_without_bridge=True)
            if len(connected_positions) <= 1:
                for position, value in self.input_grid:
                    if value != '':
                        self._island_grid.set_value(position, value)
                    elif position in self._black_cells_vars:
                        if self._solver.value(self._black_cells_vars[position]):
                            self._island_grid.set_value(position, '■')

                self._previous_solution = self._island_grid
                return self._island_grid, proposition_count

            for positions in connected_positions:
                cell_constraints = []
                for position in positions:
                    for direction, var in self._island_bridges_vars[position].items():
                        val = self._solver.value(var)
                        if val == 1:
                            cell_constraints.append(var.negated())
                        else:
                            cell_constraints.append(var)
                self._model.add_bool_or(cell_constraints)

            self._init_island_grid()

        return IslandGrid.empty(), proposition_count

    def get_other_solution(self):
        constraints = []
        for pos, direction_vars in self._island_bridges_vars.items():
            for direction, var in direction_vars.items():
                val = self._solver.value(var)
                if val == 1:
                    constraints.append(var.negated())
                else:
                    constraints.append(var)
        self._model.add_bool_or(constraints)

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
        # Initial constraints for bridges values (0 or 1) are already set in _init_solver
        # Border constraints
        for pos, direction_vars in self._island_bridges_vars.items():
            for direction, var in direction_vars.items():
                if pos.after(direction) not in self._island_bridges_vars:
                    self._model.add(var == 0)

    def _add_opposite_bridges_constraints(self):
        for pos, direction_vars in self._island_bridges_vars.items():
            for direction, var in direction_vars.items():
                neighbor = pos.after(direction)
                if neighbor in self._island_bridges_vars:
                    self._model.add(var == self._island_bridges_vars[neighbor][direction.opposite])
                else:
                    self._model.add(var == 0)

    def _add_black_cell_constraints(self):
        for position, value in self.input_grid:
            if value == '':
                continue
            blacks_count = int(value[0])
            direction = YajilinSolver.direction_map[value[1]]
            concerned_positions = self.input_grid.all_positions_in_direction(position, direction)
            self._model.add(sum([self._black_cells_vars[pos] for pos in concerned_positions if
                                  pos in self._black_cells_vars]) == blacks_count)

    def _add_bridges_sum_constraints(self):
        for position, value in self.input_grid:
            if value != '':
                continue
            bridges_sum = sum(self._island_bridges_vars[position].values())
            black_cell = self._black_cells_vars[position]

            self._model.add(bridges_sum == 0).only_enforce_if(black_cell)
            self._model.add(bridges_sum == 2).only_enforce_if(black_cell.negated())

    def _add_no_adjacent_black_constraint(self):
        for position, value in self.input_grid:
            if value != '':
                continue
            for neighbor_position in self.input_grid.neighbors_positions(position):
                if neighbor_position in self._black_cells_vars:
                    self._model.add_bool_or([self._black_cells_vars[position].negated(), self._black_cells_vars[neighbor_position].negated()])

    def _add_walls_around_digit_constraints(self):
        for position, value in self.input_grid:
            if value == '':
                continue
            for neighbor in self.input_grid.neighbors_positions(position):
                if neighbor in self._island_bridges_vars:
                    direction = neighbor.direction_to(position)
                    self._model.add(self._island_bridges_vars[neighbor][direction] == 0)
