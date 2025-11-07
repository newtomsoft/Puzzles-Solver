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
        # Optimized encoding: prune impossible squares early and reduce outside constraints.
        rows = self._rows_number
        cols = self._columns_number
        pr, pc = position.r, position.c

        # Pre-filled cells
        fixed_other = [pos for pos, val in self._grid if val is not None and val != cell_value]

        # Bounding box of same-value givens
        min_r = position.r
        max_r = position.r
        min_c = position.c
        max_c = position.c

        # Min required square size and global max
        min_size = 1
        max_size = min(rows, cols)

        candidates = []
        pos_to_selectors: dict[tuple[int, int], list] = {}

        for size in range(min_size, max_size + 1):
            # top-left ranges constrained to contain the bounding box
            r0_min = max(0, max_r - size + 1)
            c0_min = max(0, max_c - size + 1)
            r0_max = min(min_r, rows - size)
            c0_max = min(min_c, cols - size)
            if r0_min > r0_max or c0_min > c0_max:
                continue

            for r0 in range(r0_min, r0_max + 1):
                r1 = r0 + size - 1
                # seed row must fit
                if not (r0 <= pr <= r1):
                    continue
                for c0 in range(c0_min, c0_max + 1):
                    c1 = c0 + size - 1
                    # seed col must fit
                    if not (c0 <= pc <= c1):
                        continue

                    # Reject if any other fixed different value lies inside
                    conflict = False
                    for p in fixed_other:
                        if r0 <= p.r <= r1 and c0 <= p.c <= c1:
                            conflict = True
                            break
                    if conflict:
                        continue

                    # Ensure all same-value fixed cells are inside (should be guaranteed by ranges, but keep safeguard)
                    if not (r0 <= position.r <= r1 and c0 <= position.c <= c1):
                        continue

                    selector = Bool(f"sq_{cell_value}_{pr}_{pc}_{r0}_{c0}_{size}")

                    # Inside cells equal to the value when selector is true
                    for r in range(r0, r1 + 1):
                        for c in range(c0, c1 + 1):
                            pos = Position(r, c)
                            self._solver.add(Implies(selector, self._grid_z3[pos] == cell_value))
                            pos_to_selectors.setdefault((r, c), []).append(selector)

                    candidates.append(selector)

        # Need exactly one selected candidate
        if not candidates:
            self._solver.add(False)
            return
        self._solver.add(Or(candidates))
        for i in range(len(candidates)):
            for j in range(i + 1, len(candidates)):
                self._solver.add(Not(And(candidates[i], candidates[j])))

        # Coverage constraints: if a cell equals this value, it must belong to the selected candidate
        covered_positions = set(pos_to_selectors.keys())
        for r in range(rows):
            for c in range(cols):
                pos = Position(r, c)
                key = (r, c)
                if key in covered_positions:
                    self._solver.add(Implies(self._grid_z3[pos] == cell_value, Or(pos_to_selectors[key])))
                else:
                    # Can never be part of this square
                    self._solver.add(self._grid_z3[pos] != cell_value)
