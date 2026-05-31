from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class MeadowsSolver(GameSolver):
    cell_empty = None

    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows_number = self._grid.rows_number
        self._columns_number = self._grid.columns_number
        self._model = cp_model.CpModel()
        self._grid_vars = Grid.empty()
        self._previous_solution = Grid.empty()

    def _initialize_grid_vars(self):
        given_values = [value for _, value in self._grid if value is not self.empty]
        min_value = min(given_values)
        max_value = max(given_values)
        self._grid_vars = Grid([[self._model.new_int_var(min_value, max_value, f"cell_{r}_{c}") for c in range(self._columns_number)]
                                for r in range(self._rows_number)])

    def _add_constraints(self):
        self._add_init_constraints()
        self._add_all_shapes_are_squares_constraints()

    def _add_init_constraints(self):
        for position, value in self._grid:
            if value is not self.empty:
                self._model.add(self._grid_vars[position] == value)

    def get_solution(self) -> Grid:
        self._initialize_grid_vars()
        self._add_constraints()
        return self._solve()

    def get_other_solution(self):
        self._add_different_solution_constraint()
        return self._solve()

    def _solve(self) -> Grid[int]:
        solver = cp_model.CpSolver()
        status = solver.solve(self._model)
        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            return Grid.empty()

        solution = Grid([[solver.value(self._grid_vars.value(i, j)) for j in range(self._columns_number)] for i in range(self._rows_number)])
        self._previous_solution = solution
        return solution

    def _add_all_shapes_are_squares_constraints(self):
        for position, value in [(position, value) for position, value in self._grid if value is not self.empty]:
            self._add_square_constraint(position, value)

    def _add_square_constraint(self, position: Position, square_area: int):
        rows = self._rows_number
        cols = self._columns_number

        fixed_other = [pos for pos, val in self._grid if val is not None and val != square_area]
        max_size: int = min(rows, cols)

        candidates: list[cp_model.IntVar] = []
        pos_to_selectors: dict[tuple[int, int], list[cp_model.IntVar]] = {}

        for size in range(1, max_size + 1):
            r0_min = max(0, position.r - size + 1)
            c0_min = max(0, position.c - size + 1)
            r0_max = min(position.r, rows - size)
            c0_max = min(position.c, cols - size)

            for r0 in range(r0_min, r0_max + 1):
                r1 = r0 + size - 1
                for c0 in range(c0_min, c0_max + 1):
                    c1 = c0 + size - 1

                    if any(r0 <= p.r <= r1 and c0 <= p.c <= c1 for p in fixed_other):
                        continue

                    selector = self._model.new_bool_var(f"sq_{square_area}_{position.r}_{position.c}_{r0}_{c0}_{size}")

                    for r in range(r0, r1 + 1):
                        for c in range(c0, c1 + 1):
                            pos = Position(r, c)
                            self._model.add(self._grid_vars[pos] == square_area).only_enforce_if(selector)
                            pos_to_selectors.setdefault((r, c), []).append(selector)

                    candidates.append(selector)

        if not candidates:
            self._model.add(False)
            return

        self._model.add_exactly_one(candidates)

        covered_positions = set(pos_to_selectors.keys())
        for pos, var in self._grid_vars:
            key = (pos.r, pos.c)
            if key in covered_positions:
                b_eq = self._model.new_bool_var(f"eq_{square_area}_{pos.r}_{pos.c}")
                self._model.add(var == square_area).only_enforce_if(b_eq)
                b_ne = self._model.new_bool_var(f"ne_{square_area}_{pos.r}_{pos.c}")
                self._model.add(var != square_area).only_enforce_if(b_ne)
                self._model.add_bool_or([b_eq, b_ne])
                self._model.add_bool_or(pos_to_selectors[key] + [b_eq.negated()])
            else:
                self._model.add(var != square_area)

    def _add_different_solution_constraint(self):
        diffs = []
        for position, previous_value in self._previous_solution:
            value = self._grid_vars[position]
            diff = self._model.new_bool_var(f"diff_{position.r}_{position.c}")
            self._model.add(value != previous_value).only_enforce_if(diff)
            self._model.add(value == previous_value).only_enforce_if(diff.negated())
            diffs.append(diff)

        self._model.add_at_least_one(diffs)
