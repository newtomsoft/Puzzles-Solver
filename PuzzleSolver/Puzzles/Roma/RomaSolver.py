from ortools.sat.python import cp_model

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class RomaSolver(GameSolver):
    cell_empty = None
    Goal = 'G'
    up = 1
    down = 2
    right = 3
    left = 4

    _value_by_letter = {'↑': up, '↓': down, '→': right, '←': left}
    _letter_by_value = {0: Goal, up: '↑', down: '↓', right: '→', left: '←'}
    _value_by_direction = {
        Direction.up(): up,
        Direction.down(): down,
        Direction.right(): right,
        Direction.left(): left,
    }

    def __init__(self, grid: Grid, regions_grid: Grid):
        super().__init__()
        self._grid = grid
        self._regions = regions_grid.get_regions()
        self._rows_number = grid.rows_number
        self._columns_number = grid.columns_number
        self._model = cp_model.CpModel()
        self._grid_vars = Grid.empty()
        self._rank_vars = Grid.empty()
        self._previous_solution = Grid.empty()
        self._solver_initialized = False

    def _init_solver(self):
        self._grid_vars = Grid(
            [[self._model.new_int_var(0, 4, f'cell_{r}_{c}') for c in range(self._columns_number)] for r in range(self._rows_number)]
        )

        self._rank_vars = Grid(
            [[self._model.new_int_var(0, self._rows_number * self._columns_number, f'rank_{r}_{c}') for c in range(self._columns_number)]
             for r in range(self._rows_number)]
        )

        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver_initialized:
            self._init_solver()
            self._solver_initialized = True

        status = self._solver.solve(self._model)

        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            self._previous_solution = Grid(
                [[self._letter_by_value[self._solver.value(self._grid_vars[r][c])] for c in range(self._columns_number)]
                 for r in range(self._rows_number)]
            )
            return self._previous_solution

        return Grid.empty()

    def get_other_solution(self) -> Grid:
        if self._previous_solution == Grid.empty():
            return self.get_solution()

        bool_vars = []
        for position, _ in self._grid:
            if self._previous_solution[position] == self.Goal:
                continue
            value = self._value_by_letter[self._previous_solution[position]]
            b = self._model.new_bool_var(f'neq_{position.r}_{position.c}')
            self._model.add(self._grid_vars[position] != value).only_enforce_if(b)
            self._model.add(self._grid_vars[position] == value).only_enforce_if(b.negated())
            bool_vars.append(b)

        if not bool_vars:
            return Grid.empty()

        self._model.add_bool_or(bool_vars)
        return self.get_solution()

    def solution_to_string(self) -> str:
        if self._previous_solution == Grid.empty():
            self.get_solution()

        if self._previous_solution == Grid.empty():
            return "No solution found"

        return '\n'.join(' '.join(row) for row in self._previous_solution.matrix)

    def _add_constraints(self):
        self._add_input_constraints()
        self._add_region_constraints()
        self._add_flow_constraints()

    def _add_input_constraints(self):
        for position, value in self._grid:
            if value == self.Goal:
                self._model.add(self._grid_vars[position] == 0)
                self._model.add(self._rank_vars[position] == 0)
            elif value == self.cell_empty:
                self._model.add(self._grid_vars[position] >= 1)
            else:
                self._model.add(self._grid_vars[position] == self._value_by_letter[value])

    def _add_region_constraints(self):
        for positions in self._regions.values():
            arrow_vars = [self._grid_vars[position] for position in positions if self._grid[position] != self.Goal]
            if len(arrow_vars) > 1:
                self._model.add_all_different(arrow_vars)

    def _add_flow_constraints(self):
        for position, _ in self._grid:
            if self._grid[position] == self.Goal:
                continue

            for neighbor_position in position.neighbors():
                value = self._value_by_direction[position.direction_to(neighbor_position)]
                if neighbor_position not in self._grid:
                    self._model.add(self._grid_vars[position] != value)
                    continue

                points_direction = self._model.new_bool_var(f'points_{position.r}_{position.c}_{value}')
                self._model.add(self._grid_vars[position] == value).only_enforce_if(points_direction)
                self._model.add(self._grid_vars[position] != value).only_enforce_if(points_direction.negated())
                self._model.add(self._rank_vars[position] == self._rank_vars[neighbor_position] + 1).only_enforce_if(points_direction)
