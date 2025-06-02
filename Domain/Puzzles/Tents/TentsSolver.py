from z3 import Solver, Bool, Not, unsat, Or, Implies, is_true, And

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class TentsSolver(GameSolver):
    _tree_value = -1

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
        self._grid_z3 = Grid([[Bool(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return self.get_solution()
        if self._previous_solution.is_empty():
            return Grid.empty()

        constraint = Not(And([self.tent(Position(i, j)) == self._previous_solution[i, j] for i in range(self.rows_number) for j in range(self.columns_number)]))
        self._solver.add(constraint)

        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        if self._solver.check() == unsat:
            return Grid.empty()
        model = self._solver.model()
        return Grid([[(is_true(model.eval(self._grid_z3.value(i, j)))) for j in range(self.columns_number)] for i in range(self.rows_number)])

    def tent(self, position: Position):
        return self._grid_z3[position]

    def free(self, position: Position):
        return Not(self.tent(position))

    def _add_constraints(self):
        self._add_sum_constraints()
        self.add_free_if_no_tent_near_constraint()
        self.add_no_adjacent_tent_constraint()
        self.add_free_over_tree_constraint()
        self.add_one_tent_for_each_tree_constraint()

    def _add_sum_constraints(self):
        constraints = []
        for i, row in enumerate(self._grid_z3.matrix):
            constraints.append(sum(row) == self.rows_tents_numbers[i])
        for i, column in enumerate(zip(*self._grid_z3.matrix)):
            constraints.append(sum(column) == self.columns_tents_numbers[i])
        self._solver.add(constraints)

    def add_free_if_no_tent_near_constraint(self):
        for position, _ in self._grid:
            if all(self._grid[neighbor_position] != TentsSolver._tree_value for neighbor_position in self._grid.neighbors_positions(position)):
                self._solver.add(self.free(position))

    def add_no_adjacent_tent_constraint(self):
        for position, _ in self._grid:
            r, c = position
            if r > 0:
                self._solver.add(Implies(self.tent(position), self.free(position.up)))
                if c > 0:
                    self._solver.add(Implies(self.tent(position), self.free(position.left)))
                    self._solver.add(Implies(self.tent(position), self.free(position.up_left)))
                if c < self.columns_number - 1:
                    self._solver.add(Implies(self.tent(position), self.free(position.right)))
                    self._solver.add(Implies(self.tent(position), self.free(position.up_right)))

            if r < self.rows_number - 1:
                self._solver.add(Implies(self.tent(position), self.free(position.down)))
                if c > 0:
                    self._solver.add(Implies(self.tent(position), self.free(position.left)))
                    self._solver.add(Implies(self.tent(position), self.free(position.down_left)))
                if c < self.columns_number - 1:
                    self._solver.add(Implies(self.tent(position), self.free(position.right)))
                    self._solver.add(Implies(self.tent(position), self.free(position.down_right)))

    def add_free_over_tree_constraint(self):
        for tree_position in [position for position, value in self._grid if value == TentsSolver._tree_value]:
            self._solver.add(self.free(tree_position))

    def add_one_tent_for_each_tree_constraint(self):
        for position in [position for position, value in self._grid if value == TentsSolver._tree_value]:
            neighbors_positions = self._grid.neighbors_positions(position)
            if len(neighbors_positions) > 0:
                self._solver.add(Or([self.tent(position) for position in neighbors_positions]))
