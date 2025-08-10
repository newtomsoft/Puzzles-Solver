from z3 import Solver, Not, And, Or, sat, Bool, is_true, BoolRef

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver
from Utils.ShapeGenerator import ShapeGenerator


class YajikabeSolver(GameSolver):
    direction_map = {
        '→': Direction.right(),
        '↓': Direction.down(),
        '←': Direction.left(),
        '↑': Direction.up()
    }

    def __init__(self, grid: Grid):
        self._input_grid = grid
        self._solver = Solver()
        self._grid_z3: Grid[BoolRef] | None = None
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._grid_z3 = Grid([[Bool(f"c_{r}-{c}") for c in range(self._input_grid.columns_number)] for r in range(self._input_grid.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.assertions():
            self._init_solver()

        self._previous_solution, _ = self._ensure_all_black_connected()
        return self._previous_solution

    def _ensure_all_black_connected(self) -> tuple[Grid, int]:
        proposition_count = 0
        while self._solver.check() == sat:
            model = self._solver.model()
            proposition_count += 1
            current_grid = Grid([[is_true(model.eval(self._grid_z3.value(i, j))) for j in range(self._grid_z3.columns_number)] for i in
                                 range(self._grid_z3.rows_number)])
            black_shapes = current_grid.get_all_shapes()
            if len(black_shapes) == 1:
                return current_grid, proposition_count

            biggest_shape = max(black_shapes, key=len)
            black_shapes.remove(biggest_shape)
            for black_shape in black_shapes:
                shape_not_all_black = Not(And([self._grid_z3[position] for position in black_shape]))
                around_shape = ShapeGenerator.around_shape(black_shape)
                around_not_all_white = Not(And([Not(self._grid_z3[position]) for position in around_shape if position in self._grid_z3]))
                constraint = Or(shape_not_all_black, around_not_all_white)
                self._solver.add(constraint)

        return Grid.empty(), proposition_count

    def get_other_solution(self) -> Grid:
        constraints = []
        for position, value_z3 in self._grid_z3:
            constraints.append(value_z3 == self._previous_solution[position])
        self._solver.add(Not(And(constraints)))

        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_black_cell_constraints()
        self._add_no_black_2x2_constraints()

    def _add_initial_constraints(self):
        for grid_z3_value in [self._grid_z3[position] for position, value in self._input_grid if value != '']:
            self._solver.add(Not(grid_z3_value))

    def _add_black_cell_constraints(self):
        for position, blacks_count_direction in [(position, self._convert_cell_value(value)) for position, value in self._input_grid if value != '']:
            count = blacks_count_direction[0]
            direction = blacks_count_direction[1]
            positions = [position for position in self._grid_z3.all_positions_in_direction(position, direction) if self._input_grid[position] == '']
            self._solver.add(sum([self._grid_z3[position] for position in positions]) == count)

    def _add_no_black_2x2_constraints(self):
        for r in range(self._input_grid.rows_number - 1):
            for c in range(self._input_grid.columns_number - 1):
                up_left = self._grid_z3.value(r, c)
                up_right = self._grid_z3.value(r, c + 1)
                down_left = self._grid_z3.value(r + 1, c)
                down_right = self._grid_z3.value(r + 1, c + 1)
                self._solver.add(Not(And(up_left, up_right, down_left, down_right)))

    @staticmethod
    def _convert_cell_value(cell_value: str) -> tuple[int, Direction]:
        if len(cell_value) != 2:
            raise ValueError(f"Invalid cell value: {cell_value}")
        count = int(cell_value[0])
        direction = YajikabeSolver.direction_map[cell_value[1]]
        return count, direction
