from GameSolver import GameSolver
from Ports.SolverEngine import SolverEngine
from Utils.Grid import Grid
from Utils.Position import Position
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

            for black_shape in black_shapes:
                shape_all_black = self._solver.And([self._solver.Not(self._grid_z3[position]) for position in black_shape])
                around_shape = ShapeGenerator.around_shape(black_shape)
                around_all_white = self._solver.And([self._grid_z3[Position(r, c)] for r, c in around_shape if Position(r, c) in self._grid_z3])
                constraint = self._solver.Not(self._solver.And(shape_all_black, around_all_white))
                self._solver.add(constraint)

            for white_shape in white_shapes:
                shape_all_white = self._solver.And([self._grid_z3[position] for position in white_shape])
                around_shape = ShapeGenerator.around_shape(white_shape)
                around_all_black = self._solver.And([self._solver.Not(self._grid_z3[Position(r, c)]) for r, c in around_shape if Position(r, c) in self._grid_z3])
                constraint = self._solver.Not(self._solver.And(shape_all_white, around_all_black))
                self._solver.add(constraint)

        return Grid.empty(), proposition_count

    def get_other_solution(self):
        exclusion_constraint = self._solver.Not(
            self._solver.And([self._grid_z3[Position(r, c)] == self._previous_solution[Position(r, c)] for r in range(self.rows_number) for c in range(self.columns_number)]))
        self._solver.add(exclusion_constraint)
        return self.get_solution()

    def _add_constraints(self):
        self._initial_constraint()
        self.add_no_square_constraint()
        self._add_no_diagonal_2_cells_isolated_constraint()
        self._add_min_2_connected_cells_constraint()

    def _initial_constraint(self):
        for position, value in self._grid:
            if value == 0:
                self._solver.add(self._grid_z3[position] == FALSE)
                continue
            if value == 1:
                self._solver.add(self._grid_z3[position])
                continue

    def add_no_square_constraint(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                self._solver.add(self._solver.Not(self._solver.And(self._grid_z3[r][c] == FALSE, self._grid_z3[r + 1][c] == FALSE, self._grid_z3[r][c + 1] == FALSE, self._grid_z3[r + 1][c + 1] == FALSE)))
                self._solver.add(self._solver.Not(self._solver.And(self._grid_z3[r][c], self._grid_z3[r + 1][c], self._grid_z3[r][c + 1], self._grid_z3[r + 1][c + 1])))

    def _add_no_diagonal_2_cells_isolated_constraint(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                for bool_value in [False, True]:
                    if0 = self._solver.And(self._grid_z3[r][c] == bool_value, self._grid_z3[r + 1][c + 1] == bool_value)
                    then0 = self._solver.Or(self._grid_z3[r + 1][c] == bool_value, self._grid_z3[r][c + 1] == bool_value)
                    self._solver.add(self._solver.Implies(if0, then0))

                    if1 = self._solver.And(self._grid_z3[r][c + 1] == bool_value, self._grid_z3[r + 1][c] == bool_value)
                    then1 = self._solver.Or(self._grid_z3[r + 1][c + 1] == bool_value, self._grid_z3[r][c] == bool_value)
                    self._solver.add(self._solver.Implies(if1, then1))

    def _add_min_2_connected_cells_constraint(self):
        for position, value in self._grid_z3:
            self._solver.add(self._solver.Or([self._grid_z3[position] == value for position in self._grid_z3.neighbors_positions(position)]))
