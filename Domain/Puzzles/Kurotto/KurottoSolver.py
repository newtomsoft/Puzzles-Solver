from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class KurottoSolver(GameSolver):
    unknown = '?'
    empty = None
    black = 1
    white = None

    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows = grid.rows_number
        self._cols = grid.columns_number
        self._n = self._rows * self._cols

        self._circles = []
        for position, value in grid:
            if value != KurottoSolver.empty:
                self._circles.append((position, value))

        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._init_vars()
        self._add_constraints()
        self._previous_solution = None

    def _init_vars(self):
        self._is_black = [[self._model.new_bool_var(f"b_{r}_{c}") for c in range(self._cols)] for r in range(self._rows)]
        self._rep = [[self._model.new_int_var(-1, self._n - 1, f"rep_{r}_{c}") for c in range(self._cols)] for r in range(self._rows)]
        self._eq = [[[self._model.new_bool_var(f"eq_{r}_{c}_{k}") for k in range(self._n)] for c in range(self._cols)] for r in range(self._rows)]

    def _add_constraints(self):
        self._add_circle_constraints()
        self._add_rep_constraints()
        self._add_connectivity_constraints()
        self._add_clue_constraints()

    def _add_circle_constraints(self):
        for position, _ in self._circles:
            self._model.add(self._is_black[position.r][position.c] == 0)

    def _add_rep_constraints(self):
        for r in range(self._rows):
            for c in range(self._cols):
                self._model.add(self._rep[r][c] == -1).only_enforce_if(self._is_black[r][c].Not())
                eq_vars = self._eq[r][c]
                self._model.add(sum(eq_vars) == self._is_black[r][c])
                for k in range(self._n):
                    self._model.add(self._rep[r][c] == k).only_enforce_if(eq_vars[k])

        for r in range(self._rows):
            for c in range(self._cols):
                for nr, nc in self._grid.neighbors_positions(Position(r, c)):
                    if (nr, nc) <= (r, c):
                        continue
                    self._model.add(self._rep[r][c] == self._rep[nr][nc]).only_enforce_if(
                        [self._is_black[r][c], self._is_black[nr][nc]]
                    )

    def _add_connectivity_constraints(self):
        self._depth = [[self._model.new_int_var(0, self._n, f"depth_{r}_{c}") for c in range(self._cols)] for r in range(self._rows)]

        for r in range(self._rows):
            for c in range(self._cols):
                k_self = r * self._cols + c
                self._model.add(self._depth[r][c] == 0).only_enforce_if(self._is_black[r][c].Not())
                self._model.add(self._depth[r][c] == 0).only_enforce_if(self._eq[r][c][k_self])

                neighbors = self._grid.neighbors_positions(Position(r, c))
                for k in range(self._n):
                    if k == k_self:
                        continue
                    parents = []
                    for nr, nc in neighbors:
                        p = self._model.new_bool_var(f"p_{r}_{c}_{k}_{nr}_{nc}")
                        self._model.add(p <= self._eq[r][c][k])
                        self._model.add(p <= self._eq[nr][nc][k])
                        self._model.add(self._depth[r][c] == self._depth[nr][nc] + 1).only_enforce_if(p)
                        parents.append(p)
                    if parents:
                        self._model.add(sum(parents) == self._eq[r][c][k])

    def _add_clue_constraints(self):
        self._size = []
        for k in range(self._n):
            size_k = self._model.new_int_var(0, self._n, f"size_{k}")
            self._model.add(size_k == sum(self._eq[r][c][k] for r in range(self._rows) for c in range(self._cols)))
            self._size.append(size_k)

        for position, value in [(pos, val) for pos, val in self._circles if isinstance(val, int)]:
            neighbors = self._grid.neighbors_positions(position)
            contrib_sum = []
            for k in range(self._n):
                is_adj = self._model.new_bool_var(f"adj_{position}_{k}")
                neighbor_eqs = [self._eq[nr][nc][k] for nr, nc in neighbors]
                self._model.add(is_adj <= sum(neighbor_eqs))
                for eq_var in neighbor_eqs:
                    self._model.add(is_adj >= eq_var)

                contrib = self._model.new_int_var(0, self._n, f"contrib_{position}_{k}")
                self._model.add(contrib == self._size[k]).only_enforce_if(is_adj)
                self._model.add(contrib == 0).only_enforce_if(is_adj.Not())
                contrib_sum.append(contrib)

            self._model.add(sum(contrib_sum) == value)

    def get_solution(self) -> Grid:
        status = self._solver.solve(self._model)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return self._build_solution()
        return Grid.empty()

    def _build_solution(self) -> Grid:
        matrix = []
        for r in range(self._rows):
            row = []
            for c in range(self._cols):
                if self._solver.boolean_value(self._is_black[r][c]):
                    row.append(self.black)
                else:
                    row.append(self.white)
            matrix.append(row)
        solution = Grid(matrix)
        self._previous_solution = solution
        return solution

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return self.get_solution()

        diff_vars = []
        for r in range(self._rows):
            for c in range(self._cols):
                val = self._previous_solution.value(r, c)
                b = self._model.new_bool_var(f"diff_{r}_{c}")
                if val == self.black:
                    self._model.add(self._is_black[r][c] == 0).only_enforce_if(b)
                    self._model.add(self._is_black[r][c] == 1).only_enforce_if(b.Not())
                else:
                    self._model.add(self._is_black[r][c] == 1).only_enforce_if(b)
                    self._model.add(self._is_black[r][c] == 0).only_enforce_if(b.Not())
                diff_vars.append(b)

        self._model.add(sum(diff_vars) > 0)
        return self.get_solution()
