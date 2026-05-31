from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class CreekSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self.solution_rows_number = self._grid.rows_number - 1
        self.solution_columns_number = self._grid.columns_number - 1
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_vars: Grid | None = None
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._grid_vars = Grid([[self._model.new_bool_var(f"grid_{r}_{c}") for c in range(self.solution_columns_number)] for r in range(self.solution_rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._grid_vars is None:
            self._init_solver()

        status = self._solver.solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()

        solution = Grid([[self._solver.boolean_value(self._grid_vars.value(i, j)) for j in range(self.solution_columns_number)] for i in range(self.solution_rows_number)])
        self._previous_solution = solution
        return solution

    def get_other_solution(self):
        if self._previous_solution is None:
            return self.get_solution()

        terms = [self._grid_vars[position] for position, value in self._previous_solution if not value]
        self._model.add_bool_or(terms)

        return self.get_solution()

    def _add_constraints(self):
        self._add_neighbors_count_constraints()
        self._add_forest_connectivity_constraint()

    def _add_forest_connectivity_constraint(self):
        total_cells = self.solution_rows_number * self.solution_columns_number
        self._rank_vars = Grid([[self._model.new_int_var(0, total_cells - 1, f"rank_{r}_{c}") for c in range(self.solution_columns_number)] for r in range(self.solution_rows_number)])
        is_root_vars = []
        for r in range(self.solution_rows_number):
            for c in range(self.solution_columns_number):
                pos = Position(r, c)
                is_root = self._model.new_bool_var(f"is_root_{r}_{c}")
                is_root_vars.append(is_root)
                is_forest = self._grid_vars[pos].negated()
                self._model.add(is_root <= is_forest)
                self._model.add(self._rank_vars[pos] == 0).OnlyEnforceIf(is_root)
        self._model.add(sum(is_root_vars) == 1)
        for r in range(self.solution_rows_number):
            for c in range(self.solution_columns_number):
                pos = Position(r, c)
                is_forest = self._grid_vars[pos].negated()
                is_root = is_root_vars[r * self.solution_columns_number + c]
                parent_literals = []
                for neighbor in self._grid_vars.neighbors_positions(pos):
                    parent = self._model.new_bool_var(f"parent_{r}_{c}_{neighbor.r}_{neighbor.c}")
                    self._model.add(self._grid_vars[neighbor] == 0).OnlyEnforceIf(parent)
                    self._model.add(self._rank_vars[neighbor] < self._rank_vars[pos]).OnlyEnforceIf(parent)
                    parent_literals.append(parent)
                if parent_literals:
                    self._model.add_bool_or(parent_literals).OnlyEnforceIf([is_forest, is_root.negated()])

    def _add_neighbors_count_constraints(self):
        for position, creek_count in [(position, value) for position, value in self._grid if value != -1]:
            solution_positions = self._get_positions_in_solution_grid(self._grid_vars, position)
            self._model.add(sum([self._grid_vars[solution_position] for solution_position in solution_positions]) == creek_count)

    @staticmethod
    def _get_positions_in_solution_grid(grid: Grid, position: Position) -> set[Position]:
        return {neighbor for neighbor in grid.straddled_neighbors_positions(Position(position.r - 0.5, position.c - 0.5))}
