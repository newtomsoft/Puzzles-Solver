from ortools.sat.python import cp_model

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class BuraitoraitoSolver(GameSolver):
    def __init__(self, input_grid: Grid):
        self._input_grid = input_grid
        self.rows_number = input_grid.rows_number
        self.columns_number = input_grid.columns_number
        self._solver = cp_model.CpSolver()
        self._model = None
        self._stars_vars = None
        self._status = None

    def _init_model(self):
        self._model = cp_model.CpModel()
        self._stars_vars = Grid([[self._model.new_bool_var(f'star_{r}_{c}')
                                  for c in range(self.columns_number)]
                                 for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._model is None:
            self._init_model()

        self._status = self._solver.solve(self._model)
        if self._status == cp_model.OPTIMAL or self._status == cp_model.FEASIBLE:
            return self._compute_solution()

        return Grid.empty()

    def get_other_solution(self) -> Grid:
        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return self.get_solution()

        current_vars = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                var = self._stars_vars[r, c]
                if self._solver.boolean_value(var):
                    current_vars.append(var.negated())
                else:
                    current_vars.append(var)

        if current_vars:
            self._model.add_bool_or(current_vars)

        self._status = self._solver.solve(self._model)
        if self._status == cp_model.OPTIMAL or self._status == cp_model.FEASIBLE:
            return self._compute_solution()

        return Grid.empty()

    def _compute_solution(self) -> Grid:
        solution_grid = Grid([[0] * self.columns_number for _ in range(self.rows_number)])
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if self._solver.boolean_value(self._stars_vars[r, c]):
                    solution_grid[r, c] = 1
                else:
                    solution_grid[r, c] = 0
        return solution_grid

    def _add_constraints(self):
        self._add_number_constraints()

    def _add_number_constraints(self):
        for position, number in [(position, number) for position, number in self._input_grid if number > 0]:
            cells_in_sight = self._get_cells_in_sight(position)
            self._model.add(sum(self._stars_vars[cell] for cell in cells_in_sight) == number)

    def _get_cells_in_sight(self, position: Position) -> list[Position]:
        cells = []
        for direction in [Direction.up(), Direction.down(), Direction.left(), Direction.right()]:
            current = position.after(direction, 1)
            while current in self._input_grid:
                if self._input_grid[current] > 0:  # Black cell blocks vision
                    break
                cells.append(current)
                current = current.after(direction, 1)
        return cells
