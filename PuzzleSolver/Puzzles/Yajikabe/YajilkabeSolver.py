from ortools.sat.python import cp_model

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class YajikabeSolver(GameSolver):
    direction_map = {
        '→': Direction.right(),
        '↓': Direction.down(),
        '←': Direction.left(),
        '↑': Direction.up()
    }

    def __init__(self, grid: Grid):
        super().__init__()
        self._input_grid = grid
        self.rows_number = grid.rows_number
        self.columns_number = grid.columns_number
        self._model = cp_model.CpModel()
        self._grid_vars: Grid | None = None
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._grid_vars = Grid([[self._model.new_bool_var(f"c_{r}_{c}") for c in range(self._input_grid.columns_number)] for r in range(self._input_grid.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._grid_vars is None:
            self._init_solver()

        status = self._solver.solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()

        solution = Grid([[self._solver.boolean_value(self._grid_vars.value(i, j)) for j in range(self._grid_vars.columns_number)] for i in range(self._grid_vars.rows_number)])
        self._previous_solution = solution
        return solution

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return self.get_solution()

        terms = []
        for position, prev_val in self._previous_solution:
            if prev_val:
                terms.append(self._grid_vars[position].negated())
            else:
                terms.append(self._grid_vars[position])
        self._model.add_bool_or(terms)

        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_black_cell_constraints()
        self._add_no_black_2x2_constraints()
        self._add_black_connectivity_constraint()

    def _add_initial_constraints(self):
        for position in [position for position, value in self._input_grid if value != '']:
            self._model.add(self._grid_vars[position] == 0)

    def _add_black_cell_constraints(self):
        for position, blacks_count_direction in [(position, self._convert_cell_value(value)) for position, value in self._input_grid if value != '']:
            count = blacks_count_direction[0]
            direction = blacks_count_direction[1]
            positions = [position for position in self._grid_vars.all_positions_in_direction(position, direction) if self._input_grid[position] == '']
            self._model.add(sum([self._grid_vars[position] for position in positions]) == count)

    def _add_no_black_2x2_constraints(self):
        for r in range(self._input_grid.rows_number - 1):
            for c in range(self._input_grid.columns_number - 1):
                up_left = self._grid_vars.value(r, c)
                up_right = self._grid_vars.value(r, c + 1)
                down_left = self._grid_vars.value(r + 1, c)
                down_right = self._grid_vars.value(r + 1, c + 1)
                self._model.add_bool_or([up_left.negated(), up_right.negated(), down_left.negated(), down_right.negated()])

    def _add_black_connectivity_constraint(self):
        total_cells = self.rows_number * self.columns_number
        self._rank_vars = Grid([[self._model.new_int_var(0, total_cells - 1, f"rank_{r}_{c}") for c in range(self._grid_vars.columns_number)] for r in range(self._grid_vars.rows_number)])
        is_root_vars = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = Position(r, c)
                is_root = self._model.new_bool_var(f"is_root_{r}_{c}")
                is_root_vars.append(is_root)
                is_black = self._grid_vars[pos]
                self._model.add(is_root <= is_black)
                self._model.add(self._rank_vars[pos] == 0).OnlyEnforceIf(is_root)
        self._model.add(sum(is_root_vars) == 1)
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = Position(r, c)
                is_black = self._grid_vars[pos]
                is_root = is_root_vars[r * self.columns_number + c]
                parent_literals = []
                for neighbor in self._grid_vars.neighbors_positions(pos):
                    parent = self._model.new_bool_var(f"parent_{r}_{c}_{neighbor.r}_{neighbor.c}")
                    self._model.add(self._grid_vars[neighbor] == 1).OnlyEnforceIf(parent)
                    self._model.add(self._rank_vars[neighbor] < self._rank_vars[pos]).OnlyEnforceIf(parent)
                    parent_literals.append(parent)
                if parent_literals:
                    self._model.add_bool_or(parent_literals).OnlyEnforceIf([is_black, is_root.negated()])

    @staticmethod
    def _convert_cell_value(cell_value: str) -> tuple[int, Direction]:
        if len(cell_value) != 2:
            raise ValueError(f"Invalid cell value: {cell_value}")
        count = int(cell_value[0])
        direction = YajikabeSolver.direction_map[cell_value[1]]
        return count, direction
