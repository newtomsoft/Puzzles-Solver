from ortools.sat.python import cp_model

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
        self._model = None
        self._solver = cp_model.CpSolver()
        self._tent_vars = None
        self._tree_match_vars: dict[Position, dict[Position, cp_model.BoolVarT]] = {}
        self._status = None
        self._previous_solution = None

    def _init_model(self):
        self._model = cp_model.CpModel()
        self._tent_vars = Grid([
            [self._model.new_bool_var(f"tent_{r}_{c}") if self._grid[Position(r, c)] != self.tree_value else None
             for c in range(self.columns_number)]
            for r in range(self.rows_number)
        ])
        self._tree_match_vars = {}
        for tree_pos in [pos for pos, val in self._grid if val == self.tree_value]:
            self._tree_match_vars[tree_pos] = {}
            for neighbor in self._grid.neighbors_positions(tree_pos):
                if self._grid[neighbor] != self.tree_value:
                    self._tree_match_vars[tree_pos][neighbor] = self._model.new_bool_var(
                        f"match_{tree_pos.r}_{tree_pos.c}_{neighbor.r}_{neighbor.c}"
                    )
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._model is None:
            self._init_model()

        self._status = self._solver.solve(self._model)

        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return Grid.empty()

        self._previous_solution = self._compute_solution()
        return self.cast_previous_solution_in_bool_matrix()

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return self.get_solution()
        if self._previous_solution.is_empty():
            return Grid.empty()

        prev = self._previous_solution
        diff_vars = []
        for i in range(self.rows_number):
            for j in range(self.columns_number):
                if self._grid[Position(i, j)] != self.tree_value:
                    diff = self._model.new_bool_var(f"diff_{i}_{j}")
                    self._model.add(self._tent_vars[Position(i, j)] != prev[i, j]).only_enforce_if(diff)
                    self._model.add(self._tent_vars[Position(i, j)] == prev[i, j]).only_enforce_if(diff.negated())
                    diff_vars.append(diff)
        self._model.add(sum(diff_vars) >= 1)

        self._status = self._solver.solve(self._model)

        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return Grid.empty()

        self._previous_solution = self._compute_solution()
        return self.cast_previous_solution_in_bool_matrix()

    def cast_previous_solution_in_bool_matrix(self):
        if self._previous_solution == Grid.empty():
            return Grid.empty()
        return Grid([[bool(self._previous_solution[i, j]) for j in range(self.columns_number)] for i in range(self.rows_number)])

    def _compute_solution(self) -> Grid:
        return Grid([
            [self._solver.value(self._tent_vars[Position(i, j)]) if self._grid[Position(i, j)] != self.tree_value else 0
             for j in range(self.columns_number)]
            for i in range(self.rows_number)
        ])

    def _add_constraints(self):
        self._add_free_if_no_tree_near_constraint()
        self._add_sum_constraints()
        self._add_no_adjacent_tent_constraint()
        self._add_one_tent_for_each_tree_constraint()

    def _add_sum_constraints(self):
        for row_index in range(self.rows_number):
            if self.rows_tents_numbers[row_index] == self.cell_empty:
                continue
            tents_in_row = [self._tent_vars[Position(row_index, c)] for c in range(self.columns_number) if self._grid[Position(row_index, c)] != self.tree_value]
            self._model.add(sum(tents_in_row) == self.rows_tents_numbers[row_index])
        for col_index in range(self.columns_number):
            if self.columns_tents_numbers[col_index] == self.cell_empty:
                continue
            tents_in_col = [self._tent_vars[Position(r, col_index)] for r in range(self.rows_number) if self._grid[Position(r, col_index)] != self.tree_value]
            self._model.add(sum(tents_in_col) == self.columns_tents_numbers[col_index])

    def _add_free_if_no_tree_near_constraint(self):
        for position in [position for position, value in self._grid if value != self.tree_value]:
            if all(self._grid[neighbor] != self.tree_value for neighbor in self._grid.neighbors_positions(position)):
                self._model.add(self._tent_vars[position] == 0)

    def _add_no_adjacent_tent_constraint(self):
        for position in [position for position, value in self._grid if value != self.tree_value]:
            neighbors = [neighbor for neighbor in self._grid.neighbors_positions(position, 'diagonal') if self._grid[neighbor] != self.tree_value]
            for neighbor in neighbors:
                self._model.add_bool_or(self._tent_vars[position].negated(), self._tent_vars[neighbor].negated())

    def _add_one_tent_for_each_tree_constraint(self):
        for tree_pos, match_dict in self._tree_match_vars.items():
            self._model.add(sum(match_dict.values()) == 1)

        for position in [pos for pos, val in self._grid if val != self.tree_value]:
            adjacent_trees = [tree_pos for tree_pos, neighbor_dict in self._tree_match_vars.items() if position in neighbor_dict]
            if not adjacent_trees:
                self._model.add(self._tent_vars[position] == 0)
                continue
            match_vars_for_cell = [self._tree_match_vars[tree_pos][position] for tree_pos in adjacent_trees]
            self._model.add(sum(match_vars_for_cell) == 1).only_enforce_if(self._tent_vars[position])
            self._model.add(sum(match_vars_for_cell) == 0).only_enforce_if(self._tent_vars[position].negated())
