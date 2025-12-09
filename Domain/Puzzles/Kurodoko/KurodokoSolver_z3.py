from z3 import Solver, Bool, And, sat, Not, is_true

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver
from Utils.ShapeGenerator import ShapeGenerator


class KurodokoSolver(GameSolver):
    empty = 0

    def __init__(self, grid: Grid):
        self._grid = grid
        self._input_grid = grid
        self._rows_number = grid.rows_number
        self._columns_number = grid.columns_number
        self._solver = Solver()
        self._grid_z3: Grid = Grid.empty()
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        # True = White, False = Black
        self._grid_z3 = Grid([[Bool(f"cell_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.assertions():
            self._init_solver()

        solution, _ = self._ensure_all_white_connected()
        self._previous_solution = solution
        return solution

    def _ensure_all_white_connected(self):
        proposition_count = 0
        while self._solver.check() == sat:
            model = self._solver.model()
            proposition_count += 1

            current_matrix = []
            for r in range(self._rows_number):
                row = []
                for c in range(self._columns_number):
                    row.append(is_true(model.eval(self._grid_z3[r][c])))
                current_matrix.append(row)

            current_grid = Grid(current_matrix)
            white_shapes = current_grid.get_all_shapes(value=True)

            if len(white_shapes) == 1:
                return current_grid, proposition_count

            biggest_white_shape = max(white_shapes, key=len)
            white_shapes.remove(biggest_white_shape)

            for white_shape in white_shapes:
                around_white = ShapeGenerator.around_shape(white_shape)
                valid_around = [p for p in around_white if 0 <= p.r < self._rows_number and 0 <= p.c < self._columns_number]

                neighbors_black = []
                for p in valid_around:
                    neighbors_black.append(Not(self._grid_z3[p.r][p.c]))

                self._solver.add(Not(And(neighbors_black)))

        return Grid.empty(), proposition_count

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return self.get_solution()

        current_solution = self._previous_solution
        previous_solution_constraints = []
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                val = current_solution.value(r, c)
                if val:
                    previous_solution_constraints.append(self._grid_z3[r][c])
                else:
                    previous_solution_constraints.append(Not(self._grid_z3[r][c]))

        self._solver.add(Not(And(previous_solution_constraints)))
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_adjacency_constraints()
        self._add_visibility_constraints()

    def _add_initial_constraints(self):
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                val = self._grid.matrix[r][c]
                if val > 0:
                    self._solver.add(self._grid_z3[r][c])

    def _add_adjacency_constraints(self):
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                if r + 1 < self._rows_number:
                    self._solver.add(Not(And(Not(self._grid_z3[r][c]), Not(self._grid_z3[r + 1][c]))))
                if c + 1 < self._columns_number:
                    self._solver.add(Not(And(Not(self._grid_z3[r][c]), Not(self._grid_z3[r][c + 1]))))

    def _add_visibility_constraints(self):
        for position, val in [(position, value) for position, value in self._grid if value > 0]:
            terms = [1]  # itself

            for direction in Direction.orthogonal_directions():
                positions = self._grid_z3.all_positions_in_direction(position, direction)[:val]
                for k, _ in enumerate(positions):
                    terms.append(And(*[self._grid_z3[pos] for pos in positions[:k + 1]]))

            self._solver.add(sum(terms) == val)
