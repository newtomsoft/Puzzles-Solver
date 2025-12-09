from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver
from Utils.ShapeGenerator import ShapeGenerator


class KurodokoSolver(GameSolver):
    empty = 0

    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows_number = grid.rows_number
        self._columns_number = grid.columns_number
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_vars = []
        self._previous_solution: Grid | None = None

    def _init_model(self):
        self._model = cp_model.CpModel()
        # 1 = White, 0 = Black
        self._grid_vars = [[self._model.NewBoolVar(f"cell_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)]
        self._add_constraints()

    def get_solution(self) -> Grid:
        self._init_model()
        return self._solve_loop()

    def _solve_loop(self):
        while True:
            status = self._solver.Solve(self._model)
            if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
                solution_matrix = []
                for r in range(self._rows_number):
                    row = []
                    for c in range(self._columns_number):
                        # Value returns 0 or 1
                        val = self._solver.Value(self._grid_vars[r][c])
                        row.append(val)
                    solution_matrix.append(row)

                solution = Grid(solution_matrix)

                # Check connectivity
                white_shapes = solution.get_all_shapes(value=1)

                # If no white cells (unlikely if clues exist), or just one component
                if len(white_shapes) <= 1:
                    self._previous_solution = solution
                    return solution

                # Block disconnected components
                # Find the biggest component and assume it's the "main" one (heuristic),
                # force others to connect to something outside their current boundary.
                biggest_white_shape = max(white_shapes, key=len)
                white_shapes.remove(biggest_white_shape)

                for white_shape in white_shapes:
                    around_white = ShapeGenerator.around_shape(white_shape)
                    valid_around = [p for p in around_white if 0 <= p.r < self._rows_number and 0 <= p.c < self._columns_number]

                    # Currently all 'valid_around' are 0 (Black) or not 1.
                    # We must flip at least one to 1 (White) to break isolation.
                    self._model.AddBoolOr([self._grid_vars[p.r][p.c] for p in valid_around])
            else:
                return Grid.empty()

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return self.get_solution()

        # Add blocking constraint for the previous solution
        diff_vars = []
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                val = self._previous_solution.matrix[r][c]
                # val is 0 or 1
                b = self._model.NewBoolVar(f"diff_{r}_{c}")
                # b <=> (grid_var != val)
                if val == 1:
                    # grid_var == 0
                    self._model.Add(self._grid_vars[r][c] == 0).OnlyEnforceIf(b)
                    self._model.Add(self._grid_vars[r][c] == 1).OnlyEnforceIf(b.Not())
                else:
                    # grid_var == 1
                    self._model.Add(self._grid_vars[r][c] == 1).OnlyEnforceIf(b)
                    self._model.Add(self._grid_vars[r][c] == 0).OnlyEnforceIf(b.Not())
                diff_vars.append(b)

        self._model.Add(sum(diff_vars) > 0)
        return self._solve_loop()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_adjacency_constraints()
        self._add_visibility_constraints()

    def _add_initial_constraints(self):
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                val = self._grid.matrix[r][c]
                if val > 0:
                    self._model.Add(self._grid_vars[r][c] == 1)

    def _add_adjacency_constraints(self):
        # No two black cells adjacent (Black is 0)
        # Not (A=0 and B=0) <=> A=1 or B=1 <=> A + B >= 1
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                if r + 1 < self._rows_number:
                    self._model.Add(self._grid_vars[r][c] + self._grid_vars[r + 1][c] >= 1)
                if c + 1 < self._columns_number:
                    self._model.Add(self._grid_vars[r][c] + self._grid_vars[r][c + 1] >= 1)

    def _add_visibility_constraints(self):
        for position, val in [(position, value) for position, value in self._grid if value > 0]:
            terms = [1]

            for direction in Direction.orthogonal_directions():
                positions = self._grid.all_positions_in_direction(position, direction)[:val]

                previous_term = None

                for k, pos in enumerate(positions):
                    current_cell_var = self._grid_vars[pos.r][pos.c]
                    current_visible_var = self._model.NewBoolVar(f"vis_{position}_{pos}")

                    if previous_term is None:
                        # First cell in direction. Visible iff it is White.
                        # Since origin is White, if current is White, it's connected to origin.
                        # So current_visible_var <=> current_cell_var == 1
                        self._model.Add(current_visible_var == 1).OnlyEnforceIf(current_cell_var)
                        self._model.Add(current_visible_var == 0).OnlyEnforceIf(current_cell_var.Not())

                        previous_term = current_visible_var
                        terms.append(current_visible_var)
                    else:
                        # Visible iff current is White AND previous was visible.
                        # term = Min(current, previous)
                        self._model.AddMinEquality(current_visible_var, [current_cell_var, previous_term])
                        previous_term = current_visible_var
                        terms.append(current_visible_var)

            self._model.Add(sum(terms) == val)
