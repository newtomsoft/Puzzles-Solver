from ortools.sat.python import cp_model
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver

class SutoretoSolver(GameSolver):
    def __init__(self, numbers_grid: Grid[int], blacks_grid: Grid[bool]):
        super().__init__()
        self._numbers_grid = numbers_grid
        self._blacks_grid = blacks_grid
        self._rows_number = self._numbers_grid.rows_number
        self._columns_number = self._numbers_grid.columns_number
        self._max_val = max(9, self._rows_number, self._columns_number)
        self._model = cp_model.CpModel()
        self._vars = [[None for _ in range(self._columns_number)] for _ in range(self._rows_number)]
        self._initialize_vars()

    def _initialize_vars(self):
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                if self._blacks_grid.value(r, c) and self._numbers_grid.value(r, c) == 0:
                    self._vars[r][c] = self._model.new_constant(0)
                else:
                    self._vars[r][c] = self._model.new_int_var(1, self._max_val, f'cell_{r}_{c}')
                    val = self._numbers_grid.value(r, c)
                    if val != 0:
                        self._model.add(self._vars[r][c] == val)

    def get_solution(self) -> tuple[Grid, Grid]:
        self._add_constraints()
        return self._solve()

    def _solve(self) -> tuple[Grid, Grid]:
        status = self._solver.solve(self._model)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            matrix = [[self._solver.value(self._vars[r][c]) for c in range(self._columns_number)] for r in range(self._rows_number)]
            self._last_solution_matrix = matrix
            blank_grid = Grid([[False for c in range(self._columns_number)] for r in range(self._rows_number)])
            for r in range(self._rows_number):
                for c in range(self._columns_number):
                    if self._numbers_grid.value(r, c) == 0 and not self._blacks_grid.value(r, c):
                        blank_grid.set_value(Position(r, c), True)
            return Grid(matrix), blank_grid
        return Grid.empty(), Grid.empty()

    def get_other_solution(self) -> tuple[Grid, Grid]:
        if not hasattr(self, '_last_solution_matrix'):
            return self.get_solution()

        literals = []
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                if not (self._blacks_grid.value(r, c) and self._numbers_grid.value(r, c) == 0):
                    diff_var = self._model.new_bool_var(f'diff_{r}_{c}_{len(literals)}')
                    self._model.add(self._vars[r][c] != self._last_solution_matrix[r][c]).only_enforce_if(diff_var)
                    literals.append(diff_var)
        
        self._model.add(sum(literals) >= 1)
        return self._solve()

    def _add_constraints(self):
        for r in range(self._rows_number):
            current_group = []
            for c in range(self._columns_number):
                if self._blacks_grid.value(r, c):
                    self._add_compartment_constraint(current_group, "h")
                    current_group = []
                else:
                    current_group.append(self._vars[r][c])
            self._add_compartment_constraint(current_group, "h")

        for c in range(self._columns_number):
            current_group = []
            for r in range(self._rows_number):
                if self._blacks_grid.value(r, c):
                    self._add_compartment_constraint(current_group, "v")
                    current_group = []
                else:
                    current_group.append(self._vars[r][c])
            self._add_compartment_constraint(current_group, "v")

    def _add_compartment_constraint(self, group, direction):
        if len(group) < 2:
            return
        
        prefix = f"{direction}_{group[0].name}"
        min_var = self._model.new_int_var(1, self._max_val, f'min_{prefix}')
        max_var = self._model.new_int_var(1, self._max_val, f'max_{prefix}')
        
        self._model.add_min_equality(min_var, group)
        self._model.add_max_equality(max_var, group)
        self._model.add(max_var - min_var == len(group) - 1)
        self._model.add_all_different(group)
