from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class KnossosSolver(GameSolver):
    cell_empty = -1

    def __init__(self, grid: Grid):
        super().__init__()
        self._grid = grid
        self._rows_number = self._grid.rows_number
        self._columns_number = self._grid.columns_number
        self._model = cp_model.CpModel()
        self._previous_solution = Grid.empty()
        self._cell_room = None
        self._cell_in_room = []

        self._clues = []
        for position, val in self._grid:
            if val != self.cell_empty:
                self._clues.append(((position.r, position.c), val))

        self._num_clues = len(self._clues)
        if self._num_clues == 0:
            raise ValueError("No clues found in the grid")

        self._clue_pos = {i: pos for i, (pos, _) in enumerate(self._clues)}
        self._clue_val = {i: val for i, (_, val) in enumerate(self._clues)}

    def _initialize_grid_vars(self):
        self._cell_room = [
            [self._model.new_int_var(0, self._num_clues - 1, f"room_r{r}_c{c}")
             for c in range(self._columns_number)]
            for r in range(self._rows_number)
        ]

    def _add_constraints(self):
        for i in range(self._num_clues):
            rr, cc = self._clue_pos[i]
            self._model.add(self._cell_room[rr][cc] == i)
        self._add_perimeter_constraints()
        self._add_connectivity_constraints()

    def _add_perimeter_constraints(self):
        self._cell_in_room = []
        for i in range(self._num_clues):
            p = self._clue_val[i]
            cell_in_room = []
            for position, _ in self._grid:
                r, c = position.r, position.c
                b = self._model.new_bool_var(f"in_room_{i}_r{r}_c{c}")
                self._model.add(self._cell_room[r][c] == i).only_enforce_if(b)
                self._model.add(self._cell_room[r][c] != i).only_enforce_if(b.Not())
                cell_in_room.append(b)

            edges_in_room = []
            for position, _ in self._grid:
                r, c = position.r, position.c
                for dr, dc in [(1, 0), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if nr >= self._rows_number or nc >= self._columns_number:
                        continue
                    b_edge = self._model.new_bool_var(f"edge_room_{i}_r{r}c{c}_r{nr}c{nc}")
                    self._model.add_bool_and([cell_in_room[r * self._columns_number + c],
                                             cell_in_room[nr * self._columns_number + nc]]).only_enforce_if(b_edge)
                    self._model.add_bool_or([cell_in_room[r * self._columns_number + c].Not(),
                                            cell_in_room[nr * self._columns_number + nc].Not()]).only_enforce_if(
                        b_edge.Not())
                    edges_in_room.append(b_edge)

            self._model.add(4 * sum(cell_in_room) - 2 * sum(edges_in_room) == p)
            self._cell_in_room.append(cell_in_room)

    def _add_connectivity_constraints(self):
        max_size = self._rows_number * self._columns_number
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        cell_order = [
            [
                [self._model.new_int_var(0, max_size, f"order_{i}_r{r}_c{c}")
                 for c in range(self._columns_number)]
                for r in range(self._rows_number)
            ]
            for i in range(self._num_clues)
        ]

        for i in range(self._num_clues):
            clue_r, clue_c = self._clue_pos[i]
            self._model.add(cell_order[i][clue_r][clue_c] == 1)

            for position, _ in self._grid:
                r, c = position.r, position.c
                cell_in = self._cell_in_room[i][r * self._columns_number + c]
                self._model.add(cell_order[i][r][c] == 0).only_enforce_if(cell_in.Not())

                if (r, c) == (clue_r, clue_c):
                    continue

                self._model.add(cell_order[i][r][c] >= 2).only_enforce_if(cell_in)

                parents = []
                for d, (dr, dc) in enumerate(directions):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self._rows_number and 0 <= nc < self._columns_number:
                        parent_var = self._model.new_bool_var(f"parent_{i}_r{r}c{c}_d{d}")
                        parents.append(parent_var)
                        neighbor_in = self._cell_in_room[i][nr * self._columns_number + nc]

                        self._model.add(cell_in == 1).only_enforce_if(parent_var)
                        self._model.add(neighbor_in == 1).only_enforce_if(parent_var)
                        self._model.add(
                            cell_order[i][r][c] == cell_order[i][nr][nc] + 1
                        ).only_enforce_if(parent_var)

                if parents:
                    self._model.add(sum(parents) == 1).only_enforce_if(cell_in)
                    self._model.add(sum(parents) == 0).only_enforce_if(cell_in.Not())

    def get_solution(self) -> Grid:
        self._initialize_grid_vars()
        self._add_constraints()
        return self._solve()

    def _solve(self) -> Grid:
        self._solver.parameters.max_time_in_seconds = 180.0
        self._solver.parameters.num_search_workers = 8
        status = self._solver.solve(self._model)

        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            solution = Grid([
                [self._solver.value(self._cell_room[r][c]) for c in range(self._columns_number)]
                for r in range(self._rows_number)
            ])
            self._previous_solution = solution
            return solution

        return Grid.empty()

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
