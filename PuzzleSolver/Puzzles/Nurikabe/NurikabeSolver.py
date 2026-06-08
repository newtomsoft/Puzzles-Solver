from ortools.sat.python import cp_model
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class NurikabeSolver(GameSolver):
    island = 0
    river = 1

    def __init__(self, grid: Grid):
        super().__init__()
        self._grid = grid
        self.rows = grid.rows_number
        self.cols = grid.columns_number
        if self.rows < 5 or self.cols < 5:
            raise ValueError("The grid must be at least 5x5")

        self._seeds = []
        for r in range(self.rows):
            for c in range(self.cols):
                val = self._grid.value(r, c)
                if val > 0:
                    self._seeds.append((r, c, val))

        self._model = cp_model.CpModel()
        self._solver.parameters.max_time_in_seconds = 30.0

        self._is_white = {}
        self._island_id = {}
        self._dist = {}
        self._init_vars()
        self._add_constraints()
        self._previous_solution = None

    def _init_vars(self):
        num_seeds = len(self._seeds)
        max_dist = max((s[2] for s in self._seeds), default=0)

        for r in range(self.rows):
            for c in range(self.cols):
                self._is_white[r, c] = self._model.new_bool_var(f"w_{r}_{c}")
                self._island_id[r, c] = self._model.new_int_var(0, num_seeds, f"id_{r}_{c}")
                self._dist[r, c] = self._model.new_int_var(0, max_dist, f"d_{r}_{c}")

    def _add_constraints(self):
        self._add_white_island_constraints()
        self._add_seed_constraints()
        self._add_adjacency_constraints()
        self._add_no_2x2_river_constraint()

    def _add_white_island_constraints(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self._model.add(self._island_id[r, c] > 0).only_enforce_if(self._is_white[r, c])
                self._model.add(self._island_id[r, c] == 0).only_enforce_if(self._is_white[r, c].negated())

                self._model.add(self._dist[r, c] == 0).only_enforce_if(self._is_white[r, c].negated())

    def _add_seed_constraints(self):
        for i, (sr, sc, size) in enumerate(self._seeds):
            seed_idx = i + 1
            self._model.add(self._island_id[sr, sc] == seed_idx)
            self._model.add(self._dist[sr, sc] == 0)
            self._model.add(self._is_white[sr, sc] == 1)

            cells_in_k = []
            for r in range(self.rows):
                for c in range(self.cols):
                    b = self._model.new_bool_var(f"in_{seed_idx}_{r}_{c}")
                    self._model.add(self._island_id[r, c] == seed_idx).only_enforce_if(b)
                    self._model.add(self._island_id[r, c] != seed_idx).only_enforce_if(b.negated())
                    cells_in_k.append(b)
            self._model.add(sum(cells_in_k) == size)

    def _add_adjacency_constraints(self):
        for r in range(self.rows):
            for c in range(self.cols):
                neighbors = []
                if r > 0: neighbors.append((r - 1, c))
                if r < self.rows - 1: neighbors.append((r + 1, c))
                if c > 0: neighbors.append((r, c - 1))
                if c < self.cols - 1: neighbors.append((r, c + 1))

                for nr, nc in neighbors:
                    self._model.add(self._island_id[r, c] == self._island_id[nr, nc]).only_enforce_if(
                        [self._is_white[r, c], self._is_white[nr, nc]]
                    )

                is_seed = False
                for sr, sc, _ in self._seeds:
                    if r == sr and c == sc:
                        is_seed = True
                        break

                if not is_seed:
                    valid_parents = []
                    for nr, nc in neighbors:
                        p_ok = self._model.new_bool_var(f"pok_{r}_{c}_{nr}_{nc}")

                        self._model.add(self._island_id[nr, nc] == self._island_id[r, c]).only_enforce_if(p_ok)
                        self._model.add(self._dist[r, c] == self._dist[nr, nc] + 1).only_enforce_if(p_ok)

                        valid_parents.append(p_ok)

                    self._model.add(sum(valid_parents) >= 1).only_enforce_if(self._is_white[r, c])

                    self._model.add(self._dist[r, c] > 0).only_enforce_if(self._is_white[r, c])

    def _add_no_2x2_river_constraint(self):
        for r in range(self.rows - 1):
            for c in range(self.cols - 1):
                self._model.add_bool_or([
                    self._is_white[r, c],
                    self._is_white[r + 1, c],
                    self._is_white[r, c + 1],
                    self._is_white[r + 1, c + 1]
                ])

    def get_solution(self) -> Grid:
        return self._solve_and_check_river_connectivity()

    def get_other_solution(self) -> Grid:
        if self._previous_solution:
            self._exclude_solution(self._previous_solution)
        return self._solve_and_check_river_connectivity()

    def _exclude_solution(self, grid: Grid):
        match_bools = []
        for r in range(self.rows):
            for c in range(self.cols):
                val = grid.value(r, c)
                if val == self.island:
                    match_bools.append(self._is_white[r, c])
                else:  # River
                    match_bools.append(self._is_white[r, c].negated())
        self._model.add_bool_or([b.negated() for b in match_bools])

    def _solve_and_check_river_connectivity(self) -> Grid:
        while True:
            status = self._solver.solve(self._model)
            if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
                sol_rows = []
                for r in range(self.rows):
                    row = []
                    for c in range(self.cols):
                        if self._solver.boolean_value(self._is_white[r, c]):
                            row.append(self.island)
                        else:
                            row.append(self.river)
                    sol_rows.append(row)

                solution = Grid(sol_rows)

                if solution.are_cells_connected(self.river) or not any(self.river in row for row in sol_rows):
                    self._previous_solution = solution
                    return solution
                else:
                    self._exclude_solution(solution)
            else:
                return Grid.empty()
