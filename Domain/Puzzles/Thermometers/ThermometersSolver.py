from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class ThermometersSolver(GameSolver):
    l1 = '─'
    l2 = '│'
    c1 = '┌'
    c2 = '┐'
    c3 = '┘'
    c4 = '└'
    s1 = '├'
    s2 = '┬'
    s3 = '┤'
    s4 = '┴'
    next_direction = {
        's1': Direction.right(),
        's2': Direction.down(),
        's3': Direction.left(),
        's4': Direction.up(),

        ('s1', 'c2'): Direction.down(),
        ('s1', 'c3'): Direction.up(),
        ('s1', 'l1'): Direction.right(),
        ('s1', 'e3'): Direction.none(),
        ('s2', 'c3'): Direction.left(),
        ('s2', 'c4'): Direction.right(),
        ('s2', 'l2'): Direction.down(),
        ('s2', 'e4'): Direction.none(),
        ('s3', 'c1'): Direction.down(),
        ('s3', 'c4'): Direction.up(),
        ('s3', 'l1'): Direction.left(),
        ('s3', 'e1'): Direction.none(),
        ('s4', 'c1'): Direction.right(),
        ('s4', 'c2'): Direction.left(),
        ('s4', 'l2'): Direction.up(),
        ('s4', 'e2'): Direction.none(),
        ('c1', 'l1'): Direction.right(),
        ('c1', 'l2'): Direction.down(),
        ('c1', 'c2'): Direction.down(),
        ('c1', 'c4'): Direction.right(),
        ('c1', 'e3'): Direction.none(),
        ('c1', 'e4'): Direction.none(),
        ('c2', 'l1'): Direction.left(),
        ('c2', 'l2'): Direction.down(),
        ('c2', 'c1'): Direction.down(),
        ('c2', 'c3'): Direction.left(),
        ('c2', 'e4'): Direction.none(),
        ('c2', 'e1'): Direction.none(),
        ('c3', 'l1'): Direction.left(),
        ('c3', 'l2'): Direction.up(),
        ('c3', 'c2'): Direction.left(),
        ('c3', 'c4'): Direction.up(),
        ('c3', 'e1'): Direction.none(),
        ('c3', 'e2'): Direction.none(),
        ('c4', 'l1'): Direction.right(),
        ('c4', 'l2'): Direction.up(),
        ('c4', 'c1'): Direction.right(),
        ('c4', 'c3'): Direction.up(),
        ('c4', 'e2'): Direction.none(),
        ('c4', 'e3'): Direction.none(),
        ('l1', 'c1'): Direction.down(),
        ('l1', 'c2'): Direction.down(),
        ('l1', 'c3'): Direction.up(),
        ('l1', 'c4'): Direction.up(),
        ('l1', 'e1'): Direction.none(),
        ('l1', 'e3'): Direction.none(),
        ('l2', 'c1'): Direction.right(),
        ('l2', 'c2'): Direction.left(),
        ('l2', 'c3'): Direction.left(),
        ('l2', 'c4'): Direction.right(),
        ('l2', 'e2'): Direction.none(),
        ('l2', 'e4'): Direction.none(),
    }

    def __init__(self, grid: Grid, full_by_column_row):
        self._grid: Grid = grid
        self.full_numbers_by_column_row: dict[str, list[int]] = full_by_column_row
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 4:
            raise ValueError("The grid must be at least 4x4")
        self.columns_full_numbers = self.full_numbers_by_column_row['column']
        self.rows_full_numbers = self.full_numbers_by_column_row['row']

        self._model = None
        self._matrix_ortools = None
        self._grid_ortools = None
        self._previous_solution_grid = None

        self._thermometers_positions = self._compute_thermometers_positions()

    def _init_solver(self):
        self._model = cp_model.CpModel()
        self._matrix_ortools = [[self._model.NewBoolVar(f"t_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)]
        self._grid_ortools = Grid(self._matrix_ortools)
        self._add_constraints()

    def get_solution(self) -> Grid | None:
        if self._model is None:
            self._init_solver()

        solver = cp_model.CpSolver()
        status = solver.Solve(self._model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            grid_data = [[solver.Value(self._matrix_ortools[r][c]) == 1 for c in range(self.columns_number)] for r in range(self.rows_number)]
            grid = Grid(grid_data)
            self._previous_solution_grid = grid
            return grid

        return Grid.empty()

    def get_other_solution(self):
        if self._previous_solution_grid is None:
            return self.get_solution()

        self._exclude_solution(self._previous_solution_grid)
        return self.get_solution()

    def _exclude_solution(self, solution_grid: Grid):
        literals = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                val = solution_grid.value(r, c)
                var = self._matrix_ortools[r][c]
                if val:
                    literals.append(var.Not())
                else:
                    literals.append(var)
        self._model.AddBoolOr(literals)

    def _add_constraints(self):
        self._add_sum_constraints()
        self._add_thermometers_constraints()

    def _add_sum_constraints(self):
        for i, row in enumerate(self._grid_ortools.matrix):
            self._model.Add(sum(row) == self.rows_full_numbers[i])
        for i, column in enumerate(zip(*self._grid_ortools.matrix)):
            self._model.Add(sum(column) == self.columns_full_numbers[i])

    def _add_thermometers_constraints(self):
        for positions in self._thermometers_positions:
            self._add_thermometer_constraint(positions)

    def _add_thermometer_constraint(self, positions):
        # In a thermometer, if a cell is filled, all previous cells (closer to the bulb) must be filled.
        # Implies: positions[i] (filled) => positions[i-1] (filled)
        # Or: positions[i-1] >= positions[i]
        for i in range(1, len(positions)):
            prev_pos = positions[i-1]
            curr_pos = positions[i]
            # If current is true, previous must be true.
            # If previous is false, current must be false.
            # So prev >= curr
            self._model.Add(self._grid_ortools[prev_pos] >= self._grid_ortools[curr_pos])

    def _compute_thermometers_positions(self):
        thermometer_positions = []
        for position, value in self._grid:
            if value in ('s1', 's2', 's3', 's4'):
                thermometer_positions.append(self._compute_single_thermometer_positions(position, value))
        return thermometer_positions

    def _compute_single_thermometer_positions(self, first_position: Position, value):
        second_position = first_position.after(self.next_direction[value])
        thermometer_positions = [first_position, second_position]
        while True:
            current_position = thermometer_positions[-1]
            current_value = self._grid[current_position]
            previous_position = thermometer_positions[-2]
            previous_value = self._grid[previous_position]
            if previous_value == 'l1' and current_value == 'l1':
                direction = previous_position.direction_to(current_position)
                thermometer_positions.append(current_position.after(direction))
                continue
            if previous_value == 'l2' and current_value == 'l2':
                direction = previous_position.direction_to(current_position)
                thermometer_positions.append(current_position.after(direction))
                continue
            if previous_value == 'c1' and current_value == 'c3':
                direction = previous_position.direction_to(current_position)
                thermometer_positions.append(current_position.after(Direction.up()) if direction == Direction.right() else current_position.after(Direction.left()))
                continue
            if previous_value == 'c2' and current_value == 'c4':
                direction = previous_position.direction_to(current_position)
                thermometer_positions.append(current_position.after(Direction.up()) if direction == Direction.left() else current_position.after(Direction.right()))
                continue
            if previous_value == 'c3' and current_value == 'c1':
                direction = previous_position.direction_to(current_position)
                thermometer_positions.append(current_position.after(Direction.down()) if direction == Direction.left() else current_position.after(Direction.right()))
                continue
            if previous_value == 'c4' and current_value == 'c2':
                direction = previous_position.direction_to(current_position)
                thermometer_positions.append(current_position.after(Direction.down()) if direction == Direction.right() else current_position.after(Direction.left()))
                continue

            key = (previous_value, current_value)
            if key in self.next_direction:
                next_position = current_position.after(self.next_direction[key])
                if next_position == current_position:
                    break
                thermometer_positions.append(next_position)
            else:
                break
        return thermometer_positions
