from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class ArafSolver(GameSolver):
    cell_empty = -1

    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows_number = self._grid.rows_number
        self._columns_number = self._grid.columns_number
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._previous_solution = Grid.empty()
        self._cell_room = None
        self._in_region = []

        self._clues = []
        for position, val in self._grid:
            if val != self.empty:
                self._clues.append((position, val))

        self._num_clues = len(self._clues)
        self._num_regions = self._num_clues // 2
        if self._num_regions == 0:
            raise ValueError("No clues found in the grid")

        # Pre-compute neighbors for each cell
        self._neighbors = {}
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                pos = Position(r, c)
                self._neighbors[(r, c)] = self._grid.neighbors_positions(pos)

    def _initialize_grid_vars(self):
        self._cell_room = [
            [self._model.new_int_var(0, self._num_clues - 1, f"room_r{r}_c{c}")
             for c in range(self._columns_number)]
            for r in range(self._rows_number)
        ]
        self._in_region = []
        for i in range(self._num_clues):
            in_i = []
            for r in range(self._rows_number):
                row_in_i = []
                for c in range(self._columns_number):
                    b = self._model.new_bool_var(f"in_region_{i}_r{r}_c{c}")
                    self._model.add(self._cell_room[r][c] == i).only_enforce_if(b)
                    self._model.add(self._cell_room[r][c] != i).only_enforce_if(b.Not())
                    row_in_i.append(b)
                in_i.append(row_in_i)
            self._in_region.append(in_i)

    def _add_constraints(self):
        possible_pairs = []
        for i in range(self._num_clues):
            for j in range(i + 1, self._num_clues):
                vi = self._clues[i][1]
                vj = self._clues[j][1]
                pos_i = self._clues[i][0]
                pos_j = self._clues[j][0]
                dist = abs(pos_i.r - pos_j.r) + abs(pos_i.c - pos_j.c)
                lo = min(vi, vj) + 1
                hi = max(vi, vj) - 1
                if lo <= hi and dist + 1 <= hi:
                    possible_pairs.append((i, j, lo, hi))

        b_vars = {}
        for i, j, lo, hi in possible_pairs:
            b_vars[(i, j)] = self._model.new_bool_var(f"b_{i}_{j}")

        # Each clue must be in exactly one pair
        for i in range(self._num_clues):
            partners_vars = []
            for (u, v) in b_vars:
                if u == i or v == i:
                    partners_vars.append(b_vars[(u, v)])
            self._model.add(sum(partners_vars) == 1)

        region_of_clue = []
        is_rep = []
        for i in range(self._num_clues):
            rep_i = self._model.new_bool_var(f"is_rep_{i}")
            is_rep.append(rep_i)
            partners_gt = [b_vars[(i, j)] for j in range(i + 1, self._num_clues) if (i, j) in b_vars]
            if not partners_gt:
                self._model.add(rep_i == 0)
            else:
                self._model.add(rep_i == sum(partners_gt))

            r_i = self._model.new_int_var(0, i, f"region_clue_{i}")
            region_of_clue.append(r_i)
            self._model.add(r_i == i).only_enforce_if(rep_i)
            for j in range(i):
                if (j, i) in b_vars:
                    self._model.add(r_i == j).only_enforce_if(b_vars[(j, i)])

            # If i is not a representative, no cell can belong to region i
            size_i = sum(self._in_region[i][r][c] for r in range(self._rows_number) for c in range(self._columns_number))
            self._model.add(size_i == 0).only_enforce_if(rep_i.Not())

        for i, j, lo, hi in possible_pairs:
            size_i = sum(self._in_region[i][r][c] for r in range(self._rows_number) for c in range(self._columns_number))
            self._model.add(size_i >= lo).only_enforce_if(b_vars[(i, j)])
            self._model.add(size_i <= hi).only_enforce_if(b_vars[(i, j)])

            # Bounding box constraints
            p1, p2 = self._clues[i][0], self._clues[j][0]
            for r in range(self._rows_number):
                for c in range(self._columns_number):
                    p3 = Position(r, c)
                    dist_bb = max(p1.r, p2.r, p3.r) - min(p1.r, p2.r, p3.r) + max(p1.c, p2.c, p3.c) - min(p1.c, p2.c, p3.c) + 1
                    if dist_bb > hi:
                        self._model.add(self._cell_room[r][c] != i).only_enforce_if(b_vars[(i, j)])

        # Clue positions must be in their assigned region
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                pos = Position(r, c)
                clue_idx = next((i for i, (p, v) in enumerate(self._clues) if p == pos), None)
                if clue_idx is not None:
                    self._model.add(self._cell_room[r][c] == region_of_clue[clue_idx])

        # Add step-based connectivity for each region
        self._add_connectivity_constraints(is_rep)

    def _add_connectivity_constraints(self, is_rep):
        """Step-based connectivity per region, conditional on region being active (is_rep)."""
        max_grid_size = self._rows_number * self._columns_number

        for i in range(self._num_clues):
            is_rep_i = is_rep[i]
            # step_vars: distance from root in BFS tree. 0 = not in region, 1 = root, >1 = non-root
            step_vars = {}
            for r in range(self._rows_number):
                for c in range(self._columns_number):
                    step_vars[(r, c)] = self._model.new_int_var(0, max_grid_size, f"step_{i}_{r}_{c}")
                    # If cell is in region i, step >= 1; otherwise step == 0
                    self._model.add(step_vars[(r, c)] >= 1).only_enforce_if(self._in_region[i][r][c])
                    self._model.add(step_vars[(r, c)] == 0).only_enforce_if(self._in_region[i][r][c].Not())

            # Exactly one root per active region
            root_cells = []
            for r in range(self._rows_number):
                for c in range(self._columns_number):
                    is_root = self._model.new_bool_var(f"is_root_{i}_{r}_{c}")
                    self._model.add(step_vars[(r, c)] == 1).only_enforce_if(is_root)
                    self._model.add(step_vars[(r, c)] != 1).only_enforce_if(is_root.Not())
                    root_cells.append(is_root)

            # Region is active (is_rep) => exactly one root; inactive => no root
            self._model.add(sum(root_cells) == 1).only_enforce_if(is_rep_i)
            self._model.add(sum(root_cells) == 0).only_enforce_if(is_rep_i.Not())

            # Non-root cells in region must have a neighbor in same region with step = step - 1
            for r in range(self._rows_number):
                for c in range(self._columns_number):
                    is_non_root_in_region = self._model.new_bool_var(f"is_non_root_{i}_{r}_{c}")
                    self._model.add(step_vars[(r, c)] > 1).only_enforce_if(is_non_root_in_region)
                    self._model.add(step_vars[(r, c)] <= 1).only_enforce_if(is_non_root_in_region.Not())

                    adjacent_constraints = []
                    for neighbor in self._neighbors[(r, c)]:
                        is_connected = self._model.new_bool_var(f"conn_{i}_{r}_{c}_{neighbor.r}_{neighbor.c}")
                        # is_connected => neighbor is in region i
                        self._model.add_implication(is_connected, self._in_region[i][neighbor.r][neighbor.c])
                        # is_connected => step[neighbor] == step[self] - 1
                        self._model.add(step_vars[(neighbor.r, neighbor.c)] == step_vars[(r, c)] - 1).only_enforce_if(is_connected)
                        adjacent_constraints.append(is_connected)

                    if adjacent_constraints:
                        # Non-root in region => exactly one parent
                        self._model.add(sum(adjacent_constraints) == 1).only_enforce_if(is_non_root_in_region)

    def get_solution(self) -> Grid:
        self._initialize_grid_vars()
        self._add_constraints()
        return self._solve()

    def _solve(self) -> Grid:
        self._solver.parameters.max_time_in_seconds = 180.0
        self._solver.parameters.num_search_workers = 8

        status = self._solver.solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()

        solution = Grid([
            [self._solver.value(self._cell_room[r][c]) for c in range(self._columns_number)]
            for r in range(self._rows_number)
        ])
        self._previous_solution = solution
        return solution

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None or self._previous_solution.is_empty():
            return self.get_solution()

        self._add_different_solution_constraint()
        return self._solve()

    def _add_different_solution_constraint(self):
        diffs = []
        for position, prev_val in self._previous_solution:
            r, c = position.r, position.c
            diff = self._model.new_bool_var(f"diff_r{r}_c{c}")
            self._model.add(self._cell_room[r][c] != prev_val).only_enforce_if(diff)
            self._model.add(self._cell_room[r][c] == prev_val).only_enforce_if(diff.Not())
            diffs.append(diff)
        self._model.add_bool_or(diffs)
