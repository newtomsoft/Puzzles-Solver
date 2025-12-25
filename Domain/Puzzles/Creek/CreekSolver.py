from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver
from Utils.ShapeGenerator import ShapeGenerator


class CreekSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self.solution_rows_number = self._grid.rows_number - 1
        self.solution_columns_number = self._grid.columns_number - 1
        self._solver = cp_model.CpSolver()
        self._model = cp_model.CpModel()
        self._grid_vars: Grid | None = None
        self._previous_solution: Grid | None = None
        self._model_initialized = False

    def _init_solver(self):
        self._model = cp_model.CpModel()
        self._grid_vars = Grid([[self._model.NewBoolVar(f"grid_{r}_{c}") for c in range(self.solution_columns_number)] for r in range(self.solution_rows_number)])
        self._add_constraints()
        self._model_initialized = True

    def get_solution(self) -> Grid:
        if not self._model_initialized:
            self._init_solver()

        solution, _ = self._ensure_all_river_connected()
        self._previous_solution = solution
        return solution

    def get_other_solution(self):
        if self._previous_solution is None:
            return self.get_solution()

        # Add constraint: new solution must be different from previous one
        # sum(cell != prev_val) >= 1
        constraints = []
        for r in range(self.solution_rows_number):
            for c in range(self.solution_columns_number):
                pos = Position(r, c)
                var = self._grid_vars[pos]
                prev_val = self._previous_solution[pos]
                # If prev_val is True (1, Black), we want Not(var) (i.e., var becomes 0/White) to count as diff
                # If prev_val is False (0, White), we want var (i.e., var becomes 1/Black) to count as diff
                if prev_val:
                    constraints.append(var.Not())
                else:
                    constraints.append(var)

        self._model.AddBoolOr(constraints)

        return self.get_solution()

    def _ensure_all_river_connected(self):
        proposition_count = 0
        while True:
            status = self._solver.Solve(self._model)
            proposition_count += 1

            if status != cp_model.OPTIMAL and status != cp_model.FEASIBLE:
                return Grid.empty(), proposition_count

            current_grid = Grid([[self._solver.BooleanValue(self._grid_vars[Position(r, c)]) for c in range(self.solution_columns_number)] for r in range(self.solution_rows_number)])

            # False = River/White, True = Land/Black
            river_shapes = current_grid.get_all_shapes(value=False)
            if len(river_shapes) <= 1:
                return current_grid, proposition_count

            biggest_river_shapes = max(river_shapes, key=len)
            river_shapes.remove(biggest_river_shapes)
            for river_shape in river_shapes:
                # Ban this isolated river shape
                # Logic: It is NOT allowed that (All 'river_shape' cells are False AND All 'around' cells are True)
                # => Or(Any 'river_shape' cell is True OR Any 'around' cell is False)

                around_positions = ShapeGenerator.around_shape(river_shape)
                valid_around_positions = [p for p in around_positions if p in self._grid_vars]

                clause = []
                # Part 1: Any 'river_shape' cell is True (Black)
                for pos in river_shape:
                    clause.append(self._grid_vars[pos])

                # Part 2: Any 'around' cell is False (White) -> Not(cell)
                for pos in valid_around_positions:
                    clause.append(self._grid_vars[pos].Not())

                self._model.AddBoolOr(clause)

    def _add_constraints(self):
        self._add_neighbors_count_constraints()

    def _add_neighbors_count_constraints(self):
        for position, creek_count in [(position, value) for position, value in self._grid if value != -1]:
            solution_positions = self._get_positions_in_solution_grid(self._grid_vars, position)
            self._model.Add(sum([self._grid_vars[solution_position] for solution_position in solution_positions]) == creek_count)

    @staticmethod
    def _get_positions_in_solution_grid(grid: Grid, position: Position) -> set[Position]:
        return {neighbor for neighbor in grid.straddled_neighbors_positions(Position(position.r - 0.5, position.c - 0.5))}
