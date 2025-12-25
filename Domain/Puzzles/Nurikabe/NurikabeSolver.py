from ortools.sat.python import cp_model
from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class NurikabeSolver(GameSolver):
    def __init__(self, grid: Grid):
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
        self._solver = cp_model.CpSolver()
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
                self._is_white[r, c] = self._model.NewBoolVar(f"w_{r}_{c}")
                self._island_id[r, c] = self._model.NewIntVar(0, num_seeds, f"id_{r}_{c}")
                self._dist[r, c] = self._model.NewIntVar(0, max_dist, f"d_{r}_{c}")

    def _add_constraints(self):
        self._add_white_island_constraints()
        self._add_seed_constraints()
        self._add_adjacency_constraints()
        self._add_no_2x2_river_constraint()

    def _add_white_island_constraints(self):
        # 1. Link is_white and island_id
        for r in range(self.rows):
            for c in range(self.cols):
                # is_white <=> island_id > 0
                self._model.Add(self._island_id[r, c] > 0).OnlyEnforceIf(self._is_white[r, c])
                self._model.Add(self._island_id[r, c] == 0).OnlyEnforceIf(self._is_white[r, c].Not())

                # if not white, dist is 0 (just to fix value)
                self._model.Add(self._dist[r, c] == 0).OnlyEnforceIf(self._is_white[r, c].Not())

    def _add_seed_constraints(self):
        # 2. Seeds
        for i, (sr, sc, size) in enumerate(self._seeds):
            seed_idx = i + 1
            self._model.Add(self._island_id[sr, sc] == seed_idx)
            self._model.Add(self._dist[sr, sc] == 0)
            self._model.Add(self._is_white[sr, sc] == 1)  # Force seed to be white

            # 3. Size constraint
            cells_in_k = []
            for r in range(self.rows):
                for c in range(self.cols):
                    # b <=> island_id == seed_idx
                    b = self._model.NewBoolVar(f"in_{seed_idx}_{r}_{c}")
                    self._model.Add(self._island_id[r, c] == seed_idx).OnlyEnforceIf(b)
                    self._model.Add(self._island_id[r, c] != seed_idx).OnlyEnforceIf(b.Not())
                    cells_in_k.append(b)
            self._model.Add(sum(cells_in_k) == size)

    def _add_adjacency_constraints(self):
        # 4. Adjacency and Connectivity
        for r in range(self.rows):
            for c in range(self.cols):
                neighbors = []
                if r > 0: neighbors.append((r - 1, c))
                if r < self.rows - 1: neighbors.append((r + 1, c))
                if c > 0: neighbors.append((r, c - 1))
                if c < self.cols - 1: neighbors.append((r, c + 1))

                # Adjacent whites have same ID (Separation of islands)
                for nr, nc in neighbors:
                    self._model.Add(self._island_id[r, c] == self._island_id[nr, nc]).OnlyEnforceIf(
                        [self._is_white[r, c], self._is_white[nr, nc]]
                    )

                # Distance / Connectivity to seed
                is_seed = False
                for sr, sc, _ in self._seeds:
                    if r == sr and c == sc:
                        is_seed = True
                        break

                if not is_seed:
                    # If white, must have a neighbor with same ID and smaller dist
                    valid_parents = []
                    for nr, nc in neighbors:
                        # p_ok <=> (island_id[nr,nc] == island_id[r,c]) AND (dist[r,c] == dist[nr,nc] + 1)
                        p_ok = self._model.NewBoolVar(f"pok_{r}_{c}_{nr}_{nc}")

                        self._model.Add(self._island_id[nr, nc] == self._island_id[r, c]).OnlyEnforceIf(p_ok)
                        self._model.Add(self._dist[r, c] == self._dist[nr, nc] + 1).OnlyEnforceIf(p_ok)

                        valid_parents.append(p_ok)

                    self._model.Add(sum(valid_parents) >= 1).OnlyEnforceIf(self._is_white[r, c])

                    # Also enforce dist > 0 if not seed
                    self._model.Add(self._dist[r, c] > 0).OnlyEnforceIf(self._is_white[r, c])

    def _add_no_2x2_river_constraint(self):
        # 5. No 2x2 River
        for r in range(self.rows - 1):
            for c in range(self.cols - 1):
                # Forbidden: All 4 are Black (Not White)
                self._model.AddBoolOr([
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
                if val == 0:  # White
                    match_bools.append(self._is_white[r, c])
                else:  # Black
                    match_bools.append(self._is_white[r, c].Not())
        self._model.AddBoolOr([b.Not() for b in match_bools])

    def _solve_and_check_river_connectivity(self) -> Grid:
        while True:
            status = self._solver.Solve(self._model)
            if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
                sol_rows = []
                for r in range(self.rows):
                    row = []
                    for c in range(self.cols):
                        if self._solver.BooleanValue(self._is_white[r, c]):
                            row.append(0)  # Island
                        else:
                            row.append(1)  # River
                    sol_rows.append(row)

                solution = Grid(sol_rows)

                if solution.are_cells_connected(1) or not any(1 in row for row in sol_rows):
                    self._previous_solution = solution
                    return solution
                else:
                    self._exclude_solution(solution)
            else:
                return Grid.empty()
