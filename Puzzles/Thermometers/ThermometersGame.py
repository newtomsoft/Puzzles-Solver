from z3 import Bool, Solver, Not, sat, is_true, Sum, Implies, Or, And

from Utils.Direction import Direction
from Utils.Grid import Grid
from Utils.Position import Position


class ThermometersGame:
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
        's1': Direction.RIGHT,
        's2': Direction.DOWN,
        's3': Direction.LEFT,
        's4': Direction.UP,

        ('s1', 'c2'): Direction.DOWN,
        ('s1', 'c3'): Direction.UP,
        ('s1', 'l1'): Direction.RIGHT,
        ('s1', 'e3'): Direction.NONE,
        ('s2', 'c3'): Direction.LEFT,
        ('s2', 'c4'): Direction.RIGHT,
        ('s2', 'l2'): Direction.DOWN,
        ('s2', 'e4'): Direction.NONE,
        ('s3', 'c1'): Direction.DOWN,
        ('s3', 'c4'): Direction.UP,
        ('s3', 'l1'): Direction.LEFT,
        ('s3', 'e1'): Direction.NONE,
        ('s4', 'c1'): Direction.RIGHT,
        ('s4', 'c2'): Direction.LEFT,
        ('s4', 'l2'): Direction.UP,
        ('s4', 'e2'): Direction.NONE,
        ('c1', 'l1'): Direction.RIGHT,
        ('c1', 'l2'): Direction.DOWN,
        ('c1', 'c4'): Direction.RIGHT,
        ('c1', 'e3'): Direction.NONE,
        ('c1', 'e4'): Direction.NONE,
        ('c2', 'l1'): Direction.LEFT,
        ('c2', 'l2'): Direction.DOWN,
        ('c2', 'c3'): Direction.LEFT,
        ('c2', 'e4'): Direction.NONE,
        ('c2', 'e1'): Direction.NONE,
        ('c3', 'l1'): Direction.LEFT,
        ('c3', 'l2'): Direction.UP,
        ('c3', 'c2'): Direction.LEFT,
        ('c3', 'e1'): Direction.NONE,
        ('c3', 'e2'): Direction.NONE,
        ('c4', 'l1'): Direction.RIGHT,
        ('c4', 'l2'): Direction.UP,
        ('c4', 'c1'): Direction.RIGHT,
        ('c4', 'c3'): Direction.UP,
        ('c4', 'e2'): Direction.NONE,
        ('c4', 'e3'): Direction.NONE,
        ('l1', 'c1'): Direction.DOWN,
        ('l1', 'c2'): Direction.DOWN,
        ('l1', 'c3'): Direction.UP,
        ('l1', 'c4'): Direction.UP,
        ('l1', 'e1'): Direction.NONE,
        ('l1', 'e3'): Direction.NONE,
        ('l2', 'c1'): Direction.RIGHT,
        ('l2', 'c2'): Direction.LEFT,
        ('l2', 'c3'): Direction.LEFT,
        ('l2', 'c4'): Direction.RIGHT,
        ('l2', 'e2'): Direction.NONE,
        ('l2', 'e4'): Direction.NONE,
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
        self._solver = None
        self._grid_z3 = None
        self._last_solution_grid = None
        self.thermometers = []

    def _init_solver(self):
        self._matrix_z3 = [[Bool(f"t_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)]
        self._grid_z3 = Grid(self._matrix_z3)
        self._solver = Solver()
        self._compute_thermometers()
        self._add_constraints()

    def get_solution(self) -> Grid | None:
        if self._solver is None:
            self._init_solver()
        if self._solver.check() != sat:
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[is_true(model.eval(self.thermometer(Position(i, j)))) for j in range(self.columns_number)] for i in range(self.rows_number)])
        self._last_solution_grid = grid
        return grid

    def get_other_solution(self):
        self._exclude_solution(self._last_solution_grid)
        solution = self.get_solution()
        return solution

    def _exclude_solution(self, solution_grid: Grid):
        exclude_constraint = Not(And([self._matrix_z3[r][c] == solution_grid.value(r, c) for r in range(self.rows_number) for c in range(self.columns_number) if solution_grid.value(r, c)]))
        self._solver.add(exclude_constraint)

    def thermometer(self, position: Position):
        return self._grid_z3[position]

    def _add_constraints(self):
        self._add_sum_constraints()
        self._add_thermometers_constraints()

    def _add_sum_constraints(self):
        constraints = []
        for i, row in enumerate(self._grid_z3.matrix):
            constraints.append(Sum(row) == self.rows_full_numbers[i])
        for i, column in enumerate(zip(*self._grid_z3.matrix)):
            constraints.append(Sum(column) == self.columns_full_numbers[i])
        self._solver.add(constraints)

    def _add_thermometers_constraints(self):
        for thermometer in self.thermometers:
            self._add_thermometer_constraint(thermometer)

    def _add_thermometer_constraint(self, thermometer):
        for i, position in enumerate(thermometer):
            if i == 0:
                continue
            self._solver.add(Implies(self.thermometer(position), And([self.thermometer(p) for p in thermometer[:i]])))

    def _compute_thermometers(self):
        for position, value in self._grid:
            if value == 's1' or value == 's2' or value == 's3' or value == 's4':
                self._compute_thermometer(position, value)

    def _compute_thermometer(self, first_position: Position, value):
        second_position = first_position.next(self.next_direction[value])
        thermometer_positions = [first_position, second_position]
        while True:
            current_position = thermometer_positions[-1]
            current_value = self._grid[current_position]
            previous_position = thermometer_positions[-2]
            previous_value = self._grid[previous_position]
            if previous_value == 'l1' and current_value == 'l1':
                direction = previous_position.direction_to(current_position)
                thermometer_positions.append(current_position.next(direction))
                continue
            if previous_value == 'l2' and current_value == 'l2':
                direction = previous_position.direction_to(current_position)
                thermometer_positions.append(current_position.next(direction))
                continue
            if previous_value == 'c1' and current_value == 'c3':
                direction = previous_position.direction_to(current_position)
                thermometer_positions.append(current_position.next(Direction.UP) if direction == Direction.RIGHT else current_position.next(Direction.LEFT))
                break
            if previous_value == 'c2' and current_value == 'c4':
                direction = previous_position.direction_to(current_position)
                thermometer_positions.append(current_position.next(Direction.UP) if direction == Direction.LEFT else current_position.next(Direction.RIGHT))
                break
            if previous_value == 'c3' and current_value == 'c1':
                direction = previous_position.direction_to(current_position)
                thermometer_positions.append(current_position.next(Direction.DOWN) if direction == Direction.LEFT else current_position.next(Direction.RIGHT))
                break
            if previous_value == 'c4' and current_value == 'c2':
                direction = previous_position.direction_to(current_position)
                thermometer_positions.append(current_position.next(Direction.DOWN) if direction == Direction.RIGHT else current_position.next(Direction.LEFT))
                break
            next_position = current_position.next(self.next_direction[(previous_value, current_value)])
            if next_position == current_position:
                break
            thermometer_positions.append(next_position)
        self.thermometers.append(thermometer_positions)


