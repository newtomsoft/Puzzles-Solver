from z3 import Solver, Not, And, Bool, Implies, Or, sat, Int

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class MeadowsSolver(GameSolver):
    empty = None

    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows_number = self._grid.rows_number
        self._columns_number = self._grid.columns_number
        self._grid_z3: Grid = Grid.empty()
        self._solver = Solver()
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._grid_z3 = Grid([[Int(f"cell_{r}-{c}") for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.assertions():
            self._init_solver()

        solution = self.compute_solution()
        return solution

    def compute_solution(self) -> Grid:
        if self._solver.check() == sat:
            model = self._solver.model()
            solution = Grid([[model.eval(self._grid_z3.value(i, j)).as_long() for j in range(self._columns_number)] for i in range(self._rows_number)])

            self._previous_solution = solution
            return solution

        return Grid.empty()

    def get_other_solution(self):
        constraints = []
        for position, value in self._previous_solution:
            constraints.append(self._grid_z3[position] == value)
        self._solver.add(Not(And(constraints)))
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_all_shapes_are_squares_constraints()

    def _add_initial_constraints(self):
        max_value = max(value for position, value in self._grid if value != self.empty)
        min_value = min(value for position, value in self._grid if value != self.empty)
        for position, value in self._grid:
            if value != self.empty:
                self._solver.add(self._grid_z3[position] == value)
            else:
                self._solver.add(self._grid_z3[position] >= min_value, self._grid_z3[position] <= max_value)

    def _add_all_shapes_are_squares_constraints(self):
        for position, value in [(position, value) for position, value in self._grid if value != self.empty]:
            self._add_square_constraint(position, value)

    def _add_square_constraint(self, position: Position, cell_value: int):
        candidates = []
        rows = self._rows_number
        cols = self._columns_number
        pr, pc = position.r, position.c

        # precompute all grid positions
        all_positions = [Position(r, c) for r in range(rows) for c in range(cols)]

        max_size = min(rows, cols)
        for size in range(1, max_size + 1):
            for r0 in range(0, rows - size + 1):
                for c0 in range(0, cols - size + 1):
                    r1 = r0 + size - 1
                    c1 = c0 + size - 1
                    # the square must include the given position
                    if not (r0 <= pr <= r1 and c0 <= pc <= c1):
                        continue

                    selector = Bool(f"sq_{cell_value}_{pr}_{pc}_{r0}_{c0}_{size}")

                    # Inside constraints
                    inside_positions = [Position(r, c) for r in range(r0, r1 + 1) for c in range(c0, c1 + 1)]
                    for pos in inside_positions:
                        self._solver.add(Implies(selector, self._grid_z3[pos] == cell_value))

                    # Outside constraints: all other cells must be != cell_value
                    outside_positions = [pos for pos in all_positions if not (r0 <= pos.r <= r1 and c0 <= pos.c <= c1)]
                    for pos in outside_positions:
                        self._solver.add(Implies(selector, self._grid_z3[pos] != cell_value))

                    candidates.append(selector)

        # At least one candidate must be true
        if candidates:
            self._solver.add(Or(candidates))
            # And they must be mutually exclusive (exactly one)
            for i in range(len(candidates)):
                for j in range(i + 1, len(candidates)):
                    self._solver.add(Not(And(candidates[i], candidates[j])))
        else:
            # No possible square (shouldn't generally happen); force contradiction to signal unsat for this puzzle
            self._solver.add(False)
