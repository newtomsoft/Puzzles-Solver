from z3 import Solver, unsat, Or, Implies, Int, Sum

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class TentsSolver(GameSolver):
    tree_value = -1

    def __init__(self, grid: Grid, tents_numbers_by_column_row):
        self._grid: Grid = grid
        self.tents_numbers_by_column_row: dict[str, list[int]] = tents_numbers_by_column_row
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number < 5:
            raise ValueError("The rows number must be at least 5")
        self.columns_tents_numbers = self.tents_numbers_by_column_row['column']
        self.rows_tents_numbers = self.tents_numbers_by_column_row['row']
        self._solver = Solver()
        self._grid_z3 = None
        self._previous_solution = None

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[Int(f"cell_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        self._previous_solution = self._compute_solution()
        return self.cast_previous_solution_in_bool_matrix()

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return self.get_solution()
        if self._previous_solution.is_empty():
            return Grid.empty()

        constraint = Or([self._grid_z3[Position(i, j)] != self._previous_solution[i, j] for i in range(self.rows_number) for j in range(self.columns_number) if self._grid[Position(i, j)] != self.tree_value])
        self._solver.add(constraint)
        self._previous_solution = self._compute_solution()
        return self.cast_previous_solution_in_bool_matrix()

    def cast_previous_solution_in_bool_matrix(self):
        if self._previous_solution == Grid.empty():
            return Grid.empty()
        return Grid([[bool(self._previous_solution[i, j]) for j in range(self.columns_number)] for i in range(self.rows_number)])

    def _compute_solution(self) -> Grid:
        if self._solver.check() == unsat:
            return Grid.empty()
        model = self._solver.model()
        return Grid([[(model.eval(self._grid_z3.value(i, j))).as_long() if self._grid[Position(i, j)] != self.tree_value else 0 for j in range(self.columns_number)] for i in range(self.rows_number)])

    def _free(self, position: Position):
        return self._grid_z3[position] == 0

    def _not_free(self, position: Position):
        return self._grid_z3[position] > 0

    def _add_constraints(self):
        self._add_id_over_tree_constraint()
        self._add_free_if_no_tree_near_constraint()
        self._add_sum_constraints()
        self._add_no_adjacent_tent_constraint()
        self._add_one_tent_for_each_tree_constraint()

    def _add_sum_constraints(self):
        constraints = []
        for row_index, row in enumerate(self._grid_z3.matrix):
            constraints.append(Sum([cell > 0 for col_index, cell in enumerate(row) if self._grid[Position(row_index, col_index)] != self.tree_value]) == self.rows_tents_numbers[row_index])
        for col_index, column in enumerate(zip(*self._grid_z3.matrix)):
            constraints.append(Sum([cell > 0 for row_index, cell in enumerate(column) if self._grid[Position(row_index, col_index)] != self.tree_value]) == self.columns_tents_numbers[col_index])
        self._solver.add(constraints)

    def _add_free_if_no_tree_near_constraint(self):
        for position in [position for position, value in self._grid if value != self.tree_value]:
            if all(self._grid[neighbor_position] != self.tree_value for neighbor_position in self._grid.neighbors_positions(position)):
                self._solver.add(self._free(position))

    def _add_no_adjacent_tent_constraint(self):
        for position in [position for position, value in self._grid if value != self.tree_value]:
            neighbors_positions = [neighbor_position for neighbor_position in self._grid.neighbors_positions(position, 'diagonal') if self._grid[neighbor_position] != self.tree_value]
            sum_tents_in_neighbors = Sum([self._not_free(neighbor) for neighbor in neighbors_positions])
            self._solver.add(Implies(self._not_free(position), sum_tents_in_neighbors == 0))

    def _add_id_over_tree_constraint(self):
        trees_positions = [position for position, value in self._grid if value == self.tree_value]
        trees_count = len(trees_positions)
        for idx, tree_position in enumerate([position for position, value in self._grid if value != self.tree_value]):
            self._solver.add(self._grid_z3[tree_position] >= 0)
            self._solver.add(self._grid_z3[tree_position] <= trees_count)
        for idx, tree_position in enumerate(trees_positions):
            self._solver.add(self._grid_z3[tree_position] == idx + 1)

    def _add_one_tent_for_each_tree_constraint(self):
        for position in [position for position, value in self._grid if value == self.tree_value]:
            orthogonal_neighbors_positions = self._grid.neighbors_positions(position)
            tree_id = self._grid_z3[position]
            sum_tent_attach_to_tree = Sum([self._grid_z3[neighbor] == tree_id for neighbor in orthogonal_neighbors_positions])
            self._solver.add(sum_tent_attach_to_tree == 1)
