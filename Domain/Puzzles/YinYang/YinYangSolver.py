from typing import Set

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Ports.SolverEngine import SolverEngine
from GameSolver import GameSolver
from Utils.ShapeGenerator import ShapeGenerator

FALSE = False


class YinYangSolver(GameSolver):
    def __init__(self, grid: Grid, solver_engine: SolverEngine):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number < 6:
            raise ValueError("Yin Yang grid must be at least 6x6")
        self._solver = solver_engine
        self._grid_z3: Grid | None = None
        self._previous_solution = None
        self.edge_positions_processed: Set[Position] = set()

    def _init_solver(self):
        self._grid_z3 = Grid([[self._solver.bool(f"matrix_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.has_constraints():
            self._init_solver()

        solution, _ = self._get_solution_when_all_yin_yang_connected()
        self._previous_solution = solution
        return solution

    def _get_solution_when_all_yin_yang_connected(self):
        proposition_count = 0
        while self._solver.has_solution():
            model = self._solver.model()
            proposition_count += 1
            current_grid = Grid([[self._solver.is_true(model.eval(self._grid_z3[Position(r, c)])) for c in range(self.columns_number)] for r in range(self.rows_number)])

            black_shapes = current_grid.get_all_shapes(False)
            white_shapes = current_grid.get_all_shapes(True)
            if len(black_shapes) == 1 and len(white_shapes) == 1:
                self._previous_solution = current_grid
                return current_grid, proposition_count

            self._add_edges_values_constraints(current_grid)
            self._exclude_isolated_shapes(black_shapes, False)
            self._exclude_isolated_shapes(white_shapes, True)

        return Grid.empty(), proposition_count

    def _exclude_isolated_shapes(self, shapes, shape_value):
        for shape in shapes:
            shape_all_value = self._solver.And([self._grid_z3[position] == shape_value for position in shape])
            around_shape = ShapeGenerator.around_shape(shape)
            around_all_not_value = self._solver.And([self._grid_z3[Position(r, c)] != shape_value for r, c in around_shape if Position(r, c) in self._grid_z3])
            constraint = self._solver.Not(self._solver.And(shape_all_value, around_all_not_value))
            self._solver.add(constraint)

    def get_other_solution(self):
        exclusion_constraint = self._solver.Not(
            self._solver.And([self._grid_z3[Position(r, c)] == self._previous_solution[Position(r, c)] for r in range(self.rows_number) for c in range(self.columns_number)]))
        self._solver.add(exclusion_constraint)
        return self.get_solution()

    def _add_constraints(self):
        self._initial_constraints()
        self.add_no_square_constraints()
        self._add_no_diagonal_2_cells_isolated_constraints()
        self._add_min_2_connected_cells_constraints()

    def _initial_constraints(self):
        self._add_initial_values__constraints()
        self._add_edges_initial_values_constraints()

    def _add_initial_values__constraints(self):
        for position, value in self._grid:
            if value == 0:
                self._solver.add(self._grid_z3[position] == FALSE)
                continue
            if value == 1:
                self._solver.add(self._grid_z3[position])
                continue

    def add_no_square_constraints(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                self._solver.add(self._solver.Not(self._solver.And(self._grid_z3[r][c] == FALSE, self._grid_z3[r + 1][c] == FALSE, self._grid_z3[r][c + 1] == FALSE, self._grid_z3[r + 1][c + 1] == FALSE)))
                self._solver.add(self._solver.Not(self._solver.And(self._grid_z3[r][c], self._grid_z3[r + 1][c], self._grid_z3[r][c + 1], self._grid_z3[r + 1][c + 1])))

    def _add_no_diagonal_2_cells_isolated_constraints(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                for bool_value in [False, True]:
                    if0 = self._solver.And(self._grid_z3[r][c] == bool_value, self._grid_z3[r + 1][c + 1] == bool_value)
                    then0 = self._solver.Or(self._grid_z3[r + 1][c] == bool_value, self._grid_z3[r][c + 1] == bool_value)
                    self._solver.add(self._solver.Implies(if0, then0))

                    if1 = self._solver.And(self._grid_z3[r][c + 1] == bool_value, self._grid_z3[r + 1][c] == bool_value)
                    then1 = self._solver.Or(self._grid_z3[r + 1][c + 1] == bool_value, self._grid_z3[r][c] == bool_value)
                    self._solver.add(self._solver.Implies(if1, then1))

    def _add_min_2_connected_cells_constraints(self):
        for position, value in self._grid_z3:
            self._solver.add(self._solver.Or([self._grid_z3[position] == value for position in self._grid_z3.neighbors_positions(position)]))

    def _add_edges_initial_values_constraints(self):
        known_edges_positions_values = []
        for position, value in [(position, bool(self._grid[position])) for position in self._grid.edges_positions() if type(self._grid[position]) is int]:
            known_edges_positions_values.append((position, value))

        self._add_computed_edges_values_constraints(known_edges_positions_values)

    def _add_edges_values_constraints(self, grid: Grid):
        known_edges_positions_values = []
        for position, value in [(position, grid[position]) for position in grid.edges_positions() if type(grid[position]) is bool]:
            if position in self.edge_positions_processed:
                known_edges_positions_values.append((position, value))
            else:
                self._solver.push()
                self._solver.add(self._grid_z3[position] != value)
                has_solution = self._solver.has_solution()
                if not has_solution:
                    known_edges_positions_values.append((position, value))
                self._solver.pop()

        self._add_computed_edges_values_constraints(known_edges_positions_values)

    def _add_computed_edges_values_constraints(self, positions_values):
        white_count = sum(1 for _, value in positions_values if value is True)
        black_count = sum(1 for _, value in positions_values if value is False)
        if white_count <= 1 and black_count <= 1 or white_count == 0 or black_count == 0:
            return

        array_fixed_edges = [(self._get_position_from_edge_index(index), None) for index in range((2 * (self.rows_number + self.columns_number) - 4))]
        for position, value in positions_values:
            index = self._clockwise_key((position, 0))
            array_fixed_edges[index] = (position, value)
        array_fixed_edges = self.fill_between_equals(array_fixed_edges)
        for position, value in [(position, value) for position, value in array_fixed_edges if value is not None and position not in self.edge_positions_processed]:
            self._solver.add(self._grid_z3[position] == value)
            self.edge_positions_processed.add(position)

    @staticmethod
    def fill_between_equals(list_to_fill: list[tuple[Position, bool | None]]) -> list[tuple[Position, bool | None]]:
        n = len(list_to_fill)
        result = list_to_fill.copy()

        for i in range(n):
            if result[i][1] is None:
                left_idx = (i - 1) % n
                while left_idx != i and result[left_idx][1] is None:
                    left_idx = (left_idx - 1) % n

                right_idx = (i + 1) % n
                while right_idx != i and result[right_idx][1] is None:
                    right_idx = (right_idx + 1) % n

                if result[left_idx][1] is not None and result[left_idx][1] == result[right_idx][1]:
                    result[i] = (result[i][0], result[left_idx][1])

        return result

    def _clockwise_key(self, pos_val) -> int:
        position, _ = pos_val
        if position.r == 0:
            return position.c
        if position.c == self.columns_number - 1:
            return self.columns_number + position.r - 1
        if position.r == self.rows_number - 1:
            return self.columns_number + self.rows_number - 1 + (self.columns_number - 1 - position.c)
        return 2 * self.columns_number + self.rows_number - 3 + (self.rows_number - 1 - position.r)

    def _get_position_from_edge_index(self, index):
        total_edges = 2 * (self.rows_number + self.columns_number) - 4
        index = index % total_edges
        if index < self.columns_number:
            return Position(0, index)
        elif index < self.columns_number + self.rows_number - 1:
            return Position(index - self.columns_number + 1, self.columns_number - 1)
        elif index < 2 * self.columns_number + self.rows_number - 2:
            bottom_index = index - (self.columns_number + self.rows_number - 1)
            column = self.columns_number - 2 - bottom_index
            return Position(self.rows_number - 1, column)
        else:
            left_index = index - (2 * self.columns_number + self.rows_number - 2)
            row = self.rows_number - 2 - left_index
            return Position(row, 0)
