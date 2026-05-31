from collections import defaultdict

from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Board.RegionsGrid import RegionsGrid
from Domain.Puzzles.GameSolver import GameSolver


class HanareSolver(GameSolver):
    cell_empty = None

    def __init__(self, regions_grid: RegionsGrid, clues_grid: Grid = None):
        self._regions_grid = regions_grid
        self._clues_grid = clues_grid if clues_grid is not None else Grid.empty()
        self._rows_number = regions_grid.rows_number
        self._columns_number = regions_grid.columns_number
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._previous_solution = Grid.empty()

        self._region_cells = defaultdict(list)
        for position, region_id in self._regions_grid:
            self._region_cells[region_id].append(position)
        self._region_sizes = {rid: len(cells) for rid, cells in self._region_cells.items()}

        self._clue_positions = [position for position, value in self._clues_grid if value != HanareSolver.empty]

    def _init_vars(self):
        self._has_number = [
            [self._model.new_bool_var(f"has_r{r}_c{c}") for c in range(self._columns_number)]
            for r in range(self._rows_number)
        ]

    def _add_constraints(self):
        self._add_region_constraints()
        self._add_clue_constraints()
        self._add_row_distance_constraints()
        self._add_column_distance_constraints()

    def _add_region_constraints(self):
        for rid, cells in self._region_cells.items():
            self._model.add(sum(self._has_number[p.r][p.c] for p in cells) == 1)

    def _add_clue_constraints(self):
        for position in self._clue_positions:
            self._model.add(self._has_number[position.r][position.c] == 1)

    def _add_row_distance_constraints(self):
        for r in range(self._rows_number):
            for c1 in range(self._columns_number):
                for c2 in range(c1 + 1, self._columns_number):
                    self._add_distance_constraint(
                        Position(r, c1),
                        Position(r, c2),
                        c2 - c1 - 1,
                        f"r{r}_c{c1}_c{c2}"
                    )

    def _add_column_distance_constraints(self):
        for c in range(self._columns_number):
            for r1 in range(self._rows_number):
                for r2 in range(r1 + 1, self._rows_number):
                    self._add_distance_constraint(
                        Position(r1, c),
                        Position(r2, c),
                        r2 - r1 - 1,
                        f"c{c}_r{r1}_r{r2}"
                    )

    def _add_distance_constraint(self, p1: Position, p2: Position, actual_gap: int, suffix: str):
        region1 = self._regions_grid[p1]
        region2 = self._regions_grid[p2]
        size1 = self._region_sizes[region1]
        size2 = self._region_sizes[region2]
        required_gap = abs(size1 - size2)

        if actual_gap == required_gap:
            return

        between_vars = []
        if p1.r == p2.r:
            between_vars = [self._has_number[p1.r][c].Not() for c in range(p1.c + 1, p2.c)]
        elif p1.c == p2.c:
            between_vars = [self._has_number[r][p1.c].Not() for r in range(p1.r + 1, p2.r)]

        if between_vars:
            no_between = self._model.new_bool_var(f"no_between_{suffix}")
            self._model.add_bool_and(between_vars).only_enforce_if(no_between)
            self._model.add_bool_or([v.Not() for v in between_vars]).only_enforce_if(no_between.Not())
        else:
            no_between = 1

        self._model.add(self._has_number[p1.r][p1.c] + self._has_number[p2.r][p2.c] + no_between <= 2)

    def _solve(self) -> Grid:
        status = self._solver.solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()

        matrix = [[self.empty for _ in range(self._columns_number)] for _ in range(self._rows_number)]
        for position, region_id in self._regions_grid:
            has_num = self._solver.value(self._has_number[position.r][position.c])
            matrix[position.r][position.c] = self._region_sizes[region_id] if has_num else self.empty
        solution = Grid(matrix)
        self._previous_solution = solution
        return solution

    def get_solution(self) -> Grid:
        self._init_vars()
        self._add_constraints()
        return self._solve()

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None or self._previous_solution.is_empty():
            return self.get_solution()

        diffs = []
        for position, prev_val in self._previous_solution:
            diff = self._model.new_bool_var(f"diff_r{position.r}_c{position.c}")
            if prev_val != self.empty:
                self._model.add(self._has_number[position.r][position.c] == 0).only_enforce_if(diff)
                self._model.add(self._has_number[position.r][position.c] == 1).only_enforce_if(diff.Not())
            else:
                self._model.add(self._has_number[position.r][position.c] == 1).only_enforce_if(diff)
                self._model.add(self._has_number[position.r][position.c] == 0).only_enforce_if(diff.Not())
            diffs.append(diff)

        self._model.add_bool_or(diffs)
        return self._solve()
